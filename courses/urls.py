from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import *

app_name = 'courses'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('courses/<int:category>/', course_list_view, name='course_list'),
    path('courses/<slug>/', login_required(CourseDetailView.as_view()), name='course_detail'),
    path('courses/<course_slug>/<lesson_slug>/', login_required(LessonDetailView.as_view()), name='lesson_detail'),
    path('search/', search_view, name='search_course'),
    path('create/class/', create_class, name='create_class'),
    path('create/course/', create_course, name='create_course'),
    path('create/lesson/', create_lesson, name='create_lesson'),
    path('delete/class/<int:pk>/', delete_class, name='delete_class'),
    path('delete/course/<slug:slug>/', delete_course, name='delete_course'),
    path('delete/lesson/<slug:slug>/', delete_lesson, name='delete_lesson'),
]
