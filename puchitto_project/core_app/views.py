from django.shortcuts import render,redirect, get_object_or_404
from core_app.models import *
from django.db.models import Count, Avg
from core_app.forms import *
from django.http import JsonResponse
from django.contrib import messages
from taggit.models import Tag
from django.template.loader import render_to_string
from user_app.forms import *
import calendar
from django.db.models.functions import ExtractMonth
# Create your views here.
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required

"========================================================================================================================================="
"========================================================================================================================================="

def index(request):
    # Get all distinct section names
    section_names = Section.objects.values_list('name', flat=True).distinct()
    

    # Create a dictionary to store packages for each section
    section_packages = {}

    # Loop through section names and filter packages for each section
    for section_name in section_names:
        packages = Package.objects.filter(section__name=section_name,package_status='published',status=True)
        section_packages[section_name] = packages
    package=Package.objects.filter(package_status='published',status=True)
    context = {
        'section_packages': section_packages,
        'package':package
        
    }

    return render(request, 'Main/index.html', context)




"========================================================================================================================================="
# category
"========================================================================================================================================="
def category_list(rq):
    categories=Category.objects.all()
    context={
        'categories':categories
    }
    return render(rq,'category/category.html',context)





def category_product_list(rq,cid):
    category=Category.objects.get(cid=cid)
    package = Package.objects.filter(package_status="published", category=category)

    context={
        'category':category,
        'package':package
    }
    return render(rq,'category/category-product-list.html',context)





"========================================================================================================================================="
# package
"========================================================================================================================================="

def Package_List(rq):
    packages=Package.objects.filter(package_status='published',status=True)
    category=Category.objects.all()
    CATID=rq.GET.get('categories')
    if CATID:
     packages = Package.objects.filter(category=CATID, package_status='published', status=True)
    else:
         packages=Package.objects.filter(package_status='published',status=True)

    context={
        'packages':packages,
        'category':category
    }
    return render(rq,'package/package_list.html',context)


"========================================================================================================================================="



def Package_detail(rq,pid):
    package=Package.objects.get(pid=pid)
    packages=Package.objects.filter(category=package.category).exclude(pid=pid)
    p_image=package.p_images.all()
    average_rating = PackageReview.objects.filter(package=package).aggregate(rating=Avg('rating'))
    form=PackageReviewForm()
    reviews = PackageReview.objects.filter(package=package).order_by("-date")
    rating_counts = PackageReview.objects.filter(package=package).values('rating').annotate(count=Count('rating'))
    total_reviews = PackageReview.objects.filter(package=package).count()
    packagess = get_object_or_404(Package, pid=pid)

    # Get weather information for the package's prefecture

    # Product Review form
    context={
        'package':package,
        'p_image':p_image,
        'packages':packages,
        "average_rating": average_rating,
        'form':form,
        'reviews':reviews,
        'rating_counts': rating_counts,
        'total_reviews':total_reviews,
        'packagess':packagess,

    }
    return render(rq,'package/package-detail.html',context)




"========================================================================================================================================="  



def package_tag(rq,tag_slug=None):
    package=Package.objects.filter(package_status='published',status=True)
    tag=None
    if tag_slug:
        tag=get_object_or_404(Tag,slug=tag_slug)
        package=package.filter(tags__in=[tag])
    context={
        'package':package,
        'tag':tag
    }
    return render(rq,'package/tag.html',context)




"========================================================================================================================================="

def ajax_add_review(request, pid):
    package = Package.objects.get(pk=pid)
    user = request.user 

    review = PackageReview.objects.create(
        user=user,
        package=package,
        review = request.POST['review'],
        rating = request.POST['rating'],
    )

    context = {
        'user': user.username,
        'review': request.POST['review'],
        'rating': request.POST['rating'],
    }

    average_reviews = PackageReview.objects.filter(package=package).aggregate(rating=Avg("rating"))
    return JsonResponse({
        'bool':True,
        'context':context,
        'average_reviews':average_reviews
    })
    

"========================================================================================================================================="

@login_required

