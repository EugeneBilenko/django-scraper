from django.shortcuts import render
from django_tables2 import SingleTableView
from scrape_items.models import ItemsToScrape, ScrapedItems, ItemsToScrapeTable, ScrapedItemsTable


# Create your views here.
class ItemsToScrapeTableView(SingleTableView):
    model = ItemsToScrape
    table_class = ItemsToScrapeTable
    template_name = "scrape_items/items_to_scrape_list.html"


class ScrapedItemsTableView(SingleTableView):
    model = ScrapedItems
    table_class = ScrapedItemsTable
    template_name = "scrape_items/scraped_items_list.html"
