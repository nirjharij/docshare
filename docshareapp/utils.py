import os
import re

path = os.environ['HOME']
from django.conf import settings


def cd_base(func):
    def wrap(*args, **kwargs):
        x = func(*args, **kwargs)
        os.chdir(settings.BASE_DIR)
        return x
    return wrap

class FileManagement:
    def __init__(self,path):
        self.path = path
        self.project_path = self.path + "/zenatix"

        if not os.path.isdir(self.project_path):
            os.chdir(self.path)
            os.mkdir('zenatix')

    #Directory Operations
    @cd_base
    def create_directory(self,current_directory,directory_name):
        self.cd(current_directory)
        if not os.path.isdir(directory_name):
            os.mkdir(directory_name)
            print ("Directory %s created Successfully" % directory_name)
        else:
            print ("Directory Already Exists")

    @cd_base
    def delete_directory(self,current_directory,directory_name):
        self.cd(current_directory)
        if os.path.isdir(directory_name):
            os.removedirs(directory_name)
            print ("Successfully Deleted %s" % directory_name)
        else:
            print ("No such directory present")
    
    def cd(self,directory_path):
        if os.path.isdir(directory_path):
            os.chdir(directory_path)
        else:
            print ("No such directory present")

    @cd_base
    def ls(self,current_directory):
        self.cd(current_directory)
        return os.listdir(current_directory)

    @cd_base
    def rename_directory(self,current_directory,old_directory,new_directory):
        self.cd(current_directory)
        if os.path.isdir(old_directory):
            os.rename(old_directory,new_directory)

    #File Operations
    def upload_file(self,f):
        if not os.path.exists(self.project_path + "/uploads/"):
            self.create_directory(self.project_path,'uploads')
        filename = f.name.split('/')[-1]

        destination = open(self.project_path + "/uploads/" + filename, 'wb+')

        for chunk in f:
            destination.write(chunk)

        destination.close()

    @cd_base
    def delete_file(self,current_directory,filename):
        self.cd(current_directory)
        if os.path.isfile(filename):
            os.remove(filename)
            print ("File %s removed Successfully" % filename)
        else:
            print ("File does not exist")

    @cd_base
    def search(self,current_directory,searched):
        self.cd(current_directory)
        list_of_files = self.ls(current_directory)
        pattern = searched
        files_found = [ f for f in list_of_files if re.search(pattern,f) ]
        print (files_found)

    def download_file(self,current_directory,filename):
        download_file_path = current_directory+filename
        if os.path.exists(download_file_path):
            return download_file_path

    @cd_base
    def rename_file(self,current_directory,old_filename,new_filename):
        self.cd(current_directory)
        if os.path.isfile(old_filename):
            os.rename(old_filename,new_filename)    

    # @cd_base
    def is_directory(self,current_directory,name):
    	# self.cd(current_directory)
    	print ('os.getcwd()', current_directory, name)
    	if os.path.isdir(os.path.join(current_directory, name)):
    		return True
    	else:
    		return False

# current_directory = path + "/" + "zenatix/" 
fileObj = FileManagement(path)

# with open('/Users/binay/Downloads/Task.txt', 'rb') as testfile:
#     fileObj.upload_file(testfile)

# fileObj.create_directory(current_directory,'test1')
# fileObj.delete_directory(current_directory,'test1')
# fileObj.rename_directory(current_directory,'test1','test123')
# fileObj.ls(current_directory)
# fileObj.delete_file(current_directory,'Task.txt')
# fileObj.search(current_directory,'.txt')
# fileObj.rename_file(current_directory,'nj.jpg','d.txt')
