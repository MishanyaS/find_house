from django.shortcuts import render
import datetime
from sqlite3 import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView, TemplateView, View
from find_house_app.models import Category, Announcement, News, AnnouncementViewHistory, Favorite, Comment
from find_house_app.forms import AnnouncementForm, AnnouncementImageFormSet, CommentForm
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from users_app.models import CustomUser
from django.http import JsonResponse
from admin_panel_app.models import Content
from slugify import slugify
from django.conf import settings
from urllib.parse import urlparse
from django.http import HttpResponseRedirect
from django.urls.base import resolve, reverse
from django.urls.exceptions import Resolver404
from django.utils import translation
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

# Create your views here.
# region Basic views
@method_decorator(cache_page(60 * 10), name='dispatch')
class HomeView(ListView):
    model = Announcement
    template_name = 'find_house_app/index.html'
    context_object_name = 'announcements'
    paginate_by = 5
    
    def get_queryset(self):
        query = self.request.GET.get('q', '')
        if query:
            return Announcement.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
        return Announcement.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if self.request.user.is_authenticated and hasattr(self.request.user, 'profile'):
            context['user_profile'] = self.request.user.profile
        
        top_announcements = Announcement.objects.filter(status=Announcement.ACTIVE).order_by('-views')[:3]
        
        context['top_announcements'] = top_announcements
        context['news'] = News.objects.all().order_by('-date_added')[:4]
        context['categories'] = Category.objects.all()
        context['content'] = Content.objects.order_by('-change_date').first()
        context['announcements_count'] = Announcement.objects.all().count()

        # Pagination
        announcements_list = Announcement.objects.filter(status=Announcement.ACTIVE)
        paginator = Paginator(announcements_list, self.paginate_by)
        page = self.request.GET.get('page')

        try:
            announcements = paginator.page(page)
        except PageNotAnInteger:
            announcements = paginator.page(1)
        except EmptyPage:
            announcements = paginator.page(paginator.num_pages)

        context['announcements'] = announcements
        
        return context
    
    def add_to_favorites(self, announcement_id):
        existing_favorite = Favorite.objects.filter(user=self.request.user, announcement_id=announcement_id, ).first()

        if not existing_favorite:
            Favorite.objects.create(user=self.request.user, announcement_id=announcement_id, is_in_favorite=True)

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        announcement_id = request.POST.get('announcement_id')

        try:
            if action == 'find_house_app:add_to_favorites':
                self.add_to_favorites(announcement_id)
        except IntegrityError as e:
            pass

        return redirect('find_house_app:favorite')

@method_decorator(cache_page(60 * 10), name='dispatch')
class HelpView(TemplateView):
    template_name = 'find_house_app/help/help.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['content'] = Content.objects.order_by('-change_date').first()

        return context

@method_decorator(cache_page(60 * 10), name='dispatch')
class ContactsView(TemplateView):
    template_name = 'find_house_app/help/contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['admin'] = CustomUser.objects.filter(is_admin=True).order_by('?').first()
        context['content'] = Content.objects.order_by('-change_date').first()
        
        return context

class SearchBySiteView(View):
    template_name = 'find_house_app/search/search_by_site.html'
    
    def get(self, request):
        search_site = self.request.GET.get('search_site', '')
        announcements = Announcement.objects.all()
        news = News.objects.all()
        categories = Category.objects.all()

        if search_site:
            announcements = announcements.filter(Q(title__icontains=search_site) | Q(description__icontains=search_site))
            news = news.filter(Q(title__icontains=search_site) | Q(content__icontains=search_site))
            categories = categories.filter(Q(name__icontains=search_site) | Q(description__icontains=search_site))

        context = {
            'search_site': search_site,
            'announcements': announcements,
            'categories': categories,
            'news': news,
        }

        context['content'] = Content.objects.order_by('-change_date').first()

        return render(request, self.template_name, context)
# endregion

# region Announcement views
class AnnouncementCreateView(CreateView):
    model = Announcement
    form_class = AnnouncementForm
    template_name = 'find_house_app/announcement/create.html'
    success_url = reverse_lazy('find_house_app:home')
        
    def form_valid(self, form):
        context = self.get_context_data()
        image_formset = context['image_formset']

        if form.is_valid() and image_formset.is_valid():
            self.object = form.save(commit=False)
            self.object.owner = form.cleaned_data['owner']
            self.object.slug = slugify(form.cleaned_data['title'])
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
        context['content'] = Content.objects.order_by('-change_date').first()
        
        if self.request.POST:
            context['image_formset'] = AnnouncementImageFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            context['image_formset'] = AnnouncementImageFormSet(instance=self.object)
        
        return context

