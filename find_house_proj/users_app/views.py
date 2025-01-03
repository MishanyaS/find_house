from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from users_app.models import CustomUser
from users_app.forms import RegistrationForm, LoginForm, EditUserForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LoginView
from find_house_app.models import Announcement, AnnouncementViewHistory, Comment
from django.contrib.auth import update_session_auth_hash
from admin_panel_app.models import Content

# Create your views here.
# region CustomUser views
class CustomUserRegistrationView(CreateView):
    model = CustomUser
    form_class = RegistrationForm
    template_name = 'users_app/registration/registration.html'
    success_url = reverse_lazy('users_app:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['content'] = Content.objects.order_by('-change_date').first()
            
        return context

class CustomUserLoginView(LoginView):
    form_class = LoginForm
    template_name = 'users_app/registration/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['content'] = Content.objects.order_by('-change_date').first()
            
        return context

class CustomUserDeleteView(LoginRequiredMixin, DeleteView):
    model = CustomUser
    template_name = 'users_app/registration/delete_user.html'
    success_url = reverse_lazy('find_house_app:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['content'] = Content.objects.order_by('-change_date').first()
            
        return context

class CustomUserUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = EditUserForm
    template_name = 'users_app/registration/user_settings_update.html'

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        old_password = form.cleaned_data.get('old_password')
        new_password1 = form.cleaned_data.get('new_password1')
        new_password2 = form.cleaned_data.get('new_password2')

        if old_password and new_password1 and new_password2:
            user = self.request.user
            if user.check_password(old_password) and new_password1 == new_password2:
                user.set_password(new_password1)
                user.save()
                update_session_auth_hash(self.request, user)
            else:
                pass
        
        response = super().form_valid(form)
        
        return response
    
    def get_success_url(self):
        return reverse_lazy('users_app:profile_read', kwargs={'pk': self.request.user.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['content'] = Content.objects.order_by('-change_date').first()

        return context
    
class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'users_app/profile/profile.html'
    
    def get_object(self, queryset=None):
        return get_object_or_404(CustomUser, pk=self.kwargs['pk'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_announcements'] = Announcement.objects.filter(owner=self.request.user)
        context['user_view_history'] = AnnouncementViewHistory.objects.filter(user=self.request.user)
        context['user_comments'] = Comment.objects.filter(user=self.request.user)

        view_history = AnnouncementViewHistory.objects.filter(user=self.request.user)
        context['view_history'] = view_history

        context['content'] = Content.objects.order_by('-change_date').first()

        return context
# endregion
