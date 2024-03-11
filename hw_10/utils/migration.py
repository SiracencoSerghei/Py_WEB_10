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

   
