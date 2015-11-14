from django.conf.urls import url

from search.views import *

urlpatterns = [
    url(r'^divisionsets/$',
        DivisionChoiceView.as_view(), name='division-choice'),
    url(r'^divisionsets/(?P<divsetpk>[0-9]+)/$',
        SubjectListRedirectView.as_view()),
    url(r'^divisionsets/(?P<divsetpk>[0-9]+)/subjects/$',
        SubjectListView.as_view(), name='div-subject-list'),
    url(r'^divisionsets/(?P<divsetpk>[0-9]+)/subjects/(?P<pk>[0-9]+)/$',
        SubjectCourseView.as_view(), name='div-subject-course-list'),
    url(r'^subjects/(?P<pk>[0-9]+)/$',
        SubjectCourseView.as_view(), name='subject-course-list'),
    url(r'^courses/(?P<pk>[0-9]+)/$',
        CourseSectionView.as_view(), name='course-section-list'),
    url(r'^sections/(?P<pk>[0-9]+)/$',
        SectionDetailView.as_view(), name='section-detail'),
]
