"""
The admin file defines what can be viewed and modified in the default django admin pages.
"""

from django.contrib import admin

from djangosourcecontrol.djangosourcecontrolmodels.Project import Project
from djangosourcecontrol.djangosourcecontrolmodels.ProjectFile import ProjectFile
from djangosourcecontrol.djangosourcecontrolmodels.ProjectFileVersion import ProjectFileVersion
      
class ProjectFileVersionInline(admin.TabularInline):
    """
    ProjectFileVersionInline is used for the inline adding of ProjectFileVersions
    """
    model = ProjectFileVersion
    ordering = ('created_date','id')
    extra = 0

class ProjectFileInline(admin.TabularInline):
    """
    ProjectFileInline is used for the inline adding of ProjectFiles
    """
    model = ProjectFile
    inlines = [ProjectFileVersionInline]
    extra = 0
    ordering = ('projectfile_name','id')

class ProjectAdmin(admin.ModelAdmin):
    """
    ProjectAdmin controls what fields are displayed on the Admin page for Project
    """
    fieldsets = [(None,{'fields': ['user','project_name', 'project_description','public','created_date','commandline']})]
    list_display = ('project_name','user','project_description','public','created_date')
    inlines = [ProjectFileInline]
    list_filter = ['public']

class ProjectFileAdmin(admin.ModelAdmin):
    """
    ProjectFileAdmin controls what fields are displayed on the Admin page for ProjectFile
    """
    fieldsets = [(None,{'fields': ['project','projectfile_name', 'projectfile_description','startup','public','created_date']})]
    list_display = ('projectfile_name','project', 'projectfile_description','startup','public','created_date')
    inlines = [ProjectFileVersionInline]
    list_filter = ['startup','public']

class ProjectFileVersionAdmin(admin.ModelAdmin):
    """
    ProjectFileVersionAdmin controls what fields are displayed on the Admin page for ProjectFileVersion
    """
    fieldsets = [(None,{'fields': ['projectfile','created_date','text']})]
    list_display = ('created_date','projectfile', 'text',)
    list_filter = ['created_date']

#The classes we define above need to be registered for the admin site to know about them
admin.site.register(Project,ProjectAdmin)
admin.site.register(ProjectFile,ProjectFileAdmin)
admin.site.register(ProjectFileVersion,ProjectFileVersionAdmin)