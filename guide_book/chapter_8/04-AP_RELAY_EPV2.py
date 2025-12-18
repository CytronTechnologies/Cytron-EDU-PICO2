import board, digitalio, socketpool, wifi
from adafruit_httpserver import Request, Response, Server, POST

AP_SSID = "EDUPICO_AP"
AP_PASSWORD = "12345678"

print("Creating access point...")
wifi.radio.start_ap(ssid=AP_SSID, password=AP_PASSWORD)
print(f"Created AP WiFi ID = {AP_SSID}")

ip = str(wifi.radio.ipv4_address_ap)
port = 5000

pool = socketpool.SocketPool(wifi.radio)
server = Server(pool, "/static", debug=False)

relay = digitalio.DigitalInOut(board.GP22)
relay.direction = digitalio.Direction.OUTPUT

@server.route("/")
def base(request: Request):
    html = f"""
        <html>
        <head>
            <meta http-equiv="refresh" content="5">
            <title>USB Relay Control</title>
        </head>
        <body style="font-family:Arial; text-align:center;
        margin-top:300px; font-size:60px;">
            <h2 style="font-size:60px;">USB Relay Light Control</h2>
            <form method="POST">
                <button name="action" value="on" type="submit"
                style="font-size:60px">Light On</button>
                <button name="action" value="off" type="submit"
                style="font-size:60px">Light Off</button>
            </form>
        </body>
        </html>
    """
    return Response(request, html, content_type='text/html')

@server.route("/", POST)
def control(request: Request):
    raw = request.raw_request.decode("utf-8")
    if "action=on" in raw:
        print("Relay ON")
        relay.value = True
    elif "action=off" in raw:
        print("Relay OFF")
        relay.value = False
    return base(request)

print("Starting HTTP server...")
print(f"Server running at: http://{ip}:{port}/")

server.serve_forever(ip, port=port)

