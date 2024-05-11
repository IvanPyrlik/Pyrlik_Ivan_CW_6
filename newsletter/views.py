from random import random

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from blog.models import Blog
from newsletter.forms import ClientForm, MessageForm, NewsletterForm, NewsletterModeratorForm
from newsletter.models import Client, Newsletter, Message


class HomeListView(ListView):

    model = Newsletter
    template_name = 'newsletter/home_list.html'

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['count_newsletter'] = len(Newsletter.objects.all())
        context_data['active_newsletter'] = len(Newsletter.objects.filter(status='started'))
        blog_list = list(Blog.objects.all())
        random.shuffle(blog_list)
        context_data['blog_list'] = blog_list[:3]
        context_data['client'] = len(Client.objects.all())
        return context_data


class ClientListView(LoginRequiredMixin, ListView):

    model = Client
    template_name = 'newsletter/client_list.html'


class ClientCreateView(LoginRequiredMixin, CreateView):

    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('newsletter:client_list')

    login_url = reverse_lazy('users:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление клиента'
        return context

    def form_valid(self, form, *args, **kwargs):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class ClientDetailView(LoginRequiredMixin, DetailView):

    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('newsletter:client_list')

    login_url = reverse_lazy('users:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Информация о клиенте'
        return context


class ClientUpdateView(LoginRequiredMixin, UpdateView):

    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('newsletter:client_list')

    def get_success_url(self):
        from django.urls import reverse
        return reverse('newsletter:client_detail', args=[self.kwargs.get('pk')])

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_staff:
            raise Http404("Вы не являетесь владельцем!")
        return self.object


class ClientDeleteView(LoginRequiredMixin, DeleteView):

    model = Client
    success_url = reverse_lazy('newsletter:client_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_staff:
            raise Http404("Вы не являетесь владельцем!")
        return self.object


class MessageListView(LoginRequiredMixin, ListView):

    model = Message
    form_class = MessageForm
    template_name = 'newsletter/message_list.html'


class MessageCreateView(LoginRequiredMixin, CreateView):

    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('newsletter:message_list')

    login_url = reverse_lazy('users:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание рассылок'
        return context

    def form_valid(self, form, *args, **kwargs):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class MessageDetailView(LoginRequiredMixin, DetailView):

    model = Message

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Информация о письме'
        return context


class MessageUpdateView(LoginRequiredMixin, UpdateView):

    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('newsletter:message_list')

    def get_success_url(self):
        from django.urls import reverse
        return reverse('newsletter:message_detail', args=[self.kwargs.get('pk')])

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_staff:
            raise Http404("Вы не являетесь владельцем!")
        return self.object


class MessageDeleteView(LoginRequiredMixin, DeleteView):

    model = Message
    success_url = reverse_lazy('newsletter:message_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_staff:
            raise Http404("Вы не являетесь владельцем!")
        return self.object


class NewsletterListView(LoginRequiredMixin,ListView):

    model = Newsletter
    template_name = 'newsletter/newsletter_list.html'


class NewsletterCreateView(LoginRequiredMixin, CreateView):

    model = Newsletter
    form_class = NewsletterForm
    success_url = reverse_lazy('newsletter:newsletter_list')

    login_url = reverse_lazy('users:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание рассылок'
        return context

    def form_valid(self, form, *args, **kwargs):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class NewsletterDetailView(LoginRequiredMixin, DetailView):

    model = Newsletter
    form_class = NewsletterForm
    success_url = reverse_lazy('newsletter:newsletter_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Информация о рассылках'
        return context


class NewsletterUpdateView(LoginRequiredMixin, UpdateView):

    model = Newsletter
    form_class = NewsletterForm
    success_url = reverse_lazy('newsletter:newsletter_list')

    login_url = reverse_lazy('users:login')

    def get_success_url(self):
        from django.urls import reverse
        return reverse('newsletter:newsletter_detail', args=[self.kwargs.get('pk')])

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"request": self.request})
        return kwargs

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_staff:
            raise Http404("Вы не являетесь владельцем!")
        return self.object

    def test_func(self):
        user = self.request.user
        instance: Newsletter = self.get_object()
        custom_perms: tuple = (
            'client.set_is_activated',
        )

        if user == instance.owner:
            return True
        elif user.groups.filter(name='moderator') and user.has_perms(custom_perms):
            return True
        return self.handle_no_permission()


class NewsletterDeleteView(LoginRequiredMixin, DeleteView):

    model = Newsletter
    success_url = reverse_lazy('newsletter:newsletter_list')

    login_url = reverse_lazy('users:login')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_staff:
            raise Http404("Вы не являетесь владельцем!")
        return self.object


class NewsletterModeratorUpdateView(LoginRequiredMixin, UpdateView):
    model = Newsletter
    form_class = NewsletterModeratorForm
    success_url = reverse_lazy('newsletter:newsletter_list')
    permission_required = 'newsletter.set_is_activated'

