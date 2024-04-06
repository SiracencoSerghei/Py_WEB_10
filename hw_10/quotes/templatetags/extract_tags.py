from django import template

register = template.Library()


def get_tagslist(tags):
    return [str(name) for name in tags.all()]


def get_tags(tags):
    return ", ".join([f"#{name}" for name in tags.all()])


register.filter("tags_list", get_tagslist)
register.filter("tags", get_tags)
