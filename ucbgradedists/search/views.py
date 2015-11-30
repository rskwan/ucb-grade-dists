from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView, RedirectView
import json

from core import utils
from core.models import Term, DivisionSet, Subject, SubjectStats, \
                        Course, Section, Grade, GradeCount, \
                        Discipline, DisciplineStats

class Home(TemplateView):
    """
    Site homepage.
    """
    template_name = 'search/home.html'

    def get_context_data(self, **kwargs):
        context = {}
        context['divisions'] = DivisionSet.objects.all()

        division = DivisionSet.objects.get(slug='undergraduate')

        context['disciplines'] = DisciplineStats.objects.filter(division_set=division).order_by('mean')
        context['hardest_subjects'] = SubjectStats.objects.filter(division_set=division).filter(letter_grades__gte=1000).order_by('mean')[0:10]
        context['easiest_subjects'] = SubjectStats.objects.filter(division_set=division).filter(letter_grades__gte=1000).order_by('-mean')[0:10]
        context['hardest_classes'] = Course.objects.filter(division__in=[0,1]).filter(letter_grades__gte=1000).order_by('mean')[0:10]
        context['easiest_classes'] = Course.objects.filter(division__in=[0,1]).filter(letter_grades__gte=1000).order_by('-mean')[0:10]
        return context


class DivisionView(ListView):
    """
    A list of subjects in a particular division.
    """
    template_name = 'search/division.html'

    def get_queryset(self):
        self.division_set = get_object_or_404(DivisionSet,
            slug=self.kwargs['division'])
        return SubjectStats.objects.filter(division_set=self.division_set) \
                .filter(letter_grades__gte=500)

    def get_context_data(self, **kwargs):
        context = {}
        courses = []
        for stat in self.get_queryset():
            info = {}
            info['sub'] = stat.subject.name
            info['slug'] = stat.subject.slug
            info['discipline'] = stat.subject.discipline.name
            info['avg'] = stat.mean
            info['grade'] = utils.lettergrade(stat.mean)
            info['std'] = stat.stdev
            info['num'] = stat.letter_grades
            info['dist'] = stat.formatted_distribution

            courses.append(info)

        context['data'] = json.dumps(courses)
        context['name'] = self.division_set.name

        return context


class SubjectDetail(DetailView):
    """
    A single subject.
    """
    model = Subject
    template_name = 'search/subject.html'
    slug_url_kwarg = 'subject'


class DisciplineDetail(DetailView):
    """
    A single discipline.
    """
    model = Discipline
    template_name = 'search/discipline.html'
    slug_url_kwarg = 'discipline'


class CourseDetail(DetailView):
    """
    A single course.
    """
    model = Course
    template_name = 'search/course.html'

