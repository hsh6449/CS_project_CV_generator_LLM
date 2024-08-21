from django import template
from django.template.loader import render_to_string
from django.template import Context, TemplateDoesNotExist
import os
from django.conf import settings

register = template.Library()

@register.simple_tag(takes_context=True)
def include_dynamic(context, user, resume_version):
    template_name = f"user_{user.id}/resume_version_{resume_version}.html"
    context_dict = context.flatten()  # RequestContext를 dict로 변환
    try:
        # 파일이 존재하는지 확인
        cv_file_path = os.path.join(settings.BASE_DIR, 'myapp/templates', f'user_{user.id}', f'resume_version_{resume_version}.html')
        if not os.path.exists(cv_file_path):
            raise TemplateDoesNotExist(f"Template {template_name} does not exist")
        return render_to_string(template_name, context_dict)
    except TemplateDoesNotExist:
        return render_to_string("resume_content.html", context_dict)
