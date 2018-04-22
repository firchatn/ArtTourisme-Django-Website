# Generated by Django 2.0.3 on 2018-04-22 22:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('art', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartline',
            name='user',
            field=models.ForeignKey(default='kjn', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='address',
            name='additional_address',
            field=models.CharField(blank=True, max_length=255, verbose_name="Complément d'adresse"),
        ),
        migrations.AlterField(
            model_name='address',
            name='address',
            field=models.CharField(max_length=255, verbose_name='Adresse'),
        ),
        migrations.AlterField(
            model_name='address',
            name='city',
            field=models.CharField(max_length=50, verbose_name='Ville'),
        ),
        migrations.AlterField(
            model_name='address',
            name='company',
            field=models.CharField(blank=True, max_length=50, verbose_name='Société'),
        ),
        migrations.AlterField(
            model_name='address',
            name='fax',
            field=models.CharField(blank=True, max_length=10, verbose_name='Fax'),
        ),
        migrations.AlterField(
            model_name='address',
            name='first_name',
            field=models.CharField(max_length=50, verbose_name='Prénom'),
        ),
        migrations.AlterField(
            model_name='address',
            name='gender',
            field=models.CharField(choices=[('MR', 'Monsieur'), ('MISS', 'Mademoiselle'), ('MRS', 'Madame')], default='MR', max_length=4, verbose_name='Civilité'),
        ),
        migrations.AlterField(
            model_name='address',
            name='last_name',
            field=models.CharField(max_length=50, verbose_name='Nom'),
        ),
        migrations.AlterField(
            model_name='address',
            name='mobilephone',
            field=models.CharField(blank=True, max_length=10, verbose_name='Téléphone portable'),
        ),
        migrations.AlterField(
            model_name='address',
            name='phone',
            field=models.CharField(max_length=10, verbose_name='Téléphone'),
        ),
        migrations.AlterField(
            model_name='address',
            name='postcode',
            field=models.CharField(max_length=5, verbose_name='Code postal'),
        ),
        migrations.AlterField(
            model_name='address',
            name='workphone',
            field=models.CharField(blank=True, max_length=10, verbose_name='Téléphone travail'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=150, verbose_name='Nom de la catégorie'),
        ),
        migrations.AlterField(
            model_name='category',
            name='parent_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='art.Category', verbose_name='Catégorie parente'),
        ),
        migrations.AlterField(
            model_name='category',
            name='short_desc',
            field=models.CharField(blank=True, max_length=150, verbose_name='Description courte'),
        ),
        migrations.AlterField(
            model_name='client',
            name='default_invoicing_address',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='default_invoicing_address', to='art.Address', verbose_name='Adresse de facturation par défaut'),
        ),
        migrations.AlterField(
            model_name='client',
            name='default_shipping_address',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='default_shipping_address', to='art.Address', verbose_name='Adresse de livraison par défaut'),
        ),
        migrations.AlterField(
            model_name='client',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Utilisateur associe'),
        ),
        migrations.AlterField(
            model_name='order',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='art.Client', verbose_name='Client ayant passé commande'),
        ),
        migrations.AlterField(
            model_name='order',
            name='invoicing_address',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_invoicing_address', to='art.Address', verbose_name='Adresse de facturation'),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_date',
            field=models.DateField(auto_now=True, verbose_name='Date de la commande'),
        ),
        migrations.AlterField(
            model_name='order',
            name='shipping_address',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_shipping_address', to='art.Address', verbose_name='Adresse de livraison'),
        ),
        migrations.AlterField(
            model_name='order',
            name='shipping_date',
            field=models.DateField(null=True, verbose_name="Date de l'expédition"),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('W', 'En attente de validation'), ('P', 'Payée'), ('S', 'Expédiée'), ('C', 'Annulée')], default='W', max_length=1, verbose_name='Statut de la commande'),
        ),
        migrations.AlterField(
            model_name='order',
            name='stripe_charge_id',
            field=models.CharField(blank=True, max_length=30, verbose_name='Identifiant de transaction Stripe'),
        ),
        migrations.AlterField(
            model_name='orderdetail',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='art.Order', verbose_name='Commande associée'),
        ),
        migrations.AlterField(
            model_name='orderdetail',
            name='product_unit_price',
            field=models.FloatField(verbose_name='Prix unitaire du produit'),
        ),
        migrations.AlterField(
            model_name='orderdetail',
            name='qty',
            field=models.IntegerField(verbose_name='Quantité'),
        ),
        migrations.AlterField(
            model_name='orderdetail',
            name='vat',
            field=models.FloatField(verbose_name='Taux de TVA'),
        ),
        migrations.AlterField(
            model_name='photo',
            name='photo',
            field=models.ImageField(upload_to='art/media'),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='art.Category', verbose_name='Catégorie du produit'),
        ),
        migrations.AlterField(
            model_name='product',
            name='long_desc',
            field=models.TextField(verbose_name='Description longue'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=150, verbose_name='Nom du produit'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.FloatField(verbose_name='Prix HT du produit'),
        ),
        migrations.AlterField(
            model_name='product',
            name='short_desc',
            field=models.CharField(max_length=150, verbose_name='Description courte'),
        ),
        migrations.AlterField(
            model_name='product',
            name='thumbnail',
            field=models.ImageField(null=True, upload_to='art/media', verbose_name='Miniature du produit'),
        ),
        migrations.AlterField(
            model_name='product',
            name='vat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='art.VAT', verbose_name='Taux de TVA'),
        ),
        migrations.AlterField(
            model_name='vat',
            name='percent',
            field=models.FloatField(verbose_name='Taux de TVA (décimal)'),
        ),
    ]