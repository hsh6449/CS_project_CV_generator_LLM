from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.core.serializers import serialize
from django.template import RequestContext

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings

from .models import User, Company, Intern, Project, Paper, ExternalActivity, ResumeVersion, Resume, Keyword
from .serializers import UserSerializer, CompanySerializer, InternSerializer, ProjectSerializer, PaperSerializer, ExternalActivitySerializer
import requests
import logging
import json
import os
import time

from weasyprint import HTML
from datetime import date, datetime


logger = logging.getLogger(__name__)
LLM_SERVER_URL = 'http://llm:5001/generate'   # local llm , 172.28.0.2

def date_converter(o):
    if isinstance(o, (date, datetime)):
        return o.isoformat()
    raise TypeError(f"Object of type {o.__class__.__name__} is not JSON serializable")

#@csrf_exempt
def home(request):
    return render(request, 'home.html')

def user_form(request):
    if request.method == 'POST':
        # User 정보 수집
        name = request.POST.get('name')
        date_of_birth = request.POST.get('date_of_birth')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        academic = request.POST.get('academic')

        # User 생성
        user = User.objects.create(
            name=name,
            date_of_birth=date_of_birth,
            email=email,
            phone_number=phone_number,
            academic=academic
        )

        # Company 정보 수집 및 생성
        company_names = request.POST.getlist('company_name[]')
        roles = request.POST.getlist('role[]')
        start_dates = request.POST.getlist('start_date[]')
        end_dates = request.POST.getlist('end_date[]')
        experiences = request.POST.getlist('experience[]')

        for company_name, role, start_date, end_date, experience in zip(company_names, roles, start_dates, end_dates, experiences):
            if company_name:  # Ensure company_name is not null
                Company.objects.create(
                    company_name=company_name,
                    role=role,
                    start_date=start_date,
                    end_date=end_date,
                    experience=experience,
                    user_id=user
                )
        
        # Intern 정보 수집 및 생성
        intern_company_names = request.POST.getlist('intern_company_name[]')
        start_dates = request.POST.getlist('start_date[]')
        end_dates = request.POST.getlist('end_date[]')
        intern_experiences = request.POST.getlist('intern_experience[]')

        for intern_company_name, start_date, end_date, intern_experience in zip(intern_company_names, start_dates, end_dates, intern_experiences):
            if intern_company_name:  # Ensure intern_company_name is not null
                Intern.objects.create(
                    intern_company_name=intern_company_name,
                    start_date=start_date,
                    end_date=end_date,
                    experience=intern_experience,
                    user_id=user
                )

        # Project 정보 수집 및 생성
        project_names = request.POST.getlist('project_name[]')
        project_descriptions = request.POST.getlist('project_description[]')
        start_dates = request.POST.getlist('start_date[]')
        end_dates = request.POST.getlist('end_date[]')

        for project_name, project_description, start_date, end_date in zip(project_names, project_descriptions, start_dates, end_dates):
            if project_name:  # Ensure project_name is not null
                Project.objects.create(
                    project_name=project_name,
                    description=project_description,
                    start_date=start_date,
                    end_date=end_date,
                    user_id=user
                )

        # Paper 정보 수집 및 생성
        paper_titles = request.POST.getlist('paper_title[]')
        publication_dates = request.POST.getlist('publication_date[]')
        journals = request.POST.getlist('journal[]')
        abstracts = request.POST.getlist('abstract[]')

        for paper_title, publication_date, journal, abstract in zip(paper_titles, publication_dates, journals, abstracts):
            if paper_title:  # Ensure paper_title is not null
                Paper.objects.create(
                    paper_title=paper_title,
                    publication_date=publication_date,
                    journal=journal,
                    abstract=abstract,
                    user_id=user
                )

        # ExternalActivity 정보 수집 및 생성
        activity_names = request.POST.getlist('activity_name[]')
        activity_descriptions = request.POST.getlist('activity_description[]')
        activity_start_dates = request.POST.getlist('activity_start_date[]')
        activity_end_dates = request.POST.getlist('activity_end_date[]')

        for activity_name, activity_description, activity_start_date, activity_end_date in zip(activity_names, activity_descriptions, activity_start_dates, activity_end_dates):
            if activity_name:  # Ensure activity_name is not null
                ExternalActivity.objects.create(
                    activity_name=activity_name,
                    description=activity_description,
                    start_date=activity_start_date,
                    end_date=activity_end_date,
                    user_id=user
                )

        Resume.objects.create(
            user=user,
            version_number=0,
            content='',  # 초기 내용은 비워둘 수 있습니다.
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        return redirect('resume_download_view',user_id=user.id)
        #return redirect('resume1', user_id=user.id)
    
    return render(request, 'user_form.html')

def resume_download_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    companies = Company.objects.filter(user_id=user)
    interns = Intern.objects.filter(user_id=user)
    projects = Project.objects.filter(user_id=user)
    papers = Paper.objects.filter(user_id=user)
    activities = ExternalActivity.objects.filter(user_id=user)
    resumes = Resume.objects.filter(user=user)
    
    context = {
        'user': user,
        'companies': companies,
        'interns': interns,
        'projects': projects,
        'papers': papers,
        'activities': activities,
        'resume_versions': resumes
    }

    html_string = render_to_string('resume1.html', context)
    html = HTML(string=html_string)
    pdf = html.write_pdf()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="resume_{user_id}.pdf"'
    
    return response




def resume_download_pdf(request, user_id):
    user = User.objects.get(id=user_id)
    companies = Company.objects.filter(user_id=user)
    interns = Intern.objects.filter(user_id=user)
    projects = Project.objects.filter(user_id=user)
    papers = Paper.objects.filter(user_id=user)
    activities = ExternalActivity.objects.filter(user_id=user)
    
    context = {
        'user': user,
        'companies': companies,
        'interns': interns,
        'projects': projects,
        'papers': papers,
        'activities': activities
    }

    html_string = render_to_string('resume1.html', context)
    html = HTML(string=html_string)
    pdf = html.write_pdf()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="resume_{user_id}.pdf"'
    
    return response

def resume1_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    companies = Company.objects.filter(user_id=user)
    interns = Intern.objects.filter(user_id=user)
    projects = Project.objects.filter(user_id=user)
    papers = Paper.objects.filter(user_id=user)
    activities = ExternalActivity.objects.filter(user_id=user)
    
    context = {
        'user': user,
        'companies': companies,
        'interns': interns,
        'projects': projects,
        'papers': papers,
        'activities': activities,
        'resume_version': '0'
    }
    
    return render(request, 'resume1.html', context)

def resume_view(request, resume_version, user_id): # 각 버전의 resume
    user = get_object_or_404(User, id=user_id)
    companies = Company.objects.filter(user_id=user)
    interns = Intern.objects.filter(user_id=user)
    projects = Project.objects.filter(user_id=user)
    papers = Paper.objects.filter(user_id=user)
    activities = ExternalActivity.objects.filter(user_id=user)
    
    context = {
        'user': user,
        'companies': companies,
        'interns': interns,
        'projects': projects,
        'papers': papers,
        'activities': activities,
        'resume_version': resume_version
    }
    
    return render(request, 'resume1.html', context)

def resume_download_view(request, user_id):

    user = get_object_or_404(User, id=user_id)
    context = {
        'user': user,
        'user_id': user_id,
        'resume_versions' : ResumeVersion.objects.filter(user=user)}
    
    return render(request, 'resume_download.html', context)

def resume_update(request):
    return render(request, 'resume_update.html')


def resume1_html(request):
    # 'resume_template.html'는 해당 Django 프로젝트의 templates 디렉토리에 있어야 합니다.
    return render(request, 'resume1.html')


@csrf_exempt
def update_cv(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode('utf-8'))
            user_id = data.get('user_id')
            prompt = data.get('prompt')
            keywords = data.get('keywords', [])

            user = get_object_or_404(User, id=user_id)
            # companies = Company.objects.filter(user_id=user)
            # interns = Intern.objects.filter(user_id=user)
            # projects = Project.objects.filter(user_id=user)
            # papers = Paper.objects.filter(user_id=user)
            # activities = ExternalActivity.objects.filter(user_id=user)

            # CV 정보를 가져와 프롬프트에 추가
            cv_info = {
                "name": user.name,
                "date_of_birth": user.date_of_birth.isoformat() if user.date_of_birth else "",
                "email": user.email,
                "phone_number": user.phone_number,
                "academic": user.academic,
                "companies": list(user.Company.all().values('company_name', 'role', 'start_date', 'end_date', 'experience')),
                "internships": list(user.Intern.all().values('intern_company_name', 'start_date', 'end_date', 'experience')),
                "projects": list(user.project.all().values('project_name', 'description', 'start_date', 'end_date')),
                "papers": list(user.paper.all().values('paper_title', 'publication_date', 'journal', 'abstract')),
                "external_activities": list(user.external_activities.all().values('activity_name', 'description', 'start_date', 'end_date'))
            }

            history = user.history.splitlines() 

            cv_info_str = json.dumps(cv_info, ensure_ascii=False, default=date_converter)
            cv_format = """
<aside>
    <span class="img"></span>
    <hr />
    <h3>Education</h3>
    <h4>{{ user.academic }}</h4>
    <p>{{ user.date_of_birth }}</p>
    <hr />
    <h3>Skills</h3>
</aside>

<main>
    <h3>Summary</h3>
    <h4>{{ user.academic }}</h4>
    <p>Summary description...</p>
    <h3>Professional Experience</h3>
    <ol>
        {% for company in companies %}
        <li>
            <h4>{{ company.role }}</h4>
            <p>
                <span class="company">{{ company.company_name }}</span> . {{ company.period }}
            </p>
            <p>{{ company.experience }}</p>
        </li>
        {% endfor %}
    </ol>

    <h3>Internship Experience</h3>
    <ol>
        {% for intern in interns %}
        <li>
            <h4>{{ intern.intern_company_name }}</h4>
            <p><span class="company">{{ intern.period }}</span></p>
            <p>{{ intern.experience }}</p>
        </li>
        {% endfor %}
    </ol>

    <h3>Project Experience</h3>
    <ol>
        {% for project in projects %}
        <li>
            <h4>{{ project.project_name }}</h4>
            <p>{{ project.description }}</p>
            <p>
                <span class="company">{{ project.start_date }} - {{ project.end_date }}</span>
            </p>
        </li>
        {% endfor %}
    </ol>

    <h3>Publications</h3>
    <ol>
        {% for paper in papers %}
        <li>
            <h4>{{ paper.paper_title }}</h4>
            <p>{{ paper.journal }}</p>
            <p>{{ paper.publication_date }}</p>
            <p>{{ paper.abstract }}</p>
        </li>
        {% endfor %}
    </ol>

    <h3>External Activities</h3>
    <ol>
        {% for activity in activities %}
        <li>
            <h4>{{ activity.activity_name }}</h4>
            <p>{{ activity.description }}</p>
            <p>
                <span class="company">{{ activity.start_date }} - {{ activity.end_date }}</span>
            </p>
        </li>
        {% endfor %}
    </ol>
</main>
            """

            # 프롬프트에 CV 정보와 명시적인 답변 형식을 요구하는 텍스트 추가
            chat_history = "\n".join(history)
            full_prompt = f"""
User CV Information:
{cv_info_str}

Chat History:
{chat_history}

Extracted Keywords:
{', '.join(keywords)}

User Query:
{prompt}

Please update the CV content based on the provided information, highlighting the user's strengths based on the extracted keywords. Follow these instructions strictly:

1. Only include content within the [cv]...[/cv] tags.
2. Do not include any HTML tags outside of the provided template format.
3. Use Django template tags {{ }} to render dynamic content where necessary. If any changes are needed to these tags, replace {{ }} with text only.
4. Ensure the content is factual and does not contain any false information.
5. Highlight the user's strengths based on the extracted keywords.
6. In [cv]...[/cv] tags, do not use bold tags and [key] tags, [chat] tags or any other HTML tags for highlighting the keywords.

You can freely add any additional comments or information in the [chat]...[/chat] tags.

Here is the template format to follow:

Format:
[chat] Your response for chat [/chat]
[cv]
{cv_format}
[/cv]

Remember, your response should only contain the updated CV content within the [cv]...[/cv] tags.
"""

            logger.debug(f"Sending request to LLM server with prompt: {full_prompt}")

            response = requests.post("http://llm:5001/generate", json={"prompt": full_prompt})

            if response.status_code == 200:
                llm_response = response.json()
                generated_text = llm_response.get('generated_text', '')
                logger.debug(f"LLM server response: {llm_response}")

                chat_text, cv_text = "", ""
                if "[chat]" in generated_text and "[/chat]" in generated_text:
                    chat_text = generated_text.split("[chat]")[1].split("[/chat]")[0].strip()
                if "[cv]" in generated_text and "[/cv]" in generated_text:
                    cv_text = generated_text.split("[cv]")[1].split("[/cv]")[0].strip()

                    # 가장 높은 버전 번호를 조회하여 새로운 버전 번호 생성
                    highest_version_resume = ResumeVersion.objects.filter(user=user).order_by('-version_number').first()
                    new_version_number = highest_version_resume.version_number + 1 if highest_version_resume else 1

                    user_dir = os.path.join(settings.BASE_DIR, 'myapp/templates/', f'user_{user.id}')
                    os.makedirs(user_dir, exist_ok=True)

                    cv_file_path = os.path.join(user_dir, f'resume_version_{new_version_number}.html')
                    with open(cv_file_path, 'w', encoding='utf-8') as cv_file:
                        cv_file.write(cv_text)

                    # 새로운 이력서 버전 저장
                    ResumeVersion.objects.create(user=user, version_number=new_version_number)

                    time.sleep(1)  # 파일이 생성되기 전에 읽을 수 있도록 충분한 시간을 줍니다.
                    # user.updated_cv_file = True
                    # user.save()

                user.add_to_history(f"User: {prompt}")
                user.add_to_history(f"LLM: {chat_text}")


                # Render the updated CV content
                return JsonResponse({
                    "chat": chat_text,
                    "cv_text": cv_text
                })
            else:
                return JsonResponse({"error": "Failed to get response from LLM server"}, status=500)
            
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)
        
