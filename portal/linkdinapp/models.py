from django.db import models
from django.contrib.auth.models import User


class Employer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    website = models.URLField(blank=True)

    def __str__(self):
        return self.company_name

class Company(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True, null=True)  # optional
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name



class Job(models.Model):
    title = models.CharField(max_length=200)
    location = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title


class Jobseeker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    skills = models.TextField(blank=True)
    email_id = models.EmailField(unique=True, default="default@example.com")
    resume = models.FileField(upload_to="resumes/", blank=True, null=True)
    experience = models.IntegerField()
    mobile = models.IntegerField()


class Application(models.Model):
    job = models.ForeignKey(Job,on_delete=models.CASCADE)
    applicant = models.ForeignKey(User ,on_delete=models.CASCADE)
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.applicant.username} -> {self.job.title}"


# Create your models here.
