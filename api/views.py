from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.views import View
from django.forms.models import model_to_dict
from django.http import JsonResponse, QueryDict
from .models import Book

# Create your views here.

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
        request_body = QueryDict(request.body)

        try:
            title = request_body.get(request.body)
            author = request_body.get(request.body)
            price = request_body.get(request.body)

            new_book = Book(title, author, price, True)
            new_book.save()

            response = HttpResponse()
            response.status_code = 201
            return response('Success!')
        except:
            return HttpResponseBadRequest('Bad request!')
        
    def put(self, request, bookId):
        request_body = QueryDict(request.body)

        try:
            book = Book.objects.get(id=bookId)

            book.title = request_body.get('title')
            book.author = request_body.get('author')
            book.price = request_body.get('price')
            book.inventory = request_body.get('inventory')

            response = HttpResponse()
            response.status_code = 201
            return response('Success!')
        except:
            return HttpResponseBadRequest('Bad request!')
        
    def delete(self, request, bookId):
        try:
            Book.objects.filter(id=bookId).delete()

            return HttpResponse('Deletion success!')
        except:
            return HttpResponseBadRequest('Bad request!')