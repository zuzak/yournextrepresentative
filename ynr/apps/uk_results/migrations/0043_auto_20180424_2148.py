# Generated by Django 1.9.13 on 2018-04-24 20:48


from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('uk_results', '0042_auto_20180424_2053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resultset',
            name='post_election',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='candidates.PostExtraElection'),
        ),
    ]
