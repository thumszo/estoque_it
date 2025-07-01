from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='item',
            unique_together={('nome', 'categoria')},
        ),
    ]
