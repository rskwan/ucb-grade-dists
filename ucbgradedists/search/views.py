from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView

from core.models import Term, Subject, Course, Section, Grade, GradeCount

class SubjectListView(ListView):
    model = Subject
    template_name = 'search/subject_list.html'

class SubjectCourseView(DetailView):
    model = Subject
    template_name = 'search/subject_course_list.html'

    def get_context_data(self, **kwargs):
        context = super(SubjectCourseView, self).get_context_data(**kwargs)
        context['courses'] = self.object.course_set.all()
        return context

class CourseSectionView(DetailView):
    model = Course
    template_name = 'search/course_section_list.html'

    def get_context_data(self, **kwargs):
        context = super(CourseSectionView, self).get_context_data(**kwargs)
        context['sections'] = self.object.section_set.all()
        return context

class SectionDetailView(DetailView):
    model = Section
    template_name = 'search/section_detail.html'

    def get_context_data(self, **kwargs):
        context = super(SectionDetailView, self).get_context_data(**kwargs)
        context['grade_counts'] = self.object.gradecount_set.in_grade_order()
        return context
