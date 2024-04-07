import os
from pathlib import Path
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib import messages
from django.contrib.auth.models import User

from .utils import get_mongodb
from .models import Quote, Author, Tag
from .forms import AuthorForm, QuoteForm, TagForm
from dotenv import load_dotenv

env_path = Path(__file__).parent.parent.parent.joinpath(".env")

if env_path.is_file():
    print("Loading environment variables from:", env_path)
    load_dotenv(env_path)
else:
    print(".env file not found. Make sure it exists in the correct location.")

PER_PAGE = os.getenv("PER_PAGE")


def main(request, page=1):
    quotes = Quote.objects.all().order_by("id")
    paginator = Paginator(quotes, per_page=PER_PAGE)

    context = {"quotes": paginator.page(page)}
    return render(request, "quotes/index.html", context)


class AuthorDetailView(View):
    template_name = "quotes/author.html"

    def get(self, request, pk):
        author = get_object_or_404(Author, pk=pk)
        return render(request, self.template_name, {"author": author})


def tag(request, tag: str, page: int = 1):
    try:
        tag_obj = Tag.objects.get(name=tag)
        tag_id = tag_obj.id
    except Tag.DoesNotExist:
        return render(request, "404.html", status=404)

    if tag_id:
        quotes = Quote.objects.all()
        quotes = quotes.filter(tags__id=tag_id).distinct()
        paginator = Paginator(quotes, per_page=PER_PAGE)

        context = {"quotes": paginator.page(page), "tag": tag_obj}
    return render(request, "quotes/tag.html", context)


@login_required
def add_author(request):
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            fullname = form.cleaned_data["fullname"]
            messages.success(request, f"Author '{fullname}' was created...")
            return render(
                request, "quotes/add_author.html", context={"form": AuthorForm()}
            )
        else:
            messages.error(request, "Not added...")
            return render(request, "quotes/add_author.html", context={"form": form})

    context = {"form": AuthorForm()}
    return render(request, "quotes/add_author.html", context)


@login_required
def add_quote(request, id: int = 0):
    tags = Tag.objects.all()
    authors = Author.objects.all()

    if request.method == "POST":
        form = QuoteForm(request.POST)
        print(request.POST)
        if form.is_valid():
            new_quote = form.save(commit=False)
            new_quote.quote = form.cleaned_data["quote"]
            new_quote.author = Author.objects.filter(
                pk=form.cleaned_data["author"]
            ).get()
            new_quote.save()

            choice_tags = Tag.objects.filter(name__in=request.POST.getlist("tags"))
            for tag in choice_tags.iterator():
                new_quote.tags.add(tag)
            messages.success(request, "Quote was added....")
        else:
            messages.error(request, "Not added....")
            return render(
                request,
                "quotes/add_quote.html",
                {"tags": tags, "authors": authors, "form": form},
            )

    return render(
        request,
        "quotes/add_quote.html",
        {"tags": tags, "authors": authors, "form": QuoteForm()},
    )


class AddAuthorView(LoginRequiredMixin, View):
    form_class = AuthorForm
    template_name = "quotes/add_author.html"

    def get(self, request):
        return render(request, self.template_name, context={"form": self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            fullname = form.cleaned_data["fullname"]
            messages.success(request, f"Author '{fullname}' was created...")
            return render(
                request, self.template_name, context={"form": self.form_class}
            )
        else:
            messages.error(request, "Not added...")
            return render(request, self.template_name, context={"form": form})


class AddTagView(LoginRequiredMixin, View):
    form_class = TagForm
    template_name = "quotes/add_tag.html"

    def get(self, request):
        return render(request, self.template_name, context={"form": self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            fullname = form.cleaned_data["name"]
            messages.success(request, f"Tag '{fullname}' was created...")
            return render(
                request, self.template_name, context={"form": self.form_class}
            )
        else:
            messages.error(request, "Not added...")
            return render(request, self.template_name, context={"form": form})
