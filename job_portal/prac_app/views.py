from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
from prac_app.models import *
from prac_app.forms import *
# from job_app.utils import calculate_skill_match

# ==================================================
# REGISTER
# ==================================================

def register_page(request):

    if request.method == 'POST':

        form_data = RegistrationForm(request.POST)

        if form_data.is_valid():

            form_data.save()

            messages.success(
                request,
                'Registration Successful'
            )

            return redirect('login_page')

    else:

        form_data = RegistrationForm()

    context = {
        'form_data': form_data,
        'form_title': 'Registration Form',
        'form_btn': 'Register',
    }

    return render(
        request,
        'master/base-form.html',
        context
    )


# ==================================================
# LOGIN
# ==================================================

def login_page(request):

    if request.method == 'POST':

        form_data = AuthenticationForm(
            request,
            data=request.POST
        )

        if form_data.is_valid():

            user = form_data.get_user()

            login(request, user)

            if user.user_type == 'recruiter':
                return redirect('recruiter_profile')

            elif user.user_type == 'jobseeker':
                return redirect('jobseeker_profile')

    else:

        form_data = AuthenticationForm()

    context = {
        'form_data': form_data,
        'form_title': 'Login Form',
        'form_btn': 'Login',
    }

    return render(
        request,
        'master/base-form.html',
        context
    )


# ==================================================
# LOGOUT
# ==================================================

@login_required
def logout_page(request):

    logout(request)

    messages.success(
        request,
        'Logout Successful'
    )

    return redirect('login_page')




@login_required
def jobseeker_profile(request):
    if request.user.user_type!='jobseeker':
        return redirect('login_page')
    profile=JobSeekerProfile.objects.filter(
        user=request.user).first()
    if request.method=='POST':
        form_data = JobSeekerProfileForm(
            request.POST,
            request.FILES,
            instance=profile)
        
        if form_data.is_valid():
            save_data = form_data.save(commit=False)
            save_data.user=request.user
            save_data.save()
            if profile:
                messages.success(request,
                'Profile updated successfully')
            else:
                messages.success(request,
                'Profile Created Successfully')
            return redirect('jobseeker_profile')
    
    if request.method=='POST' and 'delete_profile' in request.POST:
        if profile:
            profile.delete()
            messages.success(request,'Profile Deleted Successfully')
        return redirect('jobseeker_profile')

    else:
        form_data = JobSeekerProfileForm(instance=profile)

    if not profile or request.GET.get('edit'):
        context={
        'form_data' : form_data,
        'form-title' : 'jobseeker profile form',
        'form_btn' : 'Save profile'
    }
        return render(request,'master/base-form.html', context)

    return render(request,'profile/jobseeker-profile.html',{'profile' : profile})



@login_required
def recruiter_profile(request):

    if request.user.user_type!='recruiter':
        return redirect('login_page')
    
    profile = RecruiterProfile.objects.filter(
        user=request.user).first()
    
    if request.method=='POST':

        form_data = RecruiterProfileForm(
            request.POST,
            request.FILES,
            instance=profile)
        
        if form_data.is_valid():

            save_data = form_data.save(commit=False)

            save_data.user = request.user

            save_data.save()

            if profile:

                messages.success(request,'Updated')

            else:

                messages.success(request,'Created')

            return redirect('recruiter_profile')
        
        if request.method=='POST' and 'delete_profile' in request.POST:
            if profile:
                profile.delete()
                messages.success(request,'Deleted')
            return redirect('recruiter_profile')
    else:

        form_data = RecruiterProfileForm(instance=profile)

    if not profile or request.GET.get('edit'):

        context={
            'form_data' : form_data,
            'form_title' : "recruiter profile form",
            'form_btn' : 'save profile',
        }

        return render(request,'master/base-form.html', context)

    return render(          
            request,
            'profile/recruiter-profile.html',
            {'profile' : profile}
        )












@login_required
def recruiter_jobs(request):

    if request.user.user_type!= 'recruiter':
        return redirect('login_page')
    
    recruiter_profile=get_object_or_404(
        RecruiterProfile,
        user=request.user
    )

    jobs = Job.objects.filter(
        recruiter=recruiter_profile
        ).order_by('-id')
    
    job_id = request.GET.get('edit')

    job_instance = None

    if job_id:

        job_instance=get_object_or_404(
            Job,
            id=job_id,
            recruiter=recruiter_profile
            )
        
    if request.method == "POST" and 'delete_job' in request.POST:

        delete_id = request.POST.get('delete_job')

        delete_job=get_object_or_404(
            Job,
            id=delete_id,
            recruiter=recruiter_profile
            )
        
        delete_job.delete()

        messages.success(request,'deleted')

        return redirect('recruiter_jobs')
    
    if request.method == 'POST':

        form_data=JobForm(
            request.POST,
            instance=job_instance
            )

        if form_data.is_valid():

            save_data = form_data.save(commit=False)

            save_data.recruiter = recruiter_profile

            save_data.save()

            if job_instance:
                messages.success(request,'job updated')

            else:
                messages.success(request,'job created')

            return redirect('recruiter_jobs')
    else:
        form_data=JobForm(instance=job_instance)

    if request.GET.get('create') or job_instance:
        context={
            'form_data': form_data,
            'form_title': 'Job Form',
            'form_btn': 'Save Job'
        }
        return render(request,'master/base-form.html',context)
    
    return render(request,'job/recruiter-jobs.html',{'jobs' : jobs})




