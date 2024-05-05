from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Vendor)
admin.site.register(PurchaseOrder)

class HistoricalPerformanceAdmin(admin.ModelAdmin):
    list_display = ['vendor_name', 'date', 'on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate']

    def vendor_name(self, obj):
        return obj.vendor.name

    vendor_name.short_description = 'Vendor Name'  # Customizes the column name in the admin list view
    def has_add_permission(self, request):
        return False  # Disables the ability to add new HistoricalPerformance objects through the admin interface

    def has_change_permission(self, request, obj=None):
        return False  # Disables the ability to edit existing HistoricalPerformance objects through the admin interface

    def has_delete_permission(self, request, obj=None):
        return False  # Disables the ability to delete HistoricalPerformance objects through the admin interface

admin.site.register(HistoricalPerformance, HistoricalPerformanceAdmin)
