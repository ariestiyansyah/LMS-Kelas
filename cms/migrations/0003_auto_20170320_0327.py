# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import cms.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0002_file_gambar_konten_teks_video'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='content',
            options={'ordering': ['order']},
        ),
        migrations.AlterModelOptions(
            name='module',
            options={'ordering': ['order']},
        ),
        migrations.AddField(
            model_name='content',
            name='order',
            field=cms.fields.OrderField(default=0, blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='module',
            name='order',
            field=cms.fields.OrderField(default=0, blank=True),
            preserve_default=False,
        ),
    ]
