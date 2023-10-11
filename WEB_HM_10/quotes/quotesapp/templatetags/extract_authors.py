from django import template

register = template.Library()


def authors(quote_authors):
    return ', '.join([str(name) for name in quote_authors.all()])


register.filter('authors', authors)
