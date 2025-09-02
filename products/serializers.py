from rest_framework import serializers
from .models import Shoe, Category, SubCategory, Brand, Coupon

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ["id", "name"]

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ["id", "name"]

class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ["id", "code", "discount_percentage", "active"]


class ShoeSerializer(serializers.ModelSerializer):
    # For write: accept IDs
    brand = serializers.PrimaryKeyRelatedField(queryset=Brand.objects.all())
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    subcategory = serializers.PrimaryKeyRelatedField(queryset=SubCategory.objects.all(), allow_null=True, required=False)
    coupon = serializers.PrimaryKeyRelatedField(queryset=Coupon.objects.all(), allow_null=True, required=False)

    # For read: return nested details
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["brand"] = BrandSerializer(instance.brand).data
        rep["category"] = CategorySerializer(instance.category).data
        rep["subcategory"] = SubCategorySerializer(instance.subcategory).data if instance.subcategory else None
        rep["coupon"] = CouponSerializer(instance.coupon).data if instance.coupon else None
        return rep

    class Meta:
        model = Shoe
        fields = "__all__"