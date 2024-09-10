from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import *
from django.views.decorators.csrf import csrf_exempt
import sys
import io
from datetime import datetime
from random import choice

def specialNameGenerator():
    chars = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X",
             "Y", "Z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "_", ]

    special = ""

    for i in range(5):
        special += choice(chars)

    try:
        res = Competition.objects.get(session_code=special)
        specialNameGenerator()

    except:
        return special

def execute_user_code(code):
    # Capture stdout and stderr to get the output
    old_stdout = sys.stdout
    sys.stdout = buffer = io.StringIO()

    start = datetime.now()

    try:
        # Execute the code using exec()
        exec(code)
    except Exception as e:
        return f"Error: {e}"
    finally:
        # Restore stdout
        sys.stdout = old_stdout

    end = datetime.now()

    delta = end - start

    return buffer.getvalue(), delta.microseconds



def saveCompCode(question, email, code):
    user = Users.objects.get(email=email)

    try:
        x = CompCodeStorage.objects.get(question=question, user=user)
        if x.code != code:
            x.code = code
            x.save()

    except:
        CompCodeStorage(question=question, user=user, code=code).save()


# Create your views here.

def index(request):
    if request.session.get("logged-in"):
        questions = Questions.objects.all()

        return render(request, "core/index.html", {"questions":questions})

    return HttpResponse(False)

def get_questions(request):
    questions = Questions.objects.all()
    name = request.GET.get("name")
    user = Users.objects.get(name=name)
    json = []
    for i in questions:
        try:
            x = Submissions.objects.get(user=user, question=i)
            json.append(
                {"id":i.id, "title":i.title, "difficulty":i.difficulty, "completed":True}
            )
        except:
            json.append(
                {"id":i.id, "title":i.title, "difficulty":i.difficulty, "completed":False}
            )
    return JsonResponse({"questions":json})

def get_question_details(request, id):
    question = Questions.objects.get(id=id)
    email = request.GET.get("email")
    user = Users.objects.get(email=email)
    try:
        code = CodeStorage.objects.get(question=question, user=user).code
    except:
        code = ""

    return JsonResponse({
        "question":question.question,
        "inputs": eval(question.inputs),
        "outputs": eval(question.outputs),
        "code":code
    })

def getQuestion(request, id):
    question = Questions.objects.get(id=id)

    return render(request, "core/question.html", {"question":question})

#def saveCode(question, email, code):
    user = Users.objects.get(email=email)

    try:
        x = CodeStorage.objects.get(question=question, user=user)
        x.code = code
        x.save()

    except:
        CodeStorage(question=question, user=user, code=code).save()

@csrf_exempt
def saveCode(request):
    if request.method == "POST":
        qid = request.POST.get("id")
        question = Questions.objects.get(id=qid)
        code = request.POST.get("code")
        email = request.POST.get("email")

        user = Users.objects.get(email=email)

        try:
            x = CodeStorage.objects.get(question=question, user=user)
            x.code = code
            x.save()

        except:
            CodeStorage(question=question, user=user, code=code).save()

        return JsonResponse({"success":True})

    return HttpResponse("Invalid request")

@csrf_exempt
def submitCode(request):
    if request.method == "POST":
        question = Questions.objects.get(id=request.POST.get("id"))
        code = request.POST.get("code")
        email = request.POST.get("email")
        exec_time = float(request.POST.get("time"))
        memory = float(request.POST.get("memory"))
        user = Users.objects.get(email=email)
        submit_time = datetime.now()
        correct = request.POST.get("correct")

        Submissions(user=user, question=question, code=code, submit_time=submit_time, exec_time=exec_time, memory=memory, correct=correct).save()

        return JsonResponse({"success":True})

    return HttpResponse("Invalid request")


def createCompSession(request):
    if request.method == "POST":
        question = request.POST.get("question")
        output = request.POST.get("output")
        start = request.POST.get("start")
        end = request.POST.get("end")
        session_code = specialNameGenerator()

        Competition(session_code=session_code, question=question, output=output, start=start, end=end).save()

    return render(request, "core/create-comp.html")

def enterComp(request):
    return render(request, "core/enter-comp.html")

