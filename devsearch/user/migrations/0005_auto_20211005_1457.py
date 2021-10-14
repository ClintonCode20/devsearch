# Generated by Django 3.2.6 on 2021-10-05 21:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_alter_message_receiver'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='receiver',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='allmessages', to='user.profile'),
        ),
        migrations.AlterField(
            model_name='message',
            name='sender',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.profile'),
        ),
    ]
