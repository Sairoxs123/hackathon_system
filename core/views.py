from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from .models import *
from django.views.decorators.csrf import csrf_exempt
import sys
import io
from datetime import datetime, timedelta
from random import choice
from django.shortcuts import get_object_or_404
import pytz


def specialNameGenerator():
    chars = [
        "0",
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
        "G",
        "H",
        "I",
        "J",
        "K",
        "L",
        "M",
        "N",
        "O",
        "P",
        "Q",
        "R",
        "S",
        "T",
        "U",
        "V",
        "W",
        "X",
        "Y",
        "Z",
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "g",
        "h",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "q",
        "r",
        "s",
        "t",
        "u",
        "v",
        "w",
        "x",
        "y",
        "z",
        "_",
    ]

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

        return render(request, "core/index.html", {"questions": questions})

    return redirect("/admin")

def get_questions(request):
    questions = Questions.objects.all()
    name = request.GET.get("name")
    user = Users.objects.get(name=name)
    json = []
    for i in questions:
        try:
            x = Submissions.objects.get(user=user, question=i)
            json.append(
                {
                    "id": i.id,
                    "title": i.title,
                    "difficulty": i.difficulty,
                    "completed": True,
                }
            )
        except:
            json.append(
                {
                    "id": i.id,
                    "title": i.title,
                    "difficulty": i.difficulty,
                    "completed": False,
                }
            )
    return JsonResponse({"questions": json})


def get_question_details(request, id):
    question = Questions.objects.get(id=id)
    email = request.GET.get("email")
    user = Users.objects.get(email=email)
    try:
        code = CodeStorage.objects.get(question=question, user=user).code
    except:
        code = ""

    return JsonResponse(
        {
            "question": question.question,
            "inputs": eval(question.inputs),
            "outputs": eval(question.outputs),
            "code": code,
        }
    )


def getQuestion(request, id):
    question = Questions.objects.get(id=id)

    return render(request, "core/question.html", {"question": question})

    # def saveCode(question, email, code):
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

        return JsonResponse({"success": True})

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
        correct = bool(request.POST.get("correct"))

        Submissions(
            user=user,
            question=question,
            code=code,
            submit_time=submit_time,
            exec_time=exec_time,
            memory=memory,
            correct=correct,
        ).save()

        return JsonResponse({"success": True})

    return HttpResponse("Invalid request")


def createCompSession(request):
    if request.method == "POST":
        question = request.POST.get("question")
        output = request.POST.get("output")
        start = request.POST.get("start")
        end = request.POST.get("end")
        session_code = specialNameGenerator()

        Competition(
            session_code=session_code,
            question=question,
            output=output,
            start=start,
            end=end,
        ).save()

    return render(request, "core/create-comp.html")


def enterComp(request):
    return render(request, "core/enter-comp.html")


def competition(request, session_code):
    # try:
    comp = Competition.objects.get(session_code=session_code)

    comp_start = datetime(
        day=comp.start.day,
        year=comp.start.year,
        month=comp.start.month,
        hour=comp.start.hour,
        minute=comp.start.minute,
        second=comp.start.second,
    )
    comp_end = datetime(
        day=comp.end.day,
        year=comp.end.year,
        month=comp.end.month,
        hour=comp.end.hour,
        minute=comp.end.minute,
        second=comp.end.second,
    )

    if datetime.now() < comp_start:
        return HttpResponse("Competition did not start yet.")

    if datetime.now() > comp_end:
        return HttpResponse("Competition is over.")

    return HttpResponse("hello")

    # except:
    #    return HttpResponse("<h1>Competition with this session code does not exist.</h1>")


