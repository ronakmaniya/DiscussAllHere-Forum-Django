from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0002_comment_threading_fields'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='reply_to_comment',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='reply_to_user',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='depth',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='reply_count',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='is_deleted',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='is_edited',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='edited_at',
        ),
    ]
