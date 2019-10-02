from django.db import models
from datetime import datetime, timedelta
import re
import bcrypt


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NOW = str(datetime.now())


class UserManager(models.Manager):
    def regValidator(self, form):
        errors = {}

        fname = form['fname']
        lname = form['lname']
        email = form['email']
        password = form['password']


        if not fname:
            errors['name'] = "Please enter First Name!"
        elif len(fname) < 2:
            errors['name'] = " FirstName must be at least two characters!"

        if not lname:
            errors['lname'] = "Please enter Last Name!"
        elif len(lname) < 2:
            errors['lname'] = "Last Name must be at least two characters!"

        if not email:
            errors['email'] = "Please enter an email."
        elif not EMAIL_REGEX.match(email):
            errors['email'] = "Please enter a valid email."
        elif User.objects.filter(email=email):
            errors['email'] = "Email already in database. Please login."

        if not password:
            errors['password'] = "Please enter Password!"
        elif len(password) < 2:
            errors['password'] = "Password must be at least two characters!"

        return errors

    def loginValidator(self, form):
        errors = {}

        email = form['email']
        password = form['password']

        if not email:
            errors['email'] = "Please enter an email."
        elif not EMAIL_REGEX.match(email):
            errors['email'] = "Please enter a valid email."
        elif not User.objects.filter(email=email):
            errors['email'] = "Email not found. Please register."
        else:
            user_list = User.objects.filter(email=email)
            user = user_list[0]
            if not bcrypt.checkpw(password.encode(), user.password.encode()):
                errors['password'] = "Password must match."

        
        return errors


class OrgManager(models.Manager):
    def orgValidator(self, form):

        errors = {}

        org_name = form['org_name']
        description = form['description']

        if not org_name:
            errors['org_name'] = "Please enter Organization Name!"
        elif len(org_name) < 5:
            errors['org_name'] = "Organization Name must be at least five characters!"

        if not description:
            errors['description'] = "Please enter description!"
        elif len(description) < 10:
            errors['description'] ="Description must be at least ten characters!"
        return errors


class User(models.Model):
    fname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()



class Organization(models.Model):
    org_name = models.CharField(max_length=255)
    description = models.TextField()
    creator = models.ForeignKey(User, related_name='org_added', on_delete=models.CASCADE)
    users_who_joined = models.ManyToManyField(User, related_name='joined_organizations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = OrgManager()
