from django.conf.urls import url

from search.views import *

urlpatterns = [
    url(r'^$',
        Home.as_view(), name='home'),
    url(r'^division/(?P<division>.*)/$',
        DivisionView.as_view(), name='division'),
    url(r'^discipline/(?P<discipline>.*)/$',
        DisciplineDetail.as_view(), name='discipline'),
    url(r'^subject/(?P<subject>.*)/$',
        SubjectDetail.as_view(), name='subject'),
    url(r'^course/(?P<pk>.*)/$',
        CourseDetail.as_view(), name='course'),
]
