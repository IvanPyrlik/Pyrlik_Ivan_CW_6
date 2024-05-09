from django.conf import settings
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    """
    Модель клиента.
    """
    email = models.EmailField(unique=True, verbose_name='Почта')
    full_name = models.CharField(max_length=100, verbose_name='ФИО')
    comment = models.CharField(max_length=200, verbose_name='Комментарий', **NULLABLE)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Владелец', **NULLABLE)

    def __str__(self):
        return f'{self.full_name}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        ordering = ('full_name',)


class Message(models.Model):
    """
    Модель сообщения рассылки.
    """
    subject = models.CharField(max_length=100, default='Без темы', verbose_name='Тема письма')
    text = models.TextField(verbose_name='Содержание')

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Владелец', **NULLABLE)

    def __str__(self):
        return f'{self.subject}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ('subject',)


class Newsletter(models.Model):
    """
    Модель рассылки.
    """
    PERIOD_D = 'daily'
    PERIOD_W = 'weekly'
    PERIOD_M = 'monthly'

    PERIODS = (
        (PERIOD_D, 'Раз в день'),
        (PERIOD_W, 'Раз в неделю'),
        (PERIOD_M, 'Раз в месяц'),
    )

    STATUS_ST = 'started'
    STATUS_CR = 'created'
    STATUS_COMP = 'completed'

    STATUSES = (
        (STATUS_ST, 'Запущена'),
        (STATUS_CR, 'Создана'),
        (STATUS_COMP, 'Завершена'),
    )

    start_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата начала рассылки')
    end_date = models.DateTimeField(auto_now=True, verbose_name='Дата окончания рассылки')
    period = models.CharField(max_length=20, choices=PERIODS, default=PERIOD_D, verbose_name='Периодичность')
    status = models.CharField(max_length=20, choices=STATUSES, default=STATUS_CR, verbose_name='Статус')

    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='Сообщение', **NULLABLE)
    client = models.ManyToManyField(Client, verbose_name='Клиент')

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Владелец', **NULLABLE)

    is_activated = models.BooleanField(default=True)

    def __str__(self):
        return f'Начало рассылки - {self.start_date}, окончание - {self.end_date}, статус - {self.status}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        ordering = ('status',)

        permissions = [
            ('set_is_activated', 'Can change status')
        ]


class Logs(models.Model):
    """
    Модель логи.
    """
    STATUS_SUC = 'successfully'
    STATUS_ER = 'error'

    STATUSES = (
        (STATUS_SUC, 'Успешно'),
        (STATUS_ER, 'Ошибка'),
    )

    last = models.DateTimeField(auto_now_add=True, verbose_name='Дата последней попытки')
    status = models.CharField(choices=STATUSES, default=STATUS_SUC, verbose_name='Статус')

    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Клиент', **NULLABLE)
    newsletter = models.ForeignKey(Newsletter, on_delete=models.CASCADE, verbose_name='Рассылка', **NULLABLE)

    def __str__(self):
        return f'Дата попытки {self.last}, статус - {self.status}'

    class Meta:
        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'
        ordering = ('status',)
