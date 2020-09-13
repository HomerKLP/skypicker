# Vendor
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    """
    Кастомный хэндлер для вызова из любой точки
    чтоб вызвать обработанную ошибку
    """
    response = exception_handler(exc, context)

    if response is not None and response.status_code == 500:
        codes = exc.get_codes().split(';')
        if len(codes) > 1:
            response.status_code = int(codes[0])
            response.data['error_code'] = codes[1]

    return response
