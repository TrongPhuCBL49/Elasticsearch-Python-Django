from django.conf import settings
# from django.conf.urls import url
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib import admin


urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    # url(r'', include('apps.core.urls', namespace='core')),
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),

]

# if settings.DEBUG:
#     from django.conf.urls.static import static
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

