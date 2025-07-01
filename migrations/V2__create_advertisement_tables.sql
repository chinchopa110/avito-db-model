CREATE TABLE IF NOT EXISTS ad_categories (
                                             category_id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
                                             parent_id INT,
                                             name VARCHAR(50) NOT NULL,
                                             description TEXT,
                                             CONSTRAINT fk_category_parent
                                                 FOREIGN KEY(parent_id)
                                                     REFERENCES ad_categories(category_id)
                                                     ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS ad_statuses (
                                           status_id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
                                           name VARCHAR(20) NOT NULL,
                                           description TEXT
);

CREATE TABLE IF NOT EXISTS ad_types (
                                        type_id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
                                        name VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS advertisements (
                                              ad_id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
                                              user_id INT NOT NULL,
                                              category_id INT NOT NULL,
                                              location_id INT NOT NULL,
                                              status_id INT NOT NULL,
                                              type_id INT NOT NULL,
                                              title VARCHAR(100) NOT NULL,
                                              description TEXT NOT NULL,
                                              price DECIMAL(12,2) NOT NULL,
                                              creation_date TIMESTAMP NOT NULL,
                                              modification_date TIMESTAMP,
                                              views_count INT DEFAULT 0,
                                              CONSTRAINT fk_advertisement_user
                                                  FOREIGN KEY(user_id)
                                                      REFERENCES users(user_id)
                                                      ON DELETE CASCADE,
                                              CONSTRAINT fk_advertisement_category
                                                  FOREIGN KEY(category_id)
                                                      REFERENCES ad_categories(category_id),
                                              CONSTRAINT fk_advertisement_status
                                                  FOREIGN KEY(status_id)
                                                      REFERENCES ad_statuses(status_id),
                                              CONSTRAINT fk_advertisement_type
                                                  FOREIGN KEY(type_id)
                                                      REFERENCES ad_types(type_id)
);

CREATE TABLE IF NOT EXISTS ad_photos (
                                         photo_id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
                                         ad_id INT NOT NULL,
                                         photo_url VARCHAR(255) NOT NULL,
                                         is_main BOOLEAN DEFAULT FALSE,
                                         upload_date TIMESTAMP,
                                         CONSTRAINT fk_photo_advertisement
                                             FOREIGN KEY(ad_id)
                                                 REFERENCES advertisements(ad_id)
                                                 ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS product_ads (
                                           ad_id INT PRIMARY KEY,
                                           brand VARCHAR(50),
                                           model VARCHAR(50),
                                           condition VARCHAR(20),
                                           warranty BOOLEAN,
                                           CONSTRAINT fk_product_advertisement
                                               FOREIGN KEY(ad_id)
                                                   REFERENCES advertisements(ad_id)
                                                   ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS service_ads (
                                           ad_id INT PRIMARY KEY,
                                           service_type VARCHAR(50),
                                           experience VARCHAR(50),
                                           availability VARCHAR(50),
                                           CONSTRAINT fk_service_advertisement
                                               FOREIGN KEY(ad_id)
                                                   REFERENCES advertisements(ad_id)
                                                   ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS job_ads (
                                       ad_id INT PRIMARY KEY,
                                       position VARCHAR(100),
                                       employment_type VARCHAR(50),
                                       experience_required VARCHAR(50),
                                       salary_from DECIMAL(12,2),
                                       salary_to DECIMAL(12,2),
                                       CONSTRAINT fk_job_advertisement
                                           FOREIGN KEY(ad_id)
                                               REFERENCES advertisements(ad_id)
                                               ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS real_estate_ads (
                                               ad_id INT PRIMARY KEY,
                                               property_type VARCHAR(50),
                                               area DECIMAL(10,2),
                                               rooms INT,
                                               floor INT,
                                               total_floors INT,
                                               CONSTRAINT fk_real_estate_advertisement
                                                   FOREIGN KEY(ad_id)
                                                       REFERENCES advertisements(ad_id)
                                                       ON DELETE CASCADE
);