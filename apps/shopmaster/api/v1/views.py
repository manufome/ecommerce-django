from django.http import JsonResponse
from django.db.models import Sum, Count, F, ExpressionWrapper, DecimalField
from django.db.models.functions import TruncMonth, TruncYear, TruncDay, ExtractWeekDay
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from apps.orders.models import Order, OrderItem, Payment
from apps.shop.models import Product
from apps.orders.choices import OrderStatus, PaymentStatus

def get_admin_overview(request):
    # Obtener la fecha actual y la fecha de hace un año
    now = timezone.now()
    one_year_ago = now - relativedelta(years=1)

    # Filtrar órdenes completadas en el último año
    completed_orders = Order.objects.filter(status=OrderStatus.DELIVERED, created_at__gte=one_year_ago)

    data = {
        # Ingresos totales en pesos
        'total_income': Payment.objects.filter(status=PaymentStatus.COMPLETED).aggregate(total=Sum('amount'))['total'] or 0,

        # Cantidad de productos vendidos este mes
        'products_sold_this_month': OrderItem.objects.filter(
            order__status=OrderStatus.DELIVERED, 
            order__created_at__month=now.month, 
            order__created_at__year=now.year
        ).aggregate(total=Sum('quantity'))['total'] or 0,

        # Cantidad de ventas
        'sales_count': completed_orders.count(),

        # Items en existencia
        'items_in_stock': Product.objects.aggregate(total=Sum('stock'))['total'] or 0,

        # Datos de ganancias por mes del último año
        'monthly_profits': list(completed_orders.annotate(
            month=TruncMonth('created_at')
        ).values('month').annotate(
            total=Sum('payment__amount')
        ).order_by('month')),

        # Conteo de métodos de pago usados por año
        'payment_methods_per_year': list(Payment.objects.filter(
            order__in=completed_orders
        ).annotate(
            year=TruncYear('timestamp')
        ).values('year', 'payment_method').annotate(
            count=Count('id')
        ).order_by('year', 'payment_method')),

        # Top 5 productos más vendidos
        'best_selling': list(OrderItem.objects.filter(
            order__in=completed_orders
        ).values('product__name').annotate(
            total_sold=Sum('quantity')
        ).order_by('-total_sold')[:5]),

        # Top 5 productos más rentables
        'most_profitable': list(OrderItem.objects.filter(
            order__in=completed_orders
        ).annotate(
            profit=ExpressionWrapper(
                F('quantity') * (F('price') - F('product__price')),
                output_field=DecimalField()
            )
        ).values('product__name').annotate(
            total_profit=Sum('profit')
        ).order_by('-total_profit')[:5]),

        # Top 5 productos menos vendidos
        'least_selling': list(Product.objects.annotate(
            total_sold=Sum('orderitem__quantity')
        ).order_by('total_sold')[:5].values('name', 'total_sold')),

        # Top 5 productos menos rentables
        'least_profitable': list(OrderItem.objects.filter(
            order__in=completed_orders
        ).annotate(
            profit=ExpressionWrapper(
                F('quantity') * (F('price') - F('product__price')),
                output_field=DecimalField()
            )
        ).values('product__name').annotate(
            total_profit=Sum('profit')
        ).order_by('total_profit')[:5]),

        # Transacciones por día
        'transactions_per_day': list(completed_orders.annotate(
            date=TruncDay('created_at')
        ).values('date').annotate(
            products_sold=Sum('orderitem__quantity'),
            total_orders=Count('id'),
            total_profits=Sum('payment__amount')
        ).order_by('date')),

        # Transacciones por días de la semana
        'transactions_per_weekday': list(completed_orders.annotate(
            weekday=ExtractWeekDay('created_at')
        ).values('weekday').annotate(
            products_sold=Sum('orderitem__quantity'),
            total_orders=Count('id'),
            total_profits=Sum('payment__amount')
        ).order_by('weekday')),

        # Transacciones por mes
        'transactions_per_month': list(completed_orders.annotate(
            month=TruncMonth('created_at')
        ).values('month').annotate(
            products_sold=Sum('orderitem__quantity'),
            total_orders=Count('id'),
            total_profits=Sum('payment__amount')
        ).order_by('month')),

        # Transacciones por año
        'transactions_per_year': list(completed_orders.annotate(
            year=TruncYear('created_at')
        ).values('year').annotate(
            products_sold=Sum('orderitem__quantity'),
            total_orders=Count('id'),
            total_profits=Sum('payment__amount')
        ).order_by('year')),

        # Transacciones recientes
        'recent_transactions': list(Order.objects.all().order_by('-created_at')[:5].values(
            'id',
            'user__first_name',
            'user__last_name',
            'user__email',
            'status',
            'created_at'
        ).annotate(
            amount=Sum('payment__amount')
        )),
    }

    return JsonResponse(data)

