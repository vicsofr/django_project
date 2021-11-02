# django_project

<p><b>Описание:</b></p>
<p>Это блог, в котором можно создавать или читать посты. В блоге реализована древовидная система комментариев. Имеет API для работы с данными.</p>
<p>Запуск: загрузить в свой IDE, установить зависимости из requirements.txt, runserver</p>
<p>superuser</p>
<p>login: admin</p>
<p>password: 12131415</p>

<p>API:</p>
<p>/api/token/ POST, в теле указать "login": и "password"</p>
<p>/api/refresh_token/ </p>
<p>/api/posts GET все посты</p>
<p>/api/posts/<post_id> GET поста по ID</p>
<p>/api/tags/top GET топ 10 тегов</p>
<p>/api/tags/<slug:tag_slug> GET постов по тегам</p>
<p>/api/register/ POST регистрация</p>
<p>/api/profile GET профиль</p>
<p>/api/logout/ POST выход</p>
<p>/api/comments GET все комменты</p>
<p>/api/comments/<slug:post_slug> GET комментов к посту</p>
