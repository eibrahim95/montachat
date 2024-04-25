from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from montachat.chat.api.views import ConversationViewSet
from montachat.chat.api.views import MessageViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("conversations", ConversationViewSet)
router.register("messages", MessageViewSet)


app_name = "api"
urlpatterns = router.urls
