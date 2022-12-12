from django.urls import path
from stats import views


urlpatterns = [
    path("expense_category_data", views.ExpenseSummaryStatsApiView.as_view(), name='expense-category-data'),
]