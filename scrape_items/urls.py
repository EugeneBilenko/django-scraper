from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.ItemsToScrapeTableView.as_view(), name='items_to_scrape'),
    url(r'^result/$', views.ScrapedItemsTableView.as_view(), name='scraped_items'),
]
