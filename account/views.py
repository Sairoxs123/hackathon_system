from django.http import JsonResponse
from django.shortcuts import redirect, render
from core.models import *
from .password import bcrypt_hash, bcrypt_compare
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.mail import EmailMessage

#Create your views here.

tokens = [
      "$2b$12$M.70JvwsTvv7vxuBp5skIOdZVlnBxtMHAvtxkIZQ0UFDL5WVa/q6e",
      "$2b$12$egrYQinlQI.k49TxUWAOfu9vKISeYuiY1OUo/4ZsYcDwGQS65wai6",
      "$2b$12$cYN7JPawkY0IW/LF32sQ4enuodvJpxPfcTjjZg/b2erPq/hO5WVU.",
      "$2b$12$hjLNeZxvz7.HqQaZL4iYGOmO7HxJ469BVf2.H0VNvRStr9Yt0b4QK",
      "$2b$12$aplhZ3Ifvdsg2D35tZX7hOhduq6pGF.Lx7CMXBgPbgC5ZaBq3yvU6",
      "$2b$12$2aWoYQf0Ak1v3R.RID3FZOoDlLU3zA22StA36r9OE9vOmjjZ9zqvC",
      "$2b$12$uvHbklNvHABdVfDpnAMVgeN7j3Gocpx0QyKXeRf9JPKf0YziJXcxu",
      "$2b$12$JbdFf94Q5iSNoZP.5UlmGOmt.D2ccWk.TUo5e/65.TZ7doGFYEIg6",
      "$2b$12$J7pIdMi5rACiiibgXL5zQuEu2ufdnhaR5zcm9LERy1aXPOyFwLoP.",
      "$2b$12$U5MiDbKyPcTFucobNF13tu8X9wfelwiPUH7WfwrYfJWVhClpUYQCi",
      "$2b$12$XBb6Gccyxls1RdfqXwQ6c.JCNKimhMVSps7PJNaqSVo9rPXjbRNUy",
      "$2b$12$t/z6TOP4htp3KfUsUMHyjOIaJEw/AzogX5xkW6usWX1L1CuTPeV92",
      "$2b$12$1EpuH4DyHrxgvNPcfaWD9eUXfA.ge0NCnQwTJlw9ekJ5MuAtzo95a",
      "$2b$12$h0f2QIQvze/hFlfu8aGGRudTUZI8O3J.sNNciKL./AYn0tkxVGcjm",
      "$2b$12$i7ZLJJoE7iM.aZ3Sp2U4bOe/6R61v9x7UEK4oUsYu8ZM3oF.hhw8a",
      "$2b$12$9OdEsZDmQhAUxLXmykCNMuV6kS/PgmTfJUNNNW7IUJ3rvm/ycA6zm",
      "$2b$12$ucS7V4X443BIGvdzSzKbcOW/SKuwu18DmNMuoYFy5rT9OtH3qcGu.",
      "$2b$12$0hx28zBxgKFiLGLk6rJQrOBDM88j3o/sr16FgqozhTijXj1muhri6",
      "$2b$12$3rsoblRQRGuFTHjU/DeKGuJlKji12vC1crkZPj0B0sEJXe.GFK/A6",
      "$2b$12$FIR4bliTPvrqXflX/O4QSO58z8EVIfVfThDlwBl5rYwZe1SkUkV9O",
      "$2b$12$NKj75BdPs9YDMTelLmZ66u/9A0pNzMUyKU/VYoFjlH0IPu.RH4zxm",
      "$2b$12$nrodThW5uo4PDkgvxRIsg.c8o2LCSPHcYYGFsH9LVu9KOGKmgWdc6",
      "$2b$12$N97Yi6dlteMCFK1gLsmQvO4YHLbyTDV.BbsOBu66mM9VDcGB/6Qy2",
      "$2b$12$D94WjrBJWMjST/CijgGQI.i7fy61f0mnB.E2zXxspSjOZXBZjNy0q",
      "$2b$12$5WAgSoBKmL.gD6MJKEZ1oe1CEwh3GJ0A7aGEKqYHoumYmvYcyD7fe",
    ]

@csrf_exempt
def signup(request):
    if request.method == "POST":
        data = request.body.decode()
        jsdata = json.loads(data)
        email = jsdata["email"]
        token = jsdata["token"]
        verification = jsdata["verify"]

        if token not in tokens:
            return JsonResponse({"message":"Invalid Request."})

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
        token = jsdata["token"]

        if token not in tokens:
            return JsonResponse({"message":"invalid"})

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
