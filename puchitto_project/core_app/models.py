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
PREFECTURE_CHOICES = [
        ('', '都道府県を選択してください'),
        ('Hokkaido', '北海道'),
        ('Aomori', '青森県'),
        ('Iwate', '岩手県'),
        ('Miyagi', '宮城県'),
        ('Akita', '秋田県'),
        ('Yamagata', '山形県'),
        ('Fukushima', '福島県'),
        ('Ibaraki', '茨城県'),
        ('Tochigi', '栃木県'),
        ('Gunma', '群馬県'),
        ('Saitama', '埼玉県'),
        ('Chiba', '千葉県'),
        ('Tokyo', '東京都'),
        ('Kanagawa', '神奈川県'),
        ('Niigata', '新潟県'),
        ('Toyama', '富山県'),
        ('Ishikawa', '石川県'),
        ('Fukui', '福井県'),
        ('Yamanashi', '山梨県'),
        ('Nagano', '長野県'),
        ('Gifu', '岐阜県'),
        ('Shizuoka', '静岡県'),
        ('Aichi', '愛知県'),
        ('Mie', '三重県'),
        ('Shiga', '滋賀県'),
        ('Kyoto', '京都府'),
        ('Osaka', '大阪府'),
        ('Hyogo', '兵庫県'),
        ('Nara', '奈良県'),
        ('Wakayama', '和歌山県'),
        ('Tottori', '鳥取県'),
        ('Shimane', '島根県'),
        ('Okayama', '岡山県'),
        ('Hiroshima', '広島県'),
        ('Yamaguchi', '山口県'),
        ('Tokushima', '徳島県'),
        ('Kagawa', '香川県'),
        ('Ehime', '愛媛県'),
        ('Kochi', '高知県'),
        ('Fukuoka', '福岡県'),
        ('Saga', '佐賀県'),
        ('Nagasaki', '長崎県'),
        ('Kumamoto', '熊本県'),
        ('Oita', '大分県'),
        ('Miyazaki', '宮崎県'),
        ('Kagoshima', '鹿児島県'),
        ('Okinawa', '沖縄県'),
    ]
SEARCH=[
        ('', 'どのような場所に行きたいですか'),
        ('animal','生物がいる場所'),
        ('water','海がある所'),
        ('exercise','運動ができる場所'),
        ('historical_place','歴史を感じれる場所'),
        ('cultural_place','お寺がある場所'),
        ('eating_place','食べる所')


]

def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class Section(models.Model):
    name=models.CharField(max_length=200)
    def __str__(self):
        return self.name



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
    category = models.ForeignKey( Category, on_delete=models.SET_NULL, null=True, related_name="category",verbose_name='カテゴリー')
    section=models.ForeignKey(Section,on_delete=models.SET_NULL,null=True,verbose_name='セクション')
    search=models.CharField(choices=SEARCH,max_length=50,default='select')

    title = models.CharField(max_length=100, default="Fresh Pear",verbose_name='パッケージの名')
    image = models.ImageField( upload_to=user_directory_path, default="product.jpg",verbose_name='パッケージの写真')
    description = RichTextField()
    specification=RichTextField(default="詳細")

    price = models.DecimalField( max_digits=99999999999999, decimal_places=2, default="1.99",verbose_name='金額')
    prefecture=models.CharField(choices=PREFECTURE_CHOICES,max_length=200,default='東京', verbose_name='都道府県')
    location=models.CharField(max_length=200,verbose_name='場所')

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
    def get_weather_info(self):
        # Get weather information using the get_weather function
        weather_info = get_weather(self.prefecture)
        return weather_info



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
    



