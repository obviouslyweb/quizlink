import socket
import threading
import json
import random

with open("server/questions.json", "r") as f:
    questions = json.load(f)

HOST = '127.0.0.1'
PORT = 65432

current_question = None
answered_clients = set()
scores = {}
clients = {}  # conn: username

def broadcast(message, sender_conn=None):
    for conn in list(clients):
        if conn != sender_conn:
            try:
                conn.sendall((message + "\n").encode())
            except:
                conn.close()
                if conn in clients:
                    del clients[conn]

def handle_client(conn, addr):
    try:
        conn.sendall("Enter your username: ".encode())
        username = conn.recv(1024).decode().strip()
        clients[conn] = username
        scores[username] = 0
        print(f"{username} connected from {addr}")

        # Greet user and announce to others
        conn.sendall(f"Welcome, {username}! Use /scores, /startquiz, or /exit for commands.\n".encode())
        broadcast(f"{username} has joined the game!", sender_conn=conn)

        global current_question, answered_clients

        while True:
            data = conn.recv(1024)
            if not data:
                break
            msg = data.decode().strip()

            if msg.lower() == "/startquiz":
                question = random.choice(questions)
                shuffled_choices = question["choices"].copy()
                random.shuffle(shuffled_choices)

                formatted = f"\nA new quiz has started!\nQUESTION: {question['question']}\n"
                for idx, choice in enumerate(shuffled_choices, 1):
                    formatted += f"{idx}. {choice}\n"

                broadcast(formatted)
                current_question = {
                    "question": question["question"],
                    "choices": shuffled_choices,
                    "correct": question["correct"]
                }
                answered_clients = set()

            elif msg.lower() == "/scores":
                leaderboard = "\nCurrent Scoreboard:\n"
                sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
                for name, score in sorted_scores:
                    leaderboard += f"{name}: {score} point(s)\n"
                conn.sendall(leaderboard.encode())

            elif current_question and conn not in answered_clients and not msg.startswith("/"):
                answer_data = current_question
                user_answer = msg.strip()

                try:
                    selected_index = int(user_answer) - 1
                    selected_text = answer_data["choices"][selected_index]
                except:
                    selected_text = user_answer

                if selected_text.lower() == answer_data["correct"].lower():
                    conn.sendall("Correct!\n".encode())
                    scores[clients[conn]] += 1
                else:
                    conn.sendall(f"Incorrect. The correct answer was: {answer_data['correct']}\n".encode())

                answered_clients.add(conn)

            else:
                # Treat as chat
                chat_message = f"{username}: {msg}"
                broadcast(chat_message, sender_conn=conn)

            print(f"{username}: {msg}")

    except:
        pass
    finally:
        username = clients.get(conn, 'A user')
        print(f"{username} disconnected.")
        broadcast(f"{username} has left the game.", sender_conn=conn)
        conn.close()
        if conn in clients:
            del scores[clients[conn]]
            del clients[conn]

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Server listening on {HOST}:{PORT}")
    try:
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
    except KeyboardInterrupt:
        print("Server shutting down.")
