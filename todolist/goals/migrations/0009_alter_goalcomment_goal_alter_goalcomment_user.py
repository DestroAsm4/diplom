# Generated by Django 4.2.2 on 2023-07-21 20:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('goals', '0008_alter_goalcomment_goal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goalcomment',
            name='goal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='goals.goal', verbose_name='Цель'),
        ),
        migrations.AlterField(
            model_name='goalcomment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
    ]
