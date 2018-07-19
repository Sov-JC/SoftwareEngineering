from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from database.models import BOOK, COMMENT, BOOK_RATING, AUTHOR

# Create your views here.

def index(request):
    template = loader.get_template('BookDetails/book_details.html')
    if request.method=='GET':
        book = request.GET.get('book')
    if not book:
        book = "9780261103283"
    

    book = BOOK.objects.get(ISBN=str(book))
    comments = COMMENT.objects.filter(ISBN = book)

    rating = BOOK_RATING.objects.get(ISBN = book)
    
    total_ratings = (float(rating.One_star_count) + float(rating.Two_star_count) + float(rating.Three_star_count) + float(rating.Four_star_count) + float(rating.Five_star_count))
    if not total_ratings == 0:
        average_rating = ((float(rating.One_star_count)/total_ratings) * 1.0 )+ ((float(rating.Two_star_count)/total_ratings)* 2.0 )+((float(rating.Three_star_count)/total_ratings) * 3.0 )+((float(rating.Four_star_count) / total_ratings)* 4.0 )+((float(rating.Five_star_count)/total_ratings) * 5.0 )
    else:
        average_rating = 0

    # If no book found, set book found render an error

    context = { 'book':book, 'comments':comments, 'rating': int(round(average_rating)), }
    

    return HttpResponse(template.render(context, request))


def books_by_author(request):

    template = loader.get_template('BookDetails/books_by_author.html')
    author = None
    if request.method=='GET':
        author = request.GET.get('author')
        author = AUTHOR.objects.get(AuthorID=author)
        # if not author: reteurn an error

    books = BOOK.objects.filter(AuthorID = author)
    
    context = { 'author':author, 'books':books, }
    
    return HttpResponse(template.render(context, request))

