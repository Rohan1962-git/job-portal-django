from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("", views.home, name="home"),   # sample view
    path("jobseeker/register/",views.jobseeker_register, name="jobseeker_register"),
    path("signup/",views.signup, name="signup"),
    path("login/", auth_views.LoginView.as_view(template_name="portal/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="home"), name="logout"),
    path("post-job/", views.post_job, name="create_job"),
    path("apply/<int:job_id>/", views.apply_job, name="apply_job"),
    path("my-applications/", views.my_applications, name="my_applications"),
    path("edit-job/<int:job_id>/", views.edit_job, name="edit_job"),
    path('job/<int:job_id>/', views.job_detail, name='job_detail'),


]
