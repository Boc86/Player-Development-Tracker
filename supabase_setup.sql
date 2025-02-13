-- Create role table
CREATE TABLE IF NOT EXISTS role (
    id SERIAL PRIMARY KEY,
    role_name TEXT NOT NULL
);

-- Insert default roles
INSERT INTO role (id, role_name)
VALUES 
    (1, 'Admin'),
    (2, 'Coach'),
    (3, 'Player'),
    (4, 'Director of Rugby'),
    (5, 'New signup')
ON CONFLICT (id) DO NOTHING;

-- Create user table
CREATE TABLE IF NOT EXISTS "user" (
    id SERIAL PRIMARY KEY,
    first_name TEXT NOT NULL,
    sur_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role_id INTEGER,
    created_at DATE,
    FOREIGN KEY (role_id) REFERENCES role(id)
);

-- Insert default admin user
INSERT INTO "user" (first_name, sur_name, email, password_hash, role_id, created_at)
VALUES ('admin', 'admin', 'admin', crypt('admin', gen_salt('bf')), 1, CURRENT_DATE)
ON CONFLICT (email) DO NOTHING;

-- Create position table
CREATE TABLE IF NOT EXISTS position (
    id SERIAL PRIMARY KEY,
    position_name TEXT NOT NULL
);

-- Insert default positions
INSERT INTO position (id, position_name)
VALUES 
    (1, 'Loose Head Prop'),
    (2, 'Hooker'),
    (3, 'Tight Head Prop'),
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
    (16, 'N/A')
ON CONFLICT (id) DO NOTHING;

-- Create team table
CREATE TABLE IF NOT EXISTS team (
    id SERIAL PRIMARY KEY,
    team_name TEXT NOT NULL,
    coach_id INTEGER,
    assistant_coach1_id INTEGER,
    assistant_coach2_id INTEGER,
    assistant_coach3_id INTEGER,
    assistant_coach4_id INTEGER,
    assistant_coach5_id INTEGER,
    director_of_rugby_id INTEGER,
    FOREIGN KEY (coach_id) REFERENCES "user"(id),
    FOREIGN KEY (assistant_coach1_id) REFERENCES "user"(id),
    FOREIGN KEY (assistant_coach2_id) REFERENCES "user"(id),
    FOREIGN KEY (assistant_coach3_id) REFERENCES "user"(id),
    FOREIGN KEY (assistant_coach4_id) REFERENCES "user"(id),
    FOREIGN KEY (assistant_coach5_id) REFERENCES "user"(id),
    FOREIGN KEY (director_of_rugby_id) REFERENCES "user"(id)
);

-- Create player table
CREATE TABLE IF NOT EXISTS player (
    id SERIAL PRIMARY KEY,
    first_name TEXT NOT NULL,
    sur_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    team_id INTEGER,
    position_id INTEGER,
    FOREIGN KEY (team_id) REFERENCES team(id),
    FOREIGN KEY (position_id) REFERENCES position(id)
);

-- Create development_score table
CREATE TABLE IF NOT EXISTS development_score (
    id SERIAL PRIMARY KEY,
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
);