def update_cv_with_response(user_id, llm_response_text):
    try:
        # 사용자 객체 가져오기
        user = User.objects.get(id=user_id)
        
        # 사용자 정보 업데이트 (예: academic 필드 업데이트)
        user.academic = llm_response_text
        user.save()

        logger.debug("User updated: %s", user)

        # 업데이트된 사용자 정보를 HTML로 변환하여 반환
        updated_cv_html = f"<h2>{user.academic}</h2>"

        return updated_cv_html
    except User.DoesNotExist:
        logger.error("User with id %s does not exist", user_id)
        return None
    except Exception as e:
        logger.error("An error occurred while updating user: %s", str(e))
        return None
    
def analyze_job_description(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode('utf-8'))
            job_description = data.get('job_description')
            user_id = data.get('user_id')
            resume_version = data.get('resume_version', 0)
            company_id = data.get('company_id')

            if not job_description:
                return JsonResponse({"error": "Job description is required"}, status=400)

            full_prompt = f"Extract the four most relevant keywords from the following job description and wrap each keyword in [key] tags like [key]Machine learning Skill[/key]: {job_description}"

            logger.debug(f"Sending request to LLM server with prompt: {full_prompt}")

            response = requests.post("http://llm:5001/generate", json={"prompt": full_prompt})

            if response.status_code == 200:
                llm_response = response.json()
                generated_text = llm_response.get('generated_text', '')
                logger.debug(f"LLM server response: {llm_response}")

                # Extract keywords from the generated text
                keywords = []
                start = generated_text.find('[key]')
                while start != -1:
                    end = generated_text.find('[/key]', start)
                    if end == -1:
                        break
                    keyword = generated_text[start+5:end].strip()
                    keywords.append(keyword)
                    start = generated_text.find('[key]', end)

                # Save the extracted keywords to a new resume version
                user = get_object_or_404(User, id=user_id)
                latest_version = Resume.objects.filter(user=user).order_by('-version_number').first()
                new_version_number = (latest_version.version_number + 1) if latest_version else 1
                resume = Resume.objects.create(user=user, version_number=new_version_number, content='')

                company = Company.objects.get(id=company_id) if company_id else None  # 회사 객체를 가져옵니다

                for keyword in keywords:
                    Keyword.objects.create(keyword=keyword, resume=resume, company=company)

                return JsonResponse({"keywords": keywords})
            else:
                return JsonResponse({"error": "Failed to get response from LLM server"}, status=500)

        except Exception as e:
            logger.error(f"An error occurred: {e}")
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)
    
