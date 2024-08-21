from django.contrib import admin

# 아래부터는 추가한 코드
from .models import User, Company, Intern, Project, Paper, ExternalActivity

admin.site.register(User)
admin.site.register(Company)
admin.site.register(Intern)
admin.site.register(Project)
admin.site.register(Paper)
admin.site.register(ExternalActivity)
# Register your models here.
