# Generated by Django 1.9.13 on 2018-01-30 12:43


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uk_results', '0033_auto_20170506_2042'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='postelectionresult',
            options={'get_latest_by': 'confirmed_resultset__created'},
        ),
        migrations.AlterField(
            model_name='councilelectionresultset',
            name='review_status',
            field=models.CharField(blank=True, choices=[(None, b'Unreviewed'), (b'unconfirmed', b'Unconfirmed'), (b'confirmed', b'Confirmed'), (b'rejected', b'Rejected')], max_length=100),
        ),
        migrations.AlterField(
            model_name='postelectionresult',
            name='confirmed',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='resultset',
            name='review_status',
            field=models.CharField(blank=True, choices=[(None, b'Unreviewed'), (b'unconfirmed', b'Unconfirmed'), (b'confirmed', b'Confirmed'), (b'rejected', b'Rejected')], max_length=100),
        ),
    ]
