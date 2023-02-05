from django.urls import path
from app import views 
from django.conf import settings
from django.conf.urls.static import static 
from django.contrib.auth import views as auth_views 
from .forms import MyPasswordchangeForm , MypasswordresetForm ,MySetpassword
urlpatterns = [
    path('', views.home),
    path('product-detail/<int:pk>', views.product_detail, name='product-detail'),
    # path('cart/', views.add_to_cart, name='add-to-cart'),
    path('buy/', views.buy_now, name='buy-now'),
    path('profile/',views.Profileviews.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    # path('changepassword/', views.change_password, name='changepassword'),
    path('mobile/', views.mobile, name='mobile'),
    path('mobile/<slug:data>', views.mobile, name='mobiledata'),
    path("changepassword/", auth_views.PasswordChangeView.as_view(template_name='app/changepassword.html',form_class=MyPasswordchangeForm, success_url='/profile/'), name="changepassword"),
    path('login/', views.Login.as_view(), name='login'),
    path('registration/', views.CustomerRegistration.as_view(), name='customerregistration'),
    path('checkout/', views.checkout, name='checkout'),
    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='app/password_reset.html',form_class=MypasswordresetForm),name='password_reset'),
    path('password-reset-done/',auth_views.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'),name='password_reset_done'),
    path("password-reset-confirm/<uidb64>/<token>/",auth_views.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html',form_class=MySetpassword),name='password_reset_confirm'),
    path("password-reset-complete/", auth_views.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'), name="password_reset_complete"),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('cart/', views.add_to_cart, name='cart_add'),
    path('showcart',views.show_cart,name='showcart'),
    path('pluscart/',views.plus_cart,name="plus_cart"),
    path('minuscart/',views.minus_cart,name='minuscart'),
    path('deletecart/',views.delete_cart,name="delete_cart"),
    path('orderdone/',views.order_done,name="order_done"),



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
 