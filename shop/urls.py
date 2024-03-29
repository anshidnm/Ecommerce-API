from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path,include
from main import views
from order import views as cart_view
from accounts import views as accouts_view
from rest_framework import routers
from rest_framework_simplejwt import views as jwt_views



router=routers.DefaultRouter()
router.register('category',views.CategoryViewset)
router.register('brand',views.BrandViewset)
router.register('product',views.ProductViewset)
router.register('review',views.ReviewViewset)
router.register('favourite',views.FavouriteViewset)
router.register('specialoffer',views.SpecialOfferViewset)
router.register('toptwosp',views.toptwospViewset)
router.register('bestselling',views.BestSellingViewset)
router.register('toptwobs',views.toptwobsViewset)
router.register('goceries',views.GroceryViewset)
router.register('specificproductreview',views.SpecificReviewViewset)


router.register('cart',cart_view.cartViewset)
router.register('cartitem',cart_view.cartItemViewset)
router.register('order',cart_view.OrderViewset)
router.register('address',cart_view.AddressViewset)
router.register('payment',cart_view.PaymentViewset)
router.register('delivery',cart_view.DeliveryViewset)
router.register('promo',cart_view.PromoViewset)
router.register('paymethod',cart_view.PaymethodViewset)

router.register('register',accouts_view.RegisterViewset)
router.register('image',accouts_view.ImageViewset)
router.register('usershort',accouts_view.UserShortViewset)
router.register('notification',accouts_view.NotificationViewset)
router.register('mobile',accouts_view.Otpviewset)
router.register('confirm',accouts_view.ConfirmViewset)
router.register('social',accouts_view.SocialViewset)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include(router.urls)),
    path('api/login/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/login/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)