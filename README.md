# django_project

Описание:
Это блог, в котором можно создавать или читать посты. В блоге реализована древовидная система комментариев. Имеет API для работы с данными.
Запуск: загрузить в свой IDE, установить зависимости из requirements.txt, runserver
superuser
login: admin
password: 12131415

API:
/api/token/ POST, в теле указать "login": и "password"
/api/refresh_token/ 
/api/posts GET все посты
/api/posts/<post_id> GET поста по ID
/api/tags/top GET топ 10 тегов
/api/tags/<slug:tag_slug> GET постов по тегам
/api/register/ POST регистрация
/api/profile GET профиль
/api/logout/ POST выход
/api/comments GET все комменты
/api/comments/<slug:post_slug> GET комментов к посту
