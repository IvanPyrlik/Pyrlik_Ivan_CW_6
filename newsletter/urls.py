from django.urls import path
from django.views.decorators.cache import cache_page

from newsletter.apps import NewsletterConfig
from newsletter.views import ClientListView, HomeListView, ClientCreateView, ClientDetailView, ClientUpdateView, \
    ClientDeleteView, MessageListView, MessageCreateView, MessageDetailView, MessageUpdateView, MessageDeleteView, \
    NewsletterListView, NewsletterCreateView, NewsletterDetailView, NewsletterUpdateView, NewsletterDeleteView, \
    NewsletterModeratorUpdateView

app_name = NewsletterConfig.name

urlpatterns = [
    path('home/', cache_page(60)(HomeListView.as_view()), name='home'),
    path('', ClientListView.as_view(), name='client_list'),
    path('create/', ClientCreateView.as_view(), name='client_create'),
    path('newletter/<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
    path('update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    path('delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),
    path('message/', MessageListView.as_view(), name='message_list'),
    path('newletter/message_create/', MessageCreateView.as_view(), name='message_create'),
    path('newletter/message_detail/<int:pk>/', MessageDetailView.as_view(), name='message_detail'),
    path('newletter/message_update/<int:pk>/', MessageUpdateView.as_view(), name='message_update'),
    path('newletter/message_delete/<int:pk>/', MessageDeleteView.as_view(), name='message_delete'),
    path('newsletter/', NewsletterListView.as_view(), name='newsletter_list'),
    path('newletter/newsletter_create/', NewsletterCreateView.as_view(), name='newsletter_create'),
    path('newletter/newsletter_detail/<int:pk>/', NewsletterDetailView.as_view(), name='newsletter_detail'),
    path('newletter/newsletter_update/<int:pk>/', NewsletterUpdateView.as_view(), name='newsletter_update'),
    path('newletter/newsletter_delete/<int:pk>/', NewsletterDeleteView.as_view(), name='newsletter_delete'),
    path('newsletter_moder_edit/<int:pk>/', NewsletterModeratorUpdateView.as_view(), name='newsletter_moder_edit'),
]
