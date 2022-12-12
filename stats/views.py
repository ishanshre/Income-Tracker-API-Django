from django.shortcuts import render

from rest_framework import views, status
from rest_framework.response import Response

import datetime

from core.models import Expence

# Create your views here.
class ExpenseSummaryStatsApiView(views.APIView):


    def get_amount_for_category(self, expense_list, category):
        expenses = expense_list.filter(category=category)
        amount = 0
        for expense in expenses:
            amount += expense.amount
            return {"amount":str(amount)}

    def get_category(self, expense):
        return expense.category

    def get(self, request, *args, **kwargs):
        todays_date = datetime.date.today()
        a_year_ago = todays_date - datetime.timedelta(days=30*12)
        expenses = Expence.objects.filter(owner=request.user, date__gte=a_year_ago, date__lte=todays_date)
        final = {}
        categories = list(map(self.get_category, expenses))

        for expense in expenses:
            for category in categories:
                final[category] = self.get_amount_for_category(expenses, category)
        return Response({"category_data":final}, status=status.HTTP_200_OK)