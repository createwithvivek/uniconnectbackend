from django.db import models
from django.contrib.auth import get_user_model
from startups.models import Startup

User = get_user_model()

class InvestorShortlist(models.Model):
    investor = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'INVESTOR'})
    startup = models.ForeignKey(Startup, on_delete=models.CASCADE)
    shortlisted_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.investor.username} shortlisted {self.startup.startup_name}"

class InvestorPitchRequest(models.Model):
    investor = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'INVESTOR'})
    startup = models.ForeignKey(Startup, on_delete=models.CASCADE)
    message = models.TextField(blank=True, null=True)
    requested_on = models.DateTimeField(auto_now_add=True)
