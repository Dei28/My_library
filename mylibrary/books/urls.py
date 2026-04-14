from django.urls import path
from . import views

urlpatterns = [
    path('', views.BookListView.as_view(), name='book_list'),
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),
    path('author/<int:pk>/', views.AuthorDetailView.as_view(), name='author_detail'),
    path('book/<int:pk>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('book/<int:pk>/review/', views.add_review, name='add_review'),
    path('propose/', views.ProposeBookView.as_view(), name='propose_book'),
]