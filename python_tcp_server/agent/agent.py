import requests
import socket
import threading
import logging

logger = logging.getLogger(__name__)

def receive_messages(sock):
    while True:
        pokemon_name = sock.recv(1024).decode("utf-8").strip()
        if not pokemon_name:
            continue
        try:
            response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}")
            try:
                pokemon = response.json()
                sock.send(json.dumps(pokemon).encode("utf-8"))
            except Exception as json_err:
                logger.error(f"Error decoding JSON for '{pokemon_name}': {json_err}\nResponse text: {response.text}")
                break
        except Exception as e:
            logger.error(f"Error receiving messages: {e}")
            break

def start_agent(host="127.0.0.1", port=50050):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    thread = threading.Thread(target=receive_messages, args=(sock,), daemon=True)
    thread.start()

    print("Type Your Agent ID")
    agent_id = input()
    sock.send(agent_id.encode("utf-8"))

    thread.join()
    sock.close()

if __name__ == "__main__":
    start_agent()
