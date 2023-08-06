from django.db import models
from django.utils import timezone

from djangosourcecontrol.djangosourcecontrolmodels.Project import AUTH_USER_MODEL
from djangosourcecontrol.djangosourcecontrolmodels.ProjectFile import ProjectFile

class ProjectFileVersion(models.Model):
    """
    ProjectFileVersion is used to store an individual save of python file.
    """
    created_date = models.DateTimeField('date created', default = timezone.now)
    text = models.TextField()

    projectfile = models.ForeignKey(ProjectFile,related_name='projectfileversions')

    def __str__(self):
        return self.text

    @classmethod
    def create(self,projectfile, text = "", created_date=timezone.now()):
        return ProjectFileVersion(projectfile=projectfile, text = text, created_date=created_date)

    class Meta:
        app_label = "djangosourcecontrol"