def all_jobs(request):
    if request.user.is_authenticated and request.user.user_type == 'recruiter':
        return redirect('recruiter_dashboard') #A recruiter could still manually visit the URL:/all-jobs/. To fully prevent recruiters from accessing the page, add this check in the view as well:

    jobs = Job.objects.all().order_by('-id')
    search = request.GET.get('search')

    if search:
        jobs = jobs.filter(
            Q(title__icontains=search) |
            Q(category__icontains=search) |
            Q(skills_set__icontains=search)
        ).distinct()

    if request.method == 'POST':

        # User must login before applying
        if not request.user.is_authenticated:
            messages.warning(
                request,
                "Please login or register to apply for jobs."
            )
            return redirect('login_page')

        # Only jobseekers can apply
        if request.user.user_type != 'jobseeker':
            messages.warning(
                request,
                "Only jobseekers can apply for jobs."
            )
            return redirect('login_page')

        job_id = request.POST.get('job_id')

        job = get_object_or_404(Job, id=job_id)

        seeker_profile = get_object_or_404(
            JobSeekerProfile,
            user=request.user
        )

        already_applied = JobApplication.objects.filter(
            job=job,
            applicant=seeker_profile
        ).exists()

        if already_applied:
            messages.warning(request, "You already applied")
        else:
            JobApplication.objects.create(
                job=job,
                applicant=seeker_profile
            )
            messages.success(
                request,
                "Job applied successfully"
            )

        return redirect('all_jobs')

    return render(
        request,
        'job/all-jobs.html',
        {
            'jobs': jobs,
            'search': search
        }
    )


@login_required
def recruiter_applicants(request):
    if request.user.user_type!='recruiter':
        return redirect('login_page')
    recruiter_profile=get_object_or_404(
        RecruiterProfile,user=request.user)
    
    jobs = Job.objects.filter(
        recruiter=recruiter_profile,

        ).prefetch_related('jobapplication_set')
    return render(request,'job/recruiter-applicants.html',{'jobs' : jobs})


@login_required
def applied_jobs(request):
    if request.user.user_type!='jobseeker':
        return redirect('login_page')
    seeker_profile=get_object_or_404(
        JobSeekerProfile,user=request.user
    )
    applications=JobApplication.objects.filter(
        applicant=seeker_profile).select_related('job')
    if request.method == 'POST':
        application_id = request.POST.get('remove_application')
        application = get_object_or_404(
            JobApplication,
            id=application_id,
            applicant=seeker_profile
        )

        application.delete()
        messages.success(request,'deleted')
        return redirect('applied_jobs')
    return render(request,"job/applied-jobs.html",{'applications' : applications})





@login_required
def recruiter_dashboard(request):
    if request.user.user_type!='recruiter':
        return redirect('login_page')
    
    recruiter_profile=get_object_or_404(
        RecruiterProfile,
        user=request.user
    )

    jobs=Job.objects.filter(
        recruiter=recruiter_profile
    )

    total_jobs=jobs.count()

    applications=JobApplication.objects.filter(
        job__recruiter=recruiter_profile
    ).select_related('applicant','job')

    total_applicants = applications.count()

    for application in applications:
        applicant_skills = [
            skill.strip().lower()
            for skill in application.applicant.skills.split(',')
        ]

        job_skills=[
            skill.strip().lower()
            for skill in application.job.skills_set.split(',')
        ]

        matched_skill=0

        for skill in applicant_skills:
            if skill in job_skills:
                matched_skill+=1

        if len(job_skills)>0:
            application.match_percentage=int(
                (matched_skill/len(job_skills))*100
            )
        else:
            application.match_percentage = 0

    applications=sorted(
        applications,
        key=lambda x: x.match_percentage,
        reverse=True
    )

    best_candidate = None
    worst_candidate = None

    if applications:
        best_candidate = applications[0]
        worst_candidate = applications[-1]

    context={
        'total_jobs' : total_jobs,
        'total_applicants' : total_applicants,
        'applications' : applications,
        'best_candidate' : best_candidate,
        'worst_candidate' : worst_candidate,
    }
    return render(request,'dashboard/recruiter-dashboard.html',context)



@login_required
def jobseeker_dashboard(request):
    if request.user.user_type!='jobseeker':
        return redirect('login_page')
    seeker_profile=get_object_or_404(
        JobSeekerProfile,user=request.user
    )

    total_applied_jobs = JobApplication.objects.filter(
        applicant=seeker_profile
    ).count()

    jobs = Job.objects.all()

    matched_jobs=[]

    user_skills = []
    for skill in seeker_profile.skills.lower().split(','):
        user_skills.append(skill.strip())

    for job in jobs:
        job_skills=[]
        for skill in job.skills_set.lower().split(','):
            job_skills.append(skill.strip())

        total_skill = len(job_skills)

        matched_skill = 0

        for user_skill in user_skills:

            if user_skill.strip() in job_skills:
                matched_skill+=1

        if matched_skill>0:
            job.match_percentage=int(
            (matched_skill/total_skill)*100
            )

            matched_jobs.append(job)

    matched_jobs = sorted(
        matched_jobs,
        key=lambda x:x.match_percentage,
        reverse=True
    )

    context={
        'total_applied_jobs' : total_applied_jobs,
        'matched_jobs' : matched_jobs[:5]
    }

    return render(request,'dashboard/jobseeker-dashboard.html',context)



def job_details(request, id):

    job = get_object_or_404(Job, id=id)

    return render(
        request,
        'job/job-details.html',
        {
            'job': job
        }
    )