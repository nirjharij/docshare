# -*- coding: utf-8 -*-
import os
import mimetypes
from django.shortcuts import render
from django.http import JsonResponse
import json
from .utils import FileManagement

from django.conf import settings
from wsgiref.util import FileWrapper
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
# from django.conf.settings import WORK_DIR as path
path = settings.WORK_DIR

# Create your views here.

fileObj = FileManagement(path)

def index(request):
    if request.method=='GET':
        folder_path = request.GET.get('path', None)

        if folder_path == None:
            directory_content = fileObj.ls(os.path.join(path,'zenatix'))
            bread = [('zenatix','zenatix')]
            return render(
                request, 'index.html',
                {
                'files': directory_content['files'],
                 'directories': directory_content['directory'], 
                 'current_directory':'zenatix',
                 'bread':bread
                }
            )
        else:
            bread = []
            path_bread = []
            bread.extend(folder_path.split('/'))
            bread_path = ''
            for b in bread:
                if b == 'zenatix':
                    bread_path = 'zenatix'
                else:
                    bread_path = bread_path + "/" + b
                path_bread.append(bread_path)
            directory_content = fileObj.ls(os.path.join(path,folder_path))
            return render(
                request, 'index.html',
                {
                'files': directory_content['files'],
                 'directories': directory_content['directory'], 
                 'current_directory':folder_path,
                 'bread':zip(bread, path_bread)
                 }
            )

def create_folder(request):
    if request.method=='POST':
        received_json_data=json.loads(request.body)
        fileObj = FileManagement(path)
        directory = received_json_data.get('folder_path')
        current_directory = os.path.join(path,directory)
        folder_name = received_json_data.get('folder_name')
        fileObj.create_directory(current_directory,folder_name)
        return JsonResponse({'data': 'Folder Created Successfully'}, content_type="application/json")

def list_directory(request):
    data = {}
    folder_name = request.GET.get('folder_name')
    current_directory = request.GET.get('current_directory')
    # print(folder_name, current_directory, os.path.join(current_directory, folder_name), '<<<<<<<<<<<<<<<<')
    list_of_files = fileObj.ls(os.path.join(current_directory,folder_name))
    directory_list = []
    file_list = []
    for file in list_of_files:
        if fileObj.is_directory(os.path.join(current_directory, folder_name)):
            directory_list.append(file)
        else:
            file_list.append(file)
    data['directories'] = directory_list
    data['files'] = file_list
    return JsonResponse({'data': data}, content_type="application/json")

def download(request):
    file_path = request.GET.get('path', None)
    file_path = os.path.join(settings.WORK_DIR, file_path)
    filename = file_path.split('/')[-1]
    ext = {'txt': 'text/plain', 'pdf': 'application/pdf', 'py': 'application/py','JPG':'image/png','PNG':'image/png'}
    wrapper = FileWrapper(open(file_path,'rb'))
    content_type = ext.get(filename.split('.')[-1]) + "; charset=utf-8"
    response = HttpResponse(wrapper,content_type=content_type)
    attachment_name = 'attachment; filename={}'.format(filename)
    response['Content-Disposition'] = attachment_name
    response['Content-Length'] = os.path.getsize(file_path)
    return response

def upload(request):
    if request.method == 'POST':
        file = request.FILES['file_upload']
        current_directory = request.POST.get("path")
        fileObj.upload_file(file,current_directory)
    return HttpResponseRedirect(reverse("home"))

def search(request):
    if request.method == 'GET':
        current_directory = request.GET.get("path")
        pattern = request.GET.get("searchedfor")
        resp = fileObj.search(pattern)
    return render(
                request, 'index.html',
                {'files': resp['files'],
                 'directories': resp['directory'], 
                 'current_directory':current_directory
                 }
            )

def autocomplete(request):
    if request.method == 'GET':
        current_directory = request.GET.get("path")
        pattern = request.GET.get("searchedfor")
        resp = fileObj.search(pattern)
    return JsonResponse({'files': resp['files'],'directories':resp['directories']}, content_type="application/json")