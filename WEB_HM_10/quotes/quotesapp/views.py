from django.shortcuts import render
from .forms import AutorForm, QuoteForm
from .models import Author

# Create your views here.


def main(request):
    return render(request, 'quotesapp/index.html')


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
            for tag in choice_authors.iterator():
                new_quote.authors.add(tag)

            return redirect(to='quotesapp:main')
        else:
            return render(request, 'quotesapp/quotes.html', {"authors": authors, 'form': form})

    return render(request, 'quotesapp/quotes.html', {"authors": authors, 'form': QuoteForm()})
