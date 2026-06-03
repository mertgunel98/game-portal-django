from django.shortcuts import redirect

class LocalhostRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host()
        if host.startswith('127.0.0.1'):
            new_host = host.replace('127.0.0.1', 'localhost')
            return redirect(f"{request.scheme}://{new_host}{request.get_full_path()}")
        return self.get_response(request)
