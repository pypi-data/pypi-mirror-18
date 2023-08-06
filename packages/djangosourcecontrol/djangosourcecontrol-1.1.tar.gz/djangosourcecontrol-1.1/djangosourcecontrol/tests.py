"""
run in a terminal "python manage.py test" to run django tests defined in tests.py
"""
#Django Imports
from django.test import TestCase
from django.utils import timezone

#Django user permission model
from django.conf import settings
from django.contrib.auth.models import User, AnonymousUser, Permission

#python imports
import datetime
import os
from builtins import FileNotFoundError

#dsc imports
from djangosourcecontrol.repository.DjangoSourceControlRepository import DSCRepository
from djangosourcecontrol.djangosourcecontrolmodels.Project import Project
from djangosourcecontrol.djangosourcecontrolmodels.ProjectFile import ProjectFile
from djangosourcecontrol.djangosourcecontrolmodels.ProjectFileVersion import ProjectFileVersion

#for testing django rest framework
from django.test.client import encode_multipart, RequestFactory
from rest_framework.test import force_authenticate
import djangosourcecontrol.views as DSCViews
from rest_framework import status


class DSCRepoTests(TestCase):
    """
    Brief: DSCRepoTests contains one or more tests for every function on a DSCRepository
    
    Note About django.test.TestCase:  On every run a new clean instance of the sqllite database will be created
    so we must populate it fresh for every test. So I setup a test in the self.setUp() function that every test will use.

    Note: DSCRepoTest inherits from django.test.TestCase, 
        which inherits from django.test.TransactionTestCase 
        which inherits from django.test.SimpleTestCase 
        which inherits from unittest.TestCase
        
        So all basic django test cases are derived from the standard python unittest. Cool! 
    """
    
    def __PopulateTestProject__(self,user,project):
        """
        Takes a user and a project
        A public file and a private file are made on the project

        On each file there are 4 versions created with the most recent version by being #3
        """
        #With a some files public and private, startup and not
        
        self.testProjectFileCount = 0
        self.testProjectFileVersionCount = 0

        file = self.Repo.CreateOrGetFileForProject(project,self.testProjectFileName, "-", True, True)
        self.testProjectFileCount += 1
        

        #Create the versions with four timestamps, one early, one late, and two that are the same.
        #This lets us test all combinations of ordering since versions are sorted by datetime not name
        self.Repo.CreateFileVersionForFile(file, "public file ver 1", self.testTimezoneNow )
        self.testProjectFileVersionCount += 1
        self.Repo.CreateFileVersionForFile(file, "public file ver 2", self.testTimezoneNow )
        self.testProjectFileVersionCount += 1
        self.Repo.CreateFileVersionForFile(file, "public file ver 3", self.testTimezoneNow + datetime.timedelta(minutes =1))
        self.testProjectFileVersionCount += 1
        self.Repo.CreateFileVersionForFile(file, "public file ver 4", self.testTimezoneNow + datetime.timedelta(minutes =-1))
        self.testProjectFileVersionCount += 1

        privatefile = self.Repo.CreateOrGetFileForProject(project,self.testProjectFileNamePrivate, "-", False, False)
        self.testProjectFileCount += 1

        self.Repo.CreateFileVersionForFile(privatefile, "private file ver 1", self.testTimezoneNow )
        self.Repo.CreateFileVersionForFile(privatefile, "private file ver 2", self.testTimezoneNow )
        self.Repo.CreateFileVersionForFile(privatefile, "private file ver 3", self.testTimezoneNow + datetime.timedelta(minutes =1))
        self.Repo.CreateFileVersionForFile(privatefile, "private file ver 4", self.testTimezoneNow + datetime.timedelta(minutes =-1))

    def setUp(self):
        """
        Setup is run before each test which configures an empty test db with a project, some files, with a few versions

        Brief:
            Creates 4 users:
            admin
            daniel
            jamie
            anonamousUser

            It then assigns the add project permission to daniel and jamie
            and the run project permission to jamie

            It then creates two projects
            A public one for daniel, and a private one for jamie
            On each project a public and a private file are made.

            On each file both public and private there are 4 versions. The most recent version by timestamp should be #3
        """
        self.Repo = DSCRepository()

        self.workspacename = "Workspace"
        
        #get the permissions
        self.add_permission = Permission.objects.get(codename='can_add_project')
        self.run_permission = Permission.objects.get(codename='can_run_project')
        
        #setup some users with and without those permissions
        self.admin = User.objects.create_superuser('admin', 'admin@dcs.com', 'jello')
        self.daniel = User.objects.create_user(username='daniel',email='daniel@dcs.com',password='jello')
        self.daniel.user_permissions.add(self.add_permission)
        self.daniel.save()

        self.jamie = User.objects.create_user(username='jamie',email='jamie@dcs.com',password='jello')
        self.jamie.user_permissions.add(self.add_permission)
        self.jamie.user_permissions.add(self.run_permission)
        self.jamie.save()

        self.anonymousUser = AnonymousUser()
        
        #what are we naming our files and projects?
        self.testProjectName = "TestProject"
        self.testProjectFileName = "TestFile.py"
        self.testProjectFileNamePrivate = "TestFile_Private.py"
        self.testProjectNamePrivate ="{}_private".format(self.testProjectName)
        self.testTimezoneNow = timezone.now()

        self.testProjectCount = 0
        #Create a project
        self.danielproject = self.Repo.CreateOrGetProjectByName(self.testProjectName, "-", True,self.daniel)
        self.__PopulateTestProject__(self.daniel, self.danielproject)
        self.testProjectCount += 1
        

        self.jamieproject = self.Repo.CreateOrGetProjectByName(self.testProjectNamePrivate, "-", False,self.jamie)
        self.__PopulateTestProject__(self.jamie, self.jamieproject)
        self.testProjectCount += 1
            
        return super().setUp()

    ## Tests for
    #def CreateOrGetProjectByName(self, name = "name", desc = "desc", public = True, user = None):
    #    """
    #    Create or Get Project by name
    #    """
    def test_create_CreateOrGetProjectByName(self):
        """
        test_create_CreateOrGetProjectByName() attempts to add a project then verifys its existance
        """
        before = Project.objects.all().count()
        self.Repo.CreateOrGetProjectByName("{}_{}".format(self.testProjectName, before), "-", True)
        after = Project.objects.all().count()

        self.assertIs(before == after -1, True, "Before was not 1 smaller than after")

    def test_get_CreateOrGetProjectByName(self):
        """
        test_get_CreateOrGetProjectByName() attempts to get a project then verifys its existance
        """
        project = self.Repo.CreateOrGetProjectByName(self.testProjectName)
        self.assertIs(project.project_name == self.testProjectName, True, "Project '{}' could not be found".format(self.testProjectName))

    ## Tests for
    #def get_project(self, pk):
    #    """
    #    Returns the project by id
    #    """
    def test_get_project(self):
        """
        test_get_project() attempts to get a project by id then verifys its existance
        """
        project_by_name = self.Repo.CreateOrGetProjectByName(self.testProjectName)
        project_by_id = self.Repo.get_project(project_by_name.id)
        self.assertIsNotNone(project_by_name,"Project by name returned as none")
        self.assertIsNotNone(project_by_id,"Project by id returned as none")
        self.assertIs(project_by_id == project_by_name, True, "Project by id and project by name were not equal")
        
    ## Tests for
    #def get_projectfilesForProject(self, projectId):
    #    """
    #    Returns the project files for a given projectId ordered by date then id
    #    """
    def test_get_projectfilesForProject(self):
        """
        test_get_projectfilesForProject() attempts to the project files for the test project
        """
        project = self.Repo.CreateOrGetProjectByName(self.testProjectName)
        projectFiles = self.Repo.get_projectfilesForProject(project.id)
        #todo: check if they are in the 
        count = self.testProjectFileCount
        self.assertIs(len(projectFiles) == count, True, "Did not find exactly {} files for the test project".format(count))
            
    ## Tests for
    #def CreateOrGetFileForProject(self, project, name = "name", desc = "desc",startup=False, public = True, user = None):
    #    """
    #    Create or or Get ProjectFile by project and name
    #    """
    def test_create_CreateOrGetFileForProject(self):
        """
        test_create_CreateOrGetFileForProject() attempts to add a projectfile to a project
        """
        project = self.Repo.CreateOrGetProjectByName(self.testProjectName)
        projectFiles = self.Repo.get_projectfilesForProject(project.id)
        beforecount = len(projectFiles)
        file = self.Repo.CreateOrGetFileForProject(project,"{}_{}".format(self.testProjectFileName,beforecount ), "-", True)
        projectFilesAfter = self.Repo.get_projectfilesForProject(project.id)
        aftercount = len(projectFilesAfter)

        self.assertIs(file != None , True, "File does not exist")
        self.assertIs(beforecount == aftercount -1, True, "Before was not 1 smaller than after")

    def test_get_CreateOrGetFileForProject(self):
        """
        test_get_CreateOrGetFileForProject() attempts to get a projectfile from a project
        """
        project = self.Repo.CreateOrGetProjectByName(self.testProjectName)
        file = self.Repo.CreateOrGetFileForProject(project,self.testProjectFileName)

        self.assertIs(file.projectfile_name == self.testProjectFileName, True, "File name does not match")
    
    ## Tests for
    #def get_projectfile(self, pk):
    #    """
    #    Returns the project file for a given id
    #    """
    def test_get_projectfile(self):
        """
        test_get_projectfile() attempts to get a projectfile by id then verifys its existance
        """
        project = self.Repo.CreateOrGetProjectByName(self.testProjectName)
        file_by_name = self.Repo.CreateOrGetFileForProject(project,self.testProjectFileName)
        file_by_id = self.Repo.get_projectfile(file_by_name.id)

        self.assertIsNotNone(file_by_name,"file by name returned as none")
        self.assertIsNotNone(file_by_id,"file by id returned as none")
        self.assertIs(file_by_name == file_by_id, True, "file by id and file by name were not equal")
        
    ## Tests for
    
    #def get_projectFileVersionsForProjectFile(self, projectfile):
    #    """
    #    Returns the project file versions for a given projectFile (not id)  ordered by date then id
    #    """
    def test_get_projectFileVersionsForProjectFile(self):
        """
        get_projectFileVersionsForProjectFile() attempts to return the versions for the test project file
        """
        project = self.Repo.CreateOrGetProjectByName(self.testProjectName)
        file = self.Repo.CreateOrGetFileForProject(project,self.testProjectFileName)
        versions = self.Repo.get_projectFileVersionsForProjectFile(file)

        count = self.testProjectFileVersionCount

        #check if sorted correctly
        #http://stackoverflow.com/questions/3755136/pythonic-way-to-check-if-a-list-is-sorted-or-not
        sortedDate = all(versions[i].created_date <= versions[i+1].created_date for i in range(len(versions)-1))
        sortedId = all(versions[i].created_date < versions[i+1].created_date 
                       or (versions[i].created_date == versions[i+1].created_date and versions[i].id < versions[i+1].id)
                       for i in range(len(versions)-1))

        self.assertIsNotNone(versions,"versions returned as none")
        self.assertIs(sortedDate,True,"Not sorted by date")
        self.assertIs(sortedId,True,"Not sorted by date then id")
        self.assertIs(len(versions) == count, True,"expected {} versions but instead got {}".format(count, len(versions)))
    
    ## Tests for    
    #def CreateFileVersionForFile(self, projectfile, text = "text", created_date=timezone.now()):
    #    """
    #    Create Project file version for given projectfile
    #    """
    def test_CreateFileVersionForFile(self):
        """
        CreateFileVersionForFile() attempts to create a fileversion for a file object, and we verify its existance and properties
        """
        project = self.Repo.CreateOrGetProjectByName(self.testProjectName)
        file = self.Repo.CreateOrGetFileForProject(project,self.testProjectFileName)
        
        #Get the count before we add the new version
        beforeversions = self.Repo.get_projectFileVersionsForProjectFile(file)
        beforeCount = len(beforeversions)

        newVersionText = "New Version!"
        projectfileversion = self.Repo.CreateFileVersionForFile(file,newVersionText )

        #Get the count after the version
        afterversions = self.Repo.get_projectFileVersionsForProjectFile(file)
        afterCount = len(afterversions)

        self.assertIs(projectfileversion.text == newVersionText, True,"The text should have read ({}) but instead read ({})".format(newVersionText, projectfileversion.text))
        self.assertIs(beforeCount == (afterCount -1), True,"The before count ({}) should have been the 1 less than the afterCount({})".format(beforeCount, afterCount))

    ## Tests for
    #def get_projectfileversion(self, pk):
    #    """
    #    Returns the project file version for a given id
    #    """
    def test_get_projectfileversion(self):
        """
        get_projectfileversion() attempts to retrieve a projectfileversion by id, and we verify its existance and properties
        """
        project = self.Repo.CreateOrGetProjectByName(self.testProjectName)
        file = self.Repo.CreateOrGetFileForProject(project,self.testProjectFileName)
        versions = self.Repo.get_projectFileVersionsForProjectFile(file)
        for version in versions:
            getVersion = self.Repo.get_projectfileversion(version.id)
            self.assertIs(version.id == getVersion.id,True,"The {} should have read ({}) but instead read ({})".format("id",version.id, getVersion.id))
            self.assertIs(version.text == getVersion.text,True,"The {} should have read ({}) but instead read ({})".format("text",version.text, getVersion.text))
            self.assertIs(version.created_date == getVersion.created_date,True,"The {} should have read ({}) but instead read ({})".format("created_date",version.created_date, getVersion.created_date))

    ## Tests for
    #def get_projectStartup(self,projectId):
    #    """
    #    Returns the file for a given projectid that is marked as startup = True
    #    """
    def test_get_projectStartup(self):
        """
        get_projectStartup() attempts to retrieve a the startup project file,
        we also verify that only one file on the project is marked as a startup. 
        """
        project = self.Repo.CreateOrGetProjectByName(self.testProjectName)
        files = self.Repo.get_projectfilesForProject(project.id)
        startup = None
        startupCount = 0
        for file in files:
            if(file.startup):
                startupCount += 1
                startup = file

        self.assertIs(startupCount == 0 or startupCount == 1, True, "The {} should have read ({}) but instead read ({})".format("startupCount","0 or 1", startupCount))
        
        getStartup = self.Repo.get_projectStartup(project.id)

        self.assertIs(startup.id == getStartup.id, True, "The {} should have read ({}) but instead read ({})".format("id",startup.id, getStartup.id)) 
        self.assertIs(startup.projectfile_name == getStartup.projectfile_name, True, "The {} should have read ({}) but instead read ({})".format("name",startup.projectfile_name, getStartup.projectfile_name)) 
        self.assertIs(startup.startup, True, "The {} should have read ({}) but instead read ({})".format("startup",True, startup.startup) )


    ## Tests for
    #def is_authorized_project_add(self, user):
    #    """
    #    Checks for the can_add_project permission or is superuser
    #    """
    def test_is_authorized_project_add(self):
        """
        test_is_authorized_project_add() - all registered users have been given the add permission
        """
        self.assertIs(self.Repo.is_authorized_project_add(self.admin),True,"Admin cannot add project? That is way wrong.")
        self.assertIs(self.Repo.is_authorized_project_add(self.daniel),True,"Daniel cannot add project? He is supposed to be a basic user.")
        self.assertIs(self.Repo.is_authorized_project_add(self.jamie),True,"Jamie cannot add project? She is supposed to be a trusted user.")
        self.assertIs(self.Repo.is_authorized_project_add(self.anonymousUser),False,"Anonamous users shouldn't be able to add projects.")

    ### Tests for
    #def is_authorized_project(self, user, project, allowPublic=True):
    #    """
    #    Authorized if you are the project owner,
    #    or if it is public, 
    #    or if you are a superuser
    #    """
    def test_is_authorized_project(self):
        """
        test_is_authorized_project() - each user is only authorized on public projects and their own project
        """

        self.assertIs(self.Repo.is_authorized_project(self.admin, self.danielproject),True,"Daniel's project is public everyone should be able to get it")
        self.assertIs(self.Repo.is_authorized_project(self.daniel, self.danielproject ),True,"Daniel's project is public everyone should be able to get it")
        self.assertIs(self.Repo.is_authorized_project(self.jamie, self.danielproject),True,"Daniel's project is public everyone should be able to get it")
        self.assertIs(self.Repo.is_authorized_project(self.anonymousUser, self.danielproject),True,"Daniel's project is public everyone should be able to get it")

        self.assertIs(self.Repo.is_authorized_project(self.admin, self.jamieproject),True,"Jamie's project is private but this is the admin.")
        self.assertIs(self.Repo.is_authorized_project(self.daniel, self.jamieproject ),False,"Only Jamie and superusers should have access to this project")
        self.assertIs(self.Repo.is_authorized_project(self.jamie, self.jamieproject),True,"Only Jamie and superusers should have access to this project")
        self.assertIs(self.Repo.is_authorized_project(self.anonymousUser, self.jamieproject),False,"Only Jamie and superusers should have access to this project")

    ## Tests for
    #def is_authorized_project_run(self, user):
    #    """
    #    Checks for the can_run_project permission,
    #    or if is superuser
    #    """
    def test_is_authorized_project_run(self):
        """
        test_is_authorized_project_run() - only jamie has been given the has_run permission
        """
        self.assertIs(self.Repo.is_authorized_project_run(self.admin),True,"Admin and Jamie are the only ones who should be able to run projects")
        self.assertIs(self.Repo.is_authorized_project_run(self.daniel),False,"Admin and Jamie are the only ones who should be able to run projects")
        self.assertIs(self.Repo.is_authorized_project_run(self.jamie),True,"Admin and Jamie are the only ones who should be able to run projects")
        self.assertIs(self.Repo.is_authorized_project_run(self.anonymousUser),False,"Admin and Jamie are the only ones who should be able to run projects")

    ## Tests for
    #def is_authorized_file(self, user, projectfile, allowPublic=True):
    #    """
    #    Authorized if you are the project owner, 
    #    or if it is public and the project is public,
    #    or if you are a superuser
    #    """
    def test_is_authorized_file(self):
        """
        test_is_authorized_file() - to be authorized to view a file the project must be 
        public and the file must be public. Or you must be the owner of the project or a superuser
        """
        file = self.Repo.CreateOrGetFileForProject(self.danielproject,self.testProjectFileName)

        self.assertIs(self.Repo.is_authorized_file(self.admin, file ),True,"This file is public everyone should have access")
        self.assertIs(self.Repo.is_authorized_file(self.daniel, file),True,"This file is public everyone should have access")
        self.assertIs(self.Repo.is_authorized_file(self.jamie, file),True,"This file is public everyone should have access")
        self.assertIs(self.Repo.is_authorized_file(self.anonymousUser, file),True,"This file is public everyone should have access")

        privatefile = self.Repo.CreateOrGetFileForProject(self.danielproject,self.testProjectFileNamePrivate)
        self.assertIs(self.Repo.is_authorized_file(self.admin, privatefile ),True,"This file is private only Daniel and superusers should have access")
        self.assertIs(self.Repo.is_authorized_file(self.daniel, privatefile ),True,"This file is private only Daniel and superusers should have access")
        self.assertIs(self.Repo.is_authorized_file(self.jamie, privatefile ),False,"This file is private only Daniel and superusers should have access")
        self.assertIs(self.Repo.is_authorized_file(self.anonymousUser, privatefile ),False,"This file is private only Daniel and superusers should have access")

        file = self.Repo.CreateOrGetFileForProject(self.jamieproject,self.testProjectFileName)

        self.assertIs(self.Repo.is_authorized_file(self.admin, file ),True,"This file is public but the project is private so only Jamie and superusers should have access")
        self.assertIs(self.Repo.is_authorized_file(self.daniel, file),False,"This file is public but the project is private so only Jamie and superusers should have access")
        self.assertIs(self.Repo.is_authorized_file(self.jamie, file),True,"This file is public but the project is private so only Jamie and superusers should have access")
        self.assertIs(self.Repo.is_authorized_file(self.anonymousUser, file),False,"This file is public but the project is private so only Jamie and superusers should have access")

        privatefile = self.Repo.CreateOrGetFileForProject(self.jamieproject,self.testProjectFileNamePrivate)
        self.assertIs(self.Repo.is_authorized_file(self.admin, privatefile ),True,"This file is private only Daniel and superusers should have access")
        self.assertIs(self.Repo.is_authorized_file(self.daniel, privatefile ),False,"This file is private only Daniel and superusers should have access")
        self.assertIs(self.Repo.is_authorized_file(self.jamie, privatefile ),True,"This file is private only Daniel and superusers should have access")
        self.assertIs(self.Repo.is_authorized_file(self.anonymousUser, privatefile ),False,"This file is private only Daniel and superusers should have access")

    ## Tests for
    #def is_authorized_version(self, request, projectfileversion):
    #    """ 
    #    Authorized if you are the project owner, 
    #    or if its file is public and the project is public,
    #    or if you are a superuser       
    #    """
    def test_is_authorized_version(self):
        """
        test_is_authorized_version() - to be authorized to view a file and thus the version 
        the project must be public and the file must be public.
        Or you must be the owner of the project or a superuser
        """
        file = self.Repo.CreateOrGetFileForProject(self.danielproject,self.testProjectFileName)
        versions = self.Repo.get_projectFileVersionsForProjectFile(file)
        version = self.Repo.get_projectfileversion(versions[0].id)
        self.assertIs(self.Repo.is_authorized_version(self.admin, version ),True,"This file is public everyone should have access")
        self.assertIs(self.Repo.is_authorized_version(self.daniel, version ),True,"This file is public everyone should have access")
        self.assertIs(self.Repo.is_authorized_version(self.jamie, version ),True,"This file is public everyone should have access")
        self.assertIs(self.Repo.is_authorized_version(self.anonymousUser, version ),True,"This file is public everyone should have access")

        privatefile = self.Repo.CreateOrGetFileForProject(self.danielproject,self.testProjectFileNamePrivate)
        versions = self.Repo.get_projectFileVersionsForProjectFile(privatefile)
        version = self.Repo.get_projectfileversion(versions[0].id)
        self.assertIs(self.Repo.is_authorized_version(self.admin, version ),True,"This file is private only Daniel and superusers should have access")
        self.assertIs(self.Repo.is_authorized_version(self.daniel, version ),True,"This file is private only Daniel and superusers should have access")
        self.assertIs(self.Repo.is_authorized_version(self.jamie, version ),False,"This file is private only Daniel and superusers should have access")
        self.assertIs(self.Repo.is_authorized_version(self.anonymousUser, version ),False,"This file is private only Daniel and superusers should have access")

        file = self.Repo.CreateOrGetFileForProject(self.jamieproject,self.testProjectFileName)
        versions = self.Repo.get_projectFileVersionsForProjectFile(file)
        version = self.Repo.get_projectfileversion(versions[0].id)
        self.assertIs(self.Repo.is_authorized_version(self.admin, version ),True,"This file is public but the project is private so only Jamie and superusers should have access")
        self.assertIs(self.Repo.is_authorized_version(self.daniel, version ),False,"This file is public but the project is private so only Jamie and superusers should have access")
        self.assertIs(self.Repo.is_authorized_version(self.jamie, version ),True,"This file is public but the project is private so only Jamie and superusers should have access")
        self.assertIs(self.Repo.is_authorized_version(self.anonymousUser, version ),False,"This file is public but the project is private so only Jamie and superusers should have access")
        
        privatefile = self.Repo.CreateOrGetFileForProject(self.jamieproject,self.testProjectFileNamePrivate)
        versions = self.Repo.get_projectFileVersionsForProjectFile(privatefile)
        version = self.Repo.get_projectfileversion(versions[0].id)
        self.assertIs(self.Repo.is_authorized_version(self.admin, version ),True,"This file is private only Daniel and superusers should have access")
        self.assertIs(self.Repo.is_authorized_version(self.daniel, version ),False,"This file is private only Daniel and superusers should have access")
        self.assertIs(self.Repo.is_authorized_version(self.jamie, version ),True,"This file is private only Daniel and superusers should have access")
        self.assertIs(self.Repo.is_authorized_version(self.anonymousUser, version ),False,"This file is private only Daniel and superusers should have access")

    ## Tests for
    #def __getpaths__(self,username, projectId):
    #    """
    #    Get paths provides the location of the workspace folder and user and project folders.
    #    """
    def test_getpaths(self):
        """
        test_getpaths() - Checks that the workspace is under cwd\\workspace
        and that the userspace is at workspace\\username
        and that the projecspace is at userspace\\project.
        """
        (workspace, userspace, projectspace) = self.Repo.__getpaths__(self.daniel, self.danielproject.id)
        cwd = os.getcwd()
        workspace = workspace.split(cwd)[1]
        userspace = userspace.split(cwd)[1]
        projectspace = projectspace.split(cwd)[1]

        self.assertIs("\\{}".format(self.workspacename) == workspace, True, "Workspace name did not match")
        self.assertIs("\\{}\\{}".format(self.workspacename, self.daniel) == userspace, True, "Workspace name did not match")
        self.assertIs("\\{}\\{}\\{}".format(self.workspacename, self.daniel, self.danielproject.id) == projectspace, True, "Workspace name did not match")
        
        (workspace, userspace, projectspace) = self.Repo.__getpaths__(self.jamie, self.jamieproject.id)
        cwd = os.getcwd()
        workspace = workspace.split(cwd)[1]
        userspace = userspace.split(cwd)[1]
        projectspace = projectspace.split(cwd)[1]

        self.assertIs("\\{}".format(self.workspacename) == workspace, True, "Workspace name did not match")
        self.assertIs("\\{}\\{}".format(self.workspacename, self.jamie) == userspace, True, "Workspace name did not match")
        self.assertIs("\\{}\\{}\\{}".format(self.workspacename, self.jamie, self.jamieproject.id) == projectspace, True, "Workspace name did not match")
        
    ## Tests for
    #def write_project_to_disk(self,user, projectId):
    #    """
    #    Write project to disk creates a new folder for each user and project id

    #    returns the projectPath
    #    """
    def test_write_project_to_disk(self):
        """
        test_write_project_to_disk() - Checks each of the public and private files existance when writing with the various users
        """
        #check with their own project
        self.Repo.write_project_to_disk(self.daniel, self.danielproject.id)
        (workspace, userspace, projectspace) = self.Repo.__getpaths__(self.daniel, self.danielproject.id)
        f = open("{}\\{}".format(projectspace,self.testProjectFileName), 'r')
        self.assertIs(f.readline() == "public file ver 3", True, "Contents didn't match")
        f.close()

        p = open("{}\\{}".format(projectspace,self.testProjectFileNamePrivate), 'r')
        self.assertIs(p.readline() == "private file ver 3", True, "Contents didn't match")
        p.close()

        #check with their own project
        self.Repo.write_project_to_disk(self.jamie, self.jamieproject.id)
        (workspace, userspace, projectspace) = self.Repo.__getpaths__(self.jamie, self.jamieproject.id)
        f = open("{}\\{}".format(projectspace,self.testProjectFileName), 'r')
        self.assertIs(f.readline() == "public file ver 3", True, "Contents didn't match")
        f.close()

        p = open("{}\\{}".format(projectspace,self.testProjectFileNamePrivate), 'r')
        self.assertIs(p.readline() == "private file ver 3", True, "Contents didn't match")
        p.close()

        #check with the others project
        self.Repo.write_project_to_disk(self.daniel, self.jamieproject.id)
        (workspace, userspace, projectspace) = self.Repo.__getpaths__(self.daniel, self.jamieproject.id)
        try:
            f = open("{}\\{}".format(projectspace,self.testProjectFileName), 'r')
            f.close()
            self.assertIs(False,True, "The file was not supposed to exist")
        except FileNotFoundError as ex:
            self.assertIs(ex != None, True, "File was not supposed to exist")

        try:
            p = open("{}\\{}".format(projectspace,self.testProjectFileNamePrivate), 'r')
            p.close()
            self.assertIs(False,True, "The file was not supposed to exist")
        except FileNotFoundError as ex:
            self.assertIs(ex != None, True, "File was not supposed to exist")

        #check with the others project
        self.Repo.write_project_to_disk(self.jamie, self.danielproject.id)
        (workspace, userspace, projectspace) = self.Repo.__getpaths__(self.jamie, self.danielproject.id)
        f = open("{}\\{}".format(projectspace,self.testProjectFileName), 'r')
        self.assertIs(f.readline() == "public file ver 3", True, "Contents didn't match")
        f.close()

        try:
            p = open("{}\\{}".format(projectspace,self.testProjectFileNamePrivate), 'r')
            p.close()
            self.assertIs(False,True, "The file was not supposed to exist")
        except FileNotFoundError as ex:
            self.assertIs(ex != None, True, "File was not supposed to exist")

        
        self.Repo.remove_project_from_disk(self.daniel,self.danielproject.id)
        self.Repo.remove_project_from_disk(self.daniel,self.jamieproject.id)
        self.Repo.remove_project_from_disk(self.jamie,self.danielproject.id)
        self.Repo.remove_project_from_disk(self.jamie,self.jamieproject.id)

    ## Tests for
    #def remove_project_from_disk(self,username, projectId):
    #    """
    #    Removes the projectid folder and all contents
    #    """
    def test_remove_project_from_disk(self):
        """
        test_remove_project_from_disk() - Checks each of the project folder existance when removing with the various users and projects
        """
        self.Repo.write_project_to_disk(self.daniel, self.danielproject.id)
        self.Repo.write_project_to_disk(self.daniel, self.jamieproject.id)
        self.Repo.write_project_to_disk(self.jamie, self.danielproject.id)
        self.Repo.write_project_to_disk(self.jamie, self.jamieproject.id)

        (workspace, userspace, projectspace) = self.Repo.__getpaths__(self.daniel, self.danielproject.id)
        self.assertIs(os.path.isdir(projectspace), True, "Path should exist")
        (workspace, userspace, projectspace) = self.Repo.__getpaths__(self.daniel, self.jamieproject.id)
        self.assertIs(os.path.isdir(projectspace), True, "Path should exist")
        (workspace, userspace, projectspace) = self.Repo.__getpaths__(self.jamie, self.danielproject.id)
        self.assertIs(os.path.isdir(projectspace), True, "Path should exist")
        (workspace, userspace, projectspace) = self.Repo.__getpaths__(self.jamie, self.jamieproject.id)
        self.assertIs(os.path.isdir(projectspace), True, "Path should exist")

        self.Repo.remove_project_from_disk(self.daniel,self.danielproject.id)
        self.Repo.remove_project_from_disk(self.daniel,self.jamieproject.id)
        self.Repo.remove_project_from_disk(self.jamie,self.danielproject.id)
        self.Repo.remove_project_from_disk(self.jamie,self.jamieproject.id)

        (workspace, userspace, projectspace) = self.Repo.__getpaths__(self.daniel, self.danielproject.id)
        self.assertIs(os.path.isdir(projectspace), False, "Path should not exist")
        (workspace, userspace, projectspace) = self.Repo.__getpaths__(self.daniel, self.jamieproject.id)
        self.assertIs(os.path.isdir(projectspace), False, "Path should not exist")
        (workspace, userspace, projectspace) = self.Repo.__getpaths__(self.jamie, self.danielproject.id)
        self.assertIs(os.path.isdir(projectspace), False, "Path should not exist")
        (workspace, userspace, projectspace) = self.Repo.__getpaths__(self.jamie, self.jamieproject.id)
        self.assertIs(os.path.isdir(projectspace), False, "Path should not exist")