def add_to_book(request):
    book_package = {}

    book_package[str(request.GET['id'])] = {
        'title': request.GET['title'],
        'qty': request.GET['qty'],
        'price': request.GET['price'],
        'image': request.GET['image'],
        'pid': request.GET['pid'],
    }

    if 'book_data_obj' in request.session:
        if str(request.GET['id']) in request.session['book_data_obj']:

            book_data = request.session['book_data_obj']
            book_data[str(request.GET['id'])]['qty'] = int(book_package[str(request.GET['id'])]['qty'])
            book_data.update(book_data)
            request.session['book_data_obj'] = book_data
        else:
            book_data = request.session['book_data_obj']
            book_data.update(book_package)
            request.session['book_data_obj'] = book_data

    else:
        request.session['book_data_obj'] = book_package
    return JsonResponse({"data":request.session['book_data_obj'], 'totalbookitems': len(request.session['book_data_obj'])})



"========================================================================================================================================="


@login_required

def cart_view(request):
    cart_total_amount = 0
    if 'book_data_obj' in request.session:
        for package_id, item in request.session['book_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
        return render(request, "package/book/book.html", {"book_data":request.session['book_data_obj'], 'totalbookitems': len(request.session['book_data_obj']), 'cart_total_amount':cart_total_amount})
    else:
        messages.warning(request, "Your cart is empty")
        return redirect("index")


@login_required

def delete_item_from_cart(request):
    package_id = str(request.GET['id'])
    if 'book_data_obj' in request.session:
        if package_id in request.session['book_data_obj']:
            book_data = request.session['book_data_obj']
            del request.session['book_data_obj'][package_id]
            request.session['book_data_obj'] = book_data
    
    cart_total_amount = 0
    if 'book_data_obj' in request.session:
        for p_id, item in request.session['book_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])

    context = render_to_string("package/book/book-list.html", {"book_data":request.session['book_data_obj'], 'totalbookitems': len(request.session['book_data_obj']), 'cart_total_amount':cart_total_amount})
    return JsonResponse({"data": context, 'totalbookitems': len(request.session['book_data_obj'])})



@login_required

def update_cart(request):
    package_id = str(request.GET['id'])
    package_qty = request.GET['qty']

    if 'book_data_obj' in request.session:
        if package_id in request.session['book_data_obj']:
            book_data = request.session['book_data_obj']
            book_data[str(request.GET['id'])]['qty'] = package_qty
            request.session['book_data_obj'] = book_data
    
    cart_total_amount = 0
    if 'book_data_obj' in request.session:
        for package_id, item in request.session['book_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])

    context = render_to_string("package/book/book-list.html", {"book_data":request.session['book_data_obj'], 'totalbookitems': len(request.session['book_data_obj']), 'cart_total_amount':cart_total_amount})
    return JsonResponse({"data": context, 'totalbookitems': len(request.session['book_data_obj'])})



@login_required

def checkout_view(request):
    cart_total_amount = 0
    total_amount = 0

    # Checking if cart_data_obj session exists
    if 'book_data_obj' in request.session:

        # Getting total amount for Paypal Amount
        for p_id, item in request.session['book_data_obj'].items():
            total_amount += int(item['qty']) * float(item['price'])

        # Create ORder Object
        book = Book.objects.create(
            user=request.user,
            price=total_amount
        )

        # Getting total amount for The Cart
        for package_id, item in request.session['book_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])

            book_package = BookPackage.objects.create(
                book=book,
                item=item['title'],
                image=item['image'],
                price=item['price'],
            )

        host = request.get_host()


   

        return render(request, "package/book/checkout.html", 
                      {"book_data":request.session['book_data_obj'], 
                       'totalbookitems': len(request.session['book_data_obj']), 
                       'cart_total_amount':cart_total_amount,
                         })









def search(request):
    if request.method == 'POST':
        stepone_form = Stepone(request.POST)
        steptwo_form = Steptwo(request.POST)
        stepthree_form = Stepthree(request.POST)
        stepfour_form = Stepfour(request.POST)
        stepfive_form=Stepfive(request.POST)
        stepsix_form=Stepsix(request.POST)




        if stepone_form.is_valid() and steptwo_form.is_valid() and stepthree_form.is_valid() and stepfour_form.is_valid() and stepfive_form.is_valid() and stepsix_form.is_valid():
            activities = stepone_form.cleaned_data.get('activities')
            personalities=steptwo_form.cleaned_data.get('personalities')
            subcategories = stepthree_form.cleaned_data.get('subcategories')
            transports = stepfour_form.cleaned_data.get('transports')
            parkings=stepfive_form.cleaned_data.get('parkings')
            addresses=stepsix_form.cleaned_data.get('addresses')
           
            if activities:
                packages = Package.objects.filter(activity__in=activities)
            
            elif personalities:
                 packages = Package.objects.filter(personality__in=personalities)
 
            elif subcategories:
                packages = Package.objects.filter(subcategory__in=subcategories)
           
            elif transports:
                packages = Package.objects.filter(transport__in=transports)
           
            elif parkings:
                packages = Package.objects.filter(parking__in=parkings)
           
            elif addresses:
                packages = Package.objects.filter(address__in=addresses)
      
            else:
                packages = Package.objects.all()
            return render(request, 'search/search_result.html', {'packages': packages})
    else:
        stepone_form = Stepone()
        steptwo_form=Steptwo()
        stepthree_form=Stepthree()
        stepfour_form=Stepfour()
        stepfive_form=Stepfive()
        stepsix_form=Stepsix()


    context={
        'stepone_form':stepone_form,
        'steptwo_form':steptwo_form,
        'stepthree_form':stepthree_form,
        'stepfour_form':stepfour_form,
        'stepfive_form':stepfive_form,
        'stepsix_form':stepsix_form,

    }
    return render(request,'search/search.html',context)



@login_required

def customer_dashboard(request):
    book_list = Book.objects.filter(user=request.user).order_by('-id')
    address = Address.objects.filter(user=request.user)
    profile = Profile.objects.filter(user=request.user)
    
    # Assuming you want to get the count of books per month
    books = Book.objects.annotate(month=ExtractMonth("date")).values("month").annotate(count=Count("id")).values("month", "count")
    
    month = []

    for book in books:
        if "month" in book and isinstance(book["month"], int) and 1 <= book["month"] <= 12:
            month.append(calendar.month_name[book["month"]])
        else:
            # Handle the case where "month" key is missing or has an invalid value
            # You might want to log a warning or handle it based on your application's logic
            pass

    total_books = [book["count"] for book in books]

    context = {
        'book_list': book_list,
        'address': address,
        'profile': profile,
        'total_books': total_books,
        'month': month,
    }

    return render(request, 'User_Auth/dashboard.html', context)



@login_required
def book_detail(request, id):
    book = Book.objects.get(user=request.user, id=id)
    book_package= BookPackage.objects.filter(book=book)

    
    context = {
        "book_package":book_package,
    }
    return render(request, 'User_Auth/book-detail.html', context)


def contact(request):
    return render(request, "User_Auth/contact.html")


def ajax_contact_form(request):
    full_name = request.GET['full_name']
    email = request.GET['email']
    phone = request.GET['phone']
    subject = request.GET['subject']
    message = request.GET['message']

    contact = ContactUs.objects.create(
        full_name=full_name,
        email=email,
        phone=phone,
        subject=subject,
        message=message,
    )

    data = {
        "bool": True,
        "message": "メッセージを送りました。"
    }

    return JsonResponse({"data":data})


def filter_package(request):
    categories = request.GET.getlist("category[]")
    
    package=Package.objects.filter(package_status='published',status=True).order_by('-id').distinct()
    if len(categories) > 0:
        package = package.filter(category__id__in=categories).distinct() 
    else:
       package=Package.objects.filter(package_status='published',status=True).order_by('-id').distinct()

    data = render_to_string("package/filter/product-list.html", {"package": package})
    return JsonResponse({"data": data})



