from django.shortcuts import render

from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

import datetime

from core.models import Expence
from income.models import Income
# Create your views here.
class ExpenseSummaryStatsApiView(views.APIView):

    permission_classes = [IsAuthenticated]
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

class IncomeSummaruStatsApiView(views.APIView):
    permission_classes = [IsAuthenticated]
    def get_source(self, incomes):
        return incomes.source

    def get_amount_for_source(self, incomes_list, source):
        incomes = incomes_list.filter(source=source)
        amount = 0
        for income in incomes:
            amount = income.amount
            return {"amount":str(amount)}

    def get(self, request, *args, **kwargs):
        todays_date = datetime.date.today()
        a_year_ago = todays_date - datetime.timedelta(days=30*12)
        incomes = Income.objects.filter(owner=request.user, date__gte=a_year_ago, date__lte=todays_date)
        final = {}
        sources = list(map(self.get_source, incomes))

        for income in incomes:
            for source in sources:
                final[source] = self.get_amount_for_source(incomes, source)
        return Response({"source_data":final}, status=status.HTTP_200_OK)