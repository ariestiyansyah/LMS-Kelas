# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import lms.fields


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0002_file_gambar_konten_teks_video'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='konten',
            options={'ordering': ['order']},
        ),
        migrations.AlterModelOptions(
            name='modul',
            options={'ordering': ['order']},
        ),
        migrations.AddField(
            model_name='konten',
            name='order',
            field=lms.fields.OrderField(default=0, blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='modul',
            name='order',
            field=lms.fields.OrderField(default=0, blank=True),
            preserve_default=False,
        ),
    ]
