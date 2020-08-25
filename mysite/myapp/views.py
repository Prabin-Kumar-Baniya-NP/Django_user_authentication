from django.shortcuts import render, HttpResponseRedirect
from .forms import SignupForm, EditUserProfile, EditAdminProfile
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login as my_login, logout as my_logout, update_session_auth_hash
from django.contrib.auth.models import User, Group

# Create your views here.
#Sign Up
def sign_up(request):
    fm = SignupForm()
    if request.method == "POST":
        fm = SignupForm(request.POST)
        if fm.is_valid:
            messages.success(request, 'Account Created Successfully')
            user = fm.save()
            default_group = Group.objects.get(name="Editor")
            user.groups.add(default_group)
            return HttpResponseRedirect("/login/")
    else:
        fm = SignupForm()
    return render(request, 'myapp/signup.html', {'form': fm})

# Log in
def login(request):
    if not request.user.is_authenticated:
        if request.method=="POST":
            fm = AuthenticationForm(request=request, data=request.POST)
            if fm.is_valid():
                uname = fm.cleaned_data['username']
                upass = fm.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    my_login(request, user)
                    messages.success(request,"Logged in Successfully")
                    return HttpResponseRedirect('/profile/')
        else:
            fm = AuthenticationForm()
        return render(request,"myapp/login.html",{'form':fm})
    else:
        return HttpResponseRedirect('/profile/')

def user_profile(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            if request.user.is_superuser == True:
                fm = EditAdminProfile(request.POST,instance=request.user)
                users = User.objects.all()
            else:
                fm = EditUserProfile(request.POST, instance=request.user)
            if fm.is_valid():
                fm.save()
                messages.success(request, "Profile Updated !!!")
                return HttpResponseRedirect("/profile/")
        else:
            if request.user.is_superuser == True:
                fm = EditAdminProfile(instance=request.user)
                users = User.objects.all()
            else:
                fm = EditUserProfile(instance=request.user)
                users = None
        return render(request,"myapp/profile.html", {'form':fm,"users":users,"user_name":request.user.username})
    else:
        messages.success(request, "Please Login to view the Profile Page")
        return HttpResponseRedirect('/login/')

def logout(request):
    my_logout(request)
    return HttpResponseRedirect('/login/')

def change_password(request):
    if request.user.is_authenticated:
        fm = PasswordChangeForm(user=request.user)
        if request.method == "POST":
            fm= PasswordChangeForm(user=request.user, data=request.POST)
            if fm.is_valid():
                fm.save()
                update_session_auth_hash(request, fm.user)
                messages.success(request, "Password Changed Successfully")
                return HttpResponseRedirect('/profile/')
            else:
                fm = PasswordChangeForm(user=request.user)
        return render(request, "myapp/change_password.html",{'form':fm})
    else:
        messages.success(request, "You must login to change the password")
        return HttpResponseRedirect('/login/')

def about_me(request):
    if request.user.is_authenticated:
        username = request.user.get_username()
        full_name = request.user.get_full_name()
        user_permissions = request.user.get_user_permissions()
        context = {'username':username,"full_name":full_name,"user_permission":user_permissions}
        return render(request, "myapp/aboutme.html",context)

def user_detail(request, id):
    if request.user.is_authenticated:
        pi = User.objects.get(pk=id)
        fm = EditAdminProfile(instance=pi)
        return render(request, "myapp/user_detail.html", {'form':fm})
    else:
        return HttpResponseRedirect('/login/')
