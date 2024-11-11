# Generated by Django 5.1.1 on 2024-11-10 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0018_remove_seekerprofilemodel_user_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('calories', models.PositiveIntegerField(null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6, null=True)),
                ('is_available', models.BooleanField(default=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
    ]