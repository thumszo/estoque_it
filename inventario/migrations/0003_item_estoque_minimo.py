from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0002_alter_item_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='estoque_minimo',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
