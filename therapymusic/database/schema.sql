-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS therapymusic;
USE therapymusic;

-- Users table
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(150) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    first_name VARCHAR(150),
    last_name VARCHAR(150),
    date_joined DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_login DATETIME,
    is_active BOOLEAN DEFAULT TRUE,
    is_staff BOOLEAN DEFAULT FALSE,
    is_superuser BOOLEAN DEFAULT FALSE
);

-- User profiles table
CREATE TABLE user_profiles (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL UNIQUE,
    avatar VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Moods/Emotions categories table
CREATE TABLE mood_categories (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT
);

-- Daily questionnaire responses table
CREATE TABLE questionnaire_responses (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    mood_category_id INT NOT NULL,
    stress_level INT CHECK (stress_level BETWEEN 1 AND 5),
    energy_level INT CHECK (energy_level BETWEEN 1 AND 5),
    anxiety_level INT CHECK (anxiety_level BETWEEN 1 AND 5),
    response_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (mood_category_id) REFERENCES mood_categories(id)
);

-- Songs table
CREATE TABLE songs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    artist VARCHAR(255) NOT NULL,
    genre VARCHAR(100),
    mood_category_id INT,
    spotify_id VARCHAR(255),
    FOREIGN KEY (mood_category_id) REFERENCES mood_categories(id)
);

-- Playlists table
CREATE TABLE playlists (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    mood_category_id INT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (mood_category_id) REFERENCES mood_categories(id)
);

-- Playlist songs (junction table for playlists and songs)
CREATE TABLE playlist_songs (
    playlist_id INT NOT NULL,
    song_id INT NOT NULL,
    song_order INT NOT NULL,
    PRIMARY KEY (playlist_id, song_id),
    FOREIGN KEY (playlist_id) REFERENCES playlists(id) ON DELETE CASCADE,
    FOREIGN KEY (song_id) REFERENCES songs(id) ON DELETE CASCADE
);

-- Insert initial mood categories
INSERT INTO mood_categories (name, description) VALUES
('Feliz', 'Estado de alegria e bem-estar'),
('Calmo', 'Estado de tranquilidade e serenidade'),
('Energético', 'Estado de disposição e vigor'),
('Melancólico', 'Estado de tristeza ou nostalgia'),
('Ansioso', 'Estado de preocupação ou inquietação');

-- Create index for better query performance
CREATE INDEX idx_user_responses ON questionnaire_responses(user_id, response_date);
CREATE INDEX idx_playlist_creation ON playlists(user_id, created_at);
CREATE INDEX idx_songs_mood ON songs(mood_category_id);
