import sqlite3
import hydralit as hy
import pandas as pd
import hashlib

def strip_name(data):
    cleaned_names = [f"{name[0]} {name[1]}" for name in data]
    return cleaned_names

class user:
    def __init__(self, id, first_name, sur_name, email, password_hash, role_id, created_at):
        self.id = id
        self.first_name = first_name
        self.sur_name = sur_name
        self.email = email
        self.password_hash = password_hash
        self.role_id = role_id
        self.created_at = created_at

class role:
    def __init__(self, id, role_name):
        self.id = id
        self.role_name = role_name

class player:
    def __init__(self, id, first_name, sur_name, email, team_id, position_id):
        self.id = id
        self.first_name = first_name
        self.sur_name = sur_name
        self.email = email
        self.team_id = team_id
        self.position_id = position_id

class position:
    def __init__(self, id, position_name):
        self.id = id
        self.position_name = position_name

class team: 
    def __init__(self, id, team_name, coach_id, assistant_coach1_id, assistant_coach2_id, assistant_coach3_id, assistant_coach4_id, assistant_coach5_id, director_of_rugby_id):
        self.id = id
        self.team_name = team_name
        self.coach_id = coach_id
        self.assistant_coach1_id = assistant_coach1_id
        self.assistant_coach2_id = assistant_coach2_id
        self.assistant_coach3_id = assistant_coach3_id
        self.assistant_coach4_id = assistant_coach4_id
        self.assistant_coach5_id = assistant_coach5_id
        self.director_of_rugby_id = director_of_rugby_id

class development_score:
    def __init__(self, id, player_id, comments, passing, catching, tackling, kicking, rucking, scrummaging, attack, defence, positional_awareness, confidence):
        self.id = id
        self.player_id = player_id
        self.comments = comments
        self.passing = passing
        self.catching = catching
        self.tackling = tackling
        self.kicking = kicking
        self.rucking = rucking
        self.scrummaging = scrummaging
        self.attack = attack
        self.defence = defence
        self.positional_awareness = positional_awareness
        self.confidence = confidence

def create_db():
    try:
        conn = sqlite3.connect('player_tracker.db')
        cursor = conn.cursor()
        cursor.execute('PRAGMA foreign_keys = ON')
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            conn.close()

def create_tables():
    try:
        conn = sqlite3.connect('player_tracker.db')
        cursor = conn.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            sur_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            role_id INTEGER,
            created_at DATE,
            FOREIGN KEY (role_id) REFERENCES role(id)
        )
        ''')

        password = "admin"
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        data = ("admin", "admin", "admin", hashed_password, 1)

        cursor.execute("INSERT OR IGNORE INTO user (first_name, sur_name, email, password_hash, role_id) VALUES (?, ?, ?, ?, ?)", data)

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS role (
            id INTEGER PRIMARY KEY,
            role_name TEXT NOT NULL
        )
        ''')

        data = [
            (1, 'Admin'),
            (2, 'Coach'),
            (3, 'Player'),
            (4, 'Director of Rugby'),
            (5, 'New signup')
        ]

        cursor.executemany('INSERT OR IGNORE INTO role (id, role_name) VALUES (?, ?)', data)

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS player (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            sur_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            team_id INTEGER,
            position_id INTEGER,
            FOREIGN KEY (team_id) REFERENCES team(id),
            FOREIGN KEY (position_id) REFERENCES position(id)
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS position (
            id INTEGER PRIMARY KEY,
            position_name TEXT NOT NULL
        )
        ''')

        data = [
            (1, 'Loose Head Prop'),
            (2, 'Hooker'),
            (3, 'Titght Head Prop'),
            (4, 'Second Row'),
            (5, 'Second Row'),
            (6, 'Blindside Flanker'),
            (7, 'Openside Flanker'),
            (8, 'Number 8'),
            (9, 'Scrum Half'),
            (10, 'Fly Half'),
            (11, 'Left Wing'),
            (12, 'Inside Centre'),
            (13, 'Outside Centre'),
            (14, 'Right Wing'),
            (15, 'Full Back'),
            (16, 'N/A'),
        ]

        cursor.executemany('INSERT OR IGNORE INTO position (id, position_name) VALUES (?, ?)', data)

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS team (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            team_name TEXT NOT NULL,
            coach_id INTEGER,
            assistant_coach1_id INTEGER,
            assistant_coach2_id INTEGER,
            assistant_coach3_id INTEGER,
            assistant_coach4_id INTEGER,
            assistant_coach5_id INTEGER,
            director_of_rugby_id INTEGER,
            FOREIGN KEY (coach_id) REFERENCES user(id),
            FOREIGN KEY (assistant_coach1_id) REFERENCES user(id),
            FOREIGN KEY (assistant_coach2_id) REFERENCES user(id),
            FOREIGN KEY (assistant_coach3_id) REFERENCES user(id),
            FOREIGN KEY (assistant_coach4_id) REFERENCES user(id),
            FOREIGN KEY (assistant_coach5_id) REFERENCES user(id),
            FOREIGN KEY (director_of_rugby_id) REFERENCES user(id)
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS development_score (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_id INTEGER,
            comments TEXT,
            passing INTEGER,
            catching INTEGER,
            tackling INTEGER,
            kicking INTEGER,
            rucking INTEGER,
            scrummaging INTEGER,
            attack INTEGER,
            defence INTEGER,
            positional_awareness INTEGER,
            confidence INTEGER,
            FOREIGN KEY (player_id) REFERENCES player(id)
        )
        ''')

        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            conn.close()

def save_changes(table, data):
    conn = sqlite3.connect('player_tracker.db')
    cursor = conn.cursor()

    if table == "user":
        try:
            df = pd.DataFrame(data)
            for index, row in df.iterrows():
                update_query = """UPDATE user
                    SET first_name = ?, sur_name = ?, email = ?, password_hash = ?, role_id = ? 
                    WHERE id = ?"""
                cursor.execute(update_query, (row["first_name"], row["sur_name"], row["email"], row["password_hash"], row["role_id"], row["id"]))
                
            conn.commit()
            conn.close()
            hy.success("Users updated successfully")

        except sqlite3.Error as error:
            conn.close
            hy.error = error
    
    elif table == "team_add":
        try:




            cursor.execute("""INSERT OR IGNORE INTO team (
                            team_name, coach_id, assistant_coach1_id,
                            assistant_coach2_id, assistant_coach3_id, 
                            assistant_coach4_id, assistant_coach5_id, 
                            director_of_rugby_id) 
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                        data) #need to replace name in cleaned data with ID from user table
            
            conn.commit()
            conn.close()
            hy.success("Team added successfully")
            hy.rerun()
        
        except sqlite3.Error as error:
            conn.close()
            hy.error(error)
    
    elif table == "team_save":
        try:
            db = pd.DataFrame(data)
            for index, row in db.iterrows():
                update_query = """UPDATE team
                    SET team_name = ?, coach_id = ?, assistant_coach1_id = ?, assistant_coach2_id = ?, assistant_coach3_id = ?, assistant_coach4_id = ?, assistant_coach5_id = ?, director_of_rugby_id = ?
                    WHERE id = ?"""
                cursor.execute(update_query, (row["team_name"], row["coach_id"], row["assistant_coach1_id"], row["assistant_coach2_id"], row["assistant_coach3_id"], row["assistant_coach4_id"], row["assistant_coach5_id"], row["director_of_rugby_id"], row["id"]))
                
            conn.commit()
            conn.close()
            hy.success("Teams updated successfully")

        except sqlite3.Error as error:
            conn.close()
            hy.error(error)

     