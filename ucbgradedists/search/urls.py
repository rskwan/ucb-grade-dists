from django.conf.urls import url

from search.views import *

urlpatterns = [
    url(r'^divisionsets/$',
        DivisionSetListView.as_view(), name='divisionset-list'),
    url(r'^divisionsets/(?P<division_set_pk>[0-9]+)/$',
        SubjectStatsListRedirectView.as_view()),
    url(r'^divisionsets/(?P<division_set_pk>[0-9]+)/subjects/$',
        SubjectStatsListView.as_view(), name='div-subject-stats-list'),
    url(r'^divisionsets/(?P<division_set_pk>[0-9]+)/subjects/(?P<pk>[0-9]+)/$',
        SubjectCourseView.as_view(), name='div-subject-course-list'),
    url(r'^subjects/(?P<pk>[0-9]+)/$',
        SubjectCourseView.as_view(), name='subject-course-list'),
    url(r'^courses/(?P<pk>[0-9]+)/$',
        CourseSectionView.as_view(), name='course-section-list'),
    url(r'^sections/(?P<pk>[0-9]+)/$',
        SectionDetailView.as_view(), name='section-detail'),
]
