from django.urls import path

from . import views


app_name = "assessments"


urlpatterns = [
    path(
        "new/",
        views.create_assessment_view,
        name="create",
    ),
    path(
        "<int:assessment_id>/",
        views.assessment_result_view,
        name="result",
    ),
]