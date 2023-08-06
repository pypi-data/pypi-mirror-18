"""
urls define how to access the different pages and the api endpoints.  
the <pk> stands for primary key and is used as an argument being passed to the views.
"""
from django.conf.urls import url
from . import views as djangosourcecontrolviews

app_name = 'djangosourcecontrol'

urlpatterns = [
    url(r'^$', djangosourcecontrolviews.Index, name='index'),
    url(r'^(?P<pk>[0-9]+)/$', djangosourcecontrolviews.ProjectDetailView.as_view(), name='detail'),
    url(r'^api/project/$', djangosourcecontrolviews.ProjectAdd.as_view()),
    url(r'^api/project/(?P<pk>[0-9]+)/$', djangosourcecontrolviews.ProjectDetails.as_view()),
    
    url(r'^api/projectfile/$', djangosourcecontrolviews.ProjectFileAdd.as_view()),
    url(r'^api/projectfile/(?P<pk>[0-9]+)/$', djangosourcecontrolviews.ProjectFileDetails.as_view()),
    
    url(r'^api/projectfileversion/$', djangosourcecontrolviews.ProjectFileVersionAdd.as_view()),
    url(r'^api/projectfileversion/(?P<pk>[0-9]+)/$', djangosourcecontrolviews.ProjectFileVersionDetails.as_view()),

    url(r'^api/runproject/(?P<pk>[0-9]+)/$', djangosourcecontrolviews.RunProject.as_view()),
    url(r'^api/compileprojectfile/(?P<pk>[0-9]+)/$', djangosourcecontrolviews.CompileProjectFile.as_view()),
    url(r'^api/downloadproject/(?P<pk>[0-9]+)/$', djangosourcecontrolviews.DownloadProject.as_view()),
]