def verifyComp(request):
    session_code = request.GET.get("session_code").strip()
    email = request.GET.get("email")
    try:
        user = Users.objects.get(email=email)
    except:
        return JsonResponse({"message": "User with this email id does not exist."})
    try:
        comp = Competition.objects.get(session_code=session_code)
        comp_start = datetime(
            day=comp.start.day,
            year=comp.start.year,
            month=comp.start.month,
            hour=comp.start.hour,
            minute=comp.start.minute,
            second=comp.start.second,
        )
        comp_end = datetime(
            day=comp.end.day,
            year=comp.end.year,
            month=comp.end.month,
            hour=comp.end.hour,
            minute=comp.end.minute,
            second=comp.end.second,
        )

        if datetime.now() < comp_start:
            return JsonResponse(
                {"message": "Competition has not started yet. Please try again later."}
            )

        if datetime.now() > comp_end:
            return JsonResponse(
                {
                    "message": "Competition has ended. Please ask the creator to open the competition again."
                }
            )

        try:
            submission = CompSubmissions.objects.get(question=comp, user=user)
            if submission.barred:
                return JsonResponse(
                    {"message": "You have been barred from this competition."}
                )
            return JsonResponse({"message": "You have already submitted an answer."})
        except:
            pass

        return JsonResponse({"message": True})

    except:
        return JsonResponse(
            {
                "message": "Competition with this code does not exist. Please try again later."
            }
        )


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
            return JsonResponse({"message": "barred"})
        return JsonResponse({"message": "submitted"})
    except:
        pass

    return JsonResponse(
        {
            "question": competition.question,
            "inputs": eval(competition.inputs),
            "outputs": eval(competition.outputs),
            "code": code,
        }
    )


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

        return JsonResponse({"success": True})

    return HttpResponse("Invalid request")


@csrf_exempt
def compTestCode(request):
    if request.method == "POST":
        question = Competition.objects.get(
            session_code=request.POST.get("session_code")
        )
        code = request.POST.get("code")

        saveCompCode(question, request.session["email"], code)

        output, time = execute_user_code(code)

        if output.strip() == question.output:
            return JsonResponse({"exec": True, "output": output, "time": time})

        return JsonResponse({"exec": False, "output": output, "time": time})

    return HttpResponse("Invalid request")


@csrf_exempt
def compSubmitCode(request):
    if request.method == "POST":
        question = Competition.objects.get(
            session_code=request.POST.get("session_code")
        )
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
                CompSubmissions(
                    user=user,
                    question=question,
                    code=code,
                    submit_time=submit_time,
                    exec_time=0,
                    memory=0,
                    correct=False,
                    barred=barred,
                ).save()
        else:
            exec_time = float(request.POST.get("time"))
            memory = float(request.POST.get("memory"))
            correct = bool(request.POST.get("correct"))
            CompSubmissions(
                user=user,
                question=question,
                code=code,
                submit_time=submit_time,
                exec_time=exec_time,
                memory=memory,
                correct=correct,
            ).save()

        return JsonResponse({"success": True})

    return HttpResponse("Invalid request")


def getSolutions(request, id):
    question = Questions.objects.get(id=id)
    solutions_objects = (
        Submissions.objects.all()
        .exclude(user=Users.objects.get(email=request.GET.get("email")))
        .filter(correct=True, question=question)
        .order_by("-memory")
        .order_by("-exec_time")
    )
    solutions = []
    for i in solutions_objects:
        solutions.append(
            {"id": i.id, "user": i.user.name, "time": i.exec_time, "memory": i.memory}
        )
    return JsonResponse({"solutions": solutions})


def convert_datetime_format(dt):
    # Format the datetime object to the desired string format
    formatted_date = dt.strftime("%b %d, %Y")

    return formatted_date


def getSubmissions(request, id):
    question = Questions.objects.get(id=id)
    user = Users.objects.get(email=request.GET.get("email"))
    submissions_objects = (
        Submissions.objects.all()
        .filter(user=user, correct=True, question=question)
        .order_by("-memory")
        .order_by("-exec_time")
    )
    submissions = []
    for i in submissions_objects:
        submissions.append(
            {
                "id": i.id,
                "user": i.user.name,
                "time": round(i.exec_time * 1000, 3),
                "memory": i.memory,
                "correct": i.correct,
                "submit_time": convert_datetime_format(i.submit_time),
            }
        )
    return JsonResponse({"submissions": submissions})


