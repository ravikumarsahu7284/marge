
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('polls/', include('polls.urls')),
    path('', include('blog.urls')),
    path('api/V1/', include('api.apiurls')),
    path('apiview/v2/', include('apimodel.modelurls')),
    path('apiview1/v3/', include('validapi.validurl')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
