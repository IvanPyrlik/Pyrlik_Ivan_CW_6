import datetime

from django.conf import settings
from django.core.mail import send_mail

from newsletter.models import Logs, Newsletter


def _send(newsletter, message_client):
    result = send_mail(
        subject=newsletter.message.subject,
        message=newsletter.message.text,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[message_client.email],
        fail_silently=False
    )

    Logs.objects.create(
        status=Logs.STATUS_SUC if result else Logs.STATUS_ER,
        settings=newsletter,
        client_id=message_client.pk
    )


def send_mails():
    datetime_now = datetime.datetime.now(datetime.timezone.utc)
    for newsletter in Newsletter.objects.filter(status=Newsletter.STATUS_ST):
        if (datetime_now > newsletter.start_date) and (datetime_now < newsletter.end_date):
            for newsletter_client in newsletter.client.all():
                logs = Logs.objects.filter(
                    client=newsletter_client.pk,
                    settings=newsletter
                )
                if logs.exists():
                    date_last_attempt = logs.order_by('-last').first()

                    if newsletter.period == Newsletter.PERIOD_D:
                        if (datetime_now - date_last_attempt).days >= 1:
                            _send(newsletter, newsletter_client)
                    elif newsletter.period == Newsletter.PERIOD_W:
                        if (datetime_now - date_last_attempt).days >= 7:
                            _send(newsletter, newsletter_client)
                    elif newsletter.period == Newsletter.PERIOD_M:
                        if (datetime_now - date_last_attempt).days >= 30:
                            _send(newsletter, newsletter_client)
                else:
                    _send(newsletter, newsletter_client)
