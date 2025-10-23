import requests
import socket
import threading
import logging

logger = logging.getLogger(__name__)

def receive_messages(sock):
    while True:
        try:
            pokemon_name = sock.recv(1024).decode("utf-8").strip()
            if not pokemon_name:
                print("No message received, closing connection")
                break
            
            print(f"Received request for Pokemon: {pokemon_name}")
            
            try:
                response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}")
                if response.status_code == 200:
                    pokemon = response.json()
                    sprites = pokemon.get("sprites", {})
                    front_default = sprites.get("front_default", "")
                    print(f"Sending Pokemon image URL: {front_default}")
                    sock.send(front_default.encode("utf-8"))
                else:
                    error_msg = f"Pokemon '{pokemon_name}' not found (status: {response.status_code})"
                    print(error_msg)
                    sock.send(error_msg.encode("utf-8"))
                    
            except Exception as json_err:
                error_msg = f"Error fetching Pokemon '{pokemon_name}': {json_err}"
                logger.error(error_msg)
                sock.send(error_msg.encode("utf-8"))
                
        except Exception as e:
            logger.error(f"Error in agent communication: {e}")
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