def get_quiz_questions_and_options(quiz_id):
    """Retrieves all questions and their options for a specific quiz.

    Args:
      quiz_title: The title of the quiz.

    Returns:
      A dictionary where keys are Question objects and values are a list of
      corresponding Option objects.
      Returns an empty dictionary if the quiz is not found.
    """

    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.question_set.all()  # Access questions related to the quiz

    questions_and_options = {}
    for question in questions:
        options = question.option_set.all()  # Access options related to each question
        questions_and_options[question] = list(options)

    return questions_and_options


def getQuizzes(request):
    quizzes = Quiz.objects.all()
    json = []
    for quiz in quizzes:
        # questions_and_options = get_quiz_questions_and_options(quiz.id)
        time = datetime.now(pytz.utc) + timedelta(hours=4)
        if quiz.single_submit:
            if time > quiz.start_time and time < quiz.end_time:
                active = True
            else:
                active = False
        else:
            active = True
        json.append(
            {
                "id": quiz.id,
                "title": quiz.title,
                "active": active,
                "single_submit": quiz.single_submit,
                "start_time": quiz.start_time,
                "end_time": quiz.end_time,
            }
        )

    return JsonResponse({"quizzes": json if len(json) > 0 else "You have no quizzes"})


@csrf_exempt
def createQuiz(request):
    if request.method == "POST":
        title = request.POST.get("title")
        single_submit = (
            request.POST.get("single_submit") == "true"
        )  # returns true if multiple
        quiz_id = Quiz.objects.all().count() + 1
        difficulty = request.POST.get("difficulty")
        if not single_submit:
            quiz = Quiz(
                id=quiz_id,
                title=title,
                single_submit=True,
                start_time=request.POST.get("start_datetime"),
                end_time=request.POST.get("end_datetime"),
                grade=request.POST.get("grade"),
                section=request.POST.get("section"),
                difficulty=difficulty
            )
        else:
            quiz = Quiz(
                id=quiz_id,
                title=title,
                single_submit=False,
                grade=request.POST.get("grade"),
                difficulty=difficulty
            )
        quiz.save()

        no_of_questions = request.POST.get("number_of_questions")
        for i in range(int(no_of_questions)):
            quiz_obj = Quiz.objects.get(id=quiz_id)
            question = request.POST.get(f"questions[{i}][text]")
            image = request.FILES.get(f"questions[{i}][image]")

            if image:
                question_obj = Question(id=Question.objects.all().count() + 1, quiz=quiz_obj, text=question, image=image)
                question_obj.save()
            else:
                question_obj = Question(id=Question.objects.all().count() + 1, quiz=quiz_obj, text=question)
                question_obj.save()

            no_of_options = request.POST.get(f"questions[{i}][options][length]")
            for j in range(int(no_of_options)):
                text = request.POST.get(f"questions[{i}][options][{j}][text]")
                is_correct = (
                    request.POST.get(f"questions[{i}][options][{j}][isCorrect]")
                    == "true"
                )
                opt_image = request.FILES.get(f"questions[{i}][options][{j}][image]")
                if opt_image:
                    option_obj = Option(
                        question=question_obj,
                        text=text,
                        image=opt_image,
                        is_correct=is_correct,
                    )
                    option_obj.save()
                else:
                    x = Option(
                        question=question_obj, text=text, is_correct=is_correct
                    )
                    x.save()

        return JsonResponse({"message": "Quiz created successfully"})

    return JsonResponse({"error": "Invalid request"}, status=400)


