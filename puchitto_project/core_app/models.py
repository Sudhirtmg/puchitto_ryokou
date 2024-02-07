from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from user_app.models import User
from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField
from weather_app.views import get_weather


STATUS_CHOICE = (
    ("not visit", "旅行先に着てない"),
    ("visited", "旅行先に着いた"),
    ("visiting", "旅行中"),
    ('finished','旅行完了')
)


STATUS = (
    ("unpublished", "unpublished"),
    ("published", "Published"),
)


RATING = (
    (1,  "★☆☆☆☆"),
    (2,  "★★☆☆☆"),
    (3,  "★★★☆☆"),
    (4,  "★★★★☆"),
    (5,  "★★★★★"),
)


def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class Section(models.Model):
    name=models.CharField(max_length=200)
    def __str__(self):
        return self.name

class OutInActivity(models.Model):
    title = models.CharField(max_length=100, default="Food",verbose_name='どのようにして過ごすのが好きですか？',null=True,blank=True)
    class Meta:
        verbose_name_plural = "インドアアウトドア"
    def __str__(self):
        return self.title
    
class Personality(models.Model):
    pcid = ShortUUIDField(unique=True, length=10, max_length=20,prefix="scat", alphabet="abcdefgh12345",verbose_name='id')
    title = models.CharField(max_length=100, default="Food",verbose_name='お気に入りの旅行のアクティビティ何ですか？',null=True,blank=True)
    class Meta:
        verbose_name_plural = "旅行のアクティビティ"
    def __str__(self):
        return self.title
    
class SubCategory(models.Model):
    scid = ShortUUIDField(unique=True, length=10, max_length=20,prefix="scat", alphabet="abcdefgh12345",verbose_name='id')
    title = models.CharField(max_length=100, default="Food",verbose_name='場所の中にあるもの',null=True,blank=True)
    class Meta:
        verbose_name_plural = "場所の中にあるもの"

    def package_count(self):
        return Package.objects.filter(category=self).count()

    def __str__(self):
        return self.title

class Transport(models.Model):
    tid = ShortUUIDField(unique=True, length=10, max_length=20,prefix="scat", alphabet="abcdefgh12345",verbose_name='id')
    title = models.CharField(max_length=100, default="Food",verbose_name='公共交通機関アクセス',null=True,blank=True)
    class Meta:
        verbose_name_plural = "公共交通機関アクセス"
    def __str__(self):
        return self.title  

class Parking(models.Model):
    paid = ShortUUIDField(unique=True, length=10, max_length=20,prefix="scat", alphabet="abcdefgh12345",verbose_name='id')
    title = models.CharField(max_length=100, default="Food",verbose_name='駐車場',null=True,blank=True)
    class Meta:
        verbose_name_plural = "駐車場"
    def __str__(self):
        return self.title 

class Location(models.Model):
    prid = ShortUUIDField(unique=True, length=10, max_length=20,prefix="scat", alphabet="abcdefgh12345",verbose_name='id')
    title = models.CharField(max_length=100, default="Food",verbose_name='都道府県',null=True,blank=True)
    class Meta:
        verbose_name_plural = "都道府県"
    def __str__(self):
        return self.title  
   


class Category(models.Model):
    cid = ShortUUIDField(unique=True, length=10, max_length=20,
                         prefix="cat", alphabet="abcdefgh12345",verbose_name='カテゴリーのid')
    title = models.CharField(max_length=100, default="Food",verbose_name='カテゴリー名')
    image = models.ImageField(upload_to="category", default="category.jpg",verbose_name='カテゴリーの写真')
    class Meta:
        verbose_name_plural = "カテゴリー"

    def category_image(self):
        return mark_safe('<img src="%s" width="150" height="50" />' % (self.image.url))

    def package_count(self):
        return Package.objects.filter(category=self).count()

    def __str__(self):
        return self.title


