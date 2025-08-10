from django.urls import path
from . import views

urlpatterns = [
    path('', views.store_view, name='store_view'),
    path('redeem/<int:offer_id>/', views.redeem_offer, name='redeem_offer'),
    path('voucher/<int:redemption_id>/', views.redemption_voucher, name='redemption_voucher'),
    path('voucher/<int:redemption_id>/download/', views.download_voucher_pdf, name='download_voucher_pdf'),
    path('wishlist/toggle/<int:offer_id>/', views.toggle_wishlist, name='toggle_wishlist'),
    path('quick-view/<int:offer_id>/', views.quick_view_offer, name='quick_view_offer'),
    path('history/', views.user_redemptions, name='redemption_history'),
]
