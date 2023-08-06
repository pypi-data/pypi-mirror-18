"""
Django Source Control Repository is the data access control to our sqllite3 database.

It contains definitions of a single class the DSCRepository which is a colleciton of methods
for easily fetching project and their files by id.

It also contains methods for reading and writing project files and zips to disk.

And lastly it contains methods for permissions for the views.
"""
#Django Source Control Specific Stuff
from djangosourcecontrol.serializers import ProjectSerializer, ProjectFileSerializer, ProjectFileVersionSerializer
from djangosourcecontrol.djangosourcecontrolmodels.Project import Project
from djangosourcecontrol.djangosourcecontrolmodels.ProjectFile import ProjectFile
from djangosourcecontrol.djangosourcecontrolmodels.ProjectFileVersion import ProjectFileVersion

#django specific usage stuff
from django.contrib.auth.models import Permission, Group
from django.shortcuts import render
from django.views import generic
from django.utils import timezone
from django.http import Http404, HttpResponse

#rest framework stuff
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

#used for deleting and creating directorys and determining path
import os
import shutil

#used for compling and running the project
from subprocess import Popen, PIPE, check_output

import zipfile

class DSCRepository():
    """
    DSC Repository is contains the main buisness logic of the DSC project.

    Collection of functions to provide db access for reading and writing DSC Projects, files and versions.

    Additionally includes methods for writing projects to disk, compiling, running, and saving to a zip file.

    Finally it also includes methods for checking authentication of Projects, files, and versions.
    """
    def CreateOrGetProjectByName(self, name = "name", desc = "desc", public = True, user = None):
        """
        Create or Get Project by name
        """
        try:
            project = Project.objects.get(project_name=name)
        except :
            project = Project.create(user,name,desc,"",public)
            project.save()
        return project
    
    def CreateOrGetFileForProject(self, project, name = "name", desc = "desc",startup=False, public = True, user = None):
        """
        Create or or Get ProjectFile by project and name
        """
        try:
            projectfile = ProjectFile.objects.get(project=project, projectfile_name=name)
        except :
            projectfile = ProjectFile.create(project,name,desc,startup, public)
            projectfile.save()
        return projectfile

    def CreateFileVersionForFile(self, projectfile, text = "text", created_date=timezone.now()):
        """
        Create Project file version for given projectfile
        """
        projectfileversion = ProjectFileVersion.create(projectfile,text,created_date )
        projectfileversion.save()
        return projectfileversion

    def __getpaths__(self,username, projectId):
        """
        Get paths provides the location of the workspace folder and user and project folders.
        """
        workspacePath = os.path.join(os.getcwd(), "Workspace")
        if username == None or username == "":
            username = 'anon'

        userPath = os.path.join(workspacePath, "{}".format(username))
        projectPath = os.path.join(userPath, "{}".format(projectId))
        return (workspacePath, userPath, projectPath)

    def zipdir(self, path, ziph):
        """
        zip dir is a utility function for adding files to an existing zip file out of 
        a provided directory path
        http://stackoverflow.com/questions/1855095/how-to-create-a-zip-archive-of-a-directory
        """
        # ziph is zipfile handle
        for root, dirs, files in os.walk(path):
            oldcwd = os.getcwd()
            os.chdir(root)
            for file in files:
                print(root, dirs, file)
                ziph.write(file)
            os.chdir(oldcwd)

    def create_project_zip(self,user, projectId):
        """
        Creates a zip file in the workspace/username folder named {projectId}_{projectname}.zip
        """
        project = self.get_project(projectId)
        try:
            self.remove_project_from_disk(user.username,projectId)
        except:
            pass
        (workspacePath, userPath, projectPath) = self.__getpaths__(user.username,projectId)
        self.write_project_to_disk(user,projectId)
        zipPath = '{}/{}_{}.zip'.format(userPath, projectId, project.project_name)
        zipf = zipfile.ZipFile(zipPath, 'w', zipfile.ZIP_DEFLATED)
        self.zipdir(projectPath, zipf)
        zipf.close()

    def write_project_to_disk(self,user, projectId):
        """
        Write project to disk creates a new folder for each user and project id

        Write project to disk always uses the lastest version of each file

        returns the projectPath
        """
        (workspacePath, userPath, projectPath) = self.__getpaths__(user.username,projectId)

        if(not os.path.isdir(workspacePath)):
            os.mkdir(workspacePath)

        if(not os.path.isdir(userPath)):
            os.mkdir(userPath)

        if(not os.path.isdir(projectPath)):
            os.mkdir(projectPath)

        projectFiles = self.get_projectfilesForProject(projectId)
        try:
            for projectfile in projectFiles:
                if self.is_authorized_file(user, projectfile):
                    #http://stackoverflow.com/questions/6159900/correct-way-to-write-line-to-file-in-python
                    filepath = os.path.join(projectPath,projectfile.projectfile_name)
                    versions = self.get_projectFileVersionsForProjectFile(projectfile)
                    if versions.exists():
                        #already sorted, date then id
                        version = versions[len(versions)-1]
                        with open(filepath, 'w+') as the_file:
                            the_file.write(version.text)
                            the_file.close()
        except Exception as ex:
            print("EXCEPTION:",ex)
            #raise ex

        return projectPath

    def remove_project_from_disk(self,username, projectId):
        """
        Removes the projectid folder and all contents
        """
        (workspacePath, userPath, projectPath) = self.__getpaths__(username,projectId)
        #Now we are finished, clean up the project by removing everything in the folder
        #https://docs.python.org/2/library/shutil.html#shutil.rmtree
        shutil.rmtree(projectPath)
        #http://stackoverflow.com/questions/21505313/is-there-a-foolproof-way-to-give-the-system-enough-time-to-delete-a-folder-befor
        while os.path.exists(projectPath): # check if it exists
            print("in delay")
            pass

    def is_authorized_project_add(self, user):
        """
        Checks for the can_add_project permission or is superuser
        """
        authorized = False
        response = ""
        if user.is_authenticated():
            permissions = list(Permission.objects.filter(user=user).all())
            groups = Group.objects.filter(user=user).all()
            for g in groups:
                permissions = list(set(permissions + list(g.permissions.all())))
            permissions = [p.natural_key() for p in permissions]
            if ('can_add_project','djangosourcecontrol','project') in permissions:
                authorized = True            

        if user.is_superuser:
            authorized = True    

        return authorized

    def is_authorized_project_run(self, user):
        """
        Checks for the can_run_project permission,
        or if is superuser
        """
        authorized = False
        response = ""
        if user.is_authenticated():
            permissions = list(Permission.objects.filter(user=user).all())
            groups = Group.objects.filter(user=user).all()

            for g in groups:
                permissions = list(set(permissions + list(g.permissions.all())))
            permissions = [p.natural_key() for p in permissions]
            if ('can_run_project','djangosourcecontrol','project') in permissions:
                authorized = True            

        if user.is_superuser:
            authorized = True    

        return authorized

    def is_authorized_project(self, user, project, allowPublic=True):
        """
        Authorized if you are the project owner,
        or if it is public, 
        or if you are a superuser
        """
        authorized = False
        if(user == project.user):
            authorized = True
        if(project.public and allowPublic):
            authorized = True
        if(user.is_superuser):
            authorized = True
        return authorized

    def is_authorized_file(self, user, projectfile, allowPublic=True):
        """
        Authorized if you are the project owner, 
        or if it is public and the project is public,
        or if you are a superuser
        """
        authorized = False
        if(user == projectfile.project.user):
            authorized = True
        if(projectfile.public and projectfile.project.public and allowPublic):
            authorized = True
        if(user.is_superuser):
            authorized = True
        return authorized

    def is_authorized_version(self, user, projectfileversion):
        """ 
        Authorized if you are the project owner, 
        or if its file is public and the project is public,
        or if you are a superuser       
        """
        authorized = False
        if(user == projectfileversion.projectfile.project.user):
            authorized = True
        if(projectfileversion.projectfile.public and projectfileversion.projectfile.project.public):
            authorized = True
        if(user.is_superuser):
            authorized = True
        return authorized

    def get_projectfileversion(self, pk):
        """
        Returns the project file version for a given id
        """
        try:
            return ProjectFileVersion.objects.get(id=pk)
        except ProjectFileVersion.DoesNotExist:
            raise Http404

    def get_projectfile(self, pk):
        """
        Returns the project file for a given id
        """
        try:
            return ProjectFile.objects.get(id=pk)
        except ProjectFile.DoesNotExist:
            raise Http404

    def get_projectfilesForProject(self, projectId):
        """
        Returns the project files for a given projectId ordered by date then id
        """
        project = self.get_project(projectId)
        #get the startup project file
        return ProjectFile.objects.filter(project = project).order_by('projectfile_name', 'id')

    def get_projectFileVersionsForProjectFile(self, projectfile):
        """
        Returns the project file versions for a given projectFile (not id)  ordered by date then id
        """
        return ProjectFileVersion.objects.all().order_by('created_date', 'id').filter(projectfile = projectfile).all()

    def get_projectStartup(self,projectId):
        """
        Returns the file for a given projectid that is marked as startup = True
        """
        project = self.get_project(projectId)
        return ProjectFile.objects.get(project = project, startup = True)

    def get_project(self, pk):
        """
        Returns the project by id
        """
        try:
            return Project.objects.get(id=pk)
        except Project.DoesNotExist:
            raise Http404