def getQuizDetails(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    if request.GET.get("type") == "user":
        email = request.GET.get("email")
        user = Users.objects.get(email=email)
        submissions = QuizSubmissions.objects.all().filter(quiz=quiz, student=user)
        time = datetime.now(pytz.utc) + timedelta(hours=4)
        if quiz.single_submit == True:
            if f"{quiz.grade}{quiz.section}" != user.grade_sec:
                return JsonResponse({"message": "class"})
            if time < quiz.start_time or time > quiz.end_time:
                print(time, quiz.start_time)
                return JsonResponse({"message": "expired"})
            if len(submissions) > 0:
                return JsonResponse({"message": "taken"})
        else:
            if quiz.grade != int("".join([x for x in user.grade_sec if x.isdigit()])):
                return JsonResponse({"message": "grade"})
    json = []
    questions_and_options = get_quiz_questions_and_options(quiz.id)
    json.append(
        {
            "id": quiz.id,
            "title": quiz.title,
            "grade": quiz.grade,
            "start_time": quiz.start_time if quiz.single_submit == True else "",
            "end_time": quiz.end_time if quiz.single_submit == True else "",
            "section": quiz.section if quiz.single_submit == True else "",
            "single_submit": quiz.single_submit,
            "questions": [
                {
                    "id": question.id,
                    "text": question.text,
                    "options": [
                        {
                            "text": option.text,
                            "image": option.image.url if option.image else "No image",
                            "id": option.id,
                            "is_correct": option.is_correct,
                        }
                        for option in options
                    ],
                    "image": question.image.url if question.image else "No image",
                }
                for question, options in questions_and_options.items()
            ],
        }
    )

    return JsonResponse({"details": json})


def remove_common_elements(list1, list2):
    return list(set(list1) - set(list2))

@csrf_exempt
def deleteQuiz(request):
    quiz_id = request.POST.get("quiz_id")
    Quiz.objects.get(id=quiz_id).delete()
    return JsonResponse({"message": "Quiz deleted successfully"})

@csrf_exempt
def deleteSumissions(request):
    quiz_id = request.POST.get("quiz_id")
    QuizSubmissions.objects.all().filter(quiz=Quiz.objects.get(id=quiz_id)).delete()
    return JsonResponse({"message": "Submissions deleted successfully"})

#def mergeSort(L):
    if len(L) <= 1:
        return L

    mid = len(L) // 2

    left = L[:mid]
    right = L[mid:]

    sortedleft = mergeSort(left)
    sortedright = mergeSort(right)

    return merge(sortedleft, sortedright)
#def merge(left, right):

    result = []

    i = j = 0

    while i < len(left) and j < len(right):
        if int(left[i].score.split("/")[0]) < int(right[j].score.split("/")[0]):
            result.append(left[i])
            i += 1

        elif int(left[i].score.split("/")[0]) == int(right[j].score.split("/")[0]):
            result.extend([left[i], right[j]])
            i += 1
            j += 1

        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])

    return result

def getQuizResponses(request, quiz_id):
    all_submissions = list(QuizSubmissions.objects.all().filter(quiz=Quiz.objects.get(id=quiz_id)).order_by("-submit_time"))
    datetimes = []
    submissions = []
    for i in all_submissions:
        if i.submit_time not in datetimes:
            datetimes.append(i.submit_time)
            submissions.append(i)

    json = []
    for i in submissions:
        student_submissions = QuizSubmissions.objects.all().filter(student=i.student, quiz=i.quiz, submit_time=i.submit_time)
        score = 0
        for i in student_submissions:
            if i.correct:
                score += 1
        json.append(
            {
                "id": i.quiz.id,
                "name": i.student.name,
                "class": i.student.grade_sec,
                "score": f"{score}/{len(student_submissions)}",
                "datetime": i.submit_time.strftime("%Y-%m-%d %H:%M:%S"),
                "email":i.student.email
            }
        )

    return JsonResponse({"submissions": json})

def getQuizzesUsers(request):
    quizzes = Quiz.objects.all()
    email = request.GET.get("email")
    user = Users.objects.get(email=email)
    json = []
    for i in quizzes:
        if (
            i.single_submit != True
            and i.grade == int("".join([x for x in user.grade_sec if x.isdigit()]))
        ) or (i.single_submit == True and f"{i.grade}{i.section}" == user.grade_sec):
            data = {
                "id": i.id,
                "title": f"{i.id}. {i.title}",
                "difficulty": i.difficulty,
                "difficultyColor": f'text-{"green" if i.difficulty == "Easy" else "yellow" if i.difficulty == "Medium" else "red"}-500',
            }
            try:
                x = list(QuizSubmissions.objects.all().filter(student=user, quiz=i))
                if len(x) > 0:
                    score = 0
                    data["status"] = "completed"
                    for i in x:
                        if i.correct:
                            score += 1
                    data["score"] = f"{score}/{len(x)}"
            except:
                data["status"] = "not-complete"
            json.append(data)
    return JsonResponse({"data": json})

