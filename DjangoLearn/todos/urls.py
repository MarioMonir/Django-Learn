from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()
router.register("", views.TodoViewSet, basename="todo")
urlpatterns = router.urls
