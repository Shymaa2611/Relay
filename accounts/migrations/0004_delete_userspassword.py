# Generated by Django 5.1.2 on 2024-11-09 09:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_userspassword_username'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UsersPassword',
        ),
    ]