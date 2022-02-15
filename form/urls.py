from django.urls import path

from .views import register, auth, signin, logout_view, chat, ChatListView, ChatDetailView, chat_detail, ChatUpdateView, chat_update

app_name = 'accounts'

urlpatterns = [
    path('', auth, name='auth'),
    #Auth endpoint
    path('register', register, name='register'),
    path('signin', signin, name='login'),
    # Authenticated endpoints
    path('auth', auth, name='auth'),
    path('logout', logout_view, name='logout'),
    path('chat', chat, name='chat'),
    path('chat2', ChatListView.as_view(), name='chat2'),
    path('chat-detail/<slug:slug>', chat_detail, name='chat-detail'),
    path('chat-detail/<slug:slug>/update', chat_update, name='chat-detail-update'),
    # class based chat_detail
    path('chat-detail2/<slug:slug>/update', ChatUpdateView.as_view(), name='chat-detail-update2'),
    path('chat-detail2/<slug:slug>', ChatDetailView.as_view(), name='chat-detail2')
]