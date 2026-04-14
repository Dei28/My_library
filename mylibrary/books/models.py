from django.db import models
from django.conf import settings
from urllib.parse import quote_plus
from django.contrib.auth import get_user_model

User = get_user_model()

class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    genres = models.ManyToManyField(Genre, related_name='books')
    description = models.TextField()
    publication_year = models.IntegerField(null=True, blank=True)
    cover = models.ImageField(upload_to='covers/', blank=True, null=True)
    added_at = models.DateTimeField(auto_now_add=True)
    read_link = models.URLField(max_length=500, blank=True, null=True)  # если добавили ранее

    def __str__(self):
        return self.title

    def get_google_books_search_url(self):
        query = f"{self.title} {self.author.name}"
        encoded_query = quote_plus(query)
        return settings.EXTERNAL_BOOK_SEARCH_URL + encoded_query

class UserBookRelation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='book_relations')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='user_relations')
    is_favorite = models.BooleanField(default=False)
    rating = models.PositiveSmallIntegerField(null=True, blank=True)  # 1-5
    review = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'book')


class BookProposal(models.Model):
    STATUS_CHOICES = (
        ('pending', 'На модерации'),
        ('approved', 'Одобрено'),
        ('rejected', 'Отклонено'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='book_proposals')
    title = models.CharField(max_length=200)
    author_name = models.CharField(max_length=100, verbose_name="Автор")
    genres = models.ManyToManyField(Genre, blank=True, verbose_name="Жанры (выберите из списка)")
    new_genres = models.CharField(max_length=255, blank=True, verbose_name="Или укажите новые жанры через запятую")
    description = models.TextField()
    publication_year = models.IntegerField(null=True, blank=True)
    cover = models.ImageField(upload_to='proposals/', blank=True, null=True)
    read_link = models.URLField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    rejection_reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} (предложил {self.user.username})"