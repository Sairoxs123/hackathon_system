from django.http import JsonResponse
from django.shortcuts import redirect, render
from core.models import *
from .password import bcrypt_hash, bcrypt_compare
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.mail import EmailMessage

#Create your views here.

@csrf_exempt
def signup(request):
    if request.method == "POST":
        data = request.body.decode()
        jsdata = json.loads(data)
        email = jsdata["email"]
        verification = jsdata["verify"]

        try:
            x = Users.objects.get(email=email)
            return JsonResponse({"message":"Account already exists."})

        except:
            html_content = f"""
            <strong>This email is for confirming your signup to JusCode. Please do not click on the link if you did not signup.</strong>
            <br><br>
            <a href="http://localhost:5173/signup/verification/{verification}">Click here</a>
            """

            email_obj = EmailMessage("Confirmation", html_content, "jssvoting@gmail.com", [email])
            email_obj.content_subtype = "html"
            email_obj.send()

            return JsonResponse({"message":"Email has been sent for confirmation."})

@csrf_exempt
def verifySignup(request):
    if request.method == "POST":
        data = request.body.decode()
        jsdata = json.loads(data)
        name = jsdata["name"]
        email = jsdata["email"]
        password = jsdata["password"]
        grade_sec = jsdata["class"]

        try:
            user = Users.objects.get(email=email)
            return JsonResponse({"message":"exists"})

        except:
            if Users.objects.last():
                id = Users.objects.last().id + 1
            else:
                id = 1
            user = Users(id=id,name=name, email=email, grade_sec=grade_sec, password=bcrypt_hash(password))
            user.save()
        return JsonResponse({"message":"You have signed successfully."})

@csrf_exempt
def login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        try:
            x = Users.objects.get(email=email)
            if bcrypt_compare(password, x.password) == False:
                return JsonResponse({"message":"Password or email is incorrect."})
            else:
                return JsonResponse({"message":"yes", "name":x.name, "class":x.grade_sec})
        except:
            return JsonResponse({"message":"Account does not exist."})

@csrf_exempt
def deleteAccount(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        verification = request.POST["verify"]

        try:
            x = Users.objects.get(email=email)
            if bcrypt_compare(password, x.password) == False:
                return JsonResponse({"message":"Password or email is incorrect."})
            else:
                html_content = f"""
                <strong>This email is for confirming your request to delete your JusCode account. Please do not click on the link if you did not request for your account to be deleted.</strong>
                <br><br>
                <a href="http://localhost:5173/delete/verification/{verification}">Click here</a>
                """
                email_obj = EmailMessage("Confirmation", html_content, "jssvoting@gmail.com", [email])
                email_obj.content_subtype = "html"
                email_obj.send()

            return JsonResponse({"message":"Email has been sent for confirmation."})
        except:
            return JsonResponse({"message":"Account does not exist."})

@csrf_exempt
def verifyDelete(request):
    if request.method == "POST":
        email = request.POST["email"]
        try:
            Users.objects.get(email=email).delete()
            return JsonResponse({"message":"done"})
        except:
            return JsonResponse({"message":"error"})