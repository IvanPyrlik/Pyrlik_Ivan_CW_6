# Pyrlik_Ivan_CW_6
# Разработка сервиса
## Описание задач

1. Реализуйте интерфейс заполнения рассылок, то есть CRUD-механизм для управления рассылками.
2. Реализуйте скрипт рассылки, который работает как из командой строки, так и по расписанию.
3. Добавьте настройки конфигурации для периодического запуска задачи.

## Сущности системы
* Клиент сервиса:
1. контактный email,
2. ФИО,
3. комментарий.
* Рассылка (настройки):
1. время рассылки;
2. периодичность: раз в день, раз в неделю, раз в месяц;
3. статус рассылки: завершена, создана, запущена.
* Сообщение для рассылки:
1. тема письма,
2. тело письма.
* Логи рассылки:
1. дата и время последней попытки;
2. статус попытки;
3. ответ почтового сервера, если он был.

## Логика работы системы
* После создания новой рассылки, если текущее время больше времени начала и меньше времени окончания, то должны быть выбраны из справочника все клиенты, которые указаны в настройках рассылки, и запущена отправка для всех этих клиентов.
* Если создается рассылка со временем старта в будущем, то отправка должна стартовать автоматически по наступлению этого времени без дополнительных действий со стороны пользователя системы.
* По ходу отправки сообщений должна собираться статистика по каждому сообщению для последующего формирования отчетов.
* Внешний сервис, который принимает отправляемые сообщения, может долго обрабатывать запрос, отвечать некорректными данными, на какое-то время вообще не принимать запросы. Нужна корректная обработка подобных ошибок. Проблемы с внешним сервисом не должны влиять на стабильность работы разрабатываемого сервиса рассылок.

# Доработка сервиса

## Описание задач
1. Расширьте модель пользователя для регистрации по почте, а также верификации.
2. Добавьте интерфейс для входа, регистрации и подтверждения почтового ящика.
3. Реализуйте ограничение доступа к рассылкам для разных пользователей.
4. Реализуйте интерфейс менеджера.
5. Создайте блог для продвижения сервиса.

## Функционал менеджера
* Может просматривать любые рассылки.
* Может просматривать список пользователей сервиса.
* Может блокировать пользователей сервиса.
* Может отключать рассылки.
* Не может редактировать рассылки.
* Не может управлять списком рассылок.
* Не может изменять рассылки и сообщения.

## Функционал пользователя
Весь функционал дублируется из первой части курсовой работы. Но теперь нужно следить за тем, чтобы пользователь не мог случайным образом изменить чужую рассылку и мог работать только со своим списком клиентов и со своим списком рассылок.

### Продвижение
### Блог

Реализуйте приложение для ведения блога. При этом отдельный интерфейс реализовывать не требуется, но необходимо настроить административную панель для контент-менеджера.

В сущность блога добавьте следующие поля:

* заголовок,
* содержимое статьи,
* изображение,
* количество просмотров,
* дата публикации.
## Главная страница

Реализуйте главную страницу в произвольном формате, но обязательно отобразите следующую информацию:

* количество рассылок всего,
* количество активных рассылок,
* количество уникальных клиентов для рассылок,
* 3 случайные статьи из блога.

## Кеширование

Для блога и главной страницы самостоятельно выберите, какие данные необходимо кешировать, а также каким способом необходимо произвести кеширование.