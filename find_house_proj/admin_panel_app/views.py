from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView, TemplateView
from users_app.models import *
from users_app.forms import *
from find_house_app.models import *
from find_house_app.forms import *
from chat_app.models import *
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import update_session_auth_hash
from admin_panel_app.forms import (UserForm, EditUserForm, AnnouncementForm, AnnouncementImageForm, CategoryForm, FavoriteForm, NewsForm, AnnouncementViewHistoryForm, 
                                   CommentForm, ChatForm, MessageForm)
from django.contrib.auth.hashers import make_password

# region Basic views
class AdminPanelHomeView(TemplateView):
    template_name = 'admin_panel_app/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users_count'] = CustomUser.objects.all().count()
        context['announcements_count'] = Announcement.objects.all().count()
        context['categories_count'] = Category.objects.all().count()
        context['news_count'] = News.objects.all().count()
        context['comments_count'] = Comment.objects.all().count()
        context['chats_count'] = Chat.objects.all().count()
        context['messages_count'] = Message.objects.all().count()
        
        return context
# endregion
    
# region User views
class UserCreateView(CreateView):
    model = CustomUser
    form_class = UserForm
    template_name = 'admin_panel_app/users/create.html'
    success_url = reverse_lazy('admin_user_list_index')

    def form_valid(self, form):
        form.instance.password = make_password(form.cleaned_data['password'])

        if form.cleaned_data.get('is_admin'):
            form.instance.is_superuser = True
            form.instance.is_admin = True

        return super().form_valid(form)
    
class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = EditUserForm
    template_name = 'admin_panel_app/users/update.html'
    success_url = reverse_lazy('admin_user_list_index')
    
    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        return get_object_or_404(CustomUser, pk=pk)

    def form_valid(self, form):
        password = form.cleaned_data.get('password')
        password2 = form.cleaned_data.get('password2')

        if password and password2:
            user = self.request.user
            if user.check_password(password) and password == password2:
                user.set_password(password)
                user.save()
                update_session_auth_hash(self.request, user)
            else:
                pass
        
        response = super().form_valid(form)
        return response

class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = CustomUser
    template_name = 'admin_panel_app/users/delete.html'
    context_object_name = 'user'
    success_url = reverse_lazy('admin_user_list_index')

class UserDetailView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'admin_panel_app/users/read.html'
    context_object_name = 'user'

class UserListView(LoginRequiredMixin, ListView):
    model = CustomUser
    template_name = 'admin_panel_app/users/list.html'
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = CustomUser.objects.all().order_by('pk')
                
        return context
# endregion

 # region Announcement views
