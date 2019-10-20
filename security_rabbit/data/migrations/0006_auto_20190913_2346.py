# Generated by Django 2.1 on 2019-09-13 15:46

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0005_auto_20190817_1623'),
    ]

    operations = [
        migrations.AddField(
            model_name='fileinfo',
            name='company',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='fileinfo',
            name='counter_signer',
            field=models.TextField(default=' '),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='fileinfo',
            name='description',
            field=models.CharField(blank=True, max_length=60),
        ),
        migrations.AddField(
            model_name='fileinfo',
            name='file_magic',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='fileinfo',
            name='file_size',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='fileinfo',
            name='file_version',
            field=models.CharField(blank=True, max_length=40),
        ),
        migrations.AddField(
            model_name='fileinfo',
            name='link_date',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='fileinfo',
            name='machine_type',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='fileinfo',
            name='pe_characteristics',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='fileinfo',
            name='pe_entryPoint',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='fileinfo',
            name='pe_exports',
            field=models.TextField(default=' '),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='fileinfo',
            name='pe_imports',
            field=models.TextField(default=' '),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='fileinfo',
            name='pe_machine',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='fileinfo',
            name='pe_sectionNum',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='fileinfo',
            name='pe_sections',
            field=models.TextField(default=' '),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='fileinfo',
            name='pe_timeDateStamp',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='fileinfo',
            name='prod_version',
            field=models.CharField(blank=True, max_length=40),
        ),
        migrations.AddField(
            model_name='fileinfo',
            name='product',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='fileinfo',
            name='signature_verification',
            field=models.CharField(default='Signed', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='fileinfo',
            name='signing_date',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='fileinfo',
            name='file_hash',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='fileinfo',
            name='signer',
            field=models.TextField(),
        ),
    ]
