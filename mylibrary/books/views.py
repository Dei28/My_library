from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models import Q
from .models import Book, Author, UserBookRelation
from django.shortcuts import render
from .forms import ReviewForm
from django.db import models
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import BookProposalForm
from .models import BookProposal


class BookListView(ListView):
    model = Book
    template_name = 'books/book_list.html'
    context_object_name = 'books'
    paginate_by = 6
    ordering = ['-added_at'] 

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(author__name__icontains=query) |
                Q(genres__name__icontains=query)
            ).distinct()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        return context


class BookDetailView(DetailView):
    model = Book
    template_name = 'books/book_detail.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            relation = UserBookRelation.objects.filter(user=user, book=self.object).first()
            context['is_favorite'] = relation.is_favorite if relation else False
        else:
            context['is_favorite'] = False
        
        # Все отзывы (где review не пустой)
        reviews = self.object.user_relations.filter(review__isnull=False).exclude(review='')
        context['reviews'] = reviews
        
        # Средний рейтинг
        avg_rating = self.object.user_relations.filter(rating__isnull=False).aggregate(models.Avg('rating'))['rating__avg']
        context['avg_rating'] = round(avg_rating, 1) if avg_rating else None
        return context


class AuthorDetailView(DetailView):
    model = Author
    template_name = 'books/author_detail.html'
    context_object_name = 'author'


@login_required
def toggle_favorite(request, pk):
    book = get_object_or_404(Book, id=pk)
    relation, created = UserBookRelation.objects.get_or_create(
        user=request.user,
        book=book
    )
    relation.is_favorite = not relation.is_favorite
    relation.save()
    return redirect(reverse('book_detail', args=[pk]))

@login_required
def add_review(request, pk):
    book = get_object_or_404(Book, id=pk)
    relation, created = UserBookRelation.objects.get_or_create(user=request.user, book=book)

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=relation)
        if form.is_valid():
            form.save()
            return redirect('book_detail', pk=pk)
    else:
        form = ReviewForm(instance=relation)

    return render(request, 'books/review_form.html', {'form': form, 'book': book})


class ProposeBookView(LoginRequiredMixin, CreateView):
    model = BookProposal
    form_class = BookProposalForm
    template_name = 'books/propose_book.html'
    success_url = reverse_lazy('book_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        # Обработка новых жанров (пока просто сохраняем строку, позже админ разберётся)
        return super().form_valid(form)