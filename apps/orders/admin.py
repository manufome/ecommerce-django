from django.contrib import admin
from django.utils.html import format_html
from apps.orders.models import Address, Order, OrderItem, Payment, Coupon, Refund


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('subtotal_display',)
    fields = ('product', 'quantity', 'price', 'subtotal_display')
    
    def subtotal_display(self, obj):
        if obj.id:
            return format_html(
                '<strong>${}</strong>',
                obj.subtotal
            )
        return '-'
    subtotal_display.short_description = 'Subtotal'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status_badge', 'total_display', 'payment_method_display', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'user__email', 'billing_address__first_name', 'billing_address__last_name')
    readonly_fields = ('created_at', 'total_display')
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Información del Cliente', {
            'fields': ('user', 'status')
        }),
        ('Direcciones', {
            'fields': ('billing_address', 'shipping_address')
        }),
        ('Detalles del Pedido', {
            'fields': ('coupon', 'notes', 'total_display')
        }),
        ('Fechas', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_shipped', 'mark_as_delivered', 'cancel_order']
    
    def status_badge(self, obj):
        colors = {
            'P': '#ffc107',  # Pendiente - Amarillo
            'S': '#17a2b8',  # Enviado - Azul
            'D': '#28a745',  # Entregado - Verde
            'C': '#dc3545',  # Cancelado - Rojo
        }
        labels = {
            'P': 'Pendiente',
            'S': 'Enviado',
            'D': 'Entregado',
            'C': 'Cancelado',
        }
        color = colors.get(obj.status, '#6c757d')
        label = labels.get(obj.status, obj.status)
        return format_html(
            '<span style="background: {}; color: white; padding: 5px 10px; border-radius: 3px; font-weight: bold;">{}</span>',
            color, label
        )
    status_badge.short_description = 'Estado'
    
    def total_display(self, obj):
        if obj.id:
            total = sum(item.subtotal for item in obj.orderitem_set.all())
            return format_html(
                '<span style="font-size: 16px; font-weight: bold; color: #28a745;">${}</span>',
                total
            )
        return '-'
    total_display.short_description = 'Total'
    
    def payment_method_display(self, obj):
        try:
            payment = obj.payment_set.first()
            if payment:
                methods = dict(payment._meta.get_field('payment_method').choices)
                return methods.get(payment.payment_method, '-')
        except:
            pass
        return '-'
    payment_method_display.short_description = 'Método de Pago'
    
    def mark_as_shipped(self, request, queryset):
        updated = queryset.update(status='S')
        self.message_user(request, f'{updated} pedidos marcados como enviados.')
    mark_as_shipped.short_description = 'Marcar como enviado'
    
    def mark_as_delivered(self, request, queryset):
        updated = queryset.update(status='D')
        self.message_user(request, f'{updated} pedidos marcados como entregados.')
    mark_as_delivered.short_description = 'Marcar como entregado'
    
    def cancel_order(self, request, queryset):
        updated = queryset.update(status='C')
        self.message_user(request, f'{updated} pedidos cancelados.')
    cancel_order.short_description = 'Cancelar pedido'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price', 'subtotal_display')
    list_filter = ('order__status',)
    search_fields = ('product__name', 'order__id')
    
    def subtotal_display(self, obj):
        return format_html(
            '<strong>${}</strong>',
            obj.subtotal
        )
    subtotal_display.short_description = 'Subtotal'


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'street_type', 'locality_display', 'phone', 'address_type_badge')
    list_filter = ('locality', 'street_type', 'address_type')
    search_fields = ('user__username', 'first_name', 'last_name', 'phone', 'email')
    
    def full_name(self, obj):
        return f'{obj.first_name} {obj.last_name}'
    full_name.short_description = 'Nombre Completo'
    
    def locality_display(self, obj):
        localities = dict(obj._meta.get_field('locality').choices)
        return localities.get(obj.locality, obj.locality)
    locality_display.short_description = 'Localidad'
    
    def address_type_badge(self, obj):
        if obj.address_type == 'B':
            return format_html(
                '<span style="background: #007bff; color: white; padding: 3px 8px; border-radius: 3px;">Facturación</span>'
            )
        return format_html(
            '<span style="background: #28a745; color: white; padding: 3px 8px; border-radius: 3px;">Envío</span>'
        )
    address_type_badge.short_description = 'Tipo'


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'amount', 'shipping_cost', 'payment_method_display', 'status_badge', 'timestamp')
    list_filter = ('payment_method', 'status', 'timestamp')
    readonly_fields = ('timestamp', 'shipping_cost')
    
    def payment_method_display(self, obj):
        methods = dict(obj._meta.get_field('payment_method').choices)
        return methods.get(obj.payment_method, obj.payment_method)
    payment_method_display.short_description = 'Método de Pago'
    
    def status_badge(self, obj):
        colors = {
            'P': '#ffc107',
            'C': '#28a745',
            'F': '#dc3545',
        }
        color = colors.get(obj.status, '#6c757d')
        statuses = dict(obj._meta.get_field('status').choices)
        label = statuses.get(obj.status, obj.status)
        return format_html(
            '<span style="background: {}; color: white; padding: 3px 8px; border-radius: 3px;">{}</span>',
            color, label
        )
    status_badge.short_description = 'Estado'


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount', 'active', 'active_badge', 'valid_from', 'valid_to')
    list_filter = ('active', 'valid_from', 'valid_to')
    search_fields = ('code',)
    list_editable = ('active',)
    
    def active_badge(self, obj):
        if obj.active:
            return format_html(
                '<span style="background: #28a745; color: white; padding: 3px 8px; border-radius: 3px;">Activo</span>'
            )
        return format_html(
            '<span style="background: #6c757d; color: white; padding: 3px 8px; border-radius: 3px;">Inactivo</span>'
        )
    active_badge.short_description = 'Estado'


@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    list_display = ('order', 'user_display', 'reason_short', 'accepted_badge', 'created_at')
    list_filter = ('accepted', 'created_at')
    search_fields = ('order__id', 'order__user__username', 'reason')
    readonly_fields = ('created_at',)
    
    def user_display(self, obj):
        return obj.order.user.username
    user_display.short_description = 'Usuario'
    
    def reason_short(self, obj):
        return obj.reason[:50] + '...' if len(obj.reason) > 50 else obj.reason
    reason_short.short_description = 'Razón'
    
    def accepted_badge(self, obj):
        if obj.accepted:
            return format_html(
                '<span style="background: #28a745; color: white; padding: 3px 8px; border-radius: 3px;">Aceptado</span>'
            )
        return format_html(
            '<span style="background: #ffc107; color: black; padding: 3px 8px; border-radius: 3px;">Pendiente</span>'
        )
    accepted_badge.short_description = 'Estado'
