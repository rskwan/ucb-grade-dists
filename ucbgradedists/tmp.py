from __future__ import division
from core.models import *
sec_total = Section.objects.count()
sec_num = 0
for subject in Subject.objects.all():
    for course in subject.course_set.all():
        for section in course.section_set.all():
            sec_num += 1
            section.save()
            print sec_num / sec_total, "({0} of {1})".format(sec_num, sec_total)
        course.save()
        print course
    subject.save()
    print subject
