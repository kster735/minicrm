from django.urls import path, re_path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('test/', views.test, name='test'),
    path('login', views.login, name='login'),
    re_path('logout', views.logout, name='logout'),
    path('users/<int:user_id>/', views.users, name='users'),
    path('users/<int:user_id>/users_insert_form/', views.users_insert_form, name='users_insert_form'),
    path('users/<int:user_id>/contacts/', views.contacts, name='contacts'),
    path('users/<int:user_id>/contacts/<int:viewuserid>', views.contacts, name='contacts_viewuserid'),
    path('users/<int:user_id>/contacts/<str:error>', views.contacts, name='contacts'),
    path('users/<int:user_id>/contacts/<int:viewuserid>/contacts_insert_form/', views.contacts_insert_form, name='contacts_insert_form'),
    path('users/<int:user_id>/contacts/<int:viewuserid>/contacts_insert_form/<str:error>', views.contacts_insert_form, name='contacts_insert_form'),
    path('users/<int:user_id>/contacts/<int:viewuserid>/contacts_insert_form/contact_store/', views.contact_store, name='contact_store'),
    path('users/<int:user_id>/messages/', views.messages, name='messages'),
    path('users/<int:user_id>/messages/messages_insert_form/', views.messages_insert_form, name='messages_insert_form'),
    path('users/<int:user_id>/messages/messages_insert_form/<str:error>', views.messages_insert_form, name='messages_insert_form'),
    path('users/<int:user_id>/messages/messages_insert_form/message_store/', views.message_store, name='message_store'),
]