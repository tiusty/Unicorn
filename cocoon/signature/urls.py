# Django Modules
from django.conf.urls import url, include

# Rest Framework Modules
from rest_framework import routers

# App modules
from . import views

router = routers.DefaultRouter()
router.register(r'hunterDocManager', views.HunterDocManagerViewset, base_name='HunterDocManager')
router.register(r'hunterDoc', views.HunterDocManagerViewset, base_name='HunterDoc')

app_name = 'signature'
urlpatterns = [
    url(r'^$', views.signature_page, name="signaturePage"),

    # Api
    url(r'^api/', include(router.urls))
]
