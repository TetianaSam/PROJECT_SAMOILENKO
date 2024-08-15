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

def my_plastic(request):
    return render(request, "pages/my_plastic.html")

def my_literature(request):
    return render(request, "pages/my_literature.html")

def my_chemicals(request):
    return render(request, "pages/my_chemicals.html")

def my_trainings(request):
    return render(request, "pages/my_trainings.html")

def my_projects(request):
    return render(request, "pages/my_projects.html")





def privacy_policy(request):
    # Path to the text file
    file_path = os.path.join(settings.BASE_DIR, 'static/text/privacy_policy.txt')

    # Read the file content
    with open(file_path, 'r', encoding='utf-8') as file:
        policy_content = file.read()

    # Pass the content to the template
    return render(request, 'privacy_policy.html', {'policy_content': policy_content})