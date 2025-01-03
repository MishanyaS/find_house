from django.shortcuts import render, redirect, get_object_or_404
from .models import Chat, Message
from .forms import MessageForm
from users_app.models import CustomUser
from admin_panel_app.models import Content


# region Chat views
def create_or_get_chat(request, other_user_id):
    other_user = get_object_or_404(CustomUser, id=other_user_id)
    chat = Chat.objects.filter(participants=request.user).filter(participants=other_user).first()
    
    if not chat:
        chat = Chat.objects.create()
        chat.participants.add(request.user, other_user)
        
    return redirect('chat_app:chat_read', chat_id=chat.id)

def delete_chat(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    chat.delete()
    
    return redirect('chat_app:chat_list')

def chat_list(request):
    context = {}
    
    if request.user.is_authenticated and hasattr(request.user, 'profile'):
        context['user_profile'] = request.user.profile
    
    context['chats'] = request.user.chats.all()
    context['content'] = Content.objects.order_by('-change_date').first()
    
    return render(request, 'chat_app/chat/chat_list.html', context)

def chat_read(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            message = Message.objects.create(chat=chat, sender=request.user, content=content)
            
            return redirect('chat_app:chat_read', chat_id=chat_id)
    else:
        form = MessageForm()

    if request.method == 'POST' and 'chat_app:edit_message' in request.POST:
        message_id = request.POST.get('message_id')
        message = get_object_or_404(Message, id=message_id)
        form = MessageForm(request.POST, instance=message)
        if form.is_valid():
            form.save()
            
            return redirect('chat_app:chat_read', chat_id=chat_id)

    if request.method == 'POST' and 'delete_message' in request.POST:
        message_id = request.POST.get('message_id')
        message = get_object_or_404(Message, id=message_id)
        message.is_deleted = True
        message.save()
        
        return redirect('chat_app:chat_read', chat_id=chat_id)
    
    context = {}
    
    if request.user.is_authenticated and hasattr(request.user, 'profile'):
        context['user_profile'] = request.user.profile
    
    context['chat'] = chat
    context['form'] = form
    context['content'] = Content.objects.order_by('-change_date').first()
    
    return render(request, 'chat_app/chat/chat_read.html', context)

def edit_message(request, chat_id, message_id):
    message = get_object_or_404(Message, id=message_id)
    chat = get_object_or_404(Chat, id=chat_id)
    
    if request.method == 'POST':
        form = MessageForm(request.POST, instance=message)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.sender = request.user
            instance.save()
            
            return redirect('chat_app:chat_read', chat_id=chat_id)
    else:
        form = MessageForm(instance=message)
        
    context = {}
    
    if request.user.is_authenticated and hasattr(request.user, 'profile'):
        context['user_profile'] = request.user.profile
    
    context['chat'] = chat
    context['form'] = form
    context['content'] = Content.objects.order_by('-change_date').first()
    
    return render(request, 'chat_app/chat/chat_read.html', context)
# endregion
