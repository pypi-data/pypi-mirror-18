"""
serializers.py defines files for use with the django-rest-framework plugin.
http://www.django-rest-framework.org/api-guide/serializers/
// brief about serializers
# .save() will create a new instance.
serializer = ExampleSerializer(data=data)

# .save() will update the existing 'Example' instance.
serializer = ExampleSerializer(comment, data=data)
"""

from rest_framework import serializers, permissions

from djangosourcecontrol.djangosourcecontrolmodels.Project import Project
from djangosourcecontrol.djangosourcecontrolmodels.ProjectFile import ProjectFile
from djangosourcecontrol.djangosourcecontrolmodels.ProjectFileVersion import ProjectFileVersion

class ProjectFileVersionSerializer(serializers.ModelSerializer):
    """
    ProjectFileVersionSerializer allows easy validation of ProjectFileVersion Submission Data
    """
    class Meta:
        model = ProjectFileVersion
        fields = ('id', 'created_date', 'text','projectfile')
        
class ProjectFileSerializer(serializers.ModelSerializer):
    """
    ProjectFileSerializer allows easy validation of ProjectFile Submission Data
    """
    class Meta:
        projectfileversions = ProjectFileVersionSerializer(many=True, read_only=True)
        model = ProjectFile
        fields = ('id', 'projectfile_name', 'projectfile_description', 'startup','created_date','public','project','projectfileversions')

class ProjectSerializer(serializers.ModelSerializer):
    """
    ProjectSerializer allows easy validation of Project Submission Data
    """
    class Meta:
        projectfiles = ProjectFileSerializer(many=True, read_only=True)
        model = Project
        fields = ('id', 'project_name', 'project_description', 'created_date','commandline','public','user', 'projectfiles')
