from django.http import JsonResponse, FileResponse
from books.models import Book
import os
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from .forms import UploadFileForm
from .mixins import LoggingMixin


def my_json_view(request):
    data = {
        'name': 'John Doe',
        'age': 30,
        'city': 'New York'
    }
    return JsonResponse(data)


@login_required
def books_json(request):
    books = Book.objects.all()
    books_list = list(books.values('title', 'author', 'published_date', 'isbn', 'summary', 'genre'))
    return JsonResponse(books_list, safe=False)


def my_file_view(request):
    # file_path = os.path.join(settings.MEDIA_ROOT, 'files', "test_file.txt")
    file_path = os.path.join(settings.MEDIA_ROOT, 'files', "Figma basics.png")
    return FileResponse(open(file_path, 'rb'), as_attachment=True, filename='downloaded_file.png')


class FileUploadView(LoggingMixin, FormView):
    form_class = UploadFileForm
    template_name = 'upload_file.html'
    success_url = reverse_lazy('upload_file')

    def form_valid(self, form):
        self.log_action('Update')
        title = form.cleaned_data['title']
        uploaded_file = form.cleaned_data['file']

        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        file_url = fs.url(filename)

        # Adding the file_url to the context to be used in the template
        self.extra_context = {'file_url': file_url}

        return super().form_valid(form)


from django.shortcuts import render

# Create your views here.