def get_dummy_data(request):
    data = {
        'total_income': 1000000,
        'products_sold_this_month': 100,
        'sales_count': 200,
        'items_in_stock': 500,
        'monthly_profits': [
            {'month': 'Enero', 'total': 100000},
            {'month': 'Febrero', 'total': 150000},
            {'month': 'Marzo', 'total': 200000},
            {'month': 'Abril', 'total': 250000},
            {'month': 'Mayo', 'total': 300000},
            {'month': 'Junio', 'total': 350000},
            {'month': 'Julio', 'total': 400000},
            {'month': 'Agosto', 'total': 450000},
            {'month': 'Septiembre', 'total': 500000},
            {'month': 'Octubre', 'total': 550000},
            {'month': 'Noviembre', 'total': 600000},
            {'month': 'Diciembre', 'total': 650000}
        ],
        'payment_methods_per_year': [
            {'year': 2023, 'payment_method': 'Tarjeta', 'count': 100},
            {'year': 2023, 'payment_method': 'Efectivo', 'count': 150},
            {'year': 2023, 'payment_method': 'Transferencia', 'count': 200},
            {'year': 2024, 'payment_method': 'Tarjeta', 'count': 250},
            {'year': 2024, 'payment_method': 'Efectivo', 'count': 300},
            {'year': 2024, 'payment_method': 'Transferencia', 'count': 350}
        ],
        'best_selling': [
            {'name': 'Producto A', 'total_sold': 1000},
            {'name': 'Producto B', 'total_sold': 900},
            {'name': 'Producto C', 'total_sold': 800},
            {'name': 'Producto D', 'total_sold': 700},
            {'name': 'Producto E', 'total_sold': 600}
        ],
        'most_profitable': [
            {'name': 'Producto A', 'total_profit': 10000},
            {'name': 'Producto B', 'total_profit': 9000},
            {'name': 'Producto C', 'total_profit': 8000},
            {'name': 'Producto D', 'total_profit': 7000},
            {'name': 'Producto E', 'total_profit': 6000}
        ],
        'least_selling': [
            {'name': 'Producto F', 'total_sold': 500},
            {'name': 'Producto G', 'total_sold': 400},
            {'name': 'Producto H', 'total_sold': 300},
            {'name': 'Producto I', 'total_sold': 200},
            {'name': 'Producto J', 'total_sold': 100}
        ],
        'least_profitable': [
            {'name': 'Producto K', 'total_profit': 5000},
            {'name': 'Producto L', 'total_profit': 4000},
            {'name': 'Producto M', 'total_profit': 3000},
            {'name': 'Producto N', 'total_profit': 2000},
            {'name': 'Producto O', 'total_profit': 1000}
        ],
        'transactions_per_day': [
            {'date': '2023-01-01', 'products_sold': 100, 'total_orders': 10, 'total_profits': 10000},
            {'date': '2023-01-02', 'products_sold': 150, 'total_orders': 15, 'total_profits': 15000},
            {'date': '2023-01-03', 'products_sold': 200, 'total_orders': 20, 'total_profits': 20000},
            {'date': '2023-01-04', 'products_sold': 250, 'total_orders': 25, 'total_profits': 25000},
            {'date': '2023-01-05', 'products_sold': 300, 'total_orders': 30, 'total_profits': 30000},
            {'date': '2023-01-06', 'products_sold': 350, 'total_orders': 35, 'total_profits': 35000},
            {'date': '2023-01-07', 'products_sold': 400, 'total_orders': 40, 'total_profits': 40000},
            {'date': '2023-01-08', 'products_sold': 450, 'total_orders': 45, 'total_profits': 45000},
            {'date': '2023-01-09', 'products_sold': 500, 'total_orders': 50, 'total_profits': 50000},
            {'date': '2023-01-10', 'products_sold': 550, 'total_orders': 55, 'total_profits': 55000}
        ],
        'transactions_per_weekday': [
            {'weekday': 0, 'products_sold': 100, 'total_orders': 10, 'total_profits': 10000},
            {'weekday': 1, 'products_sold': 150, 'total_orders': 15, 'total_profits': 15000},
            {'weekday': 2, 'products_sold': 200, 'total_orders': 20, 'total_profits': 20000},
            {'weekday': 3, 'products_sold': 250, 'total_orders': 25, 'total_profits': 25000},
            {'weekday': 4, 'products_sold': 300, 'total_orders': 30, 'total_profits': 30000},
            {'weekday': 5, 'products_sold': 350, 'total_orders': 35, 'total_profits': 35000},
            {'weekday': 6, 'products_sold': 400, 'total_orders': 40, 'total_profits': 40000}
        ],
        'transactions_per_month': [
            {'month': 'Enero', 'products_sold': 100, 'total_orders': 10, 'total_profits': 10000},
            {'month': 'Febrero', 'products_sold': 150, 'total_orders': 15, 'total_profits': 15000},
            {'month': 'Marzo', 'products_sold': 200, 'total_orders': 20, 'total_profits': 20000},
            {'month': 'Abril', 'products_sold': 250, 'total_orders': 25, 'total_profits': 25000},
            {'month': 'Mayo', 'products_sold': 300, 'total_orders': 30, 'total_profits': 30000},
            {'month': 'Junio', 'products_sold': 350, 'total_orders': 35, 'total_profits': 35000},
            {'month': 'Julio', 'products_sold': 400, 'total_orders': 40, 'total_profits': 40000},
            {'month': 'Agosto', 'products_sold': 450, 'total_orders': 45, 'total_profits': 45000},
            {'month': 'Septiembre', 'products_sold': 500, 'total_orders': 50, 'total_profits': 50000},
        ],
        'transactions_per_year': [
            {'year': 2023, 'products_sold': 1000, 'total_orders': 100, 'total_profits': 100000},
            {'year': 2024, 'products_sold': 1500, 'total_orders': 150, 'total_profits': 150000}
        ]
    }

    return JsonResponse(data)
        
    
