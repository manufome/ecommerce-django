from django.contrib import admin
from django.utils.html import format_html
from .models import Brand, Category, Product, Wishlist, ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('url', 'width', 'height')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'brand', 'display_price', 'discount', 'stock', 'status_badges', 'created_at')
    list_filter = ('category', 'brand', 'is_new', 'is_top', 'is_featured', 'created_at')
    search_fields = ('name', 'description', 'slug')
    list_editable = ('discount', 'stock')
    readonly_fields = ('created_at', 'updated_at', 'display_price_info')
    inlines = [ProductImageInline]
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('name', 'slug', 'description')
        }),
        ('Precios e Inventario', {
            'fields': ('price', 'discount', 'discount_end_date', 'stock', 'display_price_info')
        }),
        ('Clasificación', {
            'fields': ('category', 'brand', 'is_new', 'is_top', 'is_featured')
        }),
        ('Valoraciones', {
            'fields': ('ratings', 'reviews_count')
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_featured', 'mark_as_new', 'remove_discount']
    
    def display_price(self, obj):
        prices = obj.get_display_price()
        if prices[0] != prices[1]:
            return format_html(
                '<span style="color: #28a745; font-weight: bold;">${}</span> '
                '<span style="text-decoration: line-through; color: #6c757d;">${}</span>',
                prices[0], prices[1]
            )
        return f'${prices[0]}'
    display_price.short_description = 'Precio'
    
    def display_price_info(self, obj):
        if obj.check_discount():
            prices = obj.get_display_price()
            return format_html(
                '<div style="padding: 10px; background: #d4edda; border: 1px solid #c3e6cb; border-radius: 5px;">'
                '<strong>Precio con descuento:</strong> ${}<br>'
                '<strong>Precio original:</strong> ${}<br>'
                '<strong>Ahorro:</strong> ${} ({}%)'
                '</div>',
                prices[0], prices[1], prices[1] - prices[0], obj.discount
            )
        return format_html(
            '<div style="padding: 10px; background: #f8f9fa; border: 1px solid #dee2e6; border-radius: 5px;">'
            'No hay descuento activo'
            '</div>'
        )
    display_price_info.short_description = 'Información de Precio'
    
    def status_badges(self, obj):
        badges = []
        if obj.is_new:
            badges.append('<span style="background: #007bff; color: white; padding: 3px 8px; border-radius: 3px; margin-right: 5px;">Nuevo</span>')
        if obj.is_featured:
            badges.append('<span style="background: #ffc107; color: black; padding: 3px 8px; border-radius: 3px; margin-right: 5px;">Destacado</span>')
        if obj.is_top:
            badges.append('<span style="background: #28a745; color: white; padding: 3px 8px; border-radius: 3px;">Top</span>')
        return format_html(''.join(badges)) if badges else '-'
    status_badges.short_description = 'Estado'
    
    def mark_as_featured(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} productos marcados como destacados.')
    mark_as_featured.short_description = 'Marcar como destacado'
    
    def mark_as_new(self, request, queryset):
        updated = queryset.update(is_new=True)
        self.message_user(request, f'{updated} productos marcados como nuevos.')
    mark_as_new.short_description = 'Marcar como nuevo'
    
    def remove_discount(self, request, queryset):
        updated = queryset.update(discount=0)
        self.message_user(request, f'Descuento eliminado de {updated} productos.')
    remove_discount.short_description = 'Eliminar descuento'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'product_count')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    mptt_level_indent = 20
    
    def product_count(self, obj):
        count = obj.products.count()
        return format_html(
            '<span style="background: #17a2b8; color: white; padding: 2px 8px; border-radius: 10px;">{}</span>',
            count
        )
    product_count.short_description = 'Productos'


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_count')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    
    def product_count(self, obj):
        count = obj.products.count()
        return format_html(
            '<span style="background: #6c757d; color: white; padding: 2px 8px; border-radius: 10px;">{}</span>',
            count
        )
    product_count.short_description = 'Productos'


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'product_count', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at',)
    filter_horizontal = ('products',)
    
    def product_count(self, obj):
        count = obj.products.count()
        return format_html(
            '<span style="background: #dc3545; color: white; padding: 2px 8px; border-radius: 10px;">{}</span>',
            count
        )
    product_count.short_description = 'Productos'
