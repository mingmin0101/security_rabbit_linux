# Generated by Django 2.1 on 2019-09-14 01:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0007_auto_20190913_2355'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fileinfo',
            old_name='file_hash',
            new_name='file_hash_sha1',
        ),
        migrations.RemoveField(
            model_name='fileinfo',
            name='pefile_txt',
        ),
    ]
