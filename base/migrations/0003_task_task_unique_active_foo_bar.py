# Generated by Django 4.0.10 on 2023-08-23 05:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_cheese_customer_order_pizza_topping_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('old_value', models.IntegerField()),
                ('new_value', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.order')),
            ],
        ),
        migrations.AddConstraint(
            model_name='task',
            constraint=models.UniqueConstraint(fields=('order', 'old_value', 'new_value'), name='unique_active_foo_bar'),
        ),
    ]
