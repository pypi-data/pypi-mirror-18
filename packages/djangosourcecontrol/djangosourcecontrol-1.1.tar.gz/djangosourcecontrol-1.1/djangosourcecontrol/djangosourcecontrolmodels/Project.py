from django.db import models
from django.utils import timezone

from django.conf import settings
AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

class Project(models.Model):
    """
    Project is used to store the contents of a single python project.

    The project consists of a collection of files and some general information.
    """
    project_name = models.CharField(max_length=32)
    project_description = models.CharField(max_length=256)
    created_date = models.DateTimeField('date created', default = timezone.now)
    commandline = models.CharField(max_length=256, default = "")

    public = models.BooleanField(default=True)

    user = models.ForeignKey(AUTH_USER_MODEL, blank=True, null=True)
    
    def __str__(self):
        return self.project_name

    @classmethod
    def create(self,user, project_name="",project_description="", commandline = "", public=True,created_date=timezone.now()):
        return Project(user = user, project_name=project_name,project_description=project_description,commandline=commandline, public =public, created_date=created_date)

    class Meta:
        app_label = "djangosourcecontrol"
        permissions = ( 
            ( "can_run_project", "[DjangoSourceControl]: Can run projects" ),
            ( "can_add_project", "[DjangoSourceControl]: Can add projects" ),
        )