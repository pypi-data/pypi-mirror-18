# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wooey', '0027_parameter_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='script',
            name='save_path',
            field=models.CharField(blank=True, help_text='By default save to the script name, this will change the output folder.', max_length=255, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='scriptparameter',
            name='param_help',
            field=models.TextField(verbose_name='help', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='scriptversion',
            name='script_path',
            field=models.FileField(upload_to=''),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='wooeyfile',
            name='filepath',
            field=models.FileField(upload_to='', max_length=500),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='wooeyjob',
            name='status',
            field=models.CharField(choices=[('submitted', 'Submitted'), ('running', 'Running'), ('completed', 'Completed'), ('deleted', 'Deleted')], default='submitted', max_length=255),
            preserve_default=True,
        ),
    ]