class AnnouncementDetailView(DetailView):
    model = Announcement
    template_name = 'find_house_app/announcement/read.html'
    context_object_name = 'announcement'
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        obj.views += 1
        obj.save()

        if self.request.user.is_authenticated:
            obj.views -= 1
            AnnouncementViewHistory.objects.create(user=self.request.user, announcement=obj)

        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['content'] = Content.objects.order_by('-change_date').first()
        if self.request.POST:
            context['image_formset'] = AnnouncementImageFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            context['image_formset'] = AnnouncementImageFormSet(instance=self.object)
            
        if self.request.user.is_authenticated and hasattr(self.request.user, 'profile'):
            context['user_profile'] = self.request.user.profile

        owner_email = self.object.owner.email
        context['owner_email'] = owner_email
        
        if self.request.user.is_authenticated and hasattr(self.request.user, 'profile'):
            context['user_profile'] = self.request.user.profile

        return context

class AnnouncementUpdateView(UpdateView):
    model = Announcement
    form_class = AnnouncementForm
    template_name = 'find_house_app/announcement/update.html'
    success_url = reverse_lazy('find_house_app:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['content'] = Content.objects.order_by('-change_date').first()
        
        if self.request.POST:
            context['image_formset'] = AnnouncementImageFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            context['image_formset'] = AnnouncementImageFormSet(instance=self.object)
            
        context['existing_images'] = self.object.images.all()
        
        return context
    
    def get_success_url(self):
        return reverse_lazy('users_app:profile_read', kwargs={'pk': self.request.user.pk})

class AnnouncementDeleteView(DeleteView):
    model = Announcement
    template_name = 'find_house_app/announcement/delete.html'
        
    def get_success_url(self):
        return reverse_lazy('users_app:profile_read', kwargs={'pk': self.request.user.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['content'] = Content.objects.order_by('-change_date').first()
        
        return context

class SearchAnnouncementView(View):
    template_name = 'find_house_app/index.html'
    paginate_by = 5

    def get(self, request, *args, **kwargs):
        query = request.GET.get('q', '')
        category_filter = request.GET.get('category', '')

        announcements = Announcement.objects.filter(Q(title__icontains=query))

        if category_filter:
            announcements = announcements.filter(category__name=category_filter)
            
        # Filters
        description_filter = request.GET.get('description', '')
        if description_filter:
            announcements = announcements.filter(description__icontains=description_filter)

        price_from_filter = request.GET.get('price_from', '')
        price_to_filter = request.GET.get('price_to', '')
        if price_from_filter and price_to_filter:
            announcements = announcements.filter(price__range=(price_from_filter, price_to_filter))

        square_from_filter = request.GET.get('square_from', '')
        square_to_filter = request.GET.get('square_to', '')
        if square_from_filter and square_to_filter:
            announcements = announcements.filter(square__range=(square_from_filter, square_to_filter))
            
        date_added_filter = request.GET.get('date_added', '')
        if date_added_filter:
            try:
                date_added_filter = datetime.datetime.strptime(date_added_filter, '%Y-%m-%d')
                announcements = announcements.filter(date_added__date=date_added_filter.date())
            except ValueError:
                pass
                
        address_filter = request.GET.get('address', '')
        if address_filter:
            announcements = announcements.filter(address__icontains=address_filter)

        # Pagination
        paginator = Paginator(announcements, self.paginate_by)
        page = request.GET.get('page')

        try:
            announcements = paginator.page(page)
        except PageNotAnInteger:
            announcements = paginator.page(1)
        except EmptyPage:
            announcements = paginator.page(paginator.num_pages)

        categories = Category.objects.all()
        news = News.objects.all().order_by('-date_added')[:4]
        top_announcements = Announcement.objects.filter(status=Announcement.ACTIVE).order_by('-views')[:3]

        context = {
            'announcements': announcements,
            'news': news,
            'categories': categories,
            'query': query,
            'selected_category': category_filter,
            'top_announcements': top_announcements,
        }

        context['content'] = Content.objects.order_by('-change_date').first()

        return render(request, self.template_name, context)

class SortAnnouncementView(View):
    template_name = 'find_house_app/index.html'
    paginate_by = 5

    def get(self, request, *args, **kwargs):
        sort_announcements_by = request.GET.get('sort', 'name')
        allowed_sort_fields = ['title', '-title', 'price', '-price', 'square', '-square', 'date_added', '-date_added']

        if sort_announcements_by not in allowed_sort_fields:
            sort_announcements_by = 'title'

        announcements = Announcement.objects.all().order_by(sort_announcements_by)
    
        # Pagination
        paginator = Paginator(announcements, self.paginate_by)
        page = request.GET.get('page')

        try:
            announcements = paginator.page(page)
        except PageNotAnInteger:
            announcements = paginator.page(1)
        except EmptyPage:
            announcements = paginator.page(paginator.num_pages)

        categories = Category.objects.all()
        news = News.objects.all().order_by('-date_added')[:4]
        top_announcements = Announcement.objects.filter(status=Announcement.ACTIVE).order_by('-views')[:3]

        context = {
            'announcements': announcements,
            'news': news,
            'categories': categories,
            'sort_announcements_by': sort_announcements_by,
            'top_announcements': top_announcements,
        }

        context['content'] = Content.objects.order_by('-change_date').first()

        return render(request, self.template_name, context)
    
class AddToFavoritesView(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Authentication required'}, status=403)
        
        announcement_id = request.POST.get('announcement_id')
        try:
            announcement = Announcement.objects.get(id=announcement_id)
            # Check if it already exists in favorites
            favorite, created = Favorite.objects.get_or_create(
                user=request.user, 
                announcement=announcement,
                defaults={'is_in_favorite': True}
            )
            if not created:
                return JsonResponse({'error': 'Already in favorites'}, status=400)
        except Announcement.DoesNotExist:
            return JsonResponse({'error': 'Announcement not found'}, status=404)
        except IntegrityError:
            return JsonResponse({'error': 'Error adding to favorites'}, status=500)

        return redirect('find_house_app:favorite')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['content'] = Content.objects.order_by('-change_date').first()
        
        return context
# endregion

# region News views
@method_decorator(cache_page(60 * 10), name='dispatch')
class NewsList(ListView):
    model = News
    template_name = 'find_house_app/news/news.html'
    context_object_name = 'news'
    paginate_by = 6
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        news_list = News.objects.all()
        paginator = Paginator(news_list, self.paginate_by)
        page = self.request.GET.get('page')

        try:
            news = paginator.page(page)
        except PageNotAnInteger:
            news = paginator.page(1)
        except EmptyPage:
            news = paginator.page(paginator.num_pages)

        context['news'] = news
        context['categories'] = Category.objects.all()
        context['content'] = Content.objects.order_by('-change_date').first()
        context['news_count'] = News.objects.all().count()
                            
        return context

class NewsDetail(DetailView):
    model = News
    template_name = 'find_house_app/news/read.html'
    context_object_name = 'news'
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        obj.views_count += 1
        obj.save()

        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['content'] = Content.objects.order_by('-change_date').first()
        
        return context

class SearchNewsView(ListView):
    model = News
    template_name = 'find_house_app/news/news.html'
    context_object_name = 'news'
    paginate_by = 6

    def get(self, request):
        query = self.request.GET.get('q', '')
        date_filter = self.request.GET.get('date', '')
        news = News.objects.all()

        if query:
            news = news.filter(Q(title__icontains=query))

        if date_filter:
            try:
                date_filter = datetime.datetime.strptime(date_filter, '%Y-%m-%d')
                news = news.filter(date_added__date=date_filter.date())
            except ValueError:
                pass
            
        # Pagination
        paginator = Paginator(news, self.paginate_by)
        page = request.GET.get('page')

        try:
            news = paginator.page(page)
        except PageNotAnInteger:
            news = paginator.page(1)
        except EmptyPage:
            news = paginator.page(paginator.num_pages)

        context = {
            'news': news,
            'query': query,
        }

        context['content'] = Content.objects.order_by('-change_date').first()

        return render(request, self.template_name, context)
    
class SortNewsView(ListView):
    model = News
    template_name = 'find_house_app/news/news.html'
    context_object_name = 'news'
    paginate_by = 6

    def get(self, request):
        sort_news_by = request.GET.get('sort_news', 'name')
        allowed_sort_fields = ['title', '-title', 'date_added', '-date_added']

        if sort_news_by not in allowed_sort_fields:
            sort_news_by = 'title'

        news = News.objects.all().order_by(sort_news_by)
            
        # Pagination
        paginator = Paginator(news, self.paginate_by)
        page = request.GET.get('page')

        try:
            news = paginator.page(page)
        except PageNotAnInteger:
            news = paginator.page(1)
        except EmptyPage:
            news = paginator.page(paginator.num_pages)

        context = {
            'news': news,
            'sort_news_by': sort_news_by,
        }

        context['content'] = Content.objects.order_by('-change_date').first()

        return render(request, self.template_name, context)
# endregion

# region Category views
@method_decorator(cache_page(60 * 10), name='dispatch')
class CategoriesListView(TemplateView):
    template_name = 'find_house_app/category/categories.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['content'] = Content.objects.order_by('-change_date').first()
            
        return context

@method_decorator(cache_page(60 * 10), name='dispatch')
class CategoryListView(ListView):
    model = Category
    template_name = 'find_house_app/category/categories.html'
    context_object_name = 'categories'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['content'] = Content.objects.order_by('-change_date').first()

        return context

    def get_queryset(self):
        query = self.request.GET.get('q')
        
        if query:
            return Category.objects.filter(Q(name__icontains=query))
        else:
            return Category.objects.all()

class CategoryAnnouncementsView(ListView):
    model = Announcement
    context_object_name = 'category_announcements'
    template_name = 'find_house_app/category/category_announcements.html'
    paginate_by = 5

    def get_queryset(self):
        cats = self.kwargs['cats']
        category = get_object_or_404(Category, name__iexact=cats.replace('-', ' '))
        
        return Announcement.objects.filter(category=category, status=Announcement.ACTIVE)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cats'] = self.kwargs['cats'].title().replace('-', ' ')
        context['categories'] = Category.objects.all()
        context['content'] = Content.objects.order_by('-change_date').first()

        category_announcements_list = self.get_queryset()
        paginator = Paginator(category_announcements_list, self.paginate_by)
        page = self.request.GET.get('page')

        try:
            category_announcements = paginator.page(page)
        except PageNotAnInteger:
            category_announcements = paginator.page(1)
        except EmptyPage:
            category_announcements = paginator.page(paginator.num_pages)

        context['category_announcements'] = category_announcements

        return context
    
    def add_to_favorites(self, announcement_id):
        existing_favorite = Favorite.objects.filter(user=self.request.user, announcement_id=announcement_id).first()

        if not existing_favorite:
            Favorite.objects.create(user=self.request.user, announcement_id=announcement_id, is_in_favorite=True)

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        announcement_id = request.POST.get('announcement_id')

        try:
            if action == 'find_house_app:add_to_favorites':
                self.add_to_favorites(announcement_id)

        except IntegrityError as e:
            pass

        return redirect('favorite')
# endregion

# region Favorite views
class FavoriteView(ListView):
    model = Favorite
    template_name = 'find_house_app/favorite/favorite.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['favorites'] = Favorite.objects.filter(user=self.request.user)
        context['categories'] = Category.objects.all()
        context['content'] = Content.objects.order_by('-change_date').first()
        context['favorites_count'] = Favorite.objects.filter(user=self.request.user).count()
            
        return context
    
    def remove_from_favorites(self, announcement_id):
        favorite = get_object_or_404(Favorite, user=self.request.user, announcement_id=announcement_id)
        favorite.delete()

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        announcement_id = request.POST.get('announcement_id')

        try:
            if action == 'remove_from_favorites':
                self.remove_from_favorites(announcement_id)
        except IntegrityError as e:
            pass

        return redirect('find_house_app:favorite')
# endregion

# region Comment views
class CommentAddView(View):
    def post(self, request, pk):
        announcement = get_object_or_404(Announcement, pk=pk)
        user = request.user
        text = request.POST.get('comment_your_comment')

        if text:
            Comment.objects.create(announcement=announcement, user=user, text=text)

        return redirect('find_house_app:announcement_read', pk=pk)

class CommentEditView(View):
    template_name = 'find_house_app/comment/edit.html'

    def get(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        form = CommentForm(instance=comment)

        context = {
            'form': form,
            'comment': comment,
        }

        context['content'] = Content.objects.order_by('-change_date').first()
        
        return render(request, self.template_name, context)

    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        form = CommentForm(request.POST, instance=comment)

        if form.is_valid():
            form.save()
            return redirect('find_house_app:announcement_read', pk=comment.announcement.pk)
        else:
            return render(request, self.template_name, {'form': form, 'comment': comment})
        
class CommentDeleteView(View):
    def get(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)

        if comment.user == request.user:
            comment.delete()

        return redirect('find_house_app:announcement_read', pk=comment.announcement.pk)
# endregion

# region Language views
def set_language(request, language):
    for lang, _ in settings.LANGUAGES:
        translation.activate(lang)
        try:
            view = resolve(urlparse(request.META.get("HTTP_REFERER")).path)
        except Resolver404:
            view = None
        if view:
            break
    if view:
        translation.activate(language)
        #next_url = reverse(view.url_name, args=view.args, kwargs=view.kwargs)
        next_url = reverse('find_house_app:home')
        response = HttpResponseRedirect(next_url)
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
    else:
        response = HttpResponseRedirect('/')
    return response
# endregion
