from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from .models import *
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
from random import choice
from django.shortcuts import get_object_or_404
import pytz
from django.core.mail import EmailMessage
from .password import bcrypt_hash

def specialNameGenerator(n=5):
    chars = [ "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "_", ]

    special = ""

    for i in range(n):
        special += choice(chars)

    try:
        res = Competition.objects.get(session_code=special)
        specialNameGenerator()

    except:
        return special

def caesar_cipher_decrypt(ciphertext, key):
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    result = ''
    shift = len(key)
    for char in ciphertext:
        if char.upper() in alphabet:
            current_index = alphabet.index(char.upper())
            new_index = (current_index - shift) % 26
            result += alphabet[new_index] if char.isupper() else alphabet[new_index].lower()
        else:
            result += char  # Non-letter characters are unchanged

    return result

def vigenere_cipher_decrypt(ciphertext, keyword):
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    result = ''
    keyword = keyword.upper()
    keyword_index = 0

    for char in ciphertext:
        if char.upper() in alphabet:
            text_index = alphabet.index(char.upper())
            keyword_char = keyword[keyword_index % len(keyword)]
            keyword_index_in_alphabet = alphabet.index(keyword_char)
            new_index = (text_index - keyword_index_in_alphabet) % 26
            result += alphabet[new_index] if char.isupper() else alphabet[new_index].lower()
            keyword_index += 1
        else:
            result += char  # Non-letter characters are unchanged

    return result

def xor_encrypt_decrypt(input_text, key):
    output = ''
    for i in range(len(input_text)):
        output += chr(ord(input_text[i]) ^ ord(key[i % len(key)]))
    return output

decryptions = [caesar_cipher_decrypt, xor_encrypt_decrypt, vigenere_cipher_decrypt]

keywords = ["technology", "innovation", "artificial intelligence", "machine learning", "data science", "software development", "web development", "mobile development", "cloud computing", "cybersecurity", "blockchain", "internet of things", "augmented reality", "virtual reality", "sustainable technology", "green technology", "clean energy", "renewable energy", "climate change", "sustainability", "social impact", "digital transformation", "automation", "robotics", "biotechnology", "nanotechnology", "quantum computing", "future of work", "remote work", "workplace culture", "diversity and inclusion", "mental health", "wellbeing", "work-life balance", "leadership", "management", "teamwork", "communication", "creativity", "innovation", "problem-solving", "critical thinking", "digital literacy", "data privacy", "ethical technology", "responsible AI", "human-centered design", "user experience", "user interface", "design thinking", "product management", "project management", "agile methodology", "devops", "software engineering", "full stack development", "front-end development", "back-end development", "database management", "network engineering", "cybersecurity", "cloud security", "data security", "ethical hacking", "penetration testing", "incident response", "digital forensics", "blockchain security", "IoT security", "AI ethics", "algorithmic bias", "fairness", "transparency", "accountability", "sustainability", "circular economy", "renewable energy", "climate action", "eco-friendly", "green technology", "sustainable development", "social impact", "community engagement", "philanthropy", "nonprofit", "social enterprise", "impact investing", "global citizenship", "cultural diversity", "language learning", "international relations", "global health", "human rights", "social justice", "equity", "inclusion", "diversity", "education", "lifelong learning", "online learning", "e-learning", "STEM education", "digital literacy", "financial literacy", "entrepreneurship", "small business", "startup", "innovation", "business strategy", "marketing", "sales", "customer experience", "digital marketing", "social media marketing", "content marketing", "SEO", "SEM", "email marketing", "data analytics", "business intelligence", "data visualization", "machine learning", "artificial intelligence", "natural language processing", "computer vision", "big data", "data science", "data engineering", "data mining", "data warehousing", "cloud computing", "cloud infrastructure", "cloud security", "cloud architecture", "software development", "software engineering", "agile development", "devops", "full stack development", "front-end development", "back-end development", "web development", "mobile development", "game development", "cybersecurity", "network security", "information security", "ethical hacking", "penetration testing", "incident response", "digital forensics", "blockchain", "cryptocurrency", "smart contracts", "decentralized finance", "NFT", "internet of things", "IoT devices", "IoT security", "IoT applications", "artificial intelligence", "machine learning", "natural language processing", "computer vision", "robotics", "automation", "virtual reality", "augmented reality", "mixed reality", "metaverse", "quantum computing", "biotechnology", "nanotechnology", "genetics", "neuroscience", "bioinformatics", "space exploration", "astronomy", "astrophysics", "climate change", "sustainability", "renewable energy", "green technology", "climate action", "environmental science", "ecology", "conservation", "wildlife conservation", "ocean conservation", "sustainable agriculture", "sustainable fashion", "zero waste", "circular economy", "social impact", "social justice", "human rights", "global health", "education", "lifelong learning", "online learning", "e-learning", "STEM education", "digital literacy", "financial literacy", "entrepreneurship", "small business", "startup", "innovation", "business strategy", "marketing", "sales", "customer experience", "digital marketing", "social media marketing", "content marketing", "SEO", "SEM", "email marketing", "data analytics", "business intelligence", "data visualization", "leadership", "management", "teamwork", "communication", "creativity", "innovation", "problem-solving", "critical thinking", "emotional intelligence", "mental health", "wellbeing", "work-life balance", "diversity and inclusion", "equity", "belonging", "cultural competence", "global citizenship", "language learning", "international relations", "diplomacy", "humanitarian aid", "peacebuilding", "conflict resolution", "social work", "psychology", "sociology", "anthropology", "history", "philosophy", "literature", "art", "music", "film", "theater", "dance", "design", "architecture", "urban planning", "landscape architecture", "interior design", "graphic design", "web design", "UX design", "UI design", "game design", "fashion design", "product design", "industrial design", "photography", "videography", "journalism", "writing", "editing", "publishing", "public relations", "advertising", "marketing communications", "brand management", "digital media", "social media", "content creation", "influencer marketing", "e-commerce", "retail", "supply chain management", "logistics", "operations management", "finance", "accounting", "economics", "investment", "banking", "insurance", "real estate", "law", "business law", "corporate law", "intellectual property law", "tax law", "criminal law", "constitutional law", "international law", "human rights law", "environmental law", "health law", "education law", "labor law", "family law", "criminal justice", "corrections", "probation and parole", "police science", "forensic science", "cybersecurity", "national security", "intelligence analysis", "counterterrorism", "military science", "geopolitics", "international relations", "diplomacy", "foreign policy", "political science", "public policy", "public administration", "government", "politics", "elections", "public opinion", "civic engagement", "social movements", "activism", "nonprofit", "philanthropy", "volunteerism", "community development", "social work", "mental health", "public health", "healthcare", "medicine", "nursing"]

def verify_post_request(algorithm, encrypted):
    return decryptions[algorithm - 1](encrypted, "sai teja sagiraju") in keywords

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

@csrf_exempt
def index(request):
    return JsonResponse({"message":True})

def get_questions(request):
    questions = Questions.objects.all()
    email = request.GET.get("email")
    user = Users.objects.get(email=email)
    json = []
    for i in questions:
        try:
            y = CodeStorage.objects.get(user=user, question=i)
            attempt = True
        except:
            attempt = False
        x = Submissions.objects.filter(user=user, question=i)
        json.append(
            {
                "id": i.id,
                "title": i.title,
                "difficulty": i.difficulty,
                "completed": True if len(x) > 0 else False,
                "in_progress": attempt if len(x) == 0 else False,
                "difficultyColor": f'text-{"green" if i.difficulty == "E" else "yellow" if i.difficulty == "M" else "red"}-500',
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


#def getQuestion(request, id):
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
        incorrect = 0
        prev_submissions = Submissions.objects.all().filter(user=user, question=question)
        for i in prev_submissions:
            if not i.correct:
                incorrect += 1

        if correct:
            points = 100 - (incorrect * 10)
            if points < 0:
                points = 0
            else:
                points = points * question.points / 100
            print(points)
            user.question_points = points
            user.save()

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
        incorrect = 0
        prev_submissions = CompSubmissions.objects.all().filter(user=user, question=question)
        for i in prev_submissions:
            if not i.correct:
                incorrect += 1
        if barred == True:
            try:
                x = CompSubmissions.objects.get(question=question, user=user)
                if x.barred == False:
                    x.barred = True
                x.save()
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

        if correct:
            points = 100 - (incorrect * 10)
            if points < 0:
                points = 0
            else:
                points = points * question.points / 100
            print(points)
            user.competition_points = points
            user.save()

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
                "memory": round(i.memory, 3),
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
            "difficulty": quiz.difficulty,
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
                "id": i.id,
                "email":f"/{i.student.email}",
                "name": i.student.name,
                "class": i.student.grade_sec,
                "score": f"{score}/{len(student_submissions)}",
                "datetime": i.submit_time.strftime("%Y-%m-%d %H:%M:%S"),

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
                "difficultyColor": f'text-{"green" if i.difficulty == "E" else "yellow" if i.difficulty == "M" else "red"}-500',
            }
            try:
                x = list(QuizSubmissions.objects.all().filter(student=user, quiz=i))
                questions_and_options = get_quiz_questions_and_options(i.id)
                no_of_questions = len(questions_and_options)
                if len(x) > 0:
                    score = 0
                    data["status"] = "completed"
                    if len(x) // no_of_questions > 1:
                        total, score = 0, 0
                        x.reverse()
                        for i in x[:no_of_questions]:
                            if i.correct:
                                score += 1
                            total += 1
                        data["score"] = f"{score}/{total}"
                    else:
                        score = 0
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
        return JsonResponse({"multiple":True, "data":result})

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

def profileHomePage(request):
    questions = Questions.objects.all()
    email = request.GET.get("email")
    user = Users.objects.get(email=email)
    total, completed = 0, 0
    questions_categorized = {"E":[0, 0], "M":[0, 0], "H": [0, 0]}
    quizzes = Quiz.objects.all()
    for i in questions:
        x = Submissions.objects.filter(user=user, question=i)
        if len(x) > 0:
            completed += 1
            questions_categorized[i.difficulty][0] += 1
        total += 1
        questions_categorized[i.difficulty][1] += 1
    quiz_total, quiz_completed = 0, 0
    quiz_categorized = {"E":[0, 0], "M":[0, 0], "H": [0, 0]}
    for i in quizzes:
        if (
            i.single_submit != True
            and i.grade == int("".join([x for x in user.grade_sec if x.isdigit()]))
        ) or (i.single_submit == True and f"{i.grade}{i.section}" == user.grade_sec):
            x = list(QuizSubmissions.objects.all().filter(student=user, quiz=i))
            if len(x) > 0:
                quiz_completed += 1
                quiz_categorized[i.difficulty[0]][0] += 1
            quiz_total += 1
            quiz_categorized[i.difficulty[0]][1] += 1
    return JsonResponse({"total":total, "completed":completed, "questions":questions_categorized, "quiz_total":quiz_total, "quiz_completed":quiz_completed, "quiz":quiz_categorized, "question_points":user.question_points, "competition_points":user.competition_points, "quiz_points":user.quiz_points})

def getInfo(request):
    email = request.GET.get("email")
    user = Users.objects.get(email=email)
    return JsonResponse({"data":{
        "name":user.name,
        "email":user.email,
        "class":user.grade_sec,
    }})

@csrf_exempt
def updateInfo(request):
    email = request.POST.get("email")
    name = request.POST.get("name")
    grade_sec = request.POST.get("class")
    password = request.POST.get("password")
    repass = request.POST.get("repass")
    if verify_post_request(int(request.POST.get("algorithm")), request.POST.get("encrypted")) == True:
        if password == repass:
            token = specialNameGenerator(128)
            html_content = f"""
            <strong>This email is for confirming your request to change your details. Please do not click on the link if you did not signup.</strong>
            <br><br>
            <a href="http://localhost:5173/profile/information/change?token={token}">Click here</a>
            """

            email_obj = EmailMessage("Confirmation", html_content, "jssvoting@gmail.com", [email])
            email_obj.content_subtype = "html"
            email_obj.send()

            return JsonResponse({"message":"Email has been sent for confirmation.", "token":token})
        else:
            return JsonResponse({"message":"Invalid Request."})

    return JsonResponse({"message":"Passwords do not match."})

@csrf_exempt
def updateInfoVerify(request):
    email = request.POST.get("email")
    name = request.POST.get("name")
    grade_sec = request.POST.get("class")
    password = request.POST.get("password")
    repass = request.POST.get("repass")
    user = Users.objects.get(email=email)
    user.name = name
    user.grade_sec = grade_sec
    user.password = bcrypt_hash(password)
    user.save()
    return JsonResponse({"message":"success"})

def getQuestionsAndCompetitions(request):
    questions = Questions.objects.all()
    competitions = Competition.objects.all()
    q_json = []
    c_json = []
    time = datetime.now(pytz.utc) + timedelta(hours=4)
    for q in questions:
        q_json.append({"id":q.id, "title":q.title})
    for c in competitions:
        c_json.append({"id":c.session_code, "title":c.question[:20], "active":True if time < c.end and time > c.start else False})
    return JsonResponse({"questions":q_json, "competitions":c_json})

def getQuestionsAndCompetitionsDetails(request):
    session_code = request.GET.get("session_code")
    q_id = request.GET.get("id")

    if q_id:
        question = Questions.objects.get(id=q_id)
        submissions = Submissions.objects.all().filter(question=question)
        json = []
        for i in submissions:
            json.append({"id":i.id, "user":i.user.name, "email":i.user.email, "class":i.user.grade_sec, "submit_time":i.submit_time.strftime("%Y-%m-%d %H:%M:%S")})
        return JsonResponse({"question":question.question, "inputs":question.inputs, "outputs":question.outputs, "difficulty":question.difficulty, "points":question.points, "results":json})

    competition = Competition.objects.get(session_code=session_code)
    submissions = CompSubmissions.objects.all().filter(question=competition)
    json = []
    for i in submissions:
        json.append({"id":i.id, "user":i.user.name, "class":i.user.grade_sec, "submit_time":i.submit_time.strftime("%Y-%m-%d %H:%M:%S")})
    return JsonResponse({"question":competition.question, "inputs":competition.inputs, "outputs":competition.outputs, "points":competition.points, "start":competition.start, "end":competition.end, "results":json, "quiz_code":session_code})

def getQuestionsAndCompetitionsSubmissions(request):
    session_code = request.GET.get("session_code")
    q_id = request.GET.get("q_id")
    student = Users.objects.get(email=request.GET.get("email"))

    if q_id:
        question = Questions.objects.get(id=q_id)
        submissions = Submissions.objects.all().filter(question=question, user=student)
        json = []
        for i in submissions:
            json.append({"id":i.id, "submit_time":i.submit_time.strftime("%Y-%m-%d %H:%M:%S"), "correct":i.correct, "exec_time":round(i.exec_time, 3), "memory":round(i.memory, 3), "code":i.code})
    else:
        competition = Competition.objects.get(session_code=session_code)
        submissions = CompSubmissions.objects.get(competition=competition, student=student)
        json = []
    return JsonResponse({"results":json})

@csrf_exempt
def updateQuestionsAndCompetitions(request):
    if request.method == "POST":
        question = request.POST.get("question")
        inputs = request.POST.get("inputs")
        outputs = request.POST.get("outputs")
        difficulty = request.POST.get("difficulty")
        points = request.POST.get("points")
        q_id = request.POST.get("id")
        type = request.POST.get("type")
        if type == "q":
            question_obj = Questions.objects.get(id=q_id)
            question_obj.question = question
            question_obj.inputs = inputs
            question_obj.outputs = outputs
            question_obj.difficulty = difficulty
            question_obj.points = points
            question_obj.save()
        else:
            competition = Competition.objects.get(session_code=q_id)
            competition.question = question
            competition.inputs = inputs
            competition.outputs = outputs
            competition.points = points
            competition.start = request.POST.get("start")
            competition.end = request.POST.get("end")
            competition.save()
        return JsonResponse({"message":"success"})

@csrf_exempt
def deleteQuestionAndCompetition(request):
    id = request.POST.get("id")
    type = request.POST.get("type")
    if type == "q":
        Questions.objects.get(id=id).delete()
    else:
        Competition.objects.get(session_code=id).delete()
    return JsonResponse({"message":"success"})

@csrf_exempt
def deleteQuestionAndCompetitionSubmissions(request):
    id = request.POST.get("id")
    type = request.POST.get("type")
    if type == "q":
        Submissions.objects.all().filter(question=Questions.objects.get(id=id)).delete()
    else:
        CompSubmissions.objects.all().filter(question=Competition.objects.get(session_code=id)).delete()
    return JsonResponse({"message":"success"})

@csrf_exempt
def addUpdates(request):
    title = request.POST.get("title")
    description = request.POST.get("description")
    time = datetime.now()
    Updates(title=title, description=description, date=time).save()
    return JsonResponse({"message":"success"})
