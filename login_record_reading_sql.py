import sqlite3 as sq
from faker import Faker

with sq.connect("chatbot_RR_1.db") as connector:
    cursor = connector.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        login TEXT,
        password TEXT,
        nazwisko TEXT
    );""")

    cursor.executescript("""
            CREATE TABLE IF NOT EXISTS chatbot (
                id INTEGER PRIMARY KEY,
                answer TEXT,
                chat TEXT,
                users_id INTEGER NOT NULL,
                FOREIGN KEY (users_id) REFERENCES users(id)
            );""")
    connector.commit()

class Logowanie():
    def __init__(self, connector, table):
        self.conn = connector
        self.cur = connector.cursor()
        self.tab = table
        self.rej = input("\n wejście [ 1 ], rejestracja [ 2 ], zmiana hasła [ 3 ] prosze wybrać właściwe: ")
        if self.rej == '1':
            self.logowanie()
        elif self.rej == '2':
            self.rejestracja()
        elif self.rej == '3':
            self.zmiana_hasla()
        else:
            if self.rej is not int:
                print("nie prawidłowy wybór")
                exit()

    def logowanie(self):
        login = input("Login: ")
        self.login = login
        self.cur.execute(f"SELECT login FROM users WHERE login = '{login}'")
        if not self.cur.fetchone() is None:
            self.password = input("Password: ")
            self.cur.execute(f"SELECT login, password FROM users WHERE login = '{login}'")
            if self.cur.fetchone()[1] == self.password:
                print("wszedłeś do systemu")
            else:
                i = 1
                while i <= 3:
                    if i == 3:
                        print("nie prawidłowe hasło! BLOKADA KONTA")
                        exit()
                    else:
                        print("nie prawidłowe hasło!")
                        self.password = input("Password: ")
                        self.cur.execute(f"SELECT login, password FROM users WHERE login = '{login}'")
                        if self.cur.fetchone()[1] == self.password:
                            print("wszedłeś do systemu")
                            break
                        i += 1
        else:
            if not self.cur.fetchone() is True:
                print("użytkownik nie istnieje!!!!")
                exit()

    def rejestracja(self):
        inp_login = input("Login: ")
        self.cur.execute(f"SELECT login FROM users WHERE login = '{inp_login}'")
        if self.cur.fetchone() is None:
            inp_password = input("Password: ")
            inp_nazwisko = input("Nazwisko: ")
            self.cur.execute("INSERT INTO users VALUES (NULL, ?, ?, ?)", (inp_login, inp_password, inp_nazwisko))
            self.conn.commit()
            print(f'zarejestrowałeś się pod nazwą: {inp_login}')
            exit()
        else:
            print("taki użytkownik już jest!")
            exit()

    def zmiana_hasla(self):
        zm_login = input("Login: ")
        zm_nazwisko = input("Nazwisko: ")
        self.cur.execute(f"SELECT login, nazwisko FROM users WHERE login = '{zm_login}' AND nazwisko ='{zm_nazwisko}'")
        if not self.cur.fetchone() is None:
            zm_password = input("New password: ")
            self.cur.execute(f"UPDATE users SET password='{zm_password}' WHERE login = '{zm_login}'")
            self.conn.commit()
            print('hasło zostało zmienione')
            exit()
        else:
            print('nie prawidłowe dane')
            exit()


class NLU():
    def get_text(self, req='Ask me:'):
        text = input(req)
        return text

class Responce():
    def respond(self):
        fake = Faker()
        answer = fake.text()
        print(answer)
        return answer

class Zapis(Logowanie):
    def __init__(self):
        super(Zapis, self).__init__(connector, 'users')
        self.cur.execute(
            f"SELECT login, password FROM users WHERE login = '{self.login}' AND password ='{self.password}'")
        self.start()


    def start(self):
        print('Hello from Bot')
        self.nlu = NLU()
        self.rsp = Responce()
        self.cur.execute('SELECT login FROM users WHERE login = ?', (self.login,))
        users_id = self.cur.fetchone()[0]
        zapis = (None,  f'{self.nlu.get_text()}', f'{self.rsp.respond()}', users_id)
        self.cur.execute('INSERT INTO chatbot VALUES(?,?,?,?)', zapis)
        self.conn.commit()


zzz = Zapis()


