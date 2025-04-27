from django.contrib import admin
from .models import CustomUser, StudentProfile, MentorProfile, InvestorProfile,Follow
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'role','phone', 'full_name', 'is_active', 'is_staff','profile_picture']
    readonly_fields = ['profile_picture'] 

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(StudentProfile)
admin.site.register(MentorProfile)
admin.site.register(InvestorProfile)
admin.site.register(Follow)