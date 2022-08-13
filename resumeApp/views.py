from django.http import request
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from random import randint
from django.core.mail import send_mail
from django.conf import settings
from django.conf.urls.static import static
from .models import *
from datetime import datetime

data = {
    'no_headers': ['register_page', 'login_page', 'forgot_pwd_page'],
}

# alert_system
def alert(type, text):
    data['alert'] = {
        'type': type,
        'text': text,
    }
    print('alert called.')

def exp_page(request):
    return render(request, "profile_page.html")

# def resume_index(request):
#     return render(request, "resume_index.html")

# load resume data

def view_resume(username):
    user = User.objects.get(UserName=username)
    print(user)
   
    data['resume_data'] = {
        'profile_data': user,
        'email':user.Master,
        'skills': Skill.objects.filter(User = user),
        'exp': Experience.objects.filter(User = user),
        'educ': Education.objects.filter(User = user),
        'proj':Project.objects.filter(User=user),
        'ref':Reference.objects.filter(User=user)
    }
    # edu = Education.objects.filter(User = user)
    # if edu.IsCompleted == True:


def index(request):
    return render(request, 'index.html', data)

def register_page(request):
    data['current_page'] = 'register_page'
    return render(request, 'register_or_forgot_pwd_page.html', data)

def login_page(request):
    data['current_page'] = 'login_page'
    return render(request, 'login_page.html', data)

# load user data
def profile_data(request):
    master = Master.objects.get(Email = request.session['email'])
    user = User.objects.get(Master = master)
    # print("user data: ", user.__dict__)
    new_user = {}
    
    for k,v in user.__dict__.items():
        if k.startswith('_'):
            continue
        new_user.setdefault(k, v)

    new_user['Username'] = '@' + user.Master.__dict__['Email'].split('@')[0]
    new_user['Image'] = settings.MEDIA_URL + new_user['Image']
    
    print("new user: ", new_user)
    data['profile_data'] = new_user
    data['board_universities'] = BoardOrUniversity.objects.all()
    data['course_stream'] = CourseOrStream.objects.all()
    
    data['my_educations'] = Education.objects.filter(User=user)
    data['my_exp'] = Experience.objects.filter(User=user)
    data['ski'] = Skill.objects.filter(User=user)
    data['project'] = Project.objects.filter(User=user)
    data['reference'] = Reference.objects.filter(User=user)

    gc = []
    for i,j in gender_choice:
        gc.append({"value": i, "text": j})
    # print(gc)
    data['gender_choice'] = gc

    sl = []
    for i,j in skill_level:
        sl.append({"value": i, "text": j})
    # print(gc)
    data['skill_level'] = sl

def profile_page(request):
    if 'email' in request.session:
        profile_data(request)
        data['current_page'] = 'profile_page'
    return render(request, 'profile_page.html', data)
    # return redirect(login_page)

def forgot_pwd_page(request):
    data['current_page'] = 'forgot_pwd_page'
    return render(request, 'register_or_forgot_pwd_page.html', data)

def resume_page(request):
    view_resume("makwanakinjal5@gmail.com")
    data['current_page'] = 'resume_page'
    return render(request, 'resume_page.html', data)

def resume(request, username):
    view_resume(username)
    data['current_page'] = 'resume'
    return render(request, 'resume.html', data)

def resume_index(request, username):
    view_resume(username)
    data['current_page'] = 'resume'
    return render(request, 'resume_index.html', data)

# OTP Creation
def otp(request):
    otp_number = randint(1000, 9999)
    print("OTP is: ", otp_number)
    request.session['otp'] = otp_number

# send_otp
def send_otp(request, otp_for="reg"):
    otp(request)
    print('email', request.POST['email'])
    request.session['email'] = request.POST['email']

    email_to_list = [request.POST['email'],]

    subject = 'OTP for {otp_for} Registration'

    email_from = settings.EMAIL_HOST_USER

    message = f"Your One Time Password for verification is: {request.session['otp']}."

    send_mail(subject, message, email_from, email_to_list)

    alert('success', 'An OTP has sent to your email.')
    data.update({'next_step': 'otp'})
    
    return JsonResponse(data)

# verify otp
def varify_otp(request):
    # email = request.session['email']
    if request.session['otp'] == int(request.POST['otp']):
        # register(email, pwd)
        # master = Master.objects.get(Email=email)
        # master.Password = request.POST['new_password']
        print("verified.")
        alert('success', 'An OTP verified.')
        request.session['is_active'] = True
    else:
        print("Invalid OTP")
        # return redirect(forgot_pwd_page)
        alert('danger', 'Invalid OTP')
        return JsonResponse(data)
    
    # return redirect(login_page)
    data.update({'next_step': 'password'})
    return JsonResponse(data)

# registration functionality
def register(request):
    master= Master.objects.create(
        Email = request.session['email'],
        Password = request.POST['new_password'],
        IsActive = request.session['is_active'],
    )
    alert('success', 'Account created successfully.')
    
    data.update({'next_step': 'login_page'})
    return JsonResponse(data)