def competition(request, session_code):
    #try:
    comp = Competition.objects.get(session_code=session_code)

    comp_start = datetime(day=comp.start.day, year=comp.start.year, month=comp.start.month, hour=comp.start.hour, minute=comp.start.minute, second=comp.start.second)
    comp_end = datetime(day=comp.end.day, year=comp.end.year, month=comp.end.month, hour=comp.end.hour, minute=comp.end.minute, second=comp.end.second)

    if datetime.now() < comp_start:
        return HttpResponse("Competition did not start yet.")

    if datetime.now() > comp_end:
        return HttpResponse("Competition is over.")

    return HttpResponse("hello")

    #except:
    #    return HttpResponse("<h1>Competition with this session code does not exist.</h1>")

def verifyComp(request):
    session_code = request.GET.get("session_code").strip()
    email = request.GET.get("email")
    try:
        user = Users.objects.get(email=email)
    except:
        return JsonResponse({"message":"User with this email id does not exist."})
    try:
        comp = Competition.objects.get(session_code=session_code)
        comp_start = datetime(day=comp.start.day, year=comp.start.year, month=comp.start.month, hour=comp.start.hour, minute=comp.start.minute, second=comp.start.second)
        comp_end = datetime(day=comp.end.day, year=comp.end.year, month=comp.end.month, hour=comp.end.hour, minute=comp.end.minute, second=comp.end.second)

        if datetime.now() < comp_start:
            return JsonResponse({"message":"Competition has not started yet. Please try again later."})

        if datetime.now() > comp_end:
            return JsonResponse({"message":"Competition has ended. Please ask the creator to open the competition again."})

        try:
            submission = CompSubmissions.objects.get(question=comp, user=user)
            if submission.barred:
                return JsonResponse({"message":"You have been barred from this competition."})
            return JsonResponse({"message":"You have already submitted an answer."})
        except:
            pass

        return JsonResponse({"message":True})

    except:
        return JsonResponse({"message":"Competition with this code does not exist. Please try again later."})

def get_competition_details(request, scode):
    competition = Competition.objects.get(session_code=scode)
    email = request.GET.get("email")
    user = Users.objects.get(email=email)
    try:
        code = CompCodeStorage.objects.get(question=competition, user=user).code
    except:
        code = ""

    try:
        submission = CompSubmissions.objects.get(question=competition, user=user)
        if submission.barred:
            return JsonResponse({"message":"barred"})
        return JsonResponse({"message":"submitted"})
    except:
        pass

    return JsonResponse({
        "question":competition.question,
        "inputs":eval(competition.inputs),
        "outputs":eval(competition.outputs),
        "code":code
    })

@csrf_exempt
def compSaveCode(request):
    if request.method == "POST":
        qid = request.POST.get("id")
        competition = Competition.objects.get(session_code=qid)
        code = request.POST.get("code")
        email = request.POST.get("email")

        user = Users.objects.get(email=email)

        try:
            x = CompCodeStorage.objects.get(question=competition, user=user)
            x.code = code
            x.save()

        except:
            CompCodeStorage(question=competition, user=user, code=code).save()

        return JsonResponse({"success":True})

    return HttpResponse("Invalid request")


@csrf_exempt
def compTestCode(request):
    if request.method == "POST":
        question = Competition.objects.get(session_code=request.POST.get("session_code"))
        code = request.POST.get("code")

        saveCompCode(question, request.session["email"], code)

        output, time = execute_user_code(code)

        if output.strip() == question.output:
            return JsonResponse({"exec":True, "output":output, "time":time})

        return JsonResponse({"exec":False, "output":output, "time":time})

    return HttpResponse("Invalid request")

@csrf_exempt
def compSubmitCode(request):
    if request.method == "POST":
        question = Competition.objects.get(session_code=request.POST.get("session_code"))
        code = request.POST.get("code")
        email = request.POST.get("email")
        submit_time = datetime.now()
        user = Users.objects.get(email=email)
        barred = bool(request.POST.get("barred"))
        if barred == True:
            try:
                x = CompSubmissions.objects.get(question=question, user=user)
                if x.barred == False:
                    x.barred = True
            except:
                CompSubmissions(user=user, question=question, code=code, submit_time=submit_time, exec_time=0, memory=0, correct=False, barred=barred).save()
        else:
            exec_time = float(request.POST.get("time"))
            memory = float(request.POST.get("memory"))
            correct = bool(request.POST.get("correct"))
            CompSubmissions(user=user, question=question, code=code, submit_time=submit_time, exec_time=exec_time, memory=memory, correct=correct).save()

        return JsonResponse({"success":True})

    return HttpResponse("Invalid request")
