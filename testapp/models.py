

# Create your models here.


from django.db import models
from django.db.models import Count, Avg
from django.utils import timezone

class Vendor(models.Model):
    name = models.CharField(max_length=100)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True)
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)

    def calculate_performance_metrics(self):
        completed_orders = self.purchase_orders.filter(status='completed')
        total_orders = completed_orders.count()

        if total_orders > 0:
            # Calculate On-Time Delivery Rate
            on_time_orders = completed_orders.filter(delivery_date__lte=timezone.now())
            self.on_time_delivery_rate = (on_time_orders.count() / total_orders) * 100

            # Calculate Quality Rating Average
            self.quality_rating_avg = completed_orders.aggregate(Avg('quality_rating'))['quality_rating__avg']

            # Calculate Average Response Time
            response_times = completed_orders.exclude(acknowledgment_date=None).annotate(
                response_time=models.ExpressionWrapper(models.F('acknowledgment_date') - models.F('issue_date'),output_field=models.DurationField())
                ).aggregate(Avg('response_time'))['response_time__avg']
            self.average_response_time = response_times.total_seconds() / 3600 if response_times else 0

            # Calculate Fulfilment Rate
            successful_orders = completed_orders.filter(status='completed')
            self.fulfillment_rate = (successful_orders.count() / total_orders) * 100

        else:
            # If there are no completed orders, reset metrics
            self.on_time_delivery_rate = 0
            self.quality_rating_avg = 0
            self.average_response_time = 0
            self.fulfillment_rate = 0

        self.save()

    def update_performance_metrics(self, on_time_delivery_rate, quality_rating_avg, average_response_time, fulfillment_rate):
        self.on_time_delivery_rate = on_time_delivery_rate
        self.quality_rating_avg = quality_rating_avg
        self.average_response_time = average_response_time
        self.fulfillment_rate = fulfillment_rate
        self.save()


class PurchaseOrder(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='purchase_orders')
    po_number = models.CharField(max_length=100, unique=True)
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=20, default='pending')
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField(auto_now_add=True)
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Update vendor's performance metrics upon saving the purchase order
        super().save(*args, **kwargs)
        self.vendor.calculate_performance_metrics()

    def delete(self, *args, **kwargs):
        # Update vendor's performance metrics upon deleting the purchase order
        super().delete(*args, **kwargs)
        self.vendor.calculate_performance_metrics()


class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='historical_performance')
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()