# forgot pwd functionality
def change_pwd(request):
    email = request.session['email']
    master = Master.objects.get(Email=email)
    print(request.POST)
    if 'current_password' in request.POST:
        if request.POST['current_password'] != master.Password:
            alert('warning', 'Please enter current password correctly.')
            data.update({'error': 'invalid current password.'})
    else:
        del request.session['email']
        data.update({'next_step': 'login_page'})
    
    master.Password = request.POST['new_password']
    master.save()
    alert('success', 'Password has changed successfully.')
    
    return JsonResponse(data)

import os
upload_path = os.path.join(settings.MEDIA_ROOT, 'users/profile/')
print('uplodad path: ', upload_path)
print('static url: ', settings.STATIC_ROOT)

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
print(STATIC_ROOT)

# remove profile photo
def remove_profile_image(request):
    master = Master.objects.get(Email = request.session['email'])
    user = User.objects.get(Master = master)
    
    # f = open(os.path.join(STATIC_ROOT, 'img/avatar.png'), 'rb')

    # print("bin data: ", user.Image.url.split('/')[-1])
    
    # n = open(os.path.join(upload_path, user.Image.url.split('/')[-1]), 'wb')
    
    # n.write(f.read())
    # n.close()
    # f.close()

    # print('image path: ', user.Image.url.split('/')[-1])
    os.remove(os.path.join(upload_path, user.Image.url.split('/')[-1]))
    
    user.Image = ""
    user.save()
    

    print('image removed.')
    data['image_uploaded'] = 'false'

    return redirect(profile_page)

# profile image upload
def profile_image_upload(request):
    master = Master.objects.get(Email = request.session['email'])
    user = User.objects.get(Master = master)

    if 'profile_image' in request.FILES:
        user.Image = request.FILES['profile_image']
        file_type = request.FILES['profile_image'].name.split('.')[-1]
        new_image_name = master.Email.split('@')[0] + "_profile_image"
        
        new_image_name = f"{new_image_name}.{file_type}"

        if new_image_name in os.listdir(upload_path):
            os.remove(os.path.join(upload_path, new_image_name))

        user.Image.name = new_image_name

        print("File type: ", new_image_name)
        user.save()
    
    return redirect(profile_page)

# profile update
def profile_update(request):
    master = Master.objects.get(Email = request.session['email'])
    user = User.objects.get(Master = master)

    user.FullName = request.POST['fullName']
    user.Gender = request.POST['gender']
    user.BirthDate = request.POST['birth_date']
    user.Mobile = request.POST['mobile']
    user.About = request.POST['about']
    user.Country = request.POST['country']
    user.State = request.POST['state']
    user.City = request.POST['city']
    user.Address = request.POST['address']

    user.save()
    alert('success', 'Account updated successfully.')
    return JsonResponse(data)
    # return redirect(profile_page)

# add new edcation detail
def add_education(request):
    master = Master.objects.get(Email = request.session['email'])
    user = User.objects.get(Master = master)

    board_university = BoardOrUniversity.objects.get(id=int(request.POST['board_university']))
    course_stream = CourseOrStream.objects.get(id=int(request.POST['course_stream']))

    education = Education.objects.create(
        User = user,
        BoardUniversity = board_university,
        CourseStream = course_stream,

        StartDate = request.POST['start_date'],
        EndDate = request.POST['end_date'],
        Score = float(request.POST['score']),
        Description = request.POST['description'],
    )

    if 'is_edcation_continue' in request.POST :
        education.IsCompleted = True
    
    if 'is_cgpa' in request.POST :
        education.IsPercent = False

    education.save()

    return redirect(profile_page)

# edit education functionality
def edit_education(request, pk):
    education = Education.objects.get(id=pk)
    education.StartDate = education.StartDate.strftime("%Y-%m-%d")
    education.EndDate = education.EndDate.strftime("%Y-%m-%d")
    data['edit_education'] = education

    return redirect(profile_page)

# delete education functionality
def delete_education(request, pk):
    Education.objects.get(id=pk).delete()

    return redirect(profile_page)

# Login functionality
def login(request):
    
    #login - 2
    email = request.POST['email']
    password = request.POST['password']
    error = object

    try:
        master = Master.objects.get(Email=email)
        if master.Password == password:
            # user = User.objects.create(
            #     Master = master,
            # )
            # #     # return redirect(profile_page)
            request.session['email'] = master.Email
            # data.update({'next_step': 'profile_update'})
            # return JsonResponse(data)
            return redirect(profile_page)
            # data.update({'url': 'profile_page'})
            # alert('success', 'Account logged in successfully.')
            # return JsonResponse(data)
        else:
            raise Exception("Incorrect password")

    except Master.DoesNotExist as err:
        print("User does not exist. Please check your email.")
        error = err.args[0]
    except Exception as err:
        error = err.args[0]
        print("Error: ", err)

    data.update({'error': error})
    
    print(data)
    return JsonResponse(data)
    # return redirect(login_page)

