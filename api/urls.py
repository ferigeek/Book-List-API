from django.urls import path
from .views import BookView

urlpatterns = [
    path('books/<int:bookId>', BookView.as_view(), name="Book-item"),
    path('books/', BookView.as_view(), name='book-list-create'),
]
