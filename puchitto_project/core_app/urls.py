from django.urls import path,include
from core_app import views
urlpatterns = [
 path('',views.index,name='index'),
 path('package-list/',views.Package_List,name='package'),
 path('package/<pid>',views.Package_detail,name='package-detail'),

 path('category/',views.category_list,name="category"),
 path('category_product_list/<cid>/',views.category_product_list,name="category-product-list"),

 path('search/',views.search,name="search"),
 
path('tag/<slug:tag_slug>/',views.package_tag,name='tag'),
path("ajax-add-review/<int:pid>/", views.ajax_add_review, name="ajax-add-review"),

path("add-to-cart/", views.add_to_book, name="add-to-book"),
path("cart/", views.cart_view, name="cart"),
path("delete-from-cart/", views.delete_item_from_cart, name="delete-from-cart"),

path("update-cart/", views.update_cart, name="update-cart"),
    path("checkout/", views.checkout_view, name="checkout"),


path("dashboard/", views.customer_dashboard, name="dashboard"),
path("dashboard/book/<int:id>", views.book_detail, name="book-detail"),

path("contact/", views.contact, name="contact"),
path("ajax-contact-form/", views.ajax_contact_form, name="ajax-contact-form"),

path('filter-packages/',views.filter_package,name='filter'),


]
