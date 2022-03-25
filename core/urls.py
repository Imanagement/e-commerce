from django.urls import path

from .views import (
    HomeView,
    ProductDetailView,
    OrderSummaryView,
    CategoryList,
    CategoryView,
    CheckoutView,
    ContactsPageView,
    CreditPageView,
    FAQPageView,
    TermsAndConditionsPageView,
    add_to_cart,
    remove_from_cart,
    update_cart,
    leave_product_review,
    add_to_compare,
    remove_from_compare,
    ComparePageView,
    WishlistPageView,
    add_to_wishlist,
    remove_from_wishlist,
    Search,
    email,
    get_all_reviews,
    leave_customer_phone,
)
app_name = 'core'

urlpatterns = [

    path('', HomeView.as_view(), name='home'),
    path('zakaz/', CheckoutView.as_view(), name='checkout'),
    path('korzina/', OrderSummaryView.as_view(), name='order-summary'),
    path('product/<slug>/', ProductDetailView.as_view(), name='product'),
    path('dobavit-v-korzinu/<slug>', add_to_cart, name='add-to-cart'),
    path('udalit-iz-korzini/<slug>', remove_from_cart, name='remove-from-cart'),
    path('ostavit-otziv/<slug>', leave_product_review,
         name='leave-product-review'),
    path('obnovit-korzinu/', update_cart, name='update-cart'),
    path('kategorii/<slug>', CategoryList.as_view(), name='categories-list'),
    path('kategoria/<slug>', CategoryView.as_view(), name='category-view'),
    path('dobavit-v-sravnenie/<slug>', add_to_compare, name='add-to-compare'),
    path('udalit-iz-sravneniya/<slug>',
         remove_from_compare, name='remove-from-compare'),
    path('sravnenie/', ComparePageView.as_view(), name='compare'),
    path('izbrannoe/', WishlistPageView.as_view(), name='wishlist'),
    path('dobavit-v-izbrannoe/<slug>', add_to_wishlist, name='add-to-wishlist'),
    path('udalit-iz-izbrannih/<slug>',
         remove_from_wishlist, name='remove-from-wishlist'),
    path('poisk/', Search.as_view(), name='search-product'),
    path('send-email/', email, name='send-email'),
    path('get-all-reviews/<slug>', get_all_reviews, name='get-all-reviews'),
    path('kontakti', ContactsPageView.as_view(), name='contacts'),
    # The owner had no questions so for a while disabled this page
    # path('faq', FAQPageView.as_view(), name='faq'),
    path('dopolnitelnaya-informatia',
         TermsAndConditionsPageView.as_view(), name='extra-information'),
    path('kredit', CreditPageView.as_view(), name='credit'),
    path('perezvonite-mne/', leave_customer_phone, name="customer-call-back")

]
