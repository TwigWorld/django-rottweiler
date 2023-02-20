from django.views.generic.base import TemplateView


class RottyView(TemplateView):
    template_name = "index.html"
    permission_required = "project.barkbark"
