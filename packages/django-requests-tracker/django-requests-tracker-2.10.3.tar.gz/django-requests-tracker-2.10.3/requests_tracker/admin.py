# -*- coding: utf-8 -*-
from django.contrib import admin

from requests_tracker.models import Record, Filter, Exclude


class RecordAdmin(admin.ModelAdmin):

    list_display = (
        '__unicode__',
        'api_uid', 'status_code',
        'show_date_created', 'duration',
        'state', 'remark'
    )
    list_filter = ('date_created', 'method', 'api_uid', 'status_code', 'state')
    search_fields = ('request_message', 'response_message')

    fieldsets = (
        (None, {
            'fields': ('uid',),
        }),
        ("Request", {
            'fields': ('method', 'url', 'request_message',),
        }),
        ("Response", {
            'fields': ('status_code', 'response_message',),
        }),
        ("Other Infamation", {
            'fields': ('api_uid', 'state', 'remark',),
        }),
        ("Important Datetimes", {
            'fields': ('date_created', 'duration',),
        }),
    )

    readonly_fields = (
        'uid',
        'method', 'url',
        'status_code',
        'api_uid', 'state', 'remark',
        'date_created', 'duration'
    )

    def show_date_created(self, obj):
        return obj.date_created.strftime("%Y-%m-%d %H:%M:%S")
    show_date_created.short_description = "Date created"


class BaseFilterAdmin(admin.ModelAdmin):

    list_display = (
        '__unicode__', 'is_active',
        'column', 'category', 'rule',
    )
    list_filter = ('is_active', 'column', 'category',)
    search_fields = ('name', 'rule',)

    fieldsets = (
        (None, {
            'fields': ('name', 'is_active',),
        }),
        ("Filtering Rules", {
            'fields': ('column', 'category', 'rule',),
        }),
        ("Important Datetimes", {
            'fields': ('date_created', 'last_modified',),
        }),
    )

    readonly_fields = ('date_created', 'last_modified',)


class FilterAdmin(BaseFilterAdmin):
    pass


class ExcludeAdmin(BaseFilterAdmin):
    pass


admin.site.register(Record, RecordAdmin)
admin.site.register(Filter, FilterAdmin)
admin.site.register(Exclude, ExcludeAdmin)
