from tastypie import fields
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from core.models import Term, Subject, Course, Section, Grade

class TermResource(ModelResource):
    class Meta:
        queryset = Term.objects.all()
        allowed_methods = ['get']
        fitering = {
            'season': ALL,
            'year': ALL,
            'id': ALL,
        }

class SubjectResource(ModelResource):
    class Meta:
        queryset = Subject.objects.all()
        allowed_methods = ['get']
        filtering = {
            'name': ALL,
            'id': ALL,
        }

class CourseResource(ModelResource):
    subject = fields.ForeignKey(SubjectResource, 'subject')

    class Meta:
        queryset = Course.objects.all()
        allowed_methods = ['get']
        filtering = {
            'subject': ALL_WITH_RELATIONS,
            'number': ALL,
            'id': ALL,
        }

class SectionResource(ModelResource):
    course = fields.ForeignKey(CourseResource, 'course')
    term = fields.ForeignKey(TermResource, 'term')
    grade_average = fields.FloatField(readonly=True)

    class Meta:
        queryset = Section.objects.all()
        allowed_methods = ['get']
        filtering = {
            'course': ALL_WITH_RELATIONS,
            'term': ALL_WITH_RELATIONS,
            'ccn': ALL,
            'id': ALL,
        }

    def dehydrate_grade_average(self, bundle):
        return bundle.obj.grade_average

class GradeResource(ModelResource):
    class Meta:
        queryset = Grade.objects.all()
        allowed_methods = ['get']
        filtering = {
            'id': ALL,
        }
