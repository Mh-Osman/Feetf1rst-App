from django.contrib import admin
from .models import Shoe, Category, SubCategory, Brand, Coupon


# ------------------------
# Shoe Admin
# ------------------------
@admin.register(Shoe)
class ShoeAdmin(admin.ModelAdmin):
    # Display fields in the list view
    list_display = (
        "id", "name", "brand_name", "category_name", "subcategory_name",
        "price", "discounted_price", "stock", "gender",
        "is_featured", "is_active", "created_at"
    )

    # Filters for sidebar
    list_filter = ("brand", "category", "subcategory", "gender", "is_featured", "is_active")

    # Searchable fields
    search_fields = ("name", "SKU", "barcode", "color", "material")

    # Default ordering
    ordering = ("-created_at",)

    # Read-only fields (calculated or auto-generated)
    readonly_fields = ("discounted_price", "last_discount_percentage", "created_at", "updated_at")

    # Optional: show related names instead of IDs
    def brand_name(self, obj):
        return obj.brand.name
    brand_name.admin_order_field = 'brand'
    brand_name.short_description = 'Brand'

    def category_name(self, obj):
        return obj.category.name
    category_name.admin_order_field = 'category'
    category_name.short_description = 'Category'

    def subcategory_name(self, obj):
        return obj.subcategory.name if obj.subcategory else "-"
    subcategory_name.admin_order_field = 'subcategory'
    subcategory_name.short_description = 'SubCategory'


# ------------------------
# Category Admin
# ------------------------
class SubCategoryInline(admin.TabularInline):
    model = SubCategory
    extra = 1  # allow adding 1 new subcategory inline

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
    inlines = [SubCategoryInline]  # Inline SubCategory editing


# ------------------------
# SubCategory Admin
# ------------------------
@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category")
    search_fields = ("name",)
    list_filter = ("category",)


# ------------------------
# Brand Admin
# ------------------------
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


# ------------------------
# Coupon Admin
# ------------------------
@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ("id", "code", "discount_percentage", "active")
    list_filter = ("active",)
    search_fields = ("code",)
