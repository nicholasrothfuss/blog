# Generated by Django 3.2.7 on 2021-09-09 01:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engine', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ('-published_at',), 'verbose_name_plural': 'entries'},
        ),
        migrations.AlterField(
            model_name='post',
            name='status',
            field=models.SmallIntegerField(choices=[(1, 'Draft'), (2, 'Published'), (3, 'Hidden')], default=1),
        ),
    ]