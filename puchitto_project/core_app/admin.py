from django.contrib import admin
from core_app.models import *
# Register your models here.


class PackageImagesAdmin(admin.TabularInline):
    model=PackageImages
class PackageAdmin(admin.ModelAdmin):
    inlines=[PackageImagesAdmin]
    list_display=['title','package_image','price','package_status','status','pid']
class CategoryAdmin(admin.ModelAdmin):
    list_display=['title','category_image']
class BookAdmin(admin.ModelAdmin):
    list_display=['user','price','paid_status','date']
class BookPackageAdmin(admin.ModelAdmin):
    list_display=['book','booked_img','price']
class PackageReviewAdmin(admin.ModelAdmin):
    list_display=['user','package','review','rating','date']

admin.site.register(Package,PackageAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Book,BookAdmin)
admin.site.register(BookPackage,BookPackageAdmin)
admin.site.register(PackageReview,PackageReviewAdmin)
admin.site.register(Section)
    
    