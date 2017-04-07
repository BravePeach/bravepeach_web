from bravepeach.util import flavour_render
from ..forms import GuideSearchFrom


def index(request):
    form = GuideSearchFrom()
    return flavour_render(request, "index.html", {'form': form})
