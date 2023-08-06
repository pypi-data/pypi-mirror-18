from django.db import models
from django.utils import timezone

from djangosourcecontrol.djangosourcecontrolmodels.Project import Project

class ProjectFile(models.Model):
    """
    ProjectFile is used to store the contents of a single python file.
    
    The project file consists of a collection of versions and some general information.
    """
    projectfile_name = models.CharField(max_length=32)
    projectfile_description = models.CharField(max_length=256)
    startup = models.BooleanField(default=False)
    created_date = models.DateTimeField('date created', default = timezone.now)
    public = models.BooleanField(default=True)
    project = models.ForeignKey(Project,related_name='projectfiles', blank=True, null=True)
    
    def __str__(self):
        return self.projectfile_name

    @classmethod
    def create(self,project, projectfile_name="",projectfile_description="", startup=False, public=True,created_date=timezone.now()):
        return ProjectFile(project=project, projectfile_name=projectfile_name,projectfile_description=projectfile_description,startup =startup , public=public, created_date=created_date)

    class Meta:
        app_label = "djangosourcecontrol"