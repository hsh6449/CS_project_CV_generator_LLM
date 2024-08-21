from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone

class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30,null=True,blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    email = models.EmailField(null=True,blank=True)
    phone_number = models.CharField(
        max_length=13,  
        validators=[
            RegexValidator(
                regex=r'^01[016789]-\d{3,4}-\d{4}$',
                message="Phone number must be entered in the format: '010-1234-5678' or '010-123-4567'."
            ),
        ],
        null=True,blank=True
    )
    academic = models.CharField(max_length=30,null=True,blank=True)

    history = models.TextField(default="")  # 새로운 필드 추가
    # updated_cv_file = models.BooleanField(default=False)

    def add_to_history(self, entry):
        self.history += f"{entry}\n"
        self.save()

class Company(models.Model):
    id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=255, null=True,blank=True)
    role = models.CharField(max_length=255, null=True,blank=True)
    start_date = models.DateField(null=True,blank=True)
    end_date = models.DateField(null=True,blank=True)
    experience = models.CharField(max_length=255, null=True,blank=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Company')

class Intern(models.Model):
    id = models.AutoField(primary_key=True)
    intern_company_name = models.CharField(max_length=255,null=True,blank=True)
    start_date = models.DateField(null=True,blank=True)
    end_date = models.DateField(null=True,blank=True)
    experience = models.CharField(max_length=255, null=True,blank=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Intern')

class Project(models.Model):
    id = models.AutoField(primary_key=True)
    project_name = models.CharField(max_length=255,null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    start_date = models.DateField(null=True,blank=True)
    end_date = models.DateField(null=True,blank=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='project')

class Paper(models.Model):
    id = models.AutoField(primary_key=True)
    paper_title = models.CharField(max_length=255,null=True,blank=True)
    publication_date = models.DateField(null=True,blank=True)
    journal = models.CharField(max_length=255, null=True,blank=True)
    abstract = models.TextField(null=True,blank=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='paper')

class ExternalActivity(models.Model):
    id = models.AutoField(primary_key=True)
    activity_name = models.CharField(max_length=255,null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    start_date = models.DateField(null=True,blank=True)
    end_date = models.DateField(null=True,blank=True)  
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='external_activities')

class ResumeVersion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    version_number = models.PositiveIntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.name} - Version {self.version_number}"
    

class Resume(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resumes')
    version_number = models.IntegerField(default=1)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # keywords = models.ManyToManyField('Keyword', related_name='resumes')


class Keyword(models.Model):
    id = models.AutoField(primary_key=True)
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='keywords')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='keywords', null=True, blank=True)
    keyword = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)