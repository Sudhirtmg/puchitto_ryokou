from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
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
class User(AbstractUser):
    
    email=models.EmailField(unique=True,verbose_name='メールアドレス')
    username=models.CharField(max_length=200, verbose_name='ユーザ名')
    location=models.CharField(choices=PREFECTURE_CHOICES,max_length=200,default='東京', verbose_name='都道府県')

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username']
    def __str__(self):
        return self.username
    
class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    first_name=models.CharField(max_length=200,null=True,blank=True)
    email=models.EmailField(unique=True)
    username=models.CharField(max_length=200)
    last_name=models.CharField(max_length=200,null=True,blank=True)
    location=models.CharField(choices=PREFECTURE_CHOICES,max_length=200,default='東京', verbose_name='都道府県')
    
    verified=models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    
class ContactUs(models.Model):
    full_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=200) # +234 (456) - 789
    subject = models.CharField(max_length=200) # +234 (456) - 789
    message = models.TextField()

    class Meta:
        verbose_name = "お問い合わせ"
        verbose_name_plural = "お問い合わせ"

    def __str__(self):
        return self.full_name

