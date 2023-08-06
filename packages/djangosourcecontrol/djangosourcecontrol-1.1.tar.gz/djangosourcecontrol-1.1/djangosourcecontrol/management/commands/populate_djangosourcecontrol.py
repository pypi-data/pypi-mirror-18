from django.core.management.base import BaseCommand
from djangosourcecontrol.djangosourcecontrolmodels import *

from django.utils import timezone
from datetime import datetime, timedelta


def logDjangoSourceControlPopulate(view_func):
    """
    Log DjangoSourceControl Populate prints to the console when called.
    """
    def _wrapped_view_func(*args, **kwargs): 
        try:
            print("DjangoSourceControl:",args[1:],kwargs)  
            return view_func(*args, **kwargs)
        except Exception as ex: 
            print("DjangoSourceControl - fail:", ex)
            return view_func(*args, **kwargs)
    return _wrapped_view_func

class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'our help string comes here'

    @logDjangoSourceControlPopulate    
    def handle(self, *args, **options):
        #self._create_tags()
        print("starting populate_djangosourcecontrol")
        #self.CreateProject("project name", "project desc", True)