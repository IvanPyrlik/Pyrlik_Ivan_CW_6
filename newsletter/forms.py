from django import forms

from newsletter.models import Client, Message, Newsletter


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, forms.BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class ClientForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Client
        fields = '__all__'


class MessageForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Message
        fields = '__all__'


class NewsletterForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Newsletter
        fields = '__all__'


class NewsletterModeratorForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Newsletter
        fields = ('is_activated',)
