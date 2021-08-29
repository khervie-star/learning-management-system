import string
import random
from django.utils.text import slugify

def generate_random(size):
    ''.join(random.choices(string.ascii_lowercase + string.digits, k=size))


def slug_generator(instance, new_slug=None):
    if new_slug != None:
        slug = new_slug
    slug = slugify(instance.name)

    klass = instance.__class__

    # check if unique

    slug_exists = klass.objects.filter(slug=slug).exists()
    if slug_exists:
        new_slug = "{slug}-{gen_random}".format(slug, generate_random(size=4))
        return slug_generator(instance, new_slug=new_slug)
    return slug