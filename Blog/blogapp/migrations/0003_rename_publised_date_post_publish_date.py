# Generated by Django 3.2.7 on 2021-10-04 18:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0002_post_publised_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='publised_date',
            new_name='publish_date',
        ),
    ]
