from import_export import resources
from .models import ItemsToScrape, ScrapedItems


class ItemsToScrapeResource(resources.ModelResource):

    class Meta:
        model = ItemsToScrape
        fields = ('id', 'brand', 'catalog_number', 'web_price',)


class ScrapedItemsResource(resources.ModelResource):

    class Meta:
        model = ScrapedItems
        fields = (
            'iid',
            'url',
            'scrape_date_time',
            'suggested',
            'list_price',
            'price',
            'wholesale_price',
            'image_small',
            'image_large',
            'title',
            'category_discount',
            'its'
            )
