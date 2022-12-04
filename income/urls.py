from rest_framework.routers import SimpleRouter

from income import views

app_name = "income"

router = SimpleRouter()

router.register("incomes", views.IncomeModelViewSet, basename="incomes")

urlpatterns = router.urls