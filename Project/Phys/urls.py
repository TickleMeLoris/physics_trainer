from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from trainer.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('trainer/', include('trainer.urls')),
    path('', home, name='home'), 
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)