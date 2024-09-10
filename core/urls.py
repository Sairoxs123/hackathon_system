from django.urls import path
from .views import *

urlpatterns = [
    path("", index, name="home"),
    path("questions/get/", get_questions, name="get-questions"),
    path("question/details/<int:id>/", get_question_details, name="question-details"),
    path("question/<int:id>/", getQuestion, name="question"),
    path("code/save/", saveCode, name="test-code"),
    path("code/submit/", submitCode, name="submit-code"),
    path("competition/", enterComp, name="enter-comp"),
    path("competition/create/", createCompSession, name="create-comp"),
    path("competition/verify/", verifyComp, name="comp-get-details"),
    path("competition/details/<str:scode>/", get_competition_details, name="competition-question"),
    path("competition/code/save/", compSaveCode, name="comp-save-code"),
    path("competition/code/submit/", compSubmitCode, name="comp-submit-code"),
]
