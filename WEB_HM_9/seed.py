import json
import connect

from models import Author, Quote


def load_data_from_json(file_name, model):
    with open(file_name, 'r', encoding='utf-8') as fd:
        data = json.load(fd)
        for item in data:
            if "author" in item:
                author_name = item.get('author')
                author = Author.objects(fullname=author_name).first()
                item["author"] = author
            obj = model(**item)
            obj.save()
        db_data_name = file_name.split('.')[0].title()
        print(f'{db_data_name} added to database')


def main():
    load_data_from_json('authors.json', Author)
    load_data_from_json('quotes.json', Quote)


if __name__ == '__main__':
    main()
