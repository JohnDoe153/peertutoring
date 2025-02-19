import secrets
from django.shortcuts import render, redirect
from django.views.generic import TemplateView,ListView,DetailView,View
from courses.models import Course, Lesson, Class
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ClassForm, CourseForm, LessonForm



class HomeView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Class.objects.all()
        context['categories'] = categories
        return context

class AboutView(TemplateView):
    template_name = 'about.html'


class ContactView(TemplateView):
    template_name = 'contact.html'


@login_required
def course_list_view(request, category):
    courses = Course.objects.filter(class_category=category)
    return render(request, 'courses/course_list.html', {'courses': courses})


class CourseDetailView(DetailView):
    context_object_name = 'course'
    template_name = 'courses/course_detail.html'
    model = Course


 
class LessonDetailView(View, LoginRequiredMixin):
    def get(self, request, course_slug, lesson_slug, *args, **kwargs):
        course = get_object_or_404(Course, slug=course_slug)
        lesson = get_object_or_404(Lesson, slug=lesson_slug)
        return render(request, "courses/lesson_detail.html", {'lesson': lesson})


@login_required
def search_view(request):
    if request.method == 'POST':
        query = request.POST.get('search')
        results = Lesson.objects.filter(title__icontains=query)
        return render(request, 'courses/search_result.html', {'results': results})


@login_required
def create_class(request):
    if not request.user.profile.is_teacher:
        messages.error(request, 'Your account does not have access to this page!')
        return redirect('courses:home')
    form = ClassForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Class created successfully!')
        return redirect('courses:home')
    return render(request, 'courses/create_class.html', {'form': form})

@login_required
def create_course(request):
    if not request.user.profile.is_teacher:
        messages.error(request, 'Your account does not have access to this page!')
        return redirect('courses:home')
    form = CourseForm(request.POST or None)
    if form.is_valid():
        course = form.save()
        messages.success(request, 'Course created successfully!')
        return redirect(f'/courses/{course.class_category.id}')
    return render(request, 'courses/create_course.html', {'form': form})

@login_required
def create_lesson(request):
    if not request.user.profile.is_teacher:
        messages.error(request, 'Your account does not have access to this page!')
        return redirect('courses:home')
    form = LessonForm(request.POST or None)
    if form.is_valid():
        lesson = form.save()
        messages.success(request, 'Lesson created successfully!')
        return redirect(f'/courses/{lesson.course.slug}')
    return render(request, 'courses/create_lesson.html', {'form': form})


@login_required
def delete_class(request, pk):
    class_instance = get_object_or_404(Class, pk=pk)
    if not request.user.profile.is_teacher:
        messages.error(request, 'Your account does not have permission for this action!')
        return redirect('courses:home')
    class_instance.delete()
    messages.success(request, f'Class "{class_instance.title}" was deleted!')
    return redirect('courses:home')



@login_required
def delete_course(request, slug):
    course = get_object_or_404(Course, slug=slug)
    if not request.user.profile.is_teacher:
        messages.error(request, 'Your account does not have permission for this action!')
        return redirect('courses:home')
    course.delete()
    messages.success(request, f'Course "{course.title}" was deleted!')
    return redirect('courses:home')



@login_required
def delete_lesson(request, slug):
    lesson = get_object_or_404(Lesson, slug=slug)
    if not request.user.profile.is_teacher:
        messages.error(request, 'Your account does not have permission for this action!')
        return redirect('courses:home')
    lesson.delete()
    messages.success(request, f'Lesson "{lesson.title}" was deleted!')
    return redirect('courses:home')


def view_404(request, exception):
    return render(request, '404.html')

def view_403(request, exception):
    return render(request, '403.html')

def view_500(request):
    return render(request, '500.html')
