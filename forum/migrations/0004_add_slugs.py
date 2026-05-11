from django.db import migrations, models
from django.utils.text import slugify


def _unique_slug(model, base_slug, pk):
    slug = base_slug
    counter = 1
    while model.objects.filter(slug=slug).exclude(pk=pk).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1
    return slug


def populate_slugs(apps, schema_editor):
    Category = apps.get_model('forum', 'Category')
    Discussion = apps.get_model('forum', 'Discussion')

    for category in Category.objects.all():
        base = slugify(category.name) or f"category-{category.pk}"
        category.slug = _unique_slug(Category, base, category.pk)
        category.save(update_fields=['slug'])

    for discussion in Discussion.objects.all():
        base = slugify(discussion.title) or f"discussion-{discussion.pk}"
        discussion.slug = _unique_slug(Discussion, base, discussion.pk)
        discussion.save(update_fields=['slug'])


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0003_simplify_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True, max_length=120, null=True),
        ),
        migrations.AddField(
            model_name='discussion',
            name='slug',
            field=models.SlugField(blank=True, max_length=220, null=True),
        ),
        migrations.RunPython(populate_slugs, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True, max_length=120, unique=True),
        ),
        migrations.AlterField(
            model_name='discussion',
            name='slug',
            field=models.SlugField(blank=True, max_length=220, unique=True),
        ),
    ]
