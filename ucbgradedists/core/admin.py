from django.contrib import admin

from .models import Term, DivisionSet, Subject, SubjectStats, Course, Section, Grade, GradeCount

class GradeCountInline(admin.TabularInline):
    model = GradeCount

class SectionAdmin(admin.ModelAdmin):
    inlines = [GradeCountInline]

admin.site.register(Term)
admin.site.register(DivisionSet)
admin.site.register(Subject)
admin.site.register(SubjectStats)
admin.site.register(Course)
admin.site.register(Section, SectionAdmin)
admin.site.register(Grade)
