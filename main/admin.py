from django.contrib import admin

from main.models import Products, Users, Lessons, Groups_members

admin.site.register(Products)
admin.site.register(Users)
admin.site.register(Lessons)
admin.site.register(Groups_members)
