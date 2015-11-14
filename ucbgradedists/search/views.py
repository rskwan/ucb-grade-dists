from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView, RedirectView

from core.models import Term, DivisionSet, Subject, SubjectStats, \
                        Course, Section, Grade, GradeCount, init_divsets

class DivisionChoiceView(ListView):
    template_name = 'search/division_choice.html'

    def get_queryset(self):
        if DivisionSet.objects.count() == 0:
            init_divsets()
        return DivisionSet.objects.all()

class SubjectListRedirectView(RedirectView):
    query_string = True
    pattern_name = 'div-subject-list'

class SubjectListView(ListView):
    template_name = 'search/subject_list.html'

    def get_queryset(self):
        if 'divsetpk' in self.kwargs:
            self.division_set = get_object_or_404(DivisionSet, pk=int(self.kwargs['divsetpk']))
        else:
            if DivisionSet.objects.count() == 0:
                init_divsets()
            self.division_set = get_object_or_404(DivisionSet, name="All")
        return SubjectStats.objects.filter(division_set=self.division_set)

    def get_context_data(self, **kwargs):
        context = super(SubjectListView, self).get_context_data(**kwargs)
        context['divset'] = self.division_set
        return context

class SubjectCourseView(DetailView):
    model = Subject
    template_name = 'search/subject_course_list.html'

    def get_context_data(self, **kwargs):
        context = super(SubjectCourseView, self).get_context_data(**kwargs)
        if 'divsetpk' in self.kwargs:
            divset = get_object_or_404(DivisionSet, pk=int(self.kwargs['divsetpk']))
        else:
            if DivisionSet.objects.count() == 0:
                init_divsets()
            divset = get_object_or_404(DivisionSet, name="All")
        context['divset'] = divset
        context['courses'] = self.object.course_set.\
                             filter(division__in=divset.data['divisions'])
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
