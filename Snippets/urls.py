from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from MainApp import views
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index_page, name="index"),
    path('snippets/add', views.add_snippet_page, name="add-snippet"),
    path('snippets/list', views.snippets_page, name="snippets"),
    path('snippet/<int:snippet_id>', views.snippet_page, name='one-snippet'),
    path('snippet/<int:snippet_id>/edit', views.edit_snippet, name='edit'),
    path('snippet/<int:snippet_id>/delete', views.delete_snippet, name='delete'),
    #path('snippet/create', views.create_snippet, name='create')
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('mysnippets', views.my_snippets, name='my-snippets'),
    path('register', views.user_register, name='register'),
    path('comment/add', views.add_comment, name="comment-add")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
