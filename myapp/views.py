from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, 'index.html')

def register(request):
    errors = User.objects.regValidator(request.POST)
    print(errors)

    if errors:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        newuser = User.objects.create(fname=request.POST['fname'], email=request.POST['email'], password=hashed_pw.decode())

        request.session['id'] = newuser.id
    return redirect('/')

def login(request):
    errors = User.objects.loginValidator(request.POST)

    if errors:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.filter(email=request.POST['email'])
        
        print(user)
        newuser = user[0]
        print(newuser)
        request.session['id'] = newuser.id
    return redirect('/allGroups')

def allGroups(request):
    if 'id' not in request.session:
        return redirect("/")
    else:
        loggedinuser = User.objects.get(id =request.session['id'])
        context = {
            'loggedinuser': User.objects.get(id =request.session['id']),
            'new_org': Organization.objects.all()
        }
    return render(request, 'allGroups.html', context)

def addOrganization(request):
    errors = Organization.objects.orgValidator(request.POST)
    print (errors)
    if errors:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/allGroups')
    loggedinuser = User.objects.get(id = request.session['id'])
    print(loggedinuser.fname)
    new_org = Organization.objects.create(org_name = request.POST['org_name'], description = request.POST['description'], creator = loggedinuser)
    new_org.users_who_joined.add(loggedinuser)
    print(request.POST)
    print(new_org)
    return redirect('/allGroups')


def showGroup(request, org_id):
    context = {
        "org": Organization.objects.get(id=org_id),
        'loggedinuser': User.objects.get(id = request.session['id'])
    }
    return render(request, 'showGroup.html', context)


def joinGroup(request, org_id):
    group_to_join = Organization.objects.get(id = org_id)
    loggedinuser = User.objects.get(id = request.session['id'])
    group_to_join.users_who_joined.add(loggedinuser)
    return redirect('showGroup', org_id = org_id)

def leaveGroup(request, org_id):
    group_to_leave = Organization.objects.get(id = org_id)
    loggedinuser = User.objects.get(id = request.session['id'])
    group_to_leave.users_who_joined.remove(loggedinuser)
    return redirect('showGroup', org_id = org_id)


def logout(request):
    request.session.clear()
    return redirect('/')
