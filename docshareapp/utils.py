import os
import shutil
import re
from django.conf import settings
from os import walk

path = settings.WORK_DIR
media_path = settings.MEDIA_ROOT

def cd_base(func):
    def wrap(*args, **kwargs):
        x = func(*args, **kwargs)
        os.chdir(settings.BASE_DIR)
        return x
    return wrap


class Files:
	def __init__(self,name,path):
		self.filename = name
		self.filepath = path


class Directory:
	def __init__(self,name,path):
		self.dirname = name
		self.dirpath = path


class FileManagement:
    def __init__(self, path):
        self.path = path
        self.project_path = self.path + "/zenatix"

        if not os.path.isdir(self.project_path):
            os.chdir(self.path)
            os.mkdir('zenatix')

    # Directory Operations
    @cd_base
    def create_directory(self, current_directory, directory_name):
        self.cd(current_directory)
        if not os.path.isdir(directory_name):
            os.mkdir(directory_name)
            print ("Directory %s created Successfully" % directory_name)
        else:
            print ("Directory Already Exists")

    @cd_base
    def delete_directory(self, current_directory, directory_name):
        self.cd(os.path.join(self.path,current_directory))
        if os.path.isdir(directory_name):
            shutil.rmtree(directory_name)
            print ("Successfully Deleted %s" % directory_name)
            return True
        else:
            print ("No such directory present")
            return False

    def cd(self, directory_path):
        if os.path.isdir(directory_path):
            os.chdir(directory_path)
        else:
            print ("No such directory present")

    @cd_base
    def ls(self, current_directory):
        directory_content = {}
        self.cd(current_directory)
        content_list = os.listdir(current_directory)
        directory_content['files'] = [
            content for content in content_list if not self.is_directory(
                os.path.join(current_directory, content))]
        directory_content['directory'] = [
            content for content in content_list if self.is_directory(
                os.path.join(current_directory, content))]
        return directory_content

    @cd_base
    def rename_directory(self, current_directory, old_directory, new_directory):
        self.cd(current_directory)
        if os.path.isdir(old_directory):
            os.rename(old_directory, new_directory)

    # File Operations
    def upload_file(self, f, destination_dir=None):
        if destination_dir:
            dest_dir = os.path.join(path, destination_dir)
        else:
            if not os.path.exists(self.project_path + "/uploads/"):
                self.create_directory(self.project_path, 'uploads')
            dest_dir = os.path.join(self.project_path, 'uploads')

        filename = f.name.split('/')[-1]

        destination = open(os.path.join(dest_dir, filename), 'wb+')

        for chunk in f:
            destination.write(chunk)

        destination.close()

    @cd_base
    def delete_file(self, current_directory, filename):
        self.cd(os.path.join(self.path,current_directory))
        if os.path.isfile(filename):
            os.remove(filename)
            print ("File %s removed Successfully" % filename)
            return True
        else:
            print ("File does not exist")
            return False

    @cd_base
    def search(self, searched):
        data_dict = {
            'directories': {'path': [], 'directory': []},
            'files': {'path': [], 'file': []}}
        homedir = os.path.join(path, 'zenatix')
        files, dirs = 0, 0
        for (dirpath, dirnames, filenames) in walk(homedir):
            for f in filenames:
                if files < 5 and re.search(searched, f, re.IGNORECASE):
                    files += 1
                    data_dict['files']['file'].append(f)
                    data_dict['files']['path'].append(dirpath.split('zenatix')[1])
            for d in dirnames:
                if dirs < 5 and re.search(searched, d, re.IGNORECASE):
                    dirs += 1
                    data_dict['directories']['directory'].append(d)
                    data_dict['directories']['path'].append(dirpath.split('zenatix')[1])

        print(data_dict)
        return data_dict

    def download_file(self, file_path, filename):
        full_path = os.path.join(path, file_path)
        rf = open(full_path, 'rb')
        destination_file = os.path.join(media_path + filename)
        with open(destination_file, 'wb') as f:
            for chunk in rf:
                if chunk:
                    f.write(chunk)
        # download_file_path = current_directory+filename
        # if os.path.exists(download_file_path):
        return destination_file

    @cd_base
    def rename_file(self, current_directory, old_filename, new_filename):
        self.cd(current_directory)
        if os.path.isfile(old_filename):
            os.rename(old_filename, new_filename)

    def is_directory(self, path):
        if os.path.isdir(path):
            return True
        else:
            return False
