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

    for author in authors:
        author_data = {
            "fullname": author["fullname"],
            "born_date": author["born_date"],
            "born_location": author["born_location"],
            "description": author["description"],
        }

        Author.objects.get_or_create(**author_data)

    quotes = db.quotes.find()
    for quote in quotes:
        tags = []
        for tag in quote.get("tags"):
            if tag:
                t, *_ = Tag.objects.get_or_create(name=tag)
                tags.append(t)

        exist_quote = Quote.objects.filter(text=quote["quote"]).exists()
        if not exist_quote:
            author = db.authors.find_one({"_id": quote["author"]})
            a = Author.objects.get(fullname=author["fullname"])
            quote_data = {
                "author": a,
                "text": quote["quote"],
            }  # Use 'text' instead of 'quote'
            q = Quote.objects.create(**quote_data)
            for tag in tags:
                q.tags.add(tag)


if __name__ == "__main__":
    import_records()
