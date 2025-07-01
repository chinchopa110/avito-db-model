CREATE TABLE IF NOT EXISTS locations (
                                         location_id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
                                         parent_id INT,
                                         name VARCHAR(100) NOT NULL,
                                         type VARCHAR(20),
                                         coordinates POINT,
                                         CONSTRAINT fk_location_parent
                                             FOREIGN KEY(parent_id)
                                                 REFERENCES locations(location_id)
                                                 ON DELETE SET NULL
);

ALTER TABLE advertisements
    ADD CONSTRAINT fk_advertisement_location
        FOREIGN KEY(location_id)
            REFERENCES locations(location_id);