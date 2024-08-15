from django.shortcuts import render


def home_page_view(request):
    return render(request, "pages/home.html")

def about_page_view(request):
    return render(request, "pages/about.html")
def my_lab_journal(request):
    return render(request, "pages/my_lab_journals.html")

def my_projects(request):
    return render(request, "pages/my_projects.html")


def privacy_policy(request):
    return render(request, 'privacy_policy.html')