class DSCRestApiTests(TestCase):
    """
    Brief: DSCRestApiTests contains one or more tests for rest api end point for
    getting, creating, and updating dsc projects, files, and versions
    
    Note About django.test.TestCase:  On every run a new clean instance of the sqllite database will be created
    so we must populate it fresh for every test. So I setup a test in the self.setUp() function that every test will use.

    Note: DSCRepoTest inherits from django.test.TestCase, 
        which inherits from django.test.TransactionTestCase 
        which inherits from django.test.SimpleTestCase 
        which inherits from unittest.TestCase
        
        So all basic django test cases are derived from the standard python unittest. Cool! 

    http://stackoverflow.com/questions/27641703/how-to-test-an-api-endpoint-with-django-rest-framework-using-django-oauth-toolki
    http://www.django-rest-framework.org/api-guide/testing/#forcing-authentication
    """
    def __createTestReqeust__(self,data,url,user):
        """
        Utility method which returns a setup request object with security tokens for the given user
        """
        factory = RequestFactory()
        content = encode_multipart('BoUnDaRyStRiNg', data)
        content_type = 'multipart/form-data; boundary=BoUnDaRyStRiNg'
        request = factory.post(url, content, content_type=content_type)
        force_authenticate(request, user=user)
        return request
    
    def __PopulateTestProject__(self,user,project):
        """
        Takes a user and a project
        A public file and a private file are made on the project

        On each file there are 4 versions created with the most recent version by being #3
        """
        #With a some files public and private, startup and not
        
        self.testProjectFileCount = 0
        self.testProjectFileVersionCount = 0

        file = self.Repo.CreateOrGetFileForProject(project,self.testProjectFileName, "-", True, True)
        self.testProjectFileCount += 1
        
        #Create the versions with four timestamps, one early, one late, and two that are the same.
        #This lets us test all combinations of ordering since versions are sorted by datetime not name
        self.Repo.CreateFileVersionForFile(file, "public file ver 1", self.testTimezoneNow )
        self.testProjectFileVersionCount += 1
        self.Repo.CreateFileVersionForFile(file, "public file ver 2", self.testTimezoneNow )
        self.testProjectFileVersionCount += 1
        self.Repo.CreateFileVersionForFile(file, "public file ver 3", self.testTimezoneNow + datetime.timedelta(minutes =1))
        self.testProjectFileVersionCount += 1
        self.Repo.CreateFileVersionForFile(file, "public file ver 4", self.testTimezoneNow + datetime.timedelta(minutes =-1))
        self.testProjectFileVersionCount += 1

        privatefile = self.Repo.CreateOrGetFileForProject(project,self.testProjectFileNamePrivate, "-", False, False)
        self.testProjectFileCount += 1

        self.Repo.CreateFileVersionForFile(privatefile, "private file ver 1", self.testTimezoneNow )
        self.Repo.CreateFileVersionForFile(privatefile, "private file ver 2", self.testTimezoneNow )
        self.Repo.CreateFileVersionForFile(privatefile, "private file ver 3", self.testTimezoneNow + datetime.timedelta(minutes =1))
        self.Repo.CreateFileVersionForFile(privatefile, "private file ver 4", self.testTimezoneNow + datetime.timedelta(minutes =-1))

    def setUp(self):
        """
        Setup is run before each test which configures an empty test db with a project, some files, with a few versions

        Brief:
            Creates 4 users:
            admin
            daniel
            jamie
            anonamousUser

            It then assigns the add project permission to daniel and jamie
            and the run project permission to jamie

            It then creates two projects
            A public one for daniel, and a private one for jamie
            On each project a public and a private file are made.

            On each file both public and private there are 4 versions. The most recent version by timestamp should be #3
        """
        self.Repo = DSCRepository()

        self.workspacename = "Workspace"
        
        #get the permissions
        self.add_permission = Permission.objects.get(codename='can_add_project')
        self.run_permission = Permission.objects.get(codename='can_run_project')
        
        #setup some users with and without those permissions
        self.admin = User.objects.create_superuser('admin', 'admin@dcs.com', 'jello')
        self.daniel = User.objects.create_user(username='daniel',email='daniel@dcs.com',password='jello')
        self.daniel.user_permissions.add(self.add_permission)
        self.daniel.save()

        self.jamie = User.objects.create_user(username='jamie',email='jamie@dcs.com',password='jello')
        self.jamie.user_permissions.add(self.add_permission)
        self.jamie.user_permissions.add(self.run_permission)
        self.jamie.save()

        self.anonymousUser = AnonymousUser()
        
        #what are we naming our files and projects?
        self.testProjectName = "TestProject"
        self.testProjectFileName = "TestFile.py"
        self.testProjectFileNamePrivate = "TestFile_Private.py"
        self.testProjectNamePrivate ="{}_private".format(self.testProjectName)
        self.testTimezoneNow = timezone.now()

        self.testProjectCount = 0
        #Create a project
        self.danielproject = self.Repo.CreateOrGetProjectByName(self.testProjectName, "-", True,self.daniel)
        self.__PopulateTestProject__(self.daniel, self.danielproject)
        self.testProjectCount += 1
        

        self.jamieproject = self.Repo.CreateOrGetProjectByName(self.testProjectNamePrivate, "-", False,self.jamie)
        self.__PopulateTestProject__(self.jamie, self.jamieproject)
        self.testProjectCount += 1

        #so now the repo has setup some users, projects, files, and versions. 
            
        return super().setUp()
    
    ## Tests for
    # url(r'^$', djangosourcecontrolviews.Index, name='index'),
    def test_IndexGetRequest(self):
        """
        test_IndexGetRequest() attempts to issue a get request to the dsc index from all 4 users.
        """
        def __testGetIndex__(user):
            """
            __testGetIndex__ requests the index page and ensures it succeeds for the given user
            """
            factory = RequestFactory()
            request = factory.get('/')
            request.user = user
            view = DSCViews.Index
            response = view(request)

            self.assertIs(response.status_code == status.HTTP_200_OK, True, "All users should be able to reach /")

        __testGetIndex__(self.daniel)
        __testGetIndex__(self.jamie)
        __testGetIndex__(self.admin)
        __testGetIndex__(self.anonymousUser)

    ## Tests for
    # url(r'^(?P<pk>[0-9]+)/$', djangosourcecontrolviews.DetailView.as_view(), name='detail'),
    def test_ProjectDetailsGetRequest(self):
        """
        test_ProjectDetailsGetRequest() attempts to issue a get request to the dsc project details page from all 4 users for both projects.
        """
        
        def __testGetProjectDetailsView__(user,project):
            """
            __testGetProjectDetailsView__ requests the index page and ensures it succeeds for all users. 
            Anyone can learn of a projects name and description by visiting the page. But any contents are hidden.
            """
            factory = RequestFactory()
        
            request = factory.get('/{}'.format(project.id))
            request.user = user

            view = DSCViews.ProjectDetailView.as_view()
            response = view(request,pk = project.id)

            self.assertIs(response.status_code == status.HTTP_200_OK, True, "All users should be able to reach /")

        __testGetProjectDetailsView__(self.daniel, self.danielproject)
        __testGetProjectDetailsView__(self.jamie, self.danielproject)
        __testGetProjectDetailsView__(self.admin, self.danielproject)
        __testGetProjectDetailsView__(self.anonymousUser, self.danielproject)

        __testGetProjectDetailsView__(self.daniel, self.jamieproject)
        __testGetProjectDetailsView__(self.jamie, self.jamieproject)
        __testGetProjectDetailsView__(self.admin, self.jamieproject)
        __testGetProjectDetailsView__(self.anonymousUser, self.jamieproject)

    ## Tests for
    # url(r'^api/project/(?P<pk>[0-9]+)/$', djangosourcecontrolviews.ProjectDetails.as_view()),
    def test_ProjectGetRequest(self):
        """
        test_ProjectGetRequest() attempts to a get a projects details via the exposed web api
        """
        def __testGetProject__(user,project,shouldPass = True):
            """
            __testGetProject__ is a helper function for forming sending and checking reqeusts for getting projects
            """
            view = DSCViews.ProjectDetails.as_view()
            factory = RequestFactory()

            request = factory.get('/api/project/{}'.format(project.id))
            request.user = user

            response = view(request, pk = project.id)
            if shouldPass:
                self.assertIs(response.status_code == status.HTTP_200_OK, True, "Only authorized users should be able to get project details")
            else: 
                self.assertIs(response.status_code == status.HTTP_401_UNAUTHORIZED, True, "Only authorized users should be able to get project details")


        danielfiles = self.Repo.get_projectfilesForProject(self.danielproject.id)
        #danielproject is public
        __testGetProject__(self.daniel,self.danielproject)
        __testGetProject__(self.admin,self.danielproject)
        __testGetProject__(self.jamie,self.danielproject)
        __testGetProject__(self.anonymousUser,self.danielproject)
        
        jamiefiles = self.Repo.get_projectfilesForProject(self.jamieproject.id)
        #jamieproject is private
        __testGetProject__(self.daniel,self.jamieproject,False)
        __testGetProject__(self.admin,self.jamieproject)
        __testGetProject__(self.jamie,self.jamieproject)
        __testGetProject__(self.anonymousUser,self.jamieproject,False)
        
    ## Tests for
    # url(r'^api/projectfile/(?P<pk>[0-9]+)/$', djangosourcecontrolviews.ProjectFileDetails.as_view()),
    def test_ProjectFileGetRequest(self):
        """
        test_ProjectFileGetRequest() attempts to a get a project files details via the exposed web api
        """
        def __testGetProjectFile__(user,project):
            """
            __testGetProjectFile__ is a helper function for forming sending and checking reqeusts for getting project files
            """
            files = self.Repo.get_projectfilesForProject(project.id)

            for file in files:
                view = DSCViews.ProjectFileDetails.as_view()
                factory = RequestFactory()

                request = factory.get('/api/projectfile/{}'.format(file.id))
                request.user = user

                response = view(request, pk = file.id)
                if self.Repo.is_authorized_file(user, file):
                    self.assertIs(response.status_code == status.HTTP_200_OK, True, "Only authorized users should be able to get project file details")
                else: 
                    self.assertIs(response.status_code == status.HTTP_401_UNAUTHORIZED, True, "Only authorized users should be able to get project file details")


        danielfiles = self.Repo.get_projectfilesForProject(self.danielproject.id)
        #danielproject is public
        __testGetProjectFile__(self.daniel,self.danielproject)
        __testGetProjectFile__(self.admin,self.danielproject)
        __testGetProjectFile__(self.jamie,self.danielproject)
        __testGetProjectFile__(self.anonymousUser,self.danielproject)
        
        jamiefiles = self.Repo.get_projectfilesForProject(self.jamieproject.id)
        #jamieproject is private
        __testGetProjectFile__(self.daniel,self.jamieproject)
        __testGetProjectFile__(self.admin,self.jamieproject)
        __testGetProjectFile__(self.jamie,self.jamieproject)
        __testGetProjectFile__(self.anonymousUser,self.jamieproject)
        
    ## Tests for
    # url(r'^api/projectfileversion/(?P<pk>[0-9]+)/$', djangosourcecontrolviews.ProjectFileVersionDetails.as_view()),
    def test_ProjectFileVersionGetRequest(self):
        """
        test_ProjectFileVersionGetRequest() attempts to a get a project files details via the exposed web api
        """
        def __testGetProjectFileVersion__(user,project):
            """
            __testGetProjectFileVersion__ is a helper function for forming sending and checking reqeusts for getting project file versions
            """
            files = self.Repo.get_projectfilesForProject(project.id)

            for file in files:
                view = DSCViews.ProjectFileVersionDetails.as_view()
                factory = RequestFactory()

                versions = self.Repo.get_projectFileVersionsForProjectFile(file)
                for version in versions:

                    request = factory.get('/api/projectfileversion/{}'.format(version.id))
                    request.user = user

                    response = view(request, pk = version.id)
                    if self.Repo.is_authorized_version(user, version):
                        self.assertIs(response.status_code == status.HTTP_200_OK, True, "Only authorized users should be able to get project file version details")
                    else: 
                        self.assertIs(response.status_code == status.HTTP_401_UNAUTHORIZED, True, "Only authorized users should be able to get project file version details")


        #danielproject is public
        __testGetProjectFileVersion__(self.daniel,self.danielproject)
        __testGetProjectFileVersion__(self.admin,self.danielproject)
        __testGetProjectFileVersion__(self.jamie,self.danielproject)
        __testGetProjectFileVersion__(self.anonymousUser,self.danielproject)
        
        #jamieproject is private
        __testGetProjectFileVersion__(self.daniel,self.jamieproject)
        __testGetProjectFileVersion__(self.admin,self.jamieproject)
        __testGetProjectFileVersion__(self.jamie,self.jamieproject)
        __testGetProjectFileVersion__(self.anonymousUser,self.jamieproject)


    
    ## Tests for
    # url(r'^api/project/(?P<pk>[0-9]+)/$', djangosourcecontrolviews.ProjectDetails.as_view()),
    def test_ProjectPostRequest(self):
        """
        test_ProjectPostRequest() attempts to Post a projects details via the exposed web api to update it
        """
        def __testPostProject__(user,project,shouldPass = True):
            """
            __testPostProject__ is a helper function for forming sending and checking reqeusts for updating projects
            """
            view = DSCViews.ProjectDetails.as_view()
            factory = RequestFactory()
            data = {
                'project_name': "{}_{}".format(project.project_name,user.username),
                'project_description': "{}_{}".format("new desc",user.username),
                "created_date": "{}".format(timezone.now()),
                'commandline': "none",
                'public': project.public
            }
            request = self.__createTestReqeust__(data,'/api/project/{}'.format(project.id),user)
            response = view(request, pk = project.id)
            if shouldPass:
                self.assertIs(response.status_code == status.HTTP_200_OK, True, "Only authorized users should be able to update project details")
            else: 
                self.assertIs(response.status_code == status.HTTP_401_UNAUTHORIZED, True, "Only authorized users should be able to update project details")


        danielfiles = self.Repo.get_projectfilesForProject(self.danielproject.id)
        #danielproject is public
        __testPostProject__(self.daniel,self.danielproject)
        __testPostProject__(self.admin,self.danielproject)
        __testPostProject__(self.jamie,self.danielproject, False)
        __testPostProject__(self.anonymousUser,self.danielproject, False)
        
        jamiefiles = self.Repo.get_projectfilesForProject(self.jamieproject.id)
        #jamieproject is private
        __testPostProject__(self.daniel,self.jamieproject,False)
        __testPostProject__(self.admin,self.jamieproject)
        __testPostProject__(self.jamie,self.jamieproject)
        __testPostProject__(self.anonymousUser,self.jamieproject,False)


    ## Tests for
    # url(r'^api/projectfile/(?P<pk>[0-9]+)/$', djangosourcecontrolviews.ProjectFileDetails.as_view()),
    def test_ProjectFilePostRequest(self):
        """
        test_ProjectFilePostRequest() attempts to a post a project files details via the exposed web api
        """
        def __testPostProjectFile__(user,project):
            """
            __testGetProjectFile__ is a helper function for forming sending and checking reqeusts for getting project files
            """
            files = self.Repo.get_projectfilesForProject(project.id)

            for file in files:
                newfilename = '{}_{}'.format(file.projectfile_name, user.username)
                newfiledescription = '{}_{}'.format(file.projectfile_description, user.username)
                view = DSCViews.ProjectFileDetails.as_view()
                factory = RequestFactory()
                data = {
                    'project': project.id,
                    'projectfile_name': newfilename,
                    'projectfile_description': newfiledescription,
                    'public': file.public
                }
            
                request = self.__createTestReqeust__(data,'/api/projectfile/{}'.format(file.id),user)
                response = view(request, pk = file.id)

                if self.Repo.is_authorized_file(user, file):
                    self.assertIs(response.status_code == status.HTTP_200_OK, True, "Only authorized users should be able to update project file details")
                else: 
                    self.assertIs(response.status_code == status.HTTP_401_UNAUTHORIZED, True, "Only authorized users should be able to update project file details")

        danielfiles = self.Repo.get_projectfilesForProject(self.danielproject.id)
        #danielproject is public
        __testPostProjectFile__(self.daniel,self.danielproject)
        __testPostProjectFile__(self.admin,self.danielproject)
        __testPostProjectFile__(self.jamie,self.danielproject)
        __testPostProjectFile__(self.anonymousUser,self.danielproject)
        
        jamiefiles = self.Repo.get_projectfilesForProject(self.jamieproject.id)
        #jamieproject is private
        __testPostProjectFile__(self.daniel,self.jamieproject)
        __testPostProjectFile__(self.admin,self.jamieproject)
        __testPostProjectFile__(self.jamie,self.jamieproject)
        __testPostProjectFile__(self.anonymousUser,self.jamieproject)
        
    ## Tests for
    # url(r'^api/project/$', djangosourcecontrolviews.ProjectList.as_view()),
    def test_create_Project(self):
        """
        test_create_Project() attempts to create a project then verifys its existance
        """
        #test daniel with danielproject
        def __testAddProject__(user,public, shouldPass = True):
            """
            Test addProject is a helper function for forming sending and checking reqeusts for adding projects
            """
            projectname = "new {}".format(user.username)
            view = DSCViews.ProjectAdd.as_view()
            data = {
                        'project_name': projectname,
                        'project_description': "new desc",
                        "created_date": "{}".format(timezone.now()),
                        'commandline': "none",
                        'public': public
                    }
            before = len(Project.objects.all())
            request = self.__createTestReqeust__(data,'/api/project/',user)
            response = view(request)

            #Check response code
            if shouldPass:
                self.assertIs(response.status_code == status.HTTP_201_CREATED, True, "Only authorized users should be able to create projects")
            else: 
                self.assertIs(response.status_code == status.HTTP_401_UNAUTHORIZED, True, "Only authorized users should be able to create projects")
            
            #verify only one project was created
            after = len(Project.objects.all())
            if shouldPass:
                self.assertIs(before == after -1, True, "number of projects before post should be 1 less than after post.  Instead it was before ({}) and after ({})".format(before,after))
            else: 
                self.assertIs(before == after, True, "number of projects before post should be equal to after the post.  Instead it was before ({}) and after ({})".format(before,after))

            if shouldPass:
                project = self.Repo.get_project(response.data['id'])
                #verify the response code created a project with the right name
                self.assertIs(project.project_name == projectname, True, "Project name ({}) did not match expected ({})".format(project.project_name, projectname))
                #verify the response code created a project with the right name
                self.assertIs(project.public == public, True, "Project public  ({}) did not match expected ({})".format(project.public , public ))
            else:
                self.assertIs(response.data == None, True, "Response should be none on a fail")

        #add a bunch of public projects
        __testAddProject__(self.daniel,True)
        __testAddProject__(self.admin,True)
        __testAddProject__(self.jamie,True)
        __testAddProject__(self.anonymousUser,True, False)
                           
        #and a bunch of private projects
        __testAddProject__(self.daniel,False)
        __testAddProject__(self.admin,False)
        __testAddProject__(self.jamie,False)
        __testAddProject__(self.anonymousUser,False, False)

    ## Tests for
    # url(r'^api/projectfile/$', djangosourcecontrolviews.ProjectFileList.as_view()),
    def test_create_ProjectFile(self):
        """
        test_create_ProjectFile() attempts to add a project file  then verifys its existance
        """
        #test daniel with danielproject
        def __testAddFile__(user,project,shouldPass = True):
            """
            Test addFile is a helper function for forming sending and checking reqeusts for adding files
            """
            view = DSCViews.ProjectFileAdd.as_view()
            data = {
                        'project': project.id,
                        'projectfile_name': 'new file {}'.format(user.username),
                        'projectfile_description': 'new desc'
                    }
     
            before = len(self.Repo.get_projectfilesForProject(project.id))
            request = self.__createTestReqeust__(data,'/api/projectfile/',user)
            response = view(request)

            if shouldPass:
                self.assertIs(response.status_code == status.HTTP_201_CREATED, True, "Only authorized users should be able to create")
            else: 
                self.assertIs(response.status_code == status.HTTP_401_UNAUTHORIZED, True, "Only authorized users should be able to create")

            after = len(self.Repo.get_projectfilesForProject(project.id))
            if shouldPass:
                self.assertIs(before == after -1, True, "number of files before post should be 1 less than after post.  Instead it was before ({}) and after ({})".format(before,after))
            else: 
                self.assertIs(before == after, True, "number of files before post should be equal to after the post.  Instead it was before ({}) and after ({})".format(before,after))

        __testAddFile__(self.daniel,self.danielproject)
        __testAddFile__(self.admin,self.danielproject)
        __testAddFile__(self.jamie,self.danielproject,False)
        __testAddFile__(self.anonymousUser,self.danielproject,False)

        __testAddFile__(self.daniel,self.jamieproject,False)
        __testAddFile__(self.admin,self.jamieproject)
        __testAddFile__(self.jamie,self.jamieproject)
        __testAddFile__(self.anonymousUser,self.jamieproject,False)

    ## Tests for
    # url(r'^api/projectfile/$', djangosourcecontrolviews.ProjectFileList.as_view()),
    def test_create_ProjectFileVersion(self):
        """
        test_create_ProjectFileVersion() attempts to add a project file version  then verifys its existance
        """
        #test daniel with danielproject
        def __testAddFileVersion__(user,projectfile,shouldPass = True):
            """
            Test addFile is a helper function for forming sending and checking reqeusts for adding files
            """
            view = DSCViews.ProjectFileVersionAdd.as_view()
            data = {
                        'projectfile': projectfile.id,
                        'text': 'new fileversion {}'.format(user.username),
                        "created_date": "{}".format(timezone.now())
                    }
     
            before = len(self.Repo.get_projectFileVersionsForProjectFile(projectfile))
            request = self.__createTestReqeust__(data,'/api/projectfileversion/',user)
            response = view(request)

            if shouldPass:
                self.assertIs(response.status_code == status.HTTP_201_CREATED, True, "Only authorized users should be able to create file versions")
            else: 
                self.assertIs(response.status_code == status.HTTP_401_UNAUTHORIZED, True, "Only authorized users should be able to create file versions")

            after  = len(self.Repo.get_projectFileVersionsForProjectFile(projectfile))
            if shouldPass:
                self.assertIs(before == after -1, True, "number of file versions before post should be 1 less than after post.  Instead it was before ({}) and after ({})".format(before,after))
            else: 
                self.assertIs(before == after, True, "number of file versions before post should be equal to after the post.  Instead it was before ({}) and after ({})".format(before,after))

        danielfiles = self.Repo.get_projectfilesForProject(self.danielproject.id)
        __testAddFileVersion__(self.daniel,danielfiles[0])
        __testAddFileVersion__(self.admin,danielfiles[0])
        __testAddFileVersion__(self.jamie,danielfiles[0],False)
        __testAddFileVersion__(self.anonymousUser,danielfiles[0],False)
        
        jamiefiles = self.Repo.get_projectfilesForProject(self.jamieproject.id)
        __testAddFileVersion__(self.daniel,jamiefiles[0],False)
        __testAddFileVersion__(self.admin,jamiefiles[0])
        __testAddFileVersion__(self.jamie,jamiefiles[0])
        __testAddFileVersion__(self.anonymousUser,jamiefiles[0],False)
