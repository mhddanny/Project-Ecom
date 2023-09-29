from django.contrib import admin
from . models import Product, Variation, ReviewRating, ProductGallery, ProductPaket
import admin_thumbnails

# Register your models here.
@admin_thumbnails.thumbnail('image')
class ProdutGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1

class ProductPaketInline(admin.TabularInline):
    model = ProductPaket
    extra = 0
    fieldsets = [
        (
            None,
            {
                "fields": ["max_weight"],
            },
        ),
        (
            "Advanced options",
            {
                "classes": ["collapse"],
                "fields": ["length", "width", "height"],
            },
        )
    ]
    

@admin.register(Product)
@admin_thumbnails.thumbnail('images')
class ProductAdmin(admin.ModelAdmin):
    '''Admin View for Product'''
    inlines = [
        ProdutGalleryInline,
        ProductPaketInline,
        ]
    list_display = ('product_name', 'price', 'stock', 'category', 'modifield_date', 'is_available')
    prepopulated_fields = {'slug': ('product_name',)}
    
    # list_filter = ('',)
    # raw_id_fields = ('',)
    # readonly_fields = ('',)
    # search_fields = ('',)
    # date_hierarchy = ''
    # ordering = ('',)
    

class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'varian_category', 'variation_value', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('product', 'varian_category', 'variation_value')
admin.site.register(Variation, VariationAdmin)

admin.site.register(ReviewRating)
admin.site.register(ProductGallery)
admin.site.register(ProductPaket)