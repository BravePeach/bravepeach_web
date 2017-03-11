"""
Utility Functions.
"""
import os
from django.shortcuts import render


def flavour_render(request, template_name, context=None, content_type=None, status=None, using=None):
    """
    Select template with flavour.
    request object has user_agent attr.
    """
    if request.user_agent.is_mobile:
        template_name = os.path.join("mobile", template_name)
    else:
        template_name = os.path.join("pc", template_name)
    return render(request, template_name, context, content_type, status, using)
