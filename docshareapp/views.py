import os

from django.shortcuts import render
from django.http import JsonResponse
import json
from .utils import FileManagement

from django.conf import settings
# from django.conf.settings import WORK_DIR as path
path = settings.WORK_DIR

# Create your views here.

def index(request):
    all_dirs = os.listdir(os.path.join(path, 'zenatix'))
    bread = ['zenatix']
    return render(request, 'index.html', {'all_dirs': all_dirs,'current_directory':os.path.join(path,'zenatix'),'bread':bread})

def create_folder(request):
    if request.method=='POST':
        received_json_data=json.loads(request.body)
        fileObj = FileManagement(path)
        current_directory = path+ "/zenatix/"
        folder_name = received_json_data.get('folder_name')
        print (folder_name)
        fileObj.create_directory(current_directory,folder_name)
        return JsonResponse({'data': 'Folder Created Successfully'}, content_type="application/json")

def list_directory(request):
    folder_name = request.GET.get('folder_name')
    current_directory = request.GET.get('current_directory')
    fileObj = FileManagement(path)
    list_of_files = fileObj.ls(os.path.join(current_directory,folder_name))
    return JsonResponse({'data': list_of_files}, content_type="application/json")

def download(request):
    folder_name = request.GET.get('folder_name')
    current_directory = request.GET.get('current_directory')
    fileObj = FileManagement(path)
    file_path = fileObj.download_file(current_directory,folder_name)
    return JsonResponse({'data': file_path}, content_type="application/json")