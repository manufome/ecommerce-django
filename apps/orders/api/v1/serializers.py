from rest_framework import serializers
from apps.orders.models import Address, Order, OrderItem, Payment, Coupon, Refund
from apps.shop.models import Product
from apps.shop.api.v1.serializers import ProductSerializer
from apps.orders.choices import PaymentMethod, PaymentStatus, OrderStatus
from django.db import transaction
import logging

logger = logging.getLogger(__name__)


class AddressSerializer(serializers.ModelSerializer):
    locality = serializers.SerializerMethodField()
    
    class Meta:
        model = Address
        fields = ['first_name', 'last_name', 'email', 'phone', 'locality', 'street_type', 'street_value', 'number', 'complement']
    
    def get_locality(self, obj):
        return {
            'id': obj.locality,
            'name': obj.get_locality_display()
        }

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    subtotal = serializers.SerializerMethodField()
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price', 'subtotal']

    def get_subtotal(self, obj):
        return obj.quantity * obj.price


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'

class RefundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Refund
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True, source='orderitem_set')
    payments = PaymentSerializer(many=True, read_only=True, source='payment_set')
    refunds = RefundSerializer(many=True, read_only=True, source='refund_set')
    shipping_address = AddressSerializer(read_only=True)
    billing_address = AddressSerializer(read_only=True)
    items_count = serializers.SerializerMethodField()
    status = serializers.CharField(source='get_status_display')
    created_at = serializers.DateTimeField(format='%d %b %Y')

    class Meta:
        model = Order
        fields = '__all__'

    def get_items_count(self, obj):
        return sum(item.quantity for item in obj.orderitem_set.all())

class OrderItemCreateSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(write_only=True)
    qty = serializers.IntegerField(write_only=True)

    class Meta:
        model = OrderItem
        fields = ['product_id', 'qty']

class OrderCreateSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    products = OrderItemCreateSerializer(many=True, write_only=True)
    payment_method = serializers.ChoiceField(choices=PaymentMethod.choices)
    notes = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Order
        fields = ['address', 'products', 'payment_method', 'notes']

    @transaction.atomic
    def create(self, validated_data):
        user = self.context['request'].user
        address_data = validated_data.pop('address')
        products_data = validated_data.pop('products')
        payment_method = validated_data.pop('payment_method')
        notes = validated_data.pop('notes', '')

        try:
            with transaction.atomic():
                address, _ = Address.objects.get_or_create(user=user, **address_data)
                
                order = Order.objects.create(
                    user=user, 
                    billing_address=address, 
                    shipping_address=address, 
                    status=OrderStatus.PENDING, 
                    notes=notes
                )

                total_amount = 0
                for product_data in products_data:
                    product = Product.objects.select_for_update().get(id=product_data['product_id'])
                    quantity = product_data['qty']
                    product.decrease_stock(quantity)
                    price = product.get_display_price()[0]
                    OrderItem.objects.create(order=order, product=product, quantity=quantity, price=price)
                    total_amount += price * quantity
    
                Payment.objects.create(
                    order=order,
                    amount=total_amount,
                    payment_method=payment_method,
                    status=PaymentStatus.PENDING
                )
                return order
        except serializers.ValidationError as e:
            raise e
        except Exception as e:
            logger.error(f"Error creating order: {str(e)}")
            raise serializers.ValidationError("Error al crear el pedido. Por favor, inténtelo de nuevo.")
