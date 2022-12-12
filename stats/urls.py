from django.urls import path
from stats import views

app_name = "stats"

urlpatterns = [
    path("expense_category_data", views.ExpenseSummaryStatsApiView.as_view(), name='expense-category-data'),
    path("income_source_data", views.IncomeSummaruStatsApiView.as_view(), name='income-source-data'),
]