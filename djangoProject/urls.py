from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from djangoProject import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user.urls'), name='user'),
    path('', include('social_django.urls', namespace='social')),
    path('accounts/', include('allauth.urls')),
    path('eccomerce/', include('eccomerce.urls'), name='eccomerce'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
