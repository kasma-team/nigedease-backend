class AllowDockerHostsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Allow Docker container names in the host header
        host = request.META.get('HTTP_HOST', '')
        if host and 'user_management_service' in host:
            request.META['HTTP_HOST'] = 'localhost'
        return self.get_response(request) 