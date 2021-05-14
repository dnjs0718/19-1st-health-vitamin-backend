import json
import datetime

from django.views import View
from django.http  import JsonResponse

from .models      import Product, ShippingFee, Image, Option, Discount, SubCategoryProduct,MainCategory
from users.models import Review,ReviewImage

class ProductDetailView(View):
    def get(self, request, product_id):
        try: 
            if not Product.objects.filter(id=product_id).exists():
                return JsonResponse({'MESSAGE' : 'PRODUCT_DOES_NOT_EXIST'}, status=404)

            product = Product.objects.get(id=product_id)

            if product.is_option:
                return JsonResponse({'MESSAGE' : 'NOT_FOUND'}, status=400)
            
            images = product.image_set.all()
            detail_images = [
                    {
                        'image_id'  : image.id,
                        'image_url' : image.image_url
                        }
                    for image in images]

            options      = Option.objects.filter(product=product_id)
            option_items = [
                {
                    'id'        : option.option.id,
                    'name'      : option.option.name,
                    'price'     : option.option.price,
                    'image_id'  : option.option.image_set.first().id,
                    'image_url' : option.option.image_set.first().image_url
                    }
                for option in options
                ]

            result = [
                {
                    'id'            : product.id,
                    'name'          : product.name,
                    'price'         : product.price,
                    'stock'         : product.stock,
                    'detail'        : product.detail,
                    'shipping_fee'  : product.shipping_fee.price,
                    'minimum_free'  : product.shipping_fee.minimum_free,
                    'discount'      : product.discount.rate,
                    'detail_images' : detail_images,
                    'option_items'  : option_items,
                        }
                    ]

            return JsonResponse({'MESSAGE' : 'SUCCESS', 'RESULT' : result}, status=200)

        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status=400)
        except ValueError:
            return JsonResponse({'MESSAGE' : 'VALUE_ERROR'}, status=400)

class CategoryView(View):
    def get(self,request):
            category_list = [{
                'main_category_id'   : category.id,
                'main_category_name' : category.name,
                'main_category_list' : [{'category_id'  : subcategory.id,
                                         'category_name' : subcategory.name
                                        } for subcategory in category.subcategory_set.all()]
                } for category in MainCategory.objects.all()]

            return JsonResponse({'category': category_list}, status = 200)
    
class ProductlistView(View):
    def get(self,request,sub_category_id):
        try:
            ALL_PRODUCTS = 0
            products     = Product.objects.filter(sub_category__id=sub_category_id)
            limit        = int(request.GET.get('limit', 16))
            offset       = int(request.GET.get('offset', 0))
            
            if sub_category_id == ALL_PRODUCTS:
                products = Product.objects.all()

            product_list = [{
                    'name'       : product.name,
                    'price'      : product.price,
                    'expired_at' : product.expired_at,
                    'is_best'    : product.is_best,
                    'discount'   : product.discount.rate,
                    'image'      : product.image_set.first().image_url,
                    'id'         : product.id
                    } for product in products if not product.is_option]
                    
            return JsonResponse({'product': product_list[offset:offset+limit], 'total' : len(product_list)} ,status = 200)
        
        except Product.DoesNotExist:
            return JsonResponse({'MESSAGE':"PRODUCT_DOES_NOT_EXIST"}, status = 400)

class ProductReviewView(View):
    def get(self,request):
        try:
            reviews = Review.objects.select_related('product','user').all().order_by('uploaded_at')[:10]
            main_page_review_list=[{
                    'review_id'         : review.id,
                    'product_name'      : review.product.name,
                    'product_image'     : review.product.image_set.all().first().image_url,
                    'user_account'      : review.user.account,
                    'user_age'          : datetime.datetime.today().year - int(str(review.user.date_of_birth)[:4]) +1,
                    'user_review'       : review.text,
                    'uploaded_at'       : review.uploaded_at,
                    'updated_at'        : review.updated_at,
                    'user_review_image' : review.reviewimage_set.get(review=review).image_url if review.reviewimage_set.filter(review=review) else None,
                    'gender'            : review.user.gender
                    } for review in reviews]

            return JsonResponse({'MAIN_PAGE_REVIEW' : main_page_review_list}, status = 200)

        except Review.DoesNotExist:
            return JsonResponse({'MESSAGE':'REVIEW_DOES_NOT_EXIST'}, status=404)

class BestProductView(View):
    def get(self,request):
        try:
            products = Product.objects.all().order_by('stock')
            best_product_list=[{
                        'name'       : product.name,
                        'price'      : product.price,
                        'discount'   : product.discount.rate,
                        'image'      : product.image_set.first().image_url,
                        'product_id' : product.id
                        } for product in products if product.is_best==1][:8]

            return JsonResponse({'BEST_PRODUCT' : best_product_list}, status = 200)

        except Product.DoesNotExist:
            return JsonResponse({'MESSAGE': 'PRODUCT_DOES_NOT_EXIST'},status =404)

class HashTagView(View):
    def get(self,request,sub_category_id):    
        try:
            if not sub_category_id in [1, 3, 5, 6]:
                return JsonResponse({'MESSAGE':'CHECK_YOUR_CATEGORY_NUMBER'}, status=404)
                
            sub_products = SubCategoryProduct.objects.filter(id=sub_category_id,product__is_best=1)
            product_list = [{
                        'name'       : sub_product.product.name,
                        'price'      : sub_product.product.price,
                        'discount'   : Discount.objects.get(id=sub_product.product.discount_id).rate,
                        'image'      : Image.objects.filter(product_id=sub_product.product.id).first().image_url,
                        'product_id' : sub_product.product.id
                        } for sub_product in sub_products][:3]

            return JsonResponse({'PRODUCT_LIST':product_list}, status = 200)

        except Product.DoesNotExist:
            return JsonResponse({'MESSAGE': 'PRODUCT_DOES_NOT_EXIST'},status =404)