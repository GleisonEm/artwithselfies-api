from datetime import datetime
from django.http import JsonResponse

class BaseMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

class ProcessViewNoneMiddleware(BaseMiddleware):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if (view_func.__name__ == 'serve'):
            return None
        myapps = [
            'version1-teste'
        ]

        if (not request.headers.get('Authorization-Token') in myapps):
            return JsonResponse({'message': 'sai fora ladrao'}, status=401)
        return None