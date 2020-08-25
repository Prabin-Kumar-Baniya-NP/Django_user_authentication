from django.urls import path
from . import views
urlpatterns = [
    path("",views.sign_up, name="signup"),
    path("login/", views.login, name = "login"),
    path("profile/", views.user_profile, name="profile"),
    path("logout/",views.logout, name="logout"),
    path("change_password/",views.change_password, name="change_password"),
    path("aboutme/", views.about_me, name="aboutme"),
    path("user_detail/<int:id>", views.user_detail, name="user_detail"),
]

