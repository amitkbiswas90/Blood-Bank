from rest_framework.pagination import  PageNumberPagination

class DefaultPagination(PageNumberPagination):
    page_size = 9
    
    def get_paginated_response(self, data):
        return {
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'page_size': self.page_size,
            'results': data
        }