import socket
import threading

def receive_messages(sock):
    msg = sock.recv(1024).decode("utf-8")
    if not msg:
        return
            
    while True:
        pokemon_image = sock.recv(1024).decode("utf-8")
        print(pokemon_image)
        if not pokemon_image:
            continue
        print(pokemon_image)
        break

def start_client(host="127.0.0.1", port=50051):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    thread = threading.Thread(target=receive_messages, args=(sock,), daemon=True)
    thread.start()
    thread.join()

    print("Type Agent Id to connect")
    agent_id = input()
    sock.send(agent_id.encode( "utf-8"))
    while True:
        msg = input()
        if msg.lower() == "exit":
            break
        sock.send(msg.encode("utf-8"))

    sock.close()


if __name__ == "__main__":
    start_client()
