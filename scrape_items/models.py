from django.db import models
import django_tables2 as tables
# Create your models here.


class ItemsToScrape(models.Model):
    id = models.BigIntegerField(primary_key=True)
    brand = models.IntegerField(default=0)
    catalog_number = models.CharField(max_length=25, null=True, default=None)
    web_price = models.FloatField(default=0.0)

    class Meta:
        verbose_name = 'Items To Scrape'
        verbose_name_plural = 'Items To Scrape (visible)'


class ScrapedItems(models.Model):
    iid = models.BigIntegerField(blank=True, null=True)
    url = models.CharField(max_length=128, null=True, default=None)
    scrape_date_time = models.DateTimeField(auto_now_add=True, blank=True)
    suggested = models.CharField(max_length=25, null=True, default=None)
    list_price = models.FloatField(default=0.0, blank=True, null=True)
    price = models.FloatField(default=0.0, blank=True, null=True)
    wholesale_price = models.FloatField(default=0.0, blank=True, null=True)
    image_small = models.CharField(max_length=25, null=True, default=None)
    image_large = models.CharField(max_length=25, null=True, default=None)
    title = models.CharField(max_length=256, null=True, default=None)
    category_discount = models.FloatField(default=0.0, blank=True, null=True)
    its = models.ForeignKey(ItemsToScrape, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Scraped Items'
        verbose_name_plural = 'Scraped Items (visible)'


class ItemsToScrapeTable(tables.Table):
    class Meta:
        model = ItemsToScrape
        template_name = 'django_tables2/bootstrap4.html'


class ScrapedItemsTable(tables.Table):
    class Meta:
        model = ScrapedItems
        template_name = 'django_tables2/bootstrap4.html'
