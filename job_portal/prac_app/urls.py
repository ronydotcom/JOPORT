from django.urls import path
from prac_app.views import *

urlpatterns = [
    path('',register_page,name='register_page'),
    path('login/',login_page,name='login_page'),
    path('logout/',logout_page,name='logout_page'),
    path('jobseeker/profile/',jobseeker_profile,name='jobseeker_profile'),
    path('recruiter/profile/',recruiter_profile,name='recruiter_profile'),
    path('recruiter/jobs/',recruiter_jobs,name='recruiter_jobs'),
    path('all-jobs/',all_jobs,name='all_jobs'),
    path('recruiter-applicants/',recruiter_applicants,name='recruiter_applicants'),
    path('applied-jobs/',applied_jobs,name='applied_jobs'),
    path('recruiter-dashboard/',recruiter_dashboard,name='recruiter_dashboard'),
    path('jobseeker-dashboard/',jobseeker_dashboard,name='jobseeker_dashboard'),
    path('job/<int:id>/',job_details,name='job_details'),


]