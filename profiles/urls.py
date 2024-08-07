from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import ProfileRetrieveUpdateAPIView

urlpatterns = [
    path('me/', ProfileRetrieveUpdateAPIView.as_view(), name='profile-detail')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)