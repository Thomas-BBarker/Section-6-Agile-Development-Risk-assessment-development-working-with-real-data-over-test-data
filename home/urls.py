from django.urls import path

from . import views

app_name = "home"

urlpatterns = [
    path("", views.home_page, name="home"),
    path(
        "information-centre/",
        views.information_centre,
        name="information-centre",
    ),
    path(
        "information-centre/password-security/",
        views.password_security,
        name="password-security",
    ),
    path("read-more-1/", views.readmore1, name="readmore1_page"),
    path("read-more-2/", views.readmore2, name="readmore2_page"),
    path("read-more-3/", views.readmore3, name="readmore3_page"),
    path("read-more-4/", views.readmore4, name="readmore4_page"),
    path("read-more-5/", views.readmore5, name="readmore5_page"),
    path("read-more-6/", views.readmore6, name="readmore6_page"),
]