from django.utils.deprecation import MiddlewareMixin


class DetectMobileMiddleware(MiddlewareMixin):
    def process_request(self, request):
        user_agent = request.META.get("HTTP_USER_AGENT", "").lower()
        request.is_mobile = any(
            keyword in user_agent for keyword in ["mobile", "android", "iphone", "ipad"]
        )
