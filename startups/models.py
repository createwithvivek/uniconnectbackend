from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Startup(models.Model):
    CATEGORY_CHOICES = [
        ('AI', 'Technology & AI'),
        ('Healthcare', 'Healthcare & Biotech'),
        ('Fintech', 'Fintech & Blockchain'),
        ('EdTech', 'EdTech & E-Learning'),
        ('SaaS', 'SaaS & Cloud Computing'),
        ('Ecommerce', 'E-commerce & Retail'),
        ('SocialImpact', 'Social Impact & Sustainability'),
        ('ConsumerProducts', 'Consumer Products & Services'),
    ]

    founder = models.ForeignKey(User, on_delete=models.CASCADE, related_name='startups')
    name = models.CharField(max_length=100)
    problem_statement = models.TextField()
    solution_approach = models.TextField()
    business_model = models.TextField()
    market_audience = models.TextField()
    funding_required = models.CharField(max_length=50)
    pitch_deck = models.FileField(upload_to='pitch_decks/', null=True, blank=True)
    pitch_video_link = models.URLField(null=True, blank=True)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved_by_mentor = models.BooleanField(default=False)

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    startup = models.ForeignKey(Startup, on_delete=models.CASCADE)
    voted_at = models.DateTimeField(auto_now_add=True)

class WeeklyIdeaSubmission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    startup = models.ForeignKey(Startup, on_delete=models.CASCADE, null=True, blank=True)
    idea_summary = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

class InvestorShortlist(models.Model):
    investor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shortlisted_startups')
    startup = models.ForeignKey(Startup, on_delete=models.CASCADE, related_name='investor_shortlists_startups')
    shortlisted_at = models.DateTimeField(auto_now_add=True)
