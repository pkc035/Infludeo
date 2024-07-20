# Generated by Django 4.2.14 on 2024-07-20 09:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cards', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=0, max_digits=10)),
                ('fee', models.DecimalField(decimal_places=0, max_digits=10)),
                ('state', models.CharField(choices=[('판매중', '판매중'), ('판매완료', '판매완료')], default='판매중', max_length=20)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('renewal_date', models.DateTimeField(auto_now=True)),
                ('sold_date', models.DateTimeField(blank=True, null=True)),
                ('buyer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='buyers', to=settings.AUTH_USER_MODEL)),
                ('photo_card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sales', to='cards.photocard')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sellers', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]