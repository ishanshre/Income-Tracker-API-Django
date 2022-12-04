from rest_framework.pagination import PageNumberPagination


class CustomDefaultPagination(PageNumberPagination):
    page_size = 5