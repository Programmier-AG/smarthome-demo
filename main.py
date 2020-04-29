from http.server import HTTPServer, BaseHTTPRequestHandler
import io
import scripts
import importlib
import urllib
import threading
import _thread as thread
from websocket_server import WebsocketServer
import time

print("-------------------------------------------------------")
print("|                  Smart-Home Demo                    |")
print("|              Von Fabian R. und Sönke K.             |")
print("-------------------------------------------------------")
print()

states = {
    "k-deckenlampe": "on",
    "k-tisch-licht": "on",
    "k-ofen": "on",
    "wz-deckenlampe": "on",
    "sza-deckenlampe": "on",
    "szb-spiegel-lampe": "on",
    "kz-deckenlampe": "on"
}

functions = {
    "k-deckenlampe": "gpio-manual//19",
    "k-tisch-licht": "gpio-manual//5",
    "k-ofen": "gpio-manual//3",
    "wz-deckenlampe": "gpio-manual//6",
    "sza-deckenlampe": "gpio-manual//2",
    "szb-spiegel-lampe": "gpio-manual//13",
    "kz-deckenlampe": "gpio-manual//26"
}

def webserver():
    class server(BaseHTTPRequestHandler):
        def send_page(self):
            path = str(self.path)
            if path == "/" or path == "":
                path = "/pages/index.html"

            try:
                file = io.open(path[1:], mode="r", encoding="utf-8").read()
                self.send_response(200)
            except:
                self.send_response(404)

            self.end_headers()

            try:
                self.wfile.write(bytes(file, "utf-8"))
            except:
                pass

        def do_GET(self):
            t = threading.Thread(target=lambda: getattr(self, "send_page")())
            t.start()


    httpd = HTTPServer(("0.0.0.0", 8080), server)
    print(">> Webserver listening (:8080).")
    httpd.serve_forever()


def socketserver():
    def message_received(client, server, message):
        function = message.split(",,,")[0]
        atr = message.split(",,,")[1]
        
        # ignoring states for buttons
        if not function in ["bell", "servo", "tts"]:
            device = atr.split("//")[2]
            new_state = atr.split("//")[1]
            states[device] = new_state
            socketserver.send_message_to_all(function+"//"+atr)

        try:
            module = importlib.import_module("scripts."+function)
            t = threading.Thread(target=lambda: getattr(module, "run")(atr))
            t.start()
            
            print("\n------------------------")
            print(function, atr)
            print(states)
            print(">> Erfolreich ausgeführt.")
            getattr(module,"run")(atr)
        except ModuleNotFoundError:
            print(">> Das Modul konnte nicht gefunden werden.")
            pass

    def initial_send(client, server):
        for state in states:
            message = functions[state] + "//" + states[state] + "//" + state
            socketserver.send_message(client, message)

    socketserver = WebsocketServer(2687, host="0.0.0.0")
    socketserver.set_fn_message_received(message_received)
    socketserver.set_fn_new_client(initial_send)
    print(">> Socketserver listening (:2687).")
    socketserver.run_forever()


# thread.start_new_thread(webserver,())
# thread.start_new_thread(socketserver,())

socketserver()

while True:
    time.sleep(1)
