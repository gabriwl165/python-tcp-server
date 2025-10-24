import socket
import threading
import signal

clients = {}

def handle_agent(conn, addr):
    print(f"[NEW AGENT CONNECTION] {addr}")
    try:
        client_id = conn.recv(1024).decode("utf-8").strip()
        if not client_id:
            conn.send(b"Missing client ID. Closing connection.")
            conn.close()
            return
        
        clients[client_id] = (conn, addr)
        print(f"[CONNECTED AGENT] Agent {client_id}")
    except:
        print(f"[DISCONNECTED] Agent {client_id}")
        conn.close()

running = True

def handle_client(conn, addr):
    print(f"[NEW CLIENT CONNECTION] {addr}")
    try:
        client_id = conn.recv(1024).decode("utf-8").strip()
        if client_id not in clients:
            conn.send(b"Agent Id not found!")
            conn.close()
            return
        
        keep_listening = True
        while keep_listening and running:
            try:
                msg = conn.recv(1024).decode("utf-8").strip()
                if not msg:
                    break
                if msg.lower() == "exit":
                    keep_listening = False
                    break
                
                print(f"Forwarding message to agent: {msg}")
                (conn_agent, _) = clients[client_id]
                conn_agent.send(msg.encode("utf-8"))
                
                # Wait for response from agent
                response = conn_agent.recv(1024).decode("utf-8").strip()
                if response:
                    print(f"Received response from agent: {response}")
                    conn.send(response.encode("utf-8"))
                    print("Response sent to client")
                else:
                    print("No response from agent")
                    
            except Exception as e:
                print(f"Error in client communication: {e}")
                break

        print(f"[CONNECTED] Agent {client_id}")
    finally:
        print(f"[DISCONNECTED] Agent {client_id}")
        conn.close()

def start_proxy_agent(host, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    print(f"[STARTED] Server Proxy Agent on {host}:{port}\n")
    
    while running:
        conn, addr = server.accept()
        handle_agent(conn, addr)
        

def start_proxy_client(host, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    print(f"[STARTED] Server Proxy Client on {host}:{port}\n")

    while running:
        conn, addr = server.accept()
        handle_client(conn, addr)


def handle_signal(sig, frame):
    global running
    print("\nReceived termination signal, shutting down...")
    running = False

def main():
    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)


    thread_proxy_agent = threading.Thread(target=start_proxy_agent, args=('127.0.0.1', 50050))
    thread_proxy_client = threading.Thread(target=start_proxy_client, args=('127.0.0.1', 50051))

    thread_proxy_agent.start()
    thread_proxy_client.start()
    
    thread_proxy_agent.join()
    thread_proxy_client.join()

if __name__ == "__main__":
    main()
