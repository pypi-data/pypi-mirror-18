# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20150804_1545'),
    ]

    operations = [
        migrations.AddField(
            model_name='registrant',
            name='salutation',
            field=models.CharField(default=b'', max_length=15, verbose_name='salutation', blank=True),
        ),
    ]