@csrf_exempt
def submitQuiz(request):
    if request.method == "POST":
        quiz_id = request.POST.get("quiz_id")
        user = Users.objects.get(email=request.POST.get("email"))
        questions_options = get_quiz_questions_and_options(quiz_id)
        score = 0
        time = datetime.now(pytz.utc) + timedelta(hours=4)
        for question, options in questions_options.items():
            option = int(request.POST.get(str(question.id)))
            for i in options:
                if i.id == option:
                    if i.is_correct:
                        score += 1
                        QuizSubmissions(
                            student=user,
                            quiz=Quiz.objects.get(id=quiz_id),
                            question=question,
                            correct=True,
                            submit_time=time,
                            selected_option=i
                        ).save()
                    else:
                        QuizSubmissions(
                            student=user,
                            quiz=Quiz.objects.get(id=quiz_id),
                            question=question,
                            correct=False,
                            submit_time=time,
                            selected_option=i
                        ).save()

        return JsonResponse({"score":score})

def getResults(request):
    quiz_id = request.GET.get("quiz_id")
    user = Users.objects.get(email=request.GET.get("email"))
    quiz = Quiz.objects.get(id=quiz_id)
    submissions = QuizSubmissions.objects.all().filter(student=user, quiz=quiz)
    if len(submissions) == 0:
        return JsonResponse({"message": "not-submitted"})
    questions_options = get_quiz_questions_and_options(quiz_id)
    json = []
    score = 0
    total = 0
    if quiz.single_submit:
        total = len(questions_options)
        for question, options in questions_options.items():
            submission = QuizSubmissions.objects.get(
                student=user, quiz=quiz, question=question
            )
            if submission.correct:
                score += 1
            json.append(
                {
                    "question": question.text,
                    "image": question.image.url if question.image else "No image",
                    "id":question.id,
                    "options": [
                        {
                            "text": option.text,
                            "image": option.image.url if option.image else "No image",
                            "id": option.id,
                            "is_correct": option.is_correct,
                            "selected" : True if option == submission.selected_option else False
                        }
                        for option in options
                    ],
                }
            )
    else:
        questions = {}
        for question, options in questions_options.items():
            submissions = QuizSubmissions.objects.all().filter(student=user, quiz=quiz, question=question).order_by("-submit_time")
            L = []
            for submission in submissions:
                L.append(
                    {
                        "question": question.text,
                        "image": question.image.url if question.image else "No image",
                        "id":question.id,
                        "submit_time": submission.submit_time.strftime("%Y-%m-%d %H:%M:%S"),
                        "options": [
                            {
                                "text": option.text,
                                "image": option.image.url if option.image else "No image",
                                "id": option.id,
                                "is_correct": option.is_correct,
                                "selected" : True if option == submission.selected_option else False
                            }
                            for option in options
                        ],
                    }
                )
            questions[question.id] = L

            from collections import defaultdict

            # Grouping entries by submit_time
            grouped_data = defaultdict(list)

            for key in questions:
                for entry in questions[key]:
                    grouped_data[entry['submit_time']].append(entry)

            # Converting to the desired list of dictionaries
            result = [{submit_time: entries} for submit_time, entries in grouped_data.items()]
            for item in result:
                for datetime, attempt_data in item.items():
                    correct_count = 0
                    total_count = 0
                    for attempt in attempt_data:
                        total_count +=1
                        for option in attempt["options"]:
                            if option["is_correct"] and option["selected"]:
                                correct_count += 1
                    item[datetime] = {
                        "questions": attempt_data,  #Keep the original attempt data
                        "score": f"{correct_count}/{total_count}"
                    }
            #print(result)
        return JsonResponse({"multiple":True, "data":result}, safe=False)

    return JsonResponse({"data": json, "score": f"{score}/{total}"})

def getQuestionAnalysis(request):
    question_id = request.GET.get("question_id")
    question = Question.objects.get(id=question_id)
    submissions = QuizSubmissions.objects.all().filter(question=question)
    correct = 0
    for i in submissions:
        if i.correct:
            correct += 1
    return JsonResponse({"correct":correct, "incorrect":len(submissions)-correct})

