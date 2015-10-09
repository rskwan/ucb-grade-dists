from tastypie import fields
from tastypie.resources import ModelResource
from core.models import Term, Subject, Course, Section, Grade

class TermResource(ModelResource):
    class Meta:
        queryset = Term.objects.all()
        allowed_methods = ['get']

class SubjectResource(ModelResource):
    class Meta:
        queryset = Subject.objects.all()
        allowed_methods = ['get']

class CourseResource(ModelResource):
    subject = fields.ForeignKey(SubjectResource, 'subject')

    class Meta:
        queryset = Course.objects.all()
        allowed_methods = ['get']

class SectionResource(ModelResource):
    course = fields.ForeignKey(CourseResource, 'course')
    term = fields.ForeignKey(TermResource, 'term')
    grade_average = fields.FloatField(readonly=True)

    class Meta:
        queryset = Section.objects.all()
        allowed_methods = ['get']

    def dehydrate_grade_average(self, bundle):
        return bundle.obj.grade_average

class GradeResource(ModelResource):
    class Meta:
        queryset = Grade.objects.all()
        allowed_methods = ['get']
