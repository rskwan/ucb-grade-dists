from django.contrib import admin

from .models import Term, Subject, Course, Section, Grade, GradeCount

class GradeCountInline(admin.TabularInline):
    model = GradeCount

class SectionAdmin(admin.ModelAdmin):
    inlines = [GradeCountInline]

admin.site.register(Term)
admin.site.register(Subject)
admin.site.register(Course)
admin.site.register(Section, SectionAdmin)
admin.site.register(Grade)