class AnnouncementCreateView(CreateView):
    model = Announcement
    form_class = AnnouncementForm
    template_name = 'admin_panel_app/announcement/create.html'
    success_url = reverse_lazy('admin_announcement_list')
    
    def form_valid(self, form):
        context = self.get_context_data()
        image_formset = context['image_formset']

        if form.is_valid() and image_formset.is_valid():
            self.object = form.save(commit=False)
            self.object.owner = form.cleaned_data['owner']
            self.object.save()

            image_formset.instance = self.object
            image_formset.save()

            return super().form_valid(form)
        else:
            return self.form_invalid(form)
    
    def get_form_kwargs(self):
        kwargs = super(AnnouncementCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if self.request.POST:
            context['image_formset'] = AnnouncementImageFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            context['image_formset'] = AnnouncementImageFormSet(instance=self.object)
        
        return context

class AnnouncementUpdateView(LoginRequiredMixin, UpdateView):
    model = Announcement
    form_class = AnnouncementForm
    template_name = 'admin_panel_app/announcement/update.html'
    success_url = reverse_lazy('admin_announcement_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if self.request.POST:
            context['image_formset'] = AnnouncementImageFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            context['image_formset'] = AnnouncementImageFormSet(instance=self.object)
            
        context['existing_images'] = self.object.images.all()
        
        return context

class AnnouncementDeleteView(LoginRequiredMixin, DeleteView):
    model = Announcement
    template_name = 'admin_panel_app/announcement/delete.html'
    context_object_name = 'announcement'
    success_url = reverse_lazy('admin_announcement_list')

class AnnouncementDetailView(LoginRequiredMixin, DetailView):
    model = Announcement
    template_name = 'admin_panel_app/announcement/read.html'
    context_object_name = 'announcement'
    
class AnnouncementListView(LoginRequiredMixin, ListView):
    model = Announcement
    template_name = 'admin_panel_app/announcement/list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['announcements'] = Announcement.objects.all().order_by('pk')
        
        return context
# endregion

# region CarImage views
class AnnouncementImageCreateView(CreateView):
    model = AnnouncementImage
    form_class = AnnouncementImageForm
    template_name = 'admin_panel_app/announcement image/create.html'
    success_url = reverse_lazy('admin_announcement_images_list')

class AnnouncementImageUpdateView(LoginRequiredMixin, UpdateView):
    model = AnnouncementImage
    form_class = AnnouncementImageForm
    template_name = 'admin_panel_app/announcement image/update.html'
    success_url = reverse_lazy('admin_announcement_images_list')

class AnnouncementImageDeleteView(LoginRequiredMixin, DeleteView):
    model = AnnouncementImage
    template_name = 'admin_panel_app/announcement image/delete.html'
    context_object_name = 'announcement_images'
    success_url = reverse_lazy('admin_announcement_images_list')

class AnnouncementImageDetailView(LoginRequiredMixin, DetailView):
    model = AnnouncementImage
    template_name = 'admin_panel_app/announcement image/read.html'
    context_object_name = 'announcement_images'

class AnnouncementImageListView(LoginRequiredMixin, ListView):
    model = AnnouncementImage
    template_name = 'admin_panel_app/announcement image/list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['announcement_images'] = AnnouncementImage.objects.all().order_by('pk')
        
        return context
# endregion

# region Category views
class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'admin_panel_app/category/create.html'
    success_url = reverse_lazy('admin_categories_list')

class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'admin_panel_app/category/update.html'
    success_url = reverse_lazy('admin_categories_list')

class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'admin_panel_app/category/delete.html'
    context_object_name = 'category'
    success_url = reverse_lazy('admin_categories_list')

class CategoryDetailView(LoginRequiredMixin, DetailView):
    model = Category
    template_name = 'admin_panel_app/category/read.html'
    context_object_name = 'category'

class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'admin_panel_app/category/list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all().order_by('pk')
        
        return context
# endregion

# region Favorite views
class FavoriteCreateView(CreateView):
    model = Favorite
    form_class = FavoriteForm
    template_name = 'admin_panel_app/favorite/create.html'
    success_url = reverse_lazy('admin_favorites_list')
    
    def form_valid(self, form):
        return super().form_valid(form)

class FavoriteUpdateView(LoginRequiredMixin, UpdateView):
    model = Favorite
    form_class = FavoriteForm
    template_name = 'admin_panel_app/favorite/update.html'
    success_url = reverse_lazy('admin_favorites_list')
    
    def form_valid(self, form):
        return super().form_valid(form)

class FavoriteDeleteView(LoginRequiredMixin, DeleteView):
    model = Favorite
    template_name = 'admin_panel_app/favorite/delete.html'
    context_object_name = 'favorite'
    success_url = reverse_lazy('admin_favorites_list')

class FavoriteDetailView(LoginRequiredMixin, DetailView):
    model = Favorite
    template_name = 'admin_panel_app/favorite/read.html'
    context_object_name = 'favorite'

class FavoriteListView(LoginRequiredMixin, ListView):
    model = Favorite
    template_name = 'admin_panel_app/favorite/list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['favorites'] = Favorite.objects.all().order_by('pk')
        
        return context
# endregion

# region NewsItem views
class NewsCreateView(CreateView):
    model = News
    form_class = NewsForm
    template_name = 'admin_panel_app/news/create.html'
    success_url = reverse_lazy('admin_news_list')

class NewsUpdateView(LoginRequiredMixin, UpdateView):
    model = News
    form_class = NewsForm
    template_name = 'admin_panel_app/news/update.html'
    success_url = reverse_lazy('admin_news_list')

class NewsDeleteView(LoginRequiredMixin, DeleteView):
    model = News
    template_name = 'admin_panel_app/news/delete.html'
    context_object_name = 'news_item'
    success_url = reverse_lazy('admin_news_list')

class NewsDetailView(LoginRequiredMixin, DetailView):
    model = News
    template_name = 'admin_panel_app/news/read.html'
    context_object_name = 'news_item'

class NewsListView(LoginRequiredMixin, ListView):
    model = News
    template_name = 'admin_panel_app/news/list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news'] = News.objects.all().order_by('pk')
        
        return context
# endregion 

# region AnnouncementViewHistory views
class AnnouncementViewHistoryCreateView(CreateView):
    model = AnnouncementViewHistory
    form_class = AnnouncementViewHistoryForm
    template_name = 'admin_panel_app/announcement view history/create.html'
    success_url = reverse_lazy('admin_announcement_view_histories_list')

class AnnouncementViewHistoryUpdateView(LoginRequiredMixin, UpdateView):
    model = AnnouncementViewHistory
    form_class = AnnouncementViewHistoryForm
    template_name = 'admin_panel_app/announcement view history/update.html'
    success_url = reverse_lazy('admin_announcement_view_histories_list')

class AnnouncementViewHistoryDeleteView(LoginRequiredMixin, DeleteView):
    model = AnnouncementViewHistory
    template_name = 'admin_panel_app/announcement view history/delete.html'
    context_object_name = 'announcement_view_history'
    success_url = reverse_lazy('admin_announcement_view_histories_list')

class AnnouncementViewHistoryDetailView(LoginRequiredMixin, DetailView):
    model = AnnouncementViewHistory
    template_name = 'admin_panel_app/announcement view history/read.html'
    context_object_name = 'announcement_view_history'

class AnnouncementViewHistoryListView(LoginRequiredMixin, ListView):
    model = AnnouncementViewHistory
    template_name = 'admin_panel_app/announcement view history/list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['announcement_view_histories'] = AnnouncementViewHistory.objects.all().order_by('pk')
        
        return context
# endregion

# region Comment views
class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'admin_panel_app/comment/create.html'
    success_url = reverse_lazy('admin_comments_list')

class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'admin_panel_app/comment/update.html'
    success_url = reverse_lazy('admin_comments_list')

class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'admin_panel_app/comment/delete.html'
    context_object_name = 'comment'
    success_url = reverse_lazy('admin_comments_list')

class CommentDetailView(LoginRequiredMixin, DetailView):
    model = Comment
    template_name = 'admin_panel_app/comment/read.html'
    context_object_name = 'comment'

class CommentListView(LoginRequiredMixin, ListView):
    model = Comment
    template_name = 'admin_panel_app/comment/list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.all().order_by('pk')
        
        return context
# endregion

# region Chat views
class ChatCreateView(CreateView):
    model = Chat
    form_class = ChatForm
    template_name = 'admin_panel_app/chats/create.html'
    success_url = reverse_lazy('admin_chats_list')

class ChatUpdateView(LoginRequiredMixin, UpdateView):
    model = Chat
    form_class = ChatForm
    template_name = 'admin_panel_app/chats/update.html'
    success_url = reverse_lazy('admin_chats_list')

class ChatDeleteView(LoginRequiredMixin, DeleteView):
    model = Chat
    template_name = 'admin_panel_app/chats/delete.html'
    context_object_name = 'chat'
    success_url = reverse_lazy('admin_chats_list')

class ChatDetailView(LoginRequiredMixin, DetailView):
    model = Chat
    template_name = 'admin_panel_app/chats/read.html'
    context_object_name = 'chat'

class ChatListView(LoginRequiredMixin, ListView):
    model = Chat
    template_name = 'admin_panel_app/chats/list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['chats'] = Chat.objects.all().order_by('pk')
        
        return context
# endregion

# region Chat views
class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'admin_panel_app/messages/create.html'
    success_url = reverse_lazy('admin_messages_list')

class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'admin_panel_app/messages/update.html'
    success_url = reverse_lazy('admin_messages_list')

class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    template_name = 'admin_panel_app/messages/delete.html'
    context_object_name = 'message'
    success_url = reverse_lazy('admin_messages_list')

class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    template_name = 'admin_panel_app/messages/read.html'
    context_object_name = 'message'

class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'admin_panel_app/messages/list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['messages'] = Message.objects.all().order_by('pk')
        
        return context
# endregion
