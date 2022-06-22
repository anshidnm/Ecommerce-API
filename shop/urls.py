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

router.register('cart',cart_view.cartViewset)
router.register('cartitem',cart_view.cartItemViewset)
router.register('order',cart_view.OrderViewset)
router.register('address',cart_view.AddressViewset)
router.register('payment',cart_view.PaymentViewset)

router.register('register',accouts_view.RegisterViewset)
router.register('image',accouts_view.ImageViewset)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include(router.urls)),
    path('api/login/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/login/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh')
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)