from django.db import models

# Create your models here.

class Users(models.Model):
    id = models.IntegerField(blank=False, unique=True)
    name = models.CharField("Name", max_length=50)
    email = models.EmailField("Email", max_length=50, primary_key=True)
    password = models.CharField("Password", max_length=100)
    grade_sec = models.CharField("Class", max_length=5)

    def __str__(self):
        return self.email

class Questions(models.Model):
    id = models.IntegerField(primary_key=True, blank=False, unique=True)
    title = models.CharField("Title", max_length=30, null=False)
    question = models.CharField("Question", max_length=1024, null=False)
    inputs = models.CharField("Inputs", max_length=1024, blank=True)
    outputs = models.CharField("Outputs", max_length=1024, null=False)
    difficulty = models.CharField("Difficulty", max_length=1, null=False)

    def __str__(self):
        return str(self.id)

class Submissions(models.Model):
    id = models.IntegerField(primary_key=True, blank=False, unique=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    code = models.CharField("Code", max_length=2048,null=False)
    submit_time = models.DateTimeField("Submit Time")
    exec_time = models.FloatField("Execution Time")
    memory = models.FloatField("Memory Consumed")
    correct = models.BooleanField("Correct", default=False)

    def __str__(self):
        return self.user.email

class CodeStorage(models.Model):
    id = models.IntegerField(primary_key=True, blank=False, unique=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    code = models.CharField("Code", max_length=2048,null=False)
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)

class Competition(models.Model):
    session_code = models.CharField("S.Code", max_length=6, primary_key=True, unique=True)
    question = models.CharField("Question", max_length=1024, null=False)
    inputs = models.CharField("Inputs", max_length=1024)
    outputs = models.CharField("Outputs", max_length=1024, null=False)
    start = models.DateTimeField("Start Time")
    end = models.DateTimeField("End Time")

    def __str__(self):
        return self.session_code

class CompSubmissions(models.Model):
    id = models.IntegerField(primary_key=True, blank=False, unique=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    question = models.ForeignKey(Competition, on_delete=models.CASCADE)
    code = models.CharField("Code", max_length=2048)
    submit_time = models.DateTimeField("Date Time")
    exec_time = models.FloatField("Execution Time")
    memory = models.FloatField("Memory Consumed")
    correct = models.BooleanField("Correct", default=False)
    barred = models.BooleanField("Barred", default=False)

    def __str__(self):
        return self.question.session_code

class CompCodeStorage(models.Model):
    id = models.IntegerField(primary_key=True, blank=False, unique=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    code = models.CharField("Code", max_length=2048,null=False)
    question = models.ForeignKey(Competition, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)