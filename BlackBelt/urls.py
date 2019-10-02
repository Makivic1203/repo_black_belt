from django.contrib import admin
from django.urls import path
from myapp import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('allGroups', views.allGroups),
    path('addOrganization', views.addOrganization),
    path('showGroup/<org_id>', views.showGroup, name = 'showGroup'),
    path('logout', views.logout),
    path('joinGroup/<org_id>', views.joinGroup),
    path('leaveGroup/<org_id>', views.leaveGroup)

]
