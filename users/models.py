from django.contrib.auth.models import AbstractUser
from django.db import models

USER_ROLES = (
    ('student', 'Student'),
    ('mentor', 'Mentor'),
    ('investor', 'Investor'),
)

class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    role = models.CharField(max_length=10, choices=USER_ROLES)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    cover_photo = models.ImageField(upload_to='cover_photos/', blank=True, null=True)
    REQUIRED_FIELDS = ['email', 'phone', 'role']

    def __str__(self):
        return self.username

    def follower_count(self):
        return self.followers.count()

    def following_count(self):
        return self.following.count()

    def get_followers(self):
        return [follow.follower for follow in self.followers.all()]

    def get_following(self):
        return [follow.following for follow in self.following.all()]


class Follow(models.Model):
    follower = models.ForeignKey(CustomUser, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(CustomUser, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"



class StudentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='student_profile')
    university = models.CharField(max_length=100)
    degree = models.CharField(max_length=100)
    graduation_year = models.PositiveIntegerField()
    skills = models.CharField(max_length=300)
    city = models.CharField(max_length=100,default='N/A')
    country = models.CharField(max_length=100,default='N/A')  


    def __str__(self):
        return self.user.username


class MentorProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='mentor_profile')
    work_experience = models.TextField()
    company = models.CharField(max_length=100)
    industry = models.CharField(max_length=100)
    linkedin = models.URLField(blank=True, null=True)
    portfolio = models.URLField(blank=True, null=True)
    expertise_areas = models.CharField(max_length=200)
    open_for_mentorship = models.BooleanField(default=True)
    availability = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100,default='N/A')
    country = models.CharField(max_length=100,default='N/A') 

    def __str__(self):
        return self.user.username


class InvestorProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='investor_profile')
    investment_firm = models.CharField(max_length=100, blank=True, null=True)
    investment_categories = models.CharField(max_length=200)
    min_investment = models.DecimalField(max_digits=15, decimal_places=2)
    max_investment = models.DecimalField(max_digits=15, decimal_places=2)
    stage_of_interest = models.CharField(max_length=100)
    city = models.CharField(max_length=100,default='N/A')
    country = models.CharField(max_length=100,default='N/A') 

    def __str__(self):
        return self.user.username



