from lona.html import Strong, HTML, H1
from lona import View


class HomeView(View):
    def handle_request(self, request):
        username = request.user.username or 'anonymous'

        return HTML(
            H1('Späti'),
            'Logged in as: ', Strong(username),
        )
