from django import forms
from .models import Class, Course, Lesson


class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = '__all__'
        help_texts = {
            'title': 'E.g., Grade 11 or Computer Science Class',
            'description': 'Provide a short description of the class',
            'image': 'You can upload a class image or leave it empty'
        }


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['creator', 'slug', 'title', 'class_category', 'description', 'course_image']
        help_texts = {
            'title': 'E.g., Mathematics, Geography, etc.',
            'description': 'Provide a short description of the course',
            'class_category': 'Select the class this course belongs to',
            'course_image': 'You can upload a course image or leave it empty'
        }
        labels = {
            'title': 'Course Title'
        }
        widgets = {'creator': forms.HiddenInput(), 'slug': forms.HiddenInput()}


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['slug', 'title', 'course', 'video_id', 'position']
        help_texts = {
            'title': 'Enter the lesson title',
            'course': 'Select the course this lesson belongs to',
            'video_id': 'Enter the YouTube video ID (<a href="/media/youtube_help.png">How to find the ID?</a>)',
            'position': 'Set the lesson order number'
        }
        widgets = {
            'slug': forms.HiddenInput()
        }
