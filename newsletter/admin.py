from django.contrib import admin

from newsletter.models import Client, Message, Newsletter, Logs


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'text',)


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('start_date', 'end_date', 'status', 'owner',)


admin.site.register(Logs)
