from django.urls import path
from . import views

app_name = "questions"
urlpatterns = [
    path("", views.questions, name="questions"),
    path("browse", views.browse, name="browse"),
    path("browse/<int:number_questions>", views.browse, name="browse"),
    path("create_topic", views.create_topic, name="create_topic"),
    path("create_topic/<int:topic_id>", views.create_topic, name="create_topic"),
    path("<str:topic_name>/", views.detail, name="detail"),
    path("<str:topic_name>/random/", views.random_questions, name="random"),
    path(
        "<str:topic_name>/random/<str:list_questions>",
        views.random_questions,
        name="random",
    ),
]
