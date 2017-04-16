from channels import include

channel_routing = [
    include("webapp.routing.websocket_routing", path=r"^/chat/stream"),
    include('webapp.routing.custom_routing'),
]
