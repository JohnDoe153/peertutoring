from django.contrib import admin
from courses.models import Class, Lesson, Course

admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Class)