@csrf_exempt
def editQuiz(request):
    if request.method == "POST":
        quiz_id = request.POST.get("id")
        title = request.POST.get("title")
        single_submit = request.POST.get("single_submit") == "true"
        difficulty = request.POST.get("difficulty")
        quiz = Quiz.objects.get(id=quiz_id)
        quiz.grade = request.POST.get("grade")
        quiz.title = title
        quiz.difficulty = difficulty
        if not single_submit:
            quiz.single_submit = True
            quiz.start_time = request.POST.get("start_datetime")
            quiz.end_time = request.POST.get("end_datetime")
            quiz.section = request.POST.get("section")
        else:
            quiz.single_submit = False
        quiz.save()
        questions_and_options = get_quiz_questions_and_options(quiz_id)
        question_ids = []
        option_ids = []
        for question, options in questions_and_options.items():
            question_ids.append(question.id)
            for option in options:
                option_ids.append(option.id)
        updated_question_ids = []
        updated_option_ids = []
        no_of_questions = request.POST.get("number_of_questions")
        for i in range(int(no_of_questions)):
            # quiz_obj = Quiz.objects.get(id=quiz_id)
            question = request.POST.get(f"questions[{i}][text]")
            image = request.FILES.get(f"questions[{i}][image]")
            qid = request.POST.get(f"questions[{i}][id]")
            try:
                updated_question_ids.append(int(qid))
            except:
                pass
            try:
                question_obj = Question.objects.get(id=qid)
                question_obj.text = question
                question_obj.image.delete()
                if image:
                    question_obj.image = image

                question_obj.save()

                no_of_options = request.POST.get(f"questions[{i}][options][length]")
                for j in range(int(no_of_options)):
                    text = request.POST.get(f"questions[{i}][options][{j}][text]")
                    is_correct = (
                        request.POST.get(f"questions[{i}][options][{j}][isCorrect]")
                        == "true"
                    )
                    opt_image = request.FILES.get(
                        f"questions[{i}][options][{j}][image]"
                    )
                    oid = request.POST.get(f"questions[{i}][options][{j}][id]")
                    updated_option_ids.append(oid)
                    option_obj = Option.objects.get(id=oid)
                    option_obj.text = text
                    option_obj.is_correct = is_correct
                    option_obj.image.delete()
                    if opt_image:
                        option_obj.image = opt_image
                    option_obj.save()
            except:
                quiz_obj = Quiz.objects.get(id=quiz_id)
                if image:
                    question_obj = Question(id=Question.objects.all().count() + 1, quiz=quiz_obj, text=question, image=image)
                    question_obj.save()
                else:
                    question_obj = Question(id=Question.objects.all().count() + 1, quiz=quiz_obj, text=question)
                    question_obj.save()

                no_of_options = request.POST.get(f"questions[{i}][options][length]")
                for j in range(int(no_of_options)):
                    text = request.POST.get(f"questions[{i}][options][{j}][text]")
                    is_correct = (
                        request.POST.get(f"questions[{i}][options][{j}][isCorrect]")
                        == "true"
                    )
                    opt_image = request.FILES.get(
                        f"questions[{i}][options][{j}][image]"
                    )
                    if opt_image:
                        option_obj = Option(
                            question=question_obj,
                            text=text,
                            image=opt_image,
                            is_correct=is_correct,
                        )
                        option_obj.save()
                    else:
                        Option(
                            question=question_obj, text=text, is_correct=is_correct
                        ).save()
        # delete old questions and options
        if updated_question_ids != question_ids:
            x = Question.objects.filter(id__in=question_ids).exclude(
                id__in=updated_question_ids
            )
            y = Option.objects.filter(id__in=option_ids).exclude(
                id__in=updated_option_ids
            )

            for i in x:
                i.image.delete()
                i.delete()
            for j in y:
                j.image.delete()
                j.delete()
        return JsonResponse({"message": "Quiz updated successfully"})

    return JsonResponse({"error": "Invalid request"}, status=400)
