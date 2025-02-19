from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from users.forms import ProfileUpdateForm, UserUpdateForm
from users.models import Profile, Request
from django.contrib.auth.models import User


@login_required
def profile_view(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your account has been successfully updated!')
            return redirect('users:profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'profile/profile.html', context)


@login_required
def request_teacher_account(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('e-mail')
        phone_number = request.POST.get('phone')

        profile = request.user.profile
        teacher_request = Request(profile=profile, name=name, email=email, phone_number=phone_number)
        teacher_request.save()

        Profile.objects.filter(id=profile.id).update(is_teacher=True)

        # Send confirmation email to user
        user_message = (
            "Your request for a teacher account has been approved! "
            "You can now return to the site and upload courses and lessons. Good luck!"
        )
        send_mail(
            subject="test: Request Approved",
            message=user_message,
            from_email="test@no-reply.com",
            recipient_list=[email],
            fail_silently=False,
        )

        # Notify admin
        admin_message = (
            f"New teacher request:\n"
            f"Name: {name}\n"
            f"Email: {email}\n"
            f"Phone: {phone_number}\n"
            f"Profile: {profile}"
        )
        send_mail(
            subject="test: New Teacher Request",
            message=admin_message,
            from_email="test@no-reply.com",
            recipient_list=['admin@example.com'],
            fail_silently=False,
        )

        messages.info(request, "Your request has been successfully sent. You will be notified via email.")
        return redirect('courses:home')
