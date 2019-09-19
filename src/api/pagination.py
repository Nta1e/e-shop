from django.core.paginator import InvalidPage
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class StandardResultsPagination(PageNumberPagination):
    def paginate_queryset(self, queryset, request, view=None):
        self.page_size = request.data.get("limit", None)
        if not self.page_size:
            self.page_size = 20
        self.description_length = request.data.get("description_length", None)
        paginator = self.django_paginator_class(queryset, self.page_size)
        page_number = request.data.get("page", None)
        if not page_number:
            page_number = 1
        try:
            self.page = paginator.page(page_number)
        except InvalidPage as error:
            message = self.invalid_page_message.format(
                page_number=page_number, message=str(error)
            )
            raise NotFound(message)

        self.request = request
        return list(self.page)

    def get_paginated_response(self, data):
        _data = map(self.truncate_description, data)
        return Response(
            {
                "paginationMeta": {
                    "currentPage": self.page.number,
                    "currentPageSize": self.page_size,
                    "totalPages": self.page.paginator.num_pages,
                    "totalRecords": self.page.paginator.count,
                },
                "rows": list(_data),
            }
        )

    def truncate_description(self, result):
        description_length = self.description_length
        if not description_length:
            description_length = 200
        description = {
            "description": result["description"][:description_length] + "..."
        }
        _result = result
        _result.update(description)
        return _result