class Package(models.Model):
    pid = ShortUUIDField(unique=True, length=10, max_length=20, alphabet="abcdefgh12345",verbose_name='パッケージのid')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,verbose_name='ユーザ')
   
 
    activity = models.ForeignKey( OutInActivity, on_delete=models.SET_NULL, null=True,blank=True, related_name="activity",verbose_name='インドアアウトドア❓')
    personality=models.ForeignKey(Personality,on_delete=models.SET_NULL,null=True,blank=True,related_name='personality',verbose_name='お気に入りの旅行のアクティビティ何ですか？❓')
    subcategory = models.ForeignKey( SubCategory, on_delete=models.SET_NULL, null=True, related_name="subcategory",verbose_name='場所の中にあるもの')
    transport = models.ForeignKey( Transport, on_delete=models.SET_NULL, null=True, blank=True,related_name="transport",verbose_name='公共交通機関アクセス')
    parking = models.ForeignKey( Parking, on_delete=models.SET_NULL, null=True, blank=True,related_name="parking",verbose_name='駐車場')
    address = models.ForeignKey( Location, on_delete=models.SET_NULL, null=True, blank=True,related_name="prefecturee",verbose_name='都道府県')

 
   
    category = models.ForeignKey( Category, on_delete=models.SET_NULL, null=True, related_name="category",verbose_name='カテゴリー')
    section=models.ForeignKey(Section,on_delete=models.SET_NULL,null=True,blank=True,verbose_name='セクション')

    title = models.CharField(max_length=100, default="Fresh Pear",verbose_name='パッケージの名')
    image = models.ImageField( upload_to=user_directory_path, default="product.jpg",verbose_name='パッケージの写真')
    description = RichTextField()

    price = models.DecimalField( max_digits=99999999999999, decimal_places=2, default="1.99",verbose_name='金額')


    tags = TaggableManager(blank=True)


    package_status = models.CharField(choices=STATUS, max_length=200, default="unpublished",verbose_name='パッケージのステータス')
    status = models.BooleanField(default=True,verbose_name='ステータス')

    date = models.DateTimeField(auto_now_add=True,verbose_name='日付')
    
    updated = models.DateTimeField(null=True, blank=True,verbose_name='アップデート日付')

    class Meta:
        verbose_name_plural = "パッケージ"

    def package_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

    def __str__(self):
        return self.title

    def get_precentage(self):
        new_price = (self.price / self.old_price) * 100
        return new_price




class PackageImages(models.Model):
    images = models.ImageField(upload_to="package-images", default="package.jpg",verbose_name='追加写真')
    package = models.ForeignKey(Package, related_name="p_images", on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "追加写真"


############################################## Cart, Order, OrderITems and Address ##################################
############################################## Cart, Order, OrderITems and Address ##################################
############################################## Cart, Order, OrderITems and Address ##################################
############################################## Cart, Order, OrderITems and Address ##################################


class Book(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name='ユーザ')
    price = models.DecimalField(max_digits=99999999999999, decimal_places=2, default="1.99",verbose_name='金額')
    paid_status = models.BooleanField(default=False, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=False, null=True, blank=True,verbose_name='予約の日付')
    package_status = models.CharField(choices=STATUS_CHOICE, max_length=300, default="processing",verbose_name='パッケージのステータス')


    class Meta:
        verbose_name_plural = "予約"


class BookPackage(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE,verbose_name='予約')
  
    item = models.CharField(max_length=200)
    image = models.CharField(max_length=200,verbose_name='写真')
    price = models.DecimalField(max_digits=99999999999999, decimal_places=2, default="1.99")

    class Meta:
        verbose_name_plural = "パッケージの予約"

    def booked_img(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" />' % (self.image))


############################################## Product Revew, wishlists, Address ##################################
############################################## Product Revew, wishlists, Address ##################################
############################################## Product Revew, wishlists, Address ##################################
############################################## Product Revew, wishlists, Address ##################################


class PackageReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,verbose_name='ユーザ')
    package = models.ForeignKey( Package, on_delete=models.SET_NULL, null=True, related_name="reviews",verbose_name='パッケージ')
    review = models.TextField(verbose_name='レヴュー')
    rating = models.IntegerField(choices=RATING, default=None)
    date = models.DateTimeField(auto_now_add=True,verbose_name='日付')

    class Meta:
        verbose_name_plural = "パッケージのレヴュー"

    def __str__(self):
        return self.package.title

    def get_rating(self):
        return self.rating


# class wishlist_model(models.Model):
#     user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,verbose_name='ユーザ')
#     package = models.ForeignKey( Package, on_delete=models.SET_NULL, null=True,verbose_name='パッケージ')
#     date = models.DateTimeField(auto_now_add=True,verbose_name='日付')

#     class Meta:
#         verbose_name_plural = "wishlists"

#     def __str__(self):
#         return self.package.title
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    mobile = models.CharField(max_length=300, null=True)
    address = models.CharField(max_length=100, null=True)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "住所"
    



