from django.shortcuts import render, redirect
from .models import Protocol
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from .forms import ProtocolForm, SearchForm
from django.http import HttpResponse, HttpResponseNotFound,FileResponse
from django.utils.html import escape
from django.contrib.auth.decorators import login_required
import mimetypes
import os

@login_required
def protocol_list(request):
    search_form = SearchForm(request.GET or None)
    protocols = Protocol.objects.all()

    if search_form.is_valid():
        query = search_form.cleaned_data.get('query')
        if query:
            protocols = protocols.filter(name__icontains=query)  # Пошук по назві протоколу

    # Додаємо розмір і тип файлу до кожного протоколу
    for protocol in protocols:
        if protocol.file:
            protocol.file_size = protocol.file.size
            protocol.file_type = mimetypes.guess_type(protocol.file.name)[0] or 'Unknown'

    return render(request, 'protocol_list.html', {
        'protocols': protocols,
        'search_form': search_form
    })

@login_required
def create_protocol(request):
    if request.method == 'POST':
        form = ProtocolForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('protocol_list')
    else:
        form = ProtocolForm()

    return render(request, 'create_protocol.html', {'form': form})
@login_required
def edit_protocol(request, pk):
    protocol = get_object_or_404(Protocol, pk=pk)

    if request.method == 'POST':
        form = ProtocolForm(request.POST, request.FILES, instance=protocol)
        if form.is_valid():
            if confirm_edit(request):
                form.save()
                return redirect('protocol_list')
    else:
        form = ProtocolForm(instance=protocol)

    return render(request, 'edit_protocol.html', {'form': form, 'protocol': protocol})

@login_required
def confirm_edit(request):
    # Реалізуйте тут вашу логіку підтвердження змін
    return True
@login_required
def delete_protocol(request, pk):
    protocol = get_object_or_404(Protocol, pk=pk)

    if request.method == 'POST':
        if confirm_delete(request):
            protocol.delete()
            return redirect('protocol_list')
    return render(request, 'confirm_delete.html', {'protocol': protocol})

@login_required
def confirm_delete(request):
    # Реалізуйте тут вашу логіку підтвердження видалення
    return True

@login_required
def download_protocol(request, pk):
    protocol = get_object_or_404(Protocol, pk=pk)

    response = HttpResponse(protocol.file, content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{protocol.file.name}"'

    return response
@login_required
def view_protocol(request, pk):
    protocol = get_object_or_404(Protocol, pk=pk)

    if not protocol.file:
        return HttpResponseNotFound("No file associated with this protocol")

    file_path = protocol.file.path
    file_name = protocol.file.name
    mime_type, encoding = mimetypes.guess_type(file_path)

    if mime_type is None:
        mime_type = 'application/octet-stream'

    if mime_type.startswith('image/') or mime_type == 'application/pdf':
        # For images and PDFs, serve the file directly
        if not os.path.exists(file_path):
            return HttpResponseNotFound("File not found")
        response = FileResponse(open(file_path, 'rb'), content_type=mime_type)
        response['Content-Disposition'] = f'inline; filename="{os.path.basename(file_path)}"'
        return response
    elif mime_type.startswith('text/') or mime_type in ('application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'):
        # For text files and Word documents
        try:
            with open(file_path, 'r') as file:
                content = file.read()
            return render(request, 'views_files/view_text.html', {
                'content': escape(content),
                'file_name': file_name
            })
        except IOError:
            return HttpResponseNotFound("Error reading the file")
    else:
        # Handle other file types as generic downloads
        if not os.path.exists(file_path):
            return HttpResponseNotFound("File not found")
        response = FileResponse(open(file_path, 'rb'), content_type=mime_type)
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
        return response