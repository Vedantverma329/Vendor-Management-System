

# Create your views here.
from rest_framework import generics,status
from rest_framework.response import Response
from django.utils import timezone

from .models import Vendor, PurchaseOrder
from .serializers import VendorSerializer, PurchaseOrderSerializer

class VendorListCreateAPIView(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
   

class VendorRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
   

class PurchaseOrderListCreateAPIView(generics.ListCreateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
   

class PurchaseOrderRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    


class VendorPerformanceAPIView(generics.RetrieveAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        performance_metrics = {
            'on_time_delivery_rate': instance.on_time_delivery_rate,
            'quality_rating_avg': instance.quality_rating_avg,
            'average_response_time': instance.average_response_time,
            'fulfillment_rate': instance.fulfillment_rate
        }
        return Response(performance_metrics)
    

class AcknowledgePurchaseOrderAPIView(generics.CreateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

    def post(self, request, *args, **kwargs):
        instance = self.get_object()

        # Extract acknowledgment_date from request data
        acknowledgment_date = request.data.get('acknowledgment_date')

        if acknowledgment_date:
            instance.acknowledgment_date = acknowledgment_date
            instance.save()

            # Trigger recalculation of average response time
            instance.vendor.calculate_performance_metrics()

            return Response({'acknowledgment_date': instance.acknowledgment_date}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Acknowledgment date is required'}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        # Handle GET request, if needed
        # For example, return some information about the purchase order
        instance = self.get_object()
        data = {
            'po_id': instance.id,
            'acknowledgment_date': instance.acknowledgment_date,
            # Add other fields as needed
        }
        return Response(data, status=status.HTTP_200_OK)
    
   # def update(self, request, *args, **kwargs):
    #    instance = self.get_object()
#
        # Extract acknowledgment_date from request data
 #       acknowledgment_date = request.data.get('acknowledgment_date')

  #      if acknowledgment_date:
   #         instance.acknowledgment_date = acknowledgment_date
    #        instance.save()

            # Trigger recalculation of average response time
     #       instance.vendor.calculate_performance_metrics()

      #      return Response({'acknowledgment_date': instance.acknowledgment_date}, status=status.HTTP_200_OK)
       # else:
        #    return Response({'error': 'Acknowledgment date is required'}, status=status.HTTP_400_BAD_REQUEST)