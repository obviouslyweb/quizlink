import socket
import threading
import sys
import readline  # Use pyreadline3 on Windows if needed

print("Welcome to the Quiz Game Client!")

HOST = input("Please enter a host IP. For localhost, enter nothing: ")
if HOST == "":
    HOST = '127.0.0.1'
PORT = 65432

print(f"Attempting to connect to {HOST} using port {PORT} for connection...")

should_run = True

def handle_receive(sock):
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                print("\nServer disconnected.")
                break
            message = data.decode().rstrip()

            saved_line = readline.get_line_buffer()

            sys.stdout.write('\n' + message + '\n')

            # Redisplay prompt and previous input
            sys.stdout.write("> " + saved_line)
            sys.stdout.flush()
        except ConnectionResetError:
            print("\nServer forcibly closed the connection.")
            sock.close()
            break
        except Exception as e:
            print(f"\nError: {e}")
            break

def handle_send(sock):
    global should_run
    try:
        while should_run:
            msg = input("> ")
            if not should_run:
                break
            if msg.lower() == "/exit":
                print("Disconnecting...")
                should_run = False
                sock.shutdown(socket.SHUT_RDWR)
                sock.close()
                break
            sock.sendall(msg.encode())
    except Exception as e:
        print(f"Send error: {e}")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    try:
        s.connect((HOST, PORT))
        print(f"Connected to server at {HOST}:{PORT}")

        server_prompt = s.recv(1024).decode()
        print(server_prompt, end="")
        username = input()
        s.sendall(username.encode())

        threading.Thread(target=handle_receive, args=(s,), daemon=True).start()

        handle_send(s)

    except ConnectionRefusedError:
        print("Could not connect to the server. Make sure it's running.")