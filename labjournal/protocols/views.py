from django.shortcuts import render, redirect
from .models import Protocol
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from .forms import ProtocolForm
from django.http import HttpResponse
from django.utils.html import escape

def protocol_list(request):
    protocols = Protocol.objects.all()
    return render(request, 'protocol_list.html', {'protocols': protocols})


def create_protocol(request):
    if request.method == 'POST':
        form = ProtocolForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('protocol_list')
    else:
        form = ProtocolForm()

    return render(request, 'create_protocol.html', {'form': form})

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


def confirm_edit(request):
    # Реалізуйте тут вашу логіку підтвердження змін
    return True

def delete_protocol(request, pk):
    protocol = get_object_or_404(Protocol, pk=pk)

    if request.method == 'POST':
        if confirm_delete(request):
            protocol.delete()
            return redirect('protocol_list')
    return render(request, 'confirm_delete.html', {'protocol': protocol})


def confirm_delete(request):
    # Реалізуйте тут вашу логіку підтвердження видалення
    return True


def download_protocol(request, pk):
    protocol = get_object_or_404(Protocol, pk=pk)

    response = HttpResponse(protocol.file, content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{protocol.file.name}"'

    return response

def view_protocol(request, pk):
    protocol = get_object_or_404(Protocol, pk=pk)

    if not protocol.file:
        # Handle the case where no file is associated
        return HttpResponseNotFound("No file found")

    file_url = protocol.file.url

    # For different file types, you might need to handle rendering differently
    if file_url.endswith('.pdf'):
        return render(request, 'views_files/view_pdf.html', {'file_url': file_url})
    elif file_url.endswith(('.png', '.jpg', '.jpeg', '.gif')):
        return render(request, 'views_files/view_image.html', {'file_url': file_url})
    else:
        # Default behavior for other types (e.g., text files)
        try:
            with open(protocol.file.path, 'r') as file:
                content = file.read()
            return render(request, 'views_files/view_text.html', {'content': escape(content), 'file_name': protocol.file.name})
        except IOError:
            return HttpResponseNotFound("Error reading the file")