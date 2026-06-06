from django.db import models

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    USER_TYPE =(
        ('recruiter','recruiter'),
        ('jobseeker','jobseeker'),
    )
    display_name = models.CharField(max_length=100, null=True, blank=True)

    user_type = models.CharField(max_length=20, choices=USER_TYPE,null=True)
    
    def __str__(self):
        return f'{self.username}'
    

class RecruiterProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    company_name = models.CharField(max_length=500)

    company_email = models.EmailField()

    company_website = models.URLField(
        blank=True,
        null=True
    )

    company_description = models.TextField()

    company_logo = models.ImageField(
        upload_to='company_logo/',
        blank=True,
        null=True,
        max_length=500
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.company_name
    

class JobSeekerProfile(models.Model):

        user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

        full_name = models.CharField(max_length=500)

        skills = models.TextField(
        help_text="Example: Python, Django, React"
    )

        bio = models.TextField()

        profile_image = models.ImageField(
        upload_to='profile_image/',
        blank=True,
        null=True,
        max_length=500
    )

        resume = models.FileField(
        upload_to='resume/',
        blank=True,
        null=True,
        max_length=500
    )

        created_at = models.DateTimeField(
        auto_now_add=True
    )

        updated_at = models.DateTimeField(
        auto_now=True
    )

        def __str__(self):
            return self.full_name
    


class Job(models.Model):

    CATEGORY = (
        ('remote', 'Remote'),
        ('fulltime', 'Full Time'),
        ('parttime', 'Part Time'),
        ('internship', 'Internship'),
    )

    recruiter = models.ForeignKey(
        RecruiterProfile,
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=300)

    number_of_openings = models.PositiveIntegerField()

    category = models.CharField(
        max_length=100,
        choices=CATEGORY
    )

    job_description = models.TextField()

    skills_set = models.TextField(
        help_text="Example: Python, Django, React"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.title


class JobApplication(models.Model):

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE
    )

    applicant = models.ForeignKey(
        JobSeekerProfile,
        on_delete=models.CASCADE
    )

    applied_at = models.DateTimeField(
        auto_now_add=True
    )
    def __str__(self):
        return f'{self.applicant.full_name} - {self.job.title}'
    







    # # use it when :
    # class Meta:
    #       unique_together = ['job', 'applicant']
    #because it prevents:
    # same jobseeker applying to same job multiple times
        # Example: Without it:
        # Rahim applied to Python Developer job
        # Rahim applied again
        # Rahim applied again
        # Then database stores duplicate applications.