# Exprience Functionality 

def add_exp(request):
    master = Master.objects.get(Email = request.session['email'])
    user = User.objects.get(Master = master)
    
    Exp = Experience.objects.create(
        User = user,
        CompanyName = request.POST['compname'],
        CompanyLocation = request.POST['comploc'],
        JobTitle = request.POST['jobTitle'],
        # StartDate = request.POST['start_date'],
        # EndDate = request.POST['end_date'],
        StartDate = datetime.strptime(request.POST['start_date'],"%Y-%m-%d"),
        EndDate = datetime.strptime(request.POST['end_date'],"%Y-%m-%d"),
        TotalDuration = request.POST['tduration'],
        Description = request.POST['description'],
        )
    if 'is_exp_continue' in request.POST :
        Exp.IsContinue = True
    Exp.save()
    
    alert('success', 'Expri updated successfully.')
    return redirect(profile_page)

# # edit exp functionality
def exp_update(request, pk):
    
    exp = Experience.objects.get(id=pk)
    if request.POST:
        
        exp.JobTitle = request.POST['jobTitle']
        exp.CompanyName = request.POST['compname']
        exp.CompanyLocation = request.POST['comploc']
        exp.StartDate = exp.StartDate.strftime("%Y-%m-%d")
        exp.EndDate = exp.EndDate.strftime("%Y-%m-%d")
        exp.TotalDuration = request.POST['tduration']
        exp.Description = request.POST['description']
        exp.save()
    else:
        # default_data['edit_user_item'] = master
        data['edit_exp'] = exp
    
    return redirect(profile_page)

# # delete exp functionality
def delete_exp(request, pk):
    Experience.objects.get(id=pk).delete()
    return redirect(profile_page)

# Skill functinality start

def add_skill(request):
    master = Master.objects.get(Email = request.session['email'])
    user = User.objects.get(Master = master)
    
    ski = Skill.objects.create(
        User = user,
        Skills = request.POST['skills'],
        level = request.POST['level'],
        # Description = request.POST['description'],
        )
    
    ski.save()
    alert('success', 'Skill updated successfully.')
    return redirect(profile_page)

# # edit skill functionality
def skill_update(request, pk):
    ski = Skill.objects.get(id=pk)
    
    if request.POST:
        
        ski.Skills = request.POST['skills']
        ski.level = request.POST['level']
        # ski.Description = request.POST['description']
        ski.save()
    else:
        # default_data['edit_user_item'] = master
        data['edit_ski'] = ski
           
    return redirect(profile_page)

# # delete skill functionality
def delete_skill(request, pk):
    Skill.objects.get(id=pk).delete()
    return redirect(profile_page)

# Project functionality 
def add_project(request):
    master = Master.objects.get(Email = request.session['email'])
    user = User.objects.get(Master = master)
    
    project = Project.objects.create(
        User = user,
        Title = request.POST['projecttitle'],
        Category = request.POST['category'],
        ClientName = request.POST['clientname'],
        Description = request.POST['description'],
        )
    
    project.save()
    alert('success', 'project updated successfully.')
    return redirect(profile_page)

# edit project functionality
def project_update(request, pk):
    project = Project.objects.get(id=pk)
    if request.POST:
        
        project.Title = request.POST['projecttitle']
        project.Category = request.POST['category']
        project.ClientName = request.POST['clientname']
        project.Description = request.POST['description']
        project.save()
    
    else:
        data['edit_project'] = project
        return redirect(profile_page)
    
# delete proj functionality
def delete_project(request, pk):
    Project.objects.get(id=pk).delete()
    return redirect(profile_page)

# reference functionality 
def add_reference(request):
    master = Master.objects.get(Email = request.session['email'])
    user = User.objects.get(Master = master)
    
    reference = Reference.objects.create(
        User = user,
        ClientName = request.POST['ccompname'],
        ClientContNo = request.POST['compcont'],
        Link = request.POST['link'],
        Description = request.POST['description'],
        )
    
    reference.save()
    alert('success', 'reference updated successfully.')
    return redirect(profile_page)

# edit reference functionality
def reference_update(request, pk):
    reference = Reference.objects.get(id=pk)
    if request.POST:
        
        reference.ClientName = request.POST['ccompname']
        reference.ClientContNo = request.POST['compcont']
        reference.Link = request.POST['link']
        reference.Description = request.POST['description']

    else:
            data['edit_reference'] = reference
            return redirect(profile_page)
        
        
# delete reference functionality
def delete_reference(request, pk):
    Reference.objects.get(id=pk).delete()
    return redirect(profile_page)

# logout
def logout(request):
    if 'email' in request.session:
        del request.session['email']

    return redirect(login_page)