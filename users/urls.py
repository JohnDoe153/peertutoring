from django.urls import path
from users.views import profile_view, request_teacher_account

app_name = 'users'

urlpatterns = [
    path('profile/', profile_view, name='profile'),
    path('request-teacher/', request_teacher_account, name='request_teacher')
]
