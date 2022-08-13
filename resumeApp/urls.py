from django.urls import path
from .views import *

urlpatterns = [
    # path('', index),
    path('resume_index/@<str:username>', resume_index, name="resume_index"),
    path('register_page/', register_page, name="register_page"),
    path('exp_page/', exp_page, name="exp_page"),
    path('', login_page, name="login_page"),
    path('login/', login, name="login"),
    path('profile_page/', profile_page, name="profile_page"),
    path('forgot_pwd_page/', forgot_pwd_page, name="forgot_pwd_page"),
    path('send_otp/', send_otp, name="send_otp"),
    path('varify_otp/', varify_otp, name="varify_otp"),
    path('register/', register, name="register"),
    path('change_pwd/', change_pwd, name="change_pwd"),
    path('resume_page/', resume_page, name="resume_page"),
    path('resume/@<str:username>/', resume, name="resume"),
    path('profile_image_upload/', profile_image_upload, name="profile_image_upload"),
    path('profile_update/', profile_update, name="profile_update"),
    path('remove_profile_image/', remove_profile_image, name="remove_profile_image"),
    
    path('add_education/', add_education, name="add_education"),
    path('edit_education/<int:pk>/', edit_education, name="edit_education"),
    path('delete_education/<int:pk>/', delete_education, name="delete_education"),
    
    path('add_exp/', add_exp, name="add_exp"),
    path('exp_update/<int:pk>/', exp_update, name="exp_update"),
    path('delete_exp/<int:pk>/', delete_exp, name="delete_exp"),

    path('add_skill/', add_skill, name="add_skill"),
    path('skill_update/<int:pk>/', skill_update, name="skill_update"),
    path('delete_skill/<int:pk>/', delete_skill, name="delete_skill"),
    
    path('add_project/', add_project, name="add_project"),
    path('project_update/<int:pk>/', project_update, name="project_update"),
    path('delete_project/<int:pk>/', delete_project, name="delete_project"),
    
    path('add_reference/', add_reference, name="add_reference"),
    path('reference_update/<int:pk>/', reference_update, name="reference_update"),
    path('delete_reference/<int:pk>/', delete_reference, name="delete_reference"),

    path('logout/', logout, name="logout"),
]