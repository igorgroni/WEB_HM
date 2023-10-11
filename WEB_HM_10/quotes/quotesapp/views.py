from django.shortcuts import render, redirect, get_object_or_404
from .forms import AutorForm, QuoteForm
from .models import Author, Quote
from .utils import get_mongo_db

# Create your views here.


def main(request):
    # db = get_mongo_db()
    # quotes = db.quotes.find()
    quotes = Quote.objects.all()
    return render(request, 'quotesapp/index.html', {"quotes": quotes})


def author_page(request, author_id):
    author = Author.objects.get(pk=author_id)
    return render(request, 'author_page.html', {'author': author})


def autor(request):
    if request.method == 'POST':
        form = AutorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quotesapp:main')
        else:
            return render(request, 'quotesapp/author.html', {'form': form})

    return render(request, 'quotesapp/author.html', {'form': AutorForm()})


def quote(request):
    authors = Author.objects.all()

    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            new_quote = form.save()

            choice_authors = Author.objects.filter(
                name__in=request.POST.getlist('authors'))
            for author in choice_authors.iterator():
                new_quote.authors.add(author)

            return redirect(to='quotesapp:main')
        else:
            return render(request, 'quotesapp/quotes.html', {"authors": authors, 'form': form})

    return render(request, 'quotesapp/quotes.html', {"authors": authors, 'form': QuoteForm()})


def detail(request, quote_id):
    quote = get_object_or_404(Quote, pk=quote_id)
    return render(request, 'quotesapp/detail.html', {"quote": quote})


def set_done(request, quote_id):
    Quote.objects.filter(pk=quote_id).update(done=True)
    return redirect(to='quotesapp:main')


def delete_note(request, quote_id):
    Quote.objects.get(pk=quote_id).delete()
    return redirect(to='quotesapp:main')
