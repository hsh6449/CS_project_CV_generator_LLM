# scripts/update_initial_resumes.py
from myapp.models import Resume

# Update initial resumes
initial_resumes = Resume.objects.filter(version_number='initial')
initial_resumes.update(version_number=0)