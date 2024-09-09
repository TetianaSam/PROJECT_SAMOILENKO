from django.shortcuts import render
from django.conf import settings
import os

def home_page_view(request):
    return render(request, "pages/home.html")

def about_page_view(request):
    return render(request, "pages/about.html")
def my_lab_journal(request):
    return render(request, "pages/my_lab_journals.html")

def my_projects(request):
    return render(request, "pages/my_projects.html")
def my_protocols(request):
    return render(request, "pages/my_protocols.html")
def my_literature(request):
    return render(request, "pages/my_literature.html")
def my_reagents_and_consumables(request):
    return render(request, "pages/reagents_and_consumables.html")
def my_projects(request):
    return render(request, "pages/my_projects.html")
def useful_resources(request):
    return render(request, "pages/useful_resources.html")
def privacy_policy(request):

    file_path = os.path.join(settings.BASE_DIR, 'static/text/privacy_policy.txt')

    with open(file_path, 'r', encoding='utf-8') as file:
        policy_content = file.read()

    return render(request, 'privacy_policy.html', {'policy_content': policy_content})