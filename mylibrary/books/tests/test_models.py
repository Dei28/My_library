# books/tests/test_models.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from books.models import Author, Genre, Book, UserBookRelation

User = get_user_model()

class AuthorModelTest(TestCase):
    def setUp(self):
        """Создаём тестового автора"""
        self.author = Author.objects.create(
            name="Лев Толстой",
            bio="Великий русский писатель",
            birth_date="1828-09-09"
        )

    def test_author_str(self):
        """Проверяем, что строковое представление автора — это его имя"""
        self.assertEqual(str(self.author), "Лев Толстой")

class GenreModelTest(TestCase):
    def setUp(self):
        """Создаём тестовый жанр"""
        self.genre = Genre.objects.create(name="Роман")

    def test_genre_str(self):
        """Проверяем, что строковое представление жанра — это его название"""
        self.assertEqual(str(self.genre), "Роман")

class BookModelTest(TestCase):
    def setUp(self):
        """Создаём тестового автора, жанр и книгу, связываем жанр с книгой"""
        self.author = Author.objects.create(name="Лев Толстой")
        self.genre = Genre.objects.create(name="Роман")
        self.book = Book.objects.create(
            title="Война и мир",
            author=self.author,
            description="Эпопея",
            publication_year=1869
        )
        self.book.genres.add(self.genre)

    def test_book_str(self):
        """Проверяем строковое представление книги — это её название"""
        self.assertEqual(str(self.book), "Война и мир")

    def test_google_search_url(self):
        """Проверяем, что метод get_google_books_search_url формирует правильный URL для поиска в Google Books"""
        url = self.book.get_google_books_search_url()
        self.assertTrue(url.startswith('https://www.google.com/search?tbm=bks&q='))

    def test_book_author_relation(self):
        """Проверяем связь книги с автором (Foreign Key)"""
        self.assertEqual(self.book.author.name, "Лев Толстой")

    def test_book_genres_relation(self):
        """Проверяем связь многие-ко-многим: добавленный жанр присутствует в списке жанров книги"""
        self.assertIn(self.genre, self.book.genres.all())

class UserBookRelationTest(TestCase):
    def setUp(self):
        """Создаём тестового пользователя, автора, книгу и связь избранного/отзыва"""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.author = Author.objects.create(name="Автор")
        self.book = Book.objects.create(title="Книга", author=self.author)
        self.relation = UserBookRelation.objects.create(
            user=self.user,
            book=self.book,
            is_favorite=True,
            rating=5,
            review="Отлично!"
        )

    def test_relation_fields(self):
        """Проверяем, что все поля связи UserBookRelation сохраняются корректно"""
        self.assertEqual(self.relation.user.username, "testuser")
        self.assertEqual(self.relation.book.title, "Книга")
        self.assertTrue(self.relation.is_favorite)
        self.assertEqual(self.relation.rating, 5)