# Generated by Django 1.9.13 on 2018-05-01 12:59


from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('uk_results', '0046_auto_20180501_1052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidateresult',
            name='membership',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='result', to='popolo.Membership'),
        ),
    ]
