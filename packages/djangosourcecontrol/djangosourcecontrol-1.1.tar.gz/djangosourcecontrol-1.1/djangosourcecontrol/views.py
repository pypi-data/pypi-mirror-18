"""
Views define what content each of the url endpoints return.  Both rest api endpoints and regular views.
"""

#Django Source Control Specific Stuff
from .serializers import ProjectSerializer, ProjectFileSerializer, ProjectFileVersionSerializer
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

#used for deleting and creating directorys
from os import path

#used for compling and 
from subprocess import Popen, PIPE, check_output

#file wrapper is used for returing the zip file
from wsgiref.util import FileWrapper

from djangosourcecontrol.repository.DjangoSourceControlRepository import DSCRepository

Repo = DSCRepository()
class DownloadProject(APIView):
    """
    Download Project provides an api for downloading projects as zip files.
    """
    def get(self, request, pk, format=None):
        """
        Public Method
        https://djangosnippets.org/snippets/365/
        https://docs.djangoproject.com/en/dev/ref/request-response/#telling-the-browser-to-treat-the-response-as-a-file-attachment
        Anyone can ask to download a projet.  The zip however will only contain files 
        the user is allowed to view. 
        This means if you reference code that is marked private, anonamous users will not 
        be able to properly compile the project.
        """        
        authorized = True
        if authorized:
            Repo.create_project_zip(request.user, pk)
            project = Repo.get_project(pk)
            (workspacePath, userPath, projectPath) = Repo.__getpaths__(request.user.username,pk)
            filename = "{}_{}".format(project.id,project.project_name)
            projectzip = open('{}/{}.zip'.format(userPath,filename ), 'rb')
            wrapper = FileWrapper(filelike = projectzip)
            response = HttpResponse(wrapper, content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename={}.zip'.format(filename)
            #response['Content-Length'] = projectzip.tell()
            #temp.seek(0)
            projectzip.close()
            Repo.remove_project_from_disk(request.user.username, project.id)
            return response
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

class RunProject(APIView):
    """
    Runs the project given by the project id == pk (primary key)
    """
    def post(self, request, pk, format=None):
        """
        Public Method
        """        
        project = Repo.get_project(pk)

        authorized = False
                         
        #Must be logged in and have the can_run_project permission in order to run projects
        #the project must also be marked as public or the user must be the owner \
        if request.user.is_authenticated() \
            and Repo.is_authorized_project_run(request.user) \
            and (project.public or project.user == request.user):
            authorized = True

        #or be a superuser
        if request.user.is_superuser:
            authorized = True
       
        if authorized:         
            #get the startup project file
            projectfile = Repo.get_projectStartup(pk)
            projectPath = Repo.write_project_to_disk(request.user, project.id)
            filepath = path.join(projectPath, projectfile.projectfile_name)
            try:
                #todo:
                
                #execute the code
                with Popen('python "{}"'.format(filepath), stdout=PIPE, stderr=PIPE) as proc:
                    stdout = proc.stdout.readlines(), 
                    stderr = proc.stderr.readlines()
            except Exception as ex:
                text = "{}".format(ex)

            Repo.remove_project_from_disk(request.user.username, project.id)
            data = {'id': project.id, 'stdout': stdout, 'stderr': stderr}
            return Response(data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

class CompileProjectFile(APIView):
    """
    Compiles the project given by the project id == pk (primary key)
    """
    def post(self, request, pk, format=None):
        """
        Public Method for Compiling a project file. Anyone can compile issue a compile request.
        However you must be authorized to view the file or a 401 will be returned instead. 
        """        
        projectfile = Repo.get_projectfile(pk)
        project = Repo.get_project(projectfile.project.id)
         
        authorized = False
                         
        #Must be logged in and the project and projectfile must be marked as public or the user must be the owner of the project
        if ((project.public and projectfile.public) or project.user == request.user):
        #request.user.is_authenticated() and \
            authorized = True

        #or be a superuser
        if request.user.is_superuser:
            authorized = True
       
        if authorized:         
            #get the most recent version
            projectPath = Repo.write_project_to_disk(request.user, project.id)
            filepath = path.join(projectPath, projectfile.projectfile_name)

            try:
                #execute the code
                with Popen('python -m py_compile "{}"'.format(filepath), stdout=PIPE, stderr=PIPE) as proc:
                    #text = "OUTPUT:<br/>{} ERR:<br/>{}".format(proc.stdout.readlines(), proc.stderr.readlines()) # Alternatively proc.stdout.read(1024)
                    stdout = proc.stdout.readlines(), 
                    stderr = proc.stderr.readlines()
                #os.chdir(oldcwd)
            except Exception as ex:
                stdout = "see error"
                stderr = "{}".format(ex)

            #now compile
            Repo.remove_project_from_disk(request.user.username, project.id)
            data = {'id': project.id, 'stdout': stdout, 'stderr': stderr}
            return Response(data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

class ProjectAdd(APIView):
    """
    Public Method for creating new projects.
    you must have the can_add_project permission in order to add a new project.
    """
    def post(self, request, format=None):
        serializer = ProjectSerializer(data=request.data)

        if serializer.is_valid():
            authorized = Repo.is_authorized_project_add(request.user) 

            if authorized:
                serializer.validated_data['user'] = request.user
                serializer.validated_data['created_date'] = timezone.now()
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProjectDetails(APIView):
    """
    Retrieve, or update a project instance.
    """
    def get(self, request, pk, format=None):
        """
        Public Method for getting a project. 
        """
        project = Repo.get_project(pk)
        if(Repo.is_authorized_project(request.user, project, True)):
            serializer = ProjectSerializer(project)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request, pk, format=None):
        """
        Public Method for updating a project. 
        """
        project = Repo.get_project(pk)
        #must have the post permission
        if(Repo.is_authorized_project(request.user, project, False)):
            project.project_name = request.data.get('project_name',project.project_name)
            project.project_description = request.data.get('project_description',project.project_description)
            project.commandline = request.data.get('commandline',project.commandline)
            pub = request.data.get('public', project.public)
            isPublic = pub == True or pub == 'true'
            project.public = isPublic
          
            project.save()
            return Response(status = status.HTTP_200_OK)
        else:
            return Response(status = status.HTTP_401_UNAUTHORIZED)

class ProjectFileAdd(APIView):
    """
    Public Method for creating new projectfiles.
    Does not allow an anonamous user to add a file
    """
    def post(self, request, format=None):
        """
        Public Method for creating a project file. 
        """
        serializer = ProjectFileSerializer(data=request.data)

        if serializer.is_valid():
            project = Repo.get_project(serializer.validated_data['project'].id)
            serializer.validated_data['created_date'] = timezone.now()
            authorized = Repo.is_authorized_project(request.user,project,False)

            if authorized:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProjectFileDetails(APIView):
    """
    Retrieve, or update a projectfile instance.
    """
    def get(self, request, pk, format=None):
        """
        Public Method for creating a project files. 
        """
        projectfile = Repo.get_projectfile(pk)
        
        if(Repo.is_authorized_file(request.user, projectfile)):
            serializer = ProjectFileSerializer(projectfile)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request, pk, format=None):
        """
        Public Method for updating a project file
        """
        #lookup the existing
        projectfile = Repo.get_projectfile(pk)
        #check if authorized
        if(Repo.is_authorized_file(request.user, projectfile, False)):
            #request.data.get returns either the new value if it exists, or the origional value if it doesnt
            projectfile.projectfile_name = request.data.get('projectfile_name',projectfile.projectfile_name)
            projectfile.projectfile_description = request.data.get('projectfile_description',projectfile.projectfile_description)
            
            startup = request.data.get('startup',projectfile.startup)
            
            isStartup = (startup == True or startup == 'true')
            #Only one startup file can exist on a project. If we are setting one, 
            #we must remove all of the existing claims to startup.
            if(isStartup):
                project = Repo.get_project(projectfile.project.id) 
                ps = ProjectSerializer(project)
                for file in [Repo.get_projectfile(id) for id in ps['projectfiles'].value]:
                    file.startup = False
                    file.save()
            projectfile.startup = isStartup
            pub = request.data.get('public', projectfile.public)
            isPublic = pub == True or pub == 'true'
            projectfile.public = isPublic
          
            projectfile.save()
            return Response(status = status.HTTP_200_OK)
        else:
            return Response(status = status.HTTP_401_UNAUTHORIZED)

class ProjectFileVersionAdd(APIView):
    """
    Public Method for creating a new projectfileversion.
    """
    def post(self, request, format=None):
        """
        Public Method for creating new projectfileversions
        """
        serializer = ProjectFileVersionSerializer(data=request.data)
        
        if serializer.is_valid():
            projectfile = Repo.get_projectfile(serializer.validated_data['projectfile'].id)
            serializer.validated_data['created_date'] = timezone.now()
            authorized = Repo.is_authorized_file(request.user,projectfile,False)

            if authorized:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProjectFileVersionDetails(APIView):
    """
    Retrieve a projectfileversion instance. No update is allowed
    """
    def get(self, request, pk, format=None):
        """
        Public Method for retreiving project file versions
        """
        projectfileversion = Repo.get_projectfileversion(pk)
        if(Repo.is_authorized_version(request.user, projectfileversion)):
            serializer = ProjectFileVersionSerializer(projectfileversion)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

def Index(request):
    """
    Public Method for listing all of the django source control projects the user can see
    """
    template_name = 'djangosourcecontrol/index.html'

    #get all the public projects
    projectspublic = Project.objects.filter(public = True).all()
    #and all the projects the user created
    if request.user.is_authenticated:
        projectsuser = Project.objects.filter(user = request.user).all()
    else:
        projectsuser = []

    #or if the user is a superuser get all the projects
    if request.user.is_superuser:
        projectsuser = Project.objects.all()

    #determine if we should show add project button
    can_add_project = Repo.is_authorized_project_add(request.user)
 
    context = {
        #return as set to make it distinct
        'projects' :sorted(set(list(projectspublic) + list(projectsuser)), key=lambda x: x.project_name, reverse = True), 
        'can_add_project': can_add_project
    }

    return render(request, template_name, context)

class ProjectDetailView(generic.DetailView):
    """
    Public Method for displaying and editing a Django Source Control Project.
    It utilizes the django generic's for displaying details about an object. 
    """
    model = Project

    def get_context_data(self, **kwargs):
        """
        get_context_data is used to store additional information on the data returned to the template.

        'can_run_project' is used to determine if the run button should be shown.
        """
        # Call the base implementation first to get a context
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['can_run_project'] = Repo.is_authorized_project_run(self.request.user)
        return context
