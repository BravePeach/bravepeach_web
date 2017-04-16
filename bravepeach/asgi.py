import os

from channels.asgi import get_channel_layer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bravepeach.settings")    # Change setting to use another.
channel_layer = get_channel_layer()
