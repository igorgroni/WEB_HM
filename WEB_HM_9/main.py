from models import Author, Quote
import connect


def main():

    while True:

        command = input("Enter command: ").strip().split(':')

        if command[0] == 'name':
            author_name = command[1].strip()
            author = Author.objects(fullname=author_name).first()
            if author:
                quotes = Quote.objects(author=author)
                for quote in quotes:
                    print(quote.quote)
            else:
                print(f"Author {author_name} not found")

        elif command[0] == 'tag':
            tag = command[1]
            quotes = Quote.objects(tags=tag)
            for quote in quotes:
                print(quote.quote)

        elif command[0] == 'tags':
            tags = command[1].split(',')
            quotes = Quote.objects(tags__in=tags)
            for quote in quotes:
                print(quote.quote)

        elif command[0] == 'exit':
            break


if __name__ == '__main__':
    main()
