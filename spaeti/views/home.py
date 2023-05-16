from lona.html import HTML, H1
from lona import View


class HomeView(View):
    def handle_request(self, request):
        return HTML(
            H1('Spaeti'),
        )
