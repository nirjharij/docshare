# -*- coding: utf-8 -*-
import json
import os

from .utils import FileManagement

from django.conf import settings
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from wsgiref.util import FileWrapper

path = settings.WORK_DIR

fileObj = FileManagement(path)

def index(request):
    if request.method == 'GET':
        folder_path = request.GET.get('path', None)

        if not folder_path:
            directory_content = fileObj.ls(os.path.join(path, 'zenatix'))
            bread = [('zenatix', 'zenatix')]
            folder_path = 'zenatix'
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
            directory_content = fileObj.ls(os.path.join(path, folder_path))
            bread = zip(bread, path_bread)

        return render(
            request, 'index.html',
            {'files': directory_content['files'],
             'directories': directory_content['directory'],
             'current_directory': folder_path,
             'bread': bread
             }
        )


def create_folder(request):
    if request.method == 'POST':
        received_json_data = json.loads(request.body)
        file_obj = FileManagement(path)
        directory = received_json_data.get('folder_path')
        current_directory = os.path.join(path, directory)
        folder_name = received_json_data.get('folder_name')
        file_obj.create_directory(current_directory, folder_name)
        return JsonResponse(
            {'data': 'Folder Created Successfully'},
            content_type="application/json")


def list_directory(request):
    data = {}
    folder_name = request.GET.get('folder_name')
    current_directory = request.GET.get('current_directory')
    list_of_files = fileObj.ls(os.path.join(current_directory, folder_name))
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
    ext = {
        'txt': 'text/plain', 'pdf': 'application/pdf',
        'py': 'application/py', 'JPG': 'image/png',
        'PNG': 'image/png', 'mkv': 'video/mkv'}
    wrapper = FileWrapper(open(file_path, 'rb'))
    content_type = ext.get(filename.split('.')[-1]) + "; charset=utf-8"
    response = HttpResponse(wrapper, content_type=content_type)
    attachment_name = 'attachment; filename={}'.format(filename)
    response['Content-Disposition'] = attachment_name
    response['Content-Length'] = os.path.getsize(file_path)
    return response


def upload(request):
    if request.method == 'POST':
        file = request.FILES['file_upload']
        current_directory = request.POST.get("path")
        fileObj.upload_file(file, current_directory)
        current_url = request.POST.get('current_link')
    return HttpResponseRedirect(current_url)


def search(request):
    if request.method == 'GET':
        current_directory = request.GET.get("path")
        pattern = request.GET.get("searchedfor")
        resp = fileObj.search(pattern)
    return render(
        request, 'index.html',
        {'files': resp['files'],
         'directories': resp['directory'],
         'current_directory': current_directory
         }
    )


def autocomplete(request):
    if request.method == 'GET':
        pattern = request.GET.get("searchedfor")
        resp = fileObj.search(pattern)
    return JsonResponse(
        {'files': resp['files'], 'directories': resp['directories']},
        content_type="application/json")


def delete(request):
    if request.method == 'POST':
        current_directory = request.POST.get("path")
        file = request.POST.get('file',None)
        directory = request.POST.get('dir',None)
        if file is not None:
            resp = fileObj.delete_file(current_directory, file)
        elif directory is not None:
            resp = fileObj.delete_directory(current_directory, directory)

        return JsonResponse({'resp': resp}, content_type="application/json")
