from django.contrib import admin
from .models import Author, Genre, Book, UserBookRelation
from .models import BookProposal

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'birth_date')
    search_fields = ('name',)

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year', 'read_link')
    list_filter = ('author', 'genres')
    filter_horizontal = ('genres',)
    search_fields = ('title', 'author__name', 'read_link')
    # fieldsets использовать не обязательно, но можно для красоты

@admin.register(UserBookRelation)
class UserBookRelationAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'is_favorite', 'rating')
    list_filter = ('is_favorite', 'rating')

@admin.register(BookProposal)
class BookProposalAdmin(admin.ModelAdmin):
    list_display = ('title', 'author_name', 'user', 'status', 'created_at')
    list_filter = ('status', 'user')
    search_fields = ('title', 'author_name', 'user__username')
    actions = ['approve_proposals', 'reject_proposals']
    readonly_fields = ('user', 'created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('user', 'title', 'author_name', 'description', 'publication_year', 'cover', 'read_link')
        }),
        ('Жанры', {
            'fields': ('genres', 'new_genres')
        }),
        ('Статус', {
            'fields': ('status', 'rejection_reason')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    def approve_proposals(self, request, queryset):
        for proposal in queryset:
            # Автор: ищем или создаём
            author, _ = Author.objects.get_or_create(name=proposal.author_name)
            # Жанры: существующие + новые
            genres = list(proposal.genres.all())
            if proposal.new_genres:
                for genre_name in proposal.new_genres.split(','):
                    genre_name = genre_name.strip()
                    if genre_name:
                        genre, _ = Genre.objects.get_or_create(name=genre_name)
                        genres.append(genre)
            # Создаём книгу
            book = Book.objects.create(
                title=proposal.title,
                author=author,
                description=proposal.description,
                publication_year=proposal.publication_year,
                cover=proposal.cover,
                read_link=proposal.read_link,
            )
            book.genres.set(genres)
            proposal.status = 'approved'
            proposal.save()
        self.message_user(request, f"Одобрено {queryset.count()} предложений.")
    approve_proposals.short_description = "Одобрить выбранные предложения"

    def reject_proposals(self, request, queryset):
        queryset.update(status='rejected')
        self.message_user(request, f"Отклонено {queryset.count()} предложений.")
    reject_proposals.short_description = "Отклонить выбранные предложения"