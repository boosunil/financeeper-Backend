from django.conf.urls import url, include
from rest_framework.routers import SimpleRouter
from rest_framework.urlpatterns import format_suffix_patterns
from authentication import views

router = SimpleRouter()
router.register(r'users', views.UserView)

urlpatterns = [
    url(r'^', include(router.urls))
]

urlpatterns = format_suffix_patterns(urlpatterns)
