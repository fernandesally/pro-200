import socket
from threading import Thread

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_address = '127.0.0.1'
port = 8000

server.bind((ip_address, port))
server.listen()

list_of_clients = []
nicknames=[]

print("Server has started...")

question=[
    "How many planets are there in our solar system? \n a.3 \n b.2 \n c.24 \n d.8 ",
    "Who is the father of physcis? \n a.Issac Newton \n b.Galileo \n c.Eienstine \n d.Hawkings",
    "What is the sun? \n a.dead planet \n b.tiny blackhole \n c.star\n d.asteroid",
    "Which is the planet with 80 moons? \n a.Earth \n b.Mars \n c.Jupiter \n d.Saturn",
    "Which one of the following is not an element \n a.He \n b.O \n c.P \n d.kb",
    "What is the moon responsible for? \n a.Gravity \n b.Tides \n c.Earthquakes \n d.NOTA",
    "What is a falling star? \n a.A star \n b.Piece of the moon \n c.Comet \n d.Meteors",
    "What decreases when we travel at the speed of light? \n a.Time \n b.height \n c.Speed \n d.Acceleration",
    "What is a sideral year? \n a.Time of Moon around the Earth \n b. Time of Earth arounf the sun \n c.Jupiter years\n d.NOTA",
    "Which one is the greatest space agency? \n a.ESA \n b.NASA \n c.ISRO \n d.SpaceX"
]
answers=['d','a','c','c','d','b','d','a','b','b']

def clientthread(conn, addr):
    score = 0
    conn.send("Welcome to this astrophyscis quiz!".encode('utf-8'))
    conn.send("Rules: This is a fair quiz, the answers of the questions are a,b,c or d".encode('utf-8'))
    conn.send("Good Luck!!".encode('utf-8'))
    while True:
        try:
            message = conn.recv(2048).decode('utf-8')
            if message:
               print(message)
               broadcast(message, conn)
            else:
                remove(conn)
                remove_nickname(nickname)
        except:
            continue

def broadcast(message, connection):
    for clients in list_of_clients:
        if clients!=connection:
            try:
                clients.send(message.encode('utf-8'))
            except:
                remove(clients)

def remove_nickname(nickname):
    if nickname in nicknames:
        nicknames.remove(nickname)                

def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)


def get_random_question_answer(conn):
    random_index = random.randint(0,len(question) - 1) 
    random_question = question[random_index] 
    random_answer = answers[random_index]
    conn.send(random_question.encode('utf-8')) 
    return random_index, random_question, random_answer

def remove_question(index):
    question.pop(index)
    answers.pop(index)


while True:
    conn, addr = server.accept()
    conn.send('NICKNAME'.encode('utf-8'))
    nickname=conn.recv(2048).decode('utf-8')
    list_of_clients.append(conn)
    nicknames.append(nickname)
    message="{} joined!".format(nickname)
    print (message)
    broadcast(message, conn)
    new_thread = Thread(target= clientthread,args=(conn,nickname))
    new_thread.start()
