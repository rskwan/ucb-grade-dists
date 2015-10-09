from django.conf.urls import include, url
from tastypie.api import Api
from core.api.resources import *

v1_api = Api(api_name='v1')
v1_api.register(TermResource())
v1_api.register(SubjectResource())
v1_api.register(CourseResource())
v1_api.register(SectionResource())
v1_api.register(GradeResource())

urlpatterns = [
    url(r'^api/', include(v1_api.urls)),
]
