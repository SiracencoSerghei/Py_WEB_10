import os
import django
import sys
from datetime import datetime

# print(sys.path)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# print(project_root)
sys.path.append(project_root)
# print(sys.path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hw_10.settings")
django.setup()

from quotes.models import Quote, Author, Tag  # noqa
from quotes.utils import get_mongodb


def import_records():
    db = get_mongodb()
    authors = db.authors.find()
    quotes = db.quotes.find()

    for author in authors:
        author_data = {
            "fullname": author["fullname"],
            "born_date": author["born_date"],
            "born_location": author["born_location"],
            "description": author["description"],
        }

        Author.objects.get_or_create(**author_data)
    for  quote in quotes:
        # print(quote['tags'])
        tags = []
        for tag in quote['tags']:
            t, *_ = Tag.objects.get_or_create(name=tag)
            tags.append(t)
        exist_quote = bool(len(Quote.objects.filter(quote =  quote['quote'])))
        
        if not exist_quote:
            author = db.authors.find_one({'_id': quote['author']})
            a = Author.objects.get(fullname = author['fullname'])
            q = Quote.objects.create(
                quote=quote.get("quote"),
                author = a
            )
            for tag in tags:
                q.tags.add(tags)
                

if  __name__ == '__main__':
    import_records()
    