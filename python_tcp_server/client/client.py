import socket
import threading
from rich.console import Console
from PIL import Image
import io
import requests

console = Console()

def show_image(url):
    img = Image.open(io.BytesIO(requests.get(url).content)).convert('L')
    img = img.resize((80, 40))  # smaller for terminal
    chars = " .:-=+*#%@"
    pixels = img.getdata()
    ascii_str = "".join(chars[p // 25] for p in pixels)
    for i in range(0, len(ascii_str), img.width):
        print(ascii_str[i:i + img.width])


def receive_messages(sock):
    while True:
        try:
            pokemon_image = sock.recv(1024).decode("utf-8")
            if not pokemon_image:
                break
            show_image(pokemon_image)
        except Exception as e:
            print(f"Error receiving message: {e}")
            break

def start_client(host="127.0.0.1", port=50051):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    thread = threading.Thread(target=receive_messages, args=(sock,), daemon=True)

    print("Type Agent Id to connect")
    agent_id = input()
    sock.send(agent_id.encode( "utf-8"))

    thread.start()

    while True:
        msg = input()
        if msg.lower() == "exit":
            break
        sock.send(msg.encode("utf-8"))

    sock.close()

if __name__ == "__main__":
    start_client()
