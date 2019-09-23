from django.core.paginator import InvalidPage
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class StandardResultsPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'limit'
    page_query_param = 'page'

    def paginate_queryset(self, queryset, request, view=None):
        self.description_length = request.query_params.get('description_length', 200)
        page_size = self.get_page_size(request)
        paginator = self.django_paginator_class(queryset, page_size)
        page_number = request.query_params.get(self.page_query_param, 1)
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
        description_length = int(self.description_length)
        if not description_length:
            description_length = 200
        description = {
            "description": result["description"][:description_length] + "..."
        }
        _result = result
        _result.update(description)
        return _result
