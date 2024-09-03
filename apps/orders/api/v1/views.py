from rest_framework import viewsets
from apps.orders.models import Address, Order, OrderItem, Payment, Coupon, Refund
from .serializers import AddressSerializer, OrderSerializer, OrderItemSerializer, PaymentSerializer, CouponSerializer, RefundSerializer, OrderCreateSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.orders.choices import LOCALITIES, STREET_TYPES, ORDER_STATUS, PAYMENT_METHODS
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from apps.shop.models import Product

class AddressViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return (
            Order.objects.filter(user=self.request.user)
            .select_related('billing_address', 'shipping_address')
            .prefetch_related('orderitem_set', 'payment_set', 'refund_set')
        )

    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        return OrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        try:
            serializer.is_valid(raise_exception=True)
            order = serializer.save()
            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
class OrderItemViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

class PaymentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

class CouponViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer

class RefundViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Refund.objects.all()
    serializer_class = RefundSerializer

    def get_queryset(self):
        return Refund.objects.filter(user=self.request.user)

class ChoicesView(APIView):
    def get(self, request):
        query_params = request.query_params
        data = {
            'localities': [{'id': id, 'name': name} for id, name in LOCALITIES],
            'street_types': [{'id': id, 'name': name} for id, name in STREET_TYPES],
            'order_status': [{'id': id, 'name': name} for id, name in ORDER_STATUS],
            'payment_methods': [{'id': id, 'name': name} for id, name in PAYMENT_METHODS],
        }
        if query_params:
            data = {key: value for key, value in data.items() if query_params.get(key) == 'true'}
        return Response(data, status=status.HTTP_200_OK)
