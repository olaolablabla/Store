from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from .forms import LoginForm

admin.site.site_header = "A4 Furniture Administration"
# admin.site.site_title = "A4 Furniture"
# admin.site.site_index_title = "Welcome to A4 Furniture"

urlpatterns = [
    path("", views.home, name='home'),
    path('about/', views.about, name='about'),
    path('category/<slug:val>', views.categoryView, name="category"),
    path('category-title/<val>', views.CategoryTitle, name='category-title'),
    path('product-detail/<int:pk>', views.ProductDetail, name= 'product-detail'),
    path('search/', views.search, name='search'),
    path('review/', views.review, name='review'),

    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='showcart'),
    path('checkout/', views.checkout_cart, name='checkout'),
    path('paymentdone/', views.payment_done, name='paymentdone'),
    path('orders/', views.orders, name='orders'),

    path('pluscart/', views.plus_cart),
    path('minuscart/', views.minus_cart),
    path('removecart/', views.remove_cart),

    path('registration/', views.registeration, name='customer-regis'),
    path('accounts/login/', auth_view.LoginView.as_view(template_name='app/login.html',
                                           authentication_form=LoginForm), name='login'),
    path('logout/', auth_view.LogoutView.as_view(next_page='login'), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/address/', views.address, name='address'),
    path('address/updateAddress/<int:pk>', views.update, name='updateAddress'),



]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)