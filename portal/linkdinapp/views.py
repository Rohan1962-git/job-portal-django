from django.shortcuts import render, redirect
from .models import Job, Company
from .forms import JobseekerForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import JobForm
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.contrib import messages
from .models import Application
from django.contrib.auth.decorators import user_passes_test


def home(request):
    query = request.GET.get("q")
    if query:
        jobs = Job.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(company__name__icontains=query) |
            Q(company__location__icontains=query)
        )
    else:
        jobs = Job.objects.all()

    return render(request, "portal/home.html", {"jobs": jobs})

@login_required
def jobseeker_register(request):
    if request.method == "POST":
        form = JobseekerForm(request.POST)
        if form.is_valid():
            jobseeker = form.save(commit=False)
            jobseeker.user = request.user  # link with logged-in user
            jobseeker.save()
            return redirect("home")  # after successful registration
    else:
        form = JobseekerForm()

    return render(request, "jobseeker_register.html", {"form": form})
@login_required
def post_job(request):
    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            company_name = form.cleaned_data['company_name']
            location = form.cleaned_data['location']

            # Get or create company
            company, created = Company.objects.get_or_create(name=company_name)
            company.location = location
            company.save()

            Job.objects.create(
                title=title,
                description=description,
                company=company,
                posted_by=request.user
            )

            return redirect("home")
    else:
        form = JobForm()

    return render(request, "portal/post_job.html", {"form": form})
from .models import Application

@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    application, created = Application.objects.get_or_create(
        job=job,
        applicant=request.user
    )

    if created:
        messages.success(request, "You have successfully applied for this job!")
    else:
        messages.warning(request, "You have already applied for this job.")

    return redirect("my_applications")
@login_required
def my_jobs(request):
    jobs = Job.objects.filter(posted_by=request.user)
    return render(request, "portal/my_jobs.html", {"jobs": jobs})

@login_required
def edit_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, posted_by=request.user)

    if request.method == "POST":
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            company_name = form.cleaned_data['company_name']
            location = form.cleaned_data['location']
            company, created = Company.objects.get_or_create(name=company_name)
            company.location = location
            company.save()

            job.title = title
            job.description = description
            job.company = company
            job.save()

            return redirect("my_jobs")
    else:
        initial_data = {
            "title": job.title,
            "description": job.description,
            "company_name": job.company.name if job.company else "",
            "location": job.company.location if job.company else "",
        }
        form = JobForm(initial=initial_data)

    return render(request, "portal/post_job.html", {"form": form, "edit": True})


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()

    return render(request, "portal/signup.html", {"form": form})

def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    return render(request, "portal/job_detail.html", {"job": job})

@login_required
def my_applications(request):
    jobs = Job.objects.all()
    applied_jobs = Application.objects.filter(applicant=request.user).values_list("job_id", flat=True)

    return render(request, "portal/my_applications.html", {
        "jobs": jobs,
        "applied_jobs": applied_jobs,
    })

# Check if user is admin/staff
def is_admin(user):
    return user.is_staff  # or user.is_superuser

@user_passes_test(is_admin)
def create_job(request):
    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Job posted successfully!")
            return redirect("home")  # or wherever you want
    else:
        form = JobForm()
    return render(request, "portal/create_job.html", {"form": form})

@login_required
def create_job(request):
    if not request.user.is_staff:  # only admins can post
        return redirect("home")

    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user   # save who posted
            job.save()
            return redirect("home")  # after posting, go to home page
    else:
        form = JobForm()

    return render(request, "portal/post_job.html", {"form": form})