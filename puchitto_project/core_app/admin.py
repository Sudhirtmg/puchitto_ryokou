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
# 検索
    
class SectionAdmin(admin.ModelAdmin):
    list_display=['name']
 
class InOutAdmin(admin.ModelAdmin):
    list_display=['title']
     
class PersonalityAdmin(admin.ModelAdmin):
    list_display=['title']
     
class SubCategoryAdmin(admin.ModelAdmin):
    list_display=['title']
     
class TransportAdmin(admin.ModelAdmin):
    list_display=['title']
     
class ParkingAdmin(admin.ModelAdmin):
    list_display=['title']
     
class LocationAdmin(admin.ModelAdmin):
    list_display=['title']
 


admin.site.register(Package,PackageAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Book,BookAdmin)
admin.site.register(BookPackage,BookPackageAdmin)
admin.site.register(PackageReview,PackageReviewAdmin)
admin.site.register(Section,SectionAdmin)


admin.site.register(OutInActivity,InOutAdmin)
admin.site.register(Personality,PersonalityAdmin)
admin.site.register(SubCategory,SubCategoryAdmin)
admin.site.register(Transport,TransportAdmin)
admin.site.register(Parking,ParkingAdmin)
admin.site.register(Location,LocationAdmin)

    
    