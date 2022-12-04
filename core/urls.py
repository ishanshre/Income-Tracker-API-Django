from rest_framework.routers import SimpleRouter
from core import views



app_name = "core"
router = SimpleRouter()
router.register("expences", views.ExpenceModelViewSet)

urlpatterns = router.urls