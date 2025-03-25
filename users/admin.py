from django.contrib import admin
from .models import CustomUser, StudentProfile, MentorProfile, InvestorProfile
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'role']

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(StudentProfile)
admin.site.register(MentorProfile)
admin.site.register(InvestorProfile)
