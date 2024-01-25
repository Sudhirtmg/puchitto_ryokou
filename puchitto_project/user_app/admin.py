from django.contrib import admin
from user_app.models import *
# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display=['email','username','location']
class ProfileAdmin(admin.ModelAdmin):
    list_display=['user','first_name','email','last_name','location']
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'subject']

admin.site.register(User,UserAdmin)
admin.site.register(Profile,ProfileAdmin)
admin.site.register(ContactUs, ContactUsAdmin)
