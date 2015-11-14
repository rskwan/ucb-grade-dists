from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView, RedirectView

from core.models import Term, DivisionSet, Subject, SubjectStats, \
                        Course, Section, Grade, GradeCount, init_division_sets

class DivisionSetListView(ListView):
    template_name = 'search/division_set_list.html'
    context_object_name = "division_set_list"

    def get_queryset(self):
        if DivisionSet.objects.count() == 0:
            init_division_sets()
        return DivisionSet.objects.all()

class SubjectStatsListRedirectView(RedirectView):
    query_string = True
    pattern_name = 'div-subject-stats-list'

class SubjectStatsListView(ListView):
    template_name = 'search/subject_stats_list.html'
    context_object_name = "subject_stats_list"

    def get_queryset(self):
        if 'division_set_pk' in self.kwargs:
            self.division_set = get_object_or_404(DivisionSet, pk=int(self.kwargs['division_set_pk']))
        else:
            if DivisionSet.objects.count() == 0:
                init_division_sets()
            self.division_set = get_object_or_404(DivisionSet, name="All")
        return SubjectStats.objects.filter(division_set=self.division_set)

    def get_context_data(self, **kwargs):
        context = super(SubjectStatsListView, self).get_context_data(**kwargs)
        context['division_set'] = self.division_set
        return context

class SubjectCourseView(DetailView):
    model = Subject
    template_name = 'search/subject_course_list.html'
    context_object_name = "subject"

    def get_context_data(self, **kwargs):
        context = super(SubjectCourseView, self).get_context_data(**kwargs)
        if 'division_set_pk' in self.kwargs:
            division_set = get_object_or_404(DivisionSet, pk=int(self.kwargs['division_set_pk']))
        else:
            if DivisionSet.objects.count() == 0:
                init_division_sets()
            division_set = get_object_or_404(DivisionSet, name="All")
        context['division_set'] = division_set
        context['courses'] = self.object.course_set.\
                             filter(division__in=division_set.data['divisions'])
        return context

class CourseSectionView(DetailView):
    model = Course
    template_name = 'search/course_section_list.html'
    context_object_name = "course"

    def get_context_data(self, **kwargs):
        context = super(CourseSectionView, self).get_context_data(**kwargs)
        context['sections'] = self.object.section_set.all()
        return context

class SectionDetailView(DetailView):
    model = Section
    template_name = 'search/section_detail.html'
    context_object_name = "section"

    def get_context_data(self, **kwargs):
        context = super(SectionDetailView, self).get_context_data(**kwargs)
        context['grade_counts'] = self.object.gradecount_set.in_grade_order()
        return context
