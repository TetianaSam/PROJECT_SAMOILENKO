from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserFileForm
from .models import UserFile
from django.db.models import Q

@login_required
def upload_protocol(request):
    if request.method == 'POST':
        form = UserFileForm(request.POST, request.FILES)
        if form.is_valid():
            user_file = form.save(commit=False)
            user_file.user = request.user
            user_file.save()
            return redirect('protocol_list')
    else:
        form = UserFileForm()
    return render(request, 'upload_protocol.html', {'form': form})

@login_required
def protocol_list(request):
    query = request.GET.get('q')
    files = UserFile.objects.filter(user=request.user)

    if query:
        files = files.filter(
            Q(title__icontains=query) |
            Q(uploaded_at__icontains=query)
        )

    return render(request, 'protocol_list.html', {'files': files, 'query': query})
