from django.urls import path
from .views import home, user_form, update_cv, resume_update, resume1_html, resume_download_view, resume1_view, analyze_job_description,resume_download_pdf, resume_view, resume_keywords

urlpatterns = [
    path('', home, name='home'),
    path('user_form/', user_form, name='user_form'),
    path('resume1/<int:user_id>/', resume1_view, name='resume1'),
    path('api/update-cv/', update_cv, name='update_cv'),
    path('resume_update/', resume_update, name='resume_update'),
    path('resume1/', resume1_html, name='resume1_html'),
    path('resume_download/<int:user_id>/', resume_download_view, name='resume_download_view'),
    # path('resume_download/', resume_download_view, name='resume_download_view'),
    # path('resume1/<int:user_id>/', resume1_view, name='resume1'),
    path('resume1/', resume1_view, name='resume1'),
    path('api/analyze-job-description/', analyze_job_description, name='analyze_job_description'),
    path('resume/<str:resume_version>/<int:user_id>/', resume_view, name='resume_view'),  # 추가된 경로
    path('api/resume-keywords/<int:resume_version>/<int:user_id>/', resume_keywords, name='resume_keywords'),  # 추가된 경로

    path('resume_download_pdf/<int:user_id>/', resume_download_pdf, name='resume_download_pdf'),
]