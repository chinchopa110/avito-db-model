CREATE TABLE IF NOT EXISTS users (
                                     user_id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
                                     username VARCHAR(50) NOT NULL,
                                     email VARCHAR(100) NOT NULL UNIQUE,
                                     phone VARCHAR(20) NOT NULL UNIQUE,
                                     password_hash VARCHAR(255) NOT NULL,
                                     registration_date TIMESTAMP NOT NULL,
                                     last_login TIMESTAMP,
                                     is_active BOOLEAN DEFAULT TRUE,
                                     is_blocked BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS user_profiles (
                                             profile_id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
                                             user_id INT NOT NULL,
                                             first_name VARCHAR(50),
                                             last_name VARCHAR(50),
                                             avatar_url VARCHAR(255),
                                             about TEXT,
                                             rating DECIMAL(3,2),
                                             CONSTRAINT fk_user_profile_user
                                                 FOREIGN KEY(user_id)
                                                     REFERENCES users(user_id)
                                                     ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS password_resets (
                                               reset_id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
                                               user_id INT NOT NULL,
                                               token VARCHAR(255) NOT NULL,
                                               expiration_date TIMESTAMP NOT NULL,
                                               is_used BOOLEAN DEFAULT FALSE,
                                               CONSTRAINT fk_password_reset_user
                                                   FOREIGN KEY(user_id)
                                                       REFERENCES users(user_id)
                                                       ON DELETE CASCADE
);