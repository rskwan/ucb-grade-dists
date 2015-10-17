from django.conf.urls import url

from search.views import SubjectListView, SubjectCourseView, CourseSectionView, SectionDetailView

urlpatterns = [
    url(r'^subjects/$', SubjectListView.as_view(), name='subject-list'),
    url(r'^subjects/(?P<pk>[0-9]+)/$', SubjectCourseView.as_view(), name='subject-course-list'),
    url(r'^courses/(?P<pk>[0-9]+)/$', CourseSectionView.as_view(), name='course-section-list'),
    url(r'^sections/(?P<pk>[0-9]+)/$', SectionDetailView.as_view(), name='section-detail'),
]
