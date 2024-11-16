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
    path("question/solutions/<int:id>/", getSolutions, name="get-solutions"),
    path("question/submissions/<int:id>/", getSubmissions, name="get-submissions"),
    path("owner/quiz/get/", getQuizzes, name="get-quizzes"),
    path("owner/quiz/create/", createQuiz, name="create-quiz"),
    path("owner/quiz/update/", editQuiz, name="edit-quiz"),
    path("owner/quiz/delete/", deleteQuiz, name="delete-quiz"),
    path("owner/quiz/delete/submissions/", deleteSumissions, name="delete-quiz"),
    path("owner/quiz/get/details/<int:quiz_id>/", getQuizDetails, name="get-quiz-details"),
    path("user/quiz/get/", getQuizzesUsers, name="get-quizzes-users"),
    path("user/quiz/get/details/<int:quiz_id>/", getQuizDetails, name="get-quiz-details-user"),
    path("user/quiz/submit/", submitQuiz, name="submit-quiz"),
    path("user/quiz/get/results/", getResults, name="get-quiz-results-user"),
    path("owner/quiz/get/responses/<int:quiz_id>/", getQuizResponses, name="get-quiz-responses"),
    path("owner/question/analysis/", getQuestionAnalysis, name="get-question-analysis")
]