def resume_json(request, user_id):
    user = get_object_or_404(User, id=user_id)
    companies = Company.objects.filter(user_id=user)
    interns = Intern.objects.filter(user_id=user)
    projects = Project.objects.filter(user_id=user)
    papers = Paper.objects.filter(user_id=user)
    activities = ExternalActivity.objects.filter(user_id=user)

    user_data = {
        'id': user.id,
        'name': user.name,
        'date_of_birth': user.date_of_birth.isoformat() if user.date_of_birth else "",
        'email': user.email,
        'phone_number': user.phone_number,
        'academic': user.academic,
    }

    return JsonResponse({
        'user': user_data,
        'companies': list(companies.values()),
        'interns': list(interns.values()),
        'projects': list(projects.values()),
        'papers': list(papers.values()),
        'activities': list(activities.values()),
    }, json_dumps_params={'default': date_converter})

def resume_keywords(request, resume_version, user_id):
    try:
        resume = get_object_or_404(Resume, user_id=user_id, version_number=resume_version)
        keywords = resume.keywords.all()

        if not keywords.exists():
            return JsonResponse({"keywords": []})

        keywords_data = [{"keyword": keyword.keyword} for keyword in keywords]
        return JsonResponse({"keywords": keywords_data})
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({"error": str(e)}, status=500)