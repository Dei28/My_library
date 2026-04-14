from django import forms
from .models import UserBookRelation, BookProposal, Genre

class ReviewForm(forms.ModelForm):
    class Meta:
        model = UserBookRelation
        fields = ['rating', 'review']
        widgets = {
            'rating': forms.Select(choices=[(None, 'Без оценки')] + [(i, i) for i in range(1, 6)], attrs={'class': 'form-select'}),
            'review': forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'Ваш отзыв...'}),
        }

class BookProposalForm(forms.ModelForm):
    class Meta:
        model = BookProposal
        fields = ['title', 'author_name', 'genres', 'new_genres', 'description', 'publication_year', 'cover', 'read_link']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'genres': forms.SelectMultiple(attrs={'size': 5}),
        }