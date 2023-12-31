from django.urls import path
from . import views

app_name = 'quotesapp'

urlpatterns = [
    path('', views.main, name='main'),
    path('quote/', views.quote, name='quote'),
    path('author/', views.autor, name='author'),
    path('authorspage/', views.author_page, name='authors_page'),
    path('quotesspage/', views.quotes_page, name='quotes_page'),
    path('detail/<int:quote_id>', views.detail, name='detail'),
    path('done/<int:quote_id>', views.set_done, name='set_done'),
    path('delete/<int:quote_id>', views.delete_note, name='delete'),
]
