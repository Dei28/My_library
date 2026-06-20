# books/tests/test_favorite.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from books.models import Author, Book, UserBookRelation

User = get_user_model()

class FavoriteViewTest(TestCase):
    def setUp(self):
        """Создаём тестового пользователя, автора и книгу для проверки избранного"""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.author = Author.objects.create(name="Автор")
        self.book = Book.objects.create(title="Книга для избранного", author=self.author)

    def test_favorite_redirects_if_not_logged_in(self):
        """Проверяем, что неавторизованный пользователь при попытке добавить книгу в избранное перенаправляется на страницу входа"""
        response = self.client.post(f'/book/{self.book.id}/favorite/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_favorite_toggle_authenticated(self):
        """Проверяем, что авторизованный пользователь может добавить книгу в избранное и удалить её оттуда"""
        self.client.login(username="testuser", password="testpass")
        # Добавляем в избранное
        response = self.client.post(f'/book/{self.book.id}/favorite/', follow=True)
        self.assertEqual(response.status_code, 200)
        relation = UserBookRelation.objects.get(user=self.user, book=self.book)
        self.assertTrue(relation.is_favorite)   # поле is_favorite должно стать True

        # Убираем из избранного (повторный POST)
        response = self.client.post(f'/book/{self.book.id}/favorite/', follow=True)
        relation.refresh_from_db()
        self.assertFalse(relation.is_favorite)  # поле is_favorite должно стать False