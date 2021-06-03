from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from .forms import *
from django.conf import settings
from django.core.files.storage import FileSystemStorage
# from django_encrypt_file import EncryptionService, ValidationError
from .util import *
from .models import *

# def encrypt_view(request):
#    try:
#        myfile = request.FILES.get('myfile', None)
#        password = request.POST.get('password', None)
#        encrypted_file = EncryptionService().encrypt_file(myfile, password, extension='enc')
#        mymodel = MyModel.objects.create(uploaded_file=encrypted_file)
#    except ValidationError as e:
#        print(e)




# Create your views here.

def home(request):
    # print(type(Document.objects.order_by('id').first().document))
    # print(Document.objects.order_by('id').first().document)
    return render(request,'upload/base.html')


def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)        
        # Document.objects.order_by('id').first().document
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = DocumentForm()
    return render(request, 'upload/upload.html', {
        'form': form
    })