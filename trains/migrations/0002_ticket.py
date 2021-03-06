# Generated by Django 2.2.6 on 2019-10-31 15:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trains', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField()),
                ('document_id', models.CharField(max_length=12)),
                ('l_name', models.CharField(max_length=50)),
                ('f_name', models.CharField(max_length=50)),
                ('date', models.DateTimeField()),
                ('from_station', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_station', to='trains.Station')),
                ('to_station', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_station', to='trains.Station')),
            ],
        ),
    ]
