import json
import random
import requests
from django.conf.urls import url
from django.contrib import admin
from django.contrib.admin.templatetags.admin_static import static
from django.http import HttpResponseRedirect
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin
from scrape_items.models import ItemsToScrape, ScrapedItems
from django.conf import settings
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter


@admin.register(ItemsToScrape)
class ItemsToScrapeAdmin(ImportExportModelAdmin):

    model = ItemsToScrape
    list_display = ['id', 'brand', 'catalog_number', 'web_price']
    actions = ['execute_crawler', ]

    def execute_crawler(self, request, queryset):
        for item in queryset:
            fields = dict()
            response = requests.request(
                'GET',
                settings.PARSING_URL.format(rsq=item.catalog_number),
                headers=self.get_ua()
            )
            if response.status_code == 200:
                json_response = json.loads(response.content)

            found = json_response.get('FOUND', None)
            if found:
                r = json_response.get('RESULTS', None)
                if r:
                    for r_item in r:
                        fields.update({
                            'iid': r_item.get('ID', None),
                            'url': r_item.get('URL', None),
                            'list_price': r_item.get('LIST_PRICE', None),
                            'price': r_item.get('PRICE', None),
                            'wholesale_price': r_item.get('WHOLESALE_PRICE', None),
                            'image_small': r_item.get('IMAGE_SMALL', None),
                            'image_large': r_item.get('IMAGE_LARGE', None),
                            'title': r_item.get('TITLE', None),
                            'category_discount': r_item.get('CATEGORY_DISCOUNT', None),
                            'its': item
                        })
            else:
                suggested = json_response.get('SUGGESTED', None)
                if suggested:
                    fields.update({
                        'iid': json_response.get('ID', None),
                        'suggested': json_response.get('SUGGESTED', None),
                        'its': item
                    })
                else:
                    fields.update({
                        'iid': json_response.get('ID', None),
                        'its': item
                    })

            if fields:
                obj, created = ScrapedItems.objects.update_or_create(**fields)

    execute_crawler.short_description = 'Execute Crawler (for selected objects)'

    @staticmethod
    def get_ua():
        return dict({'User-Agent': random.choice(settings.USER_AGENTS)})

    def get_urls(self):
        urls = super(ItemsToScrapeAdmin, self).get_urls()
        add_urls = [
            url(r"^importcsv/$", importcsv)
        ]
        return add_urls + urls


@staff_member_required
def importcsv(request):

    print('run IMPORT stuff!!!')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class ScrapeResultsFilter(admin.SimpleListFilter):
    title = 'Scrape Results Filter'
    parameter_name = 'suggested'

    def lookups(self, request, model_admin):
        return (
            ('Yes', 'successful'),
            ('No',  'unsuccessful'),
            ('Suggestion', 'suggestion'),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'Yes':
            return queryset.filter(iid__isnull=False)
        elif value == 'No':
            return queryset.filter(Q(iid__isnull=True) & Q(suggested__isnull=True))
        elif value == 'Suggestion':
            return queryset.filter(suggested__isnull=False)
        return queryset


@admin.register(ScrapedItems)
class ScrapedItemsAdmin(ImportExportModelAdmin):

    model = ScrapedItems

    list_filter = (
        ('scrape_date_time', DateTimeRangeFilter),
        ScrapeResultsFilter,
    )

    list_display = [
        'set_flag_status',
        'iid',
        'prepare_link',
        'scrape_date_time',
        'suggested',
        'list_price',
        'price',
        'wholesale_price',
        'image_small',
        'image_large',
        'title',
        'category_discount',
        'get_its_id',
        'get_its_catalog_number',
    ]

    def prepare_link(self, obj):
        if obj.url:
            return format_html('<a href="{}">{}</a>', settings.PARSING_HOST.format(obj.url), obj.url)
        else:
            return None

    prepare_link.short_description = 'remote url'
    prepare_link.admin_order_field = 'url'

    def get_its_id(self, obj):
        return format_html(
            '<span>{}</span>',
            obj.its.id
        )

    get_its_id.short_description = 'source(id)'   # Item To Scrape
    get_its_id.admin_order_field = 'its'
    get_its_id.allow_tags = True

    def get_its_catalog_number(self, obj):
        return format_html(
            '<span>{}</span>',
            obj.its.catalog_number
        )

    get_its_catalog_number.short_description = 'source(catalog number)'   # Item To Scrape
    get_its_catalog_number.admin_order_field = 'its'
    get_its_catalog_number.allow_tags = True

    def set_flag_status(self, obj):

        if obj.iid is not None:
            field_val = True
        elif obj.iid is None and obj.suggested is None:
            field_val = False
        elif obj.suggested is not None:
            field_val = None

        icon_url = static('admin/img/icon-%s.svg' %
                          {True: 'yes', False: 'no', None: 'unknown'}[field_val])
        return format_html('<img src="{}" alt="{}" />', icon_url, field_val)

    set_flag_status.short_description = 'status'
    set_flag_status.admin_order_field = 'iid'
    set_flag_status.allow_tags = True



