from django.urls import path

from . import views

urlpatterns = [
    path('', views.Home.as_view()),
    path(r'contact_form/', views.ContactForm.as_view(), name='contact_form'),
    path(r'<str:category>/', views.Category.as_view(), name='category'),
    path(r'<str:category>/content/<int:content_id>/', views.Content.as_view(), name='content'),
    path(r'cms_howto/', views.Content.as_view(), name='cms_howto'),
]
