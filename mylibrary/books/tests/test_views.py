# books/tests/test_views.py
from django.test import TestCase
from books.models import Author, Book

class BookListViewTest(TestCase):
    def setUp(self):
        """Создаём тестового автора и книгу для проверки главной страницы"""
        self.author = Author.objects.create(name="Тестовый автор")
        self.book = Book.objects.create(
            title="Тестовая книга",
            author=self.author,
            description="Описание"
        )

    def test_home_page_status(self):
        """Проверяем, что главная страница возвращает статус 200 и использует правильный шаблон"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/book_list.html')

    def test_home_page_contains_book(self):
        """Проверяем, что на главной странице отображается название тестовой книги"""
        response = self.client.get('/')
        self.assertContains(response, "Тестовая книга")

class BookDetailViewTest(TestCase):
    def setUp(self):
        """Создаём тестового автора и книгу для детальной страницы"""
        self.author = Author.objects.create(name="Автор")
        self.book = Book.objects.create(
            title="Детальная книга",
            author=self.author,
            description="Описание"
        )

    def test_detail_page_status(self):
        """Проверяем, что страница книги открывается со статусом 200, использует правильный шаблон и содержит название книги"""
        response = self.client.get(f'/book/{self.book.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/book_detail.html')
        self.assertContains(response, "Детальная книга")

    def test_detail_page_context(self):
        """Проверяем, что в контекст страницы передаётся объект книги и флаг is_favorite = False для неавторизованного пользователя"""
        response = self.client.get(f'/book/{self.book.id}/')
        self.assertEqual(response.context['book'].title, "Детальная книга")
        self.assertFalse(response.context['is_favorite'])

class AuthorDetailViewTest(TestCase):
    def setUp(self):
        """Создаём тестового автора и его книгу"""
        self.author = Author.objects.create(name="Пушкин", bio="Поэт")
        self.book = Book.objects.create(title="Сказки", author=self.author)

    def test_author_page_status(self):
        """Проверяем, что страница автора открывается (200), использует правильный шаблон, содержит имя автора и его книгу"""
        response = self.client.get(f'/author/{self.author.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/author_detail.html')
        self.assertContains(response, "Пушкин")
        self.assertContains(response, "Сказки")