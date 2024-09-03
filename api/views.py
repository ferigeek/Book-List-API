from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.views import View
from django.forms.models import model_to_dict
from django.http import JsonResponse, QueryDict
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Book

# Create your views here.

@method_decorator(csrf_exempt, name='dispatch')
class BookView(View):

    def get(self, request, bookId=None):
        if bookId:
            try:
                book = Book.objects.get(id=bookId)
                if not book:
                    return HttpResponseNotFound('Book not found!')
                
                return JsonResponse(model_to_dict(book))
            except:
                return HttpResponseBadRequest()
        else:
            books = Book.objects.all()
            if books:
                books_list = list(books.values())
                return JsonResponse(books_list,safe=False)
            else:
                return HttpResponseNotFound('No books found!')

    def post(self, request):
        try:
            title = request.POST.get('title')
            author = request.POST.get('author')
            price = request.POST.get('price')

            new_book = Book(title=title, author=author, price=price, inventory=True)
            new_book.save()

            response = HttpResponse('Successfully created!')
            response.status_code = 201
            return response
        except:
            return HttpResponseBadRequest('Bad request!')
    
    def put(self, request, bookId):
        request_body = QueryDict(request.body)

        try:
            book = Book.objects.get(id=bookId)

            title = request_body.get('title')
            author = request_body.get('author')
            price = request_body.get('price')
            inventory = request_body.get('inventory')

            if title:
                book.title = title
            if author:
                book.author = author
            if price:
                book.price = price
            if inventory:
                book.inventory = inventory

            book.save()

            response = HttpResponse('Successfully updated!')
            response.status_code = 201
            return response
        except:
            return HttpResponseBadRequest('Bad request!')
        
    def delete(self, request, bookId):
        try:
            Book.objects.filter(id=bookId).delete()

            return HttpResponse('Deletion success!')
        except:
            return HttpResponseBadRequest('Bad request!')