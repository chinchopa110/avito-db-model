CREATE TABLE IF NOT EXISTS conversations (
                                             conversation_id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
                                             ad_id INT NOT NULL,
                                             start_date TIMESTAMP,
                                             last_message_date TIMESTAMP,
                                             CONSTRAINT fk_conversation_advertisement
                                                 FOREIGN KEY(ad_id)
                                                     REFERENCES advertisements(ad_id)
                                                     ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS messages (
                                        message_id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
                                        sender_id INT NOT NULL,
                                        recipient_id INT NOT NULL,
                                        conversation_id INT NOT NULL,
                                        content TEXT NOT NULL,
                                        send_date TIMESTAMP NOT NULL,
                                        is_read BOOLEAN DEFAULT FALSE,
                                        CONSTRAINT fk_message_sender
                                            FOREIGN KEY(sender_id)
                                                REFERENCES users(user_id)
                                                ON DELETE CASCADE,
                                        CONSTRAINT fk_message_recipient
                                            FOREIGN KEY(recipient_id)
                                                REFERENCES users(user_id)
                                                ON DELETE CASCADE,
                                        CONSTRAINT fk_message_conversation
                                            FOREIGN KEY(conversation_id)
                                                REFERENCES conversations(conversation_id)
                                                ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS reviews (
                                       review_id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
                                       reviewer_id INT NOT NULL,
                                       reviewed_user_id INT NOT NULL,
                                       ad_id INT NOT NULL,
                                       rating INT NOT NULL,
                                       comment TEXT,
                                       creation_date TIMESTAMP,
                                       CONSTRAINT fk_review_reviewer
                                           FOREIGN KEY(reviewer_id)
                                               REFERENCES users(user_id)
                                               ON DELETE CASCADE,
                                       CONSTRAINT fk_review_reviewed_user
                                           FOREIGN KEY(reviewed_user_id)
                                               REFERENCES users(user_id)
                                               ON DELETE CASCADE,
                                       CONSTRAINT fk_review_advertisement
                                           FOREIGN KEY(ad_id)
                                               REFERENCES advertisements(ad_id)
                                               ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS complaint_types (
                                               type_id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
                                               name VARCHAR(50) NOT NULL,
                                               description TEXT
);

CREATE TABLE IF NOT EXISTS complaints (
                                          complaint_id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
                                          reporter_id INT NOT NULL,
                                          ad_id INT NOT NULL,
                                          complaint_type_id INT NOT NULL,
                                          description TEXT,
                                          status VARCHAR(20),
                                          creation_date TIMESTAMP,
                                          resolution_date TIMESTAMP,
                                          CONSTRAINT fk_complaint_reporter
                                              FOREIGN KEY(reporter_id)
                                                  REFERENCES users(user_id)
                                                  ON DELETE CASCADE,
                                          CONSTRAINT fk_complaint_advertisement
                                              FOREIGN KEY(ad_id)
                                                  REFERENCES advertisements(ad_id)
                                                  ON DELETE CASCADE,
                                          CONSTRAINT fk_complaint_type
                                              FOREIGN KEY(complaint_type_id)
                                                  REFERENCES complaint_types(type_id)
);

CREATE TABLE IF NOT EXISTS safe_deals (
                                          deal_id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
                                          buyer_id INT NOT NULL,
                                          seller_id INT NOT NULL,
                                          ad_id INT NOT NULL,
                                          amount DECIMAL(12,2),
                                          status VARCHAR(20),
                                          creation_date TIMESTAMP,
                                          completion_date TIMESTAMP,
                                          CONSTRAINT fk_deal_buyer
                                              FOREIGN KEY(buyer_id)
                                                  REFERENCES users(user_id)
                                                  ON DELETE CASCADE,
                                          CONSTRAINT fk_deal_seller
                                              FOREIGN KEY(seller_id)
                                                  REFERENCES users(user_id)
                                                  ON DELETE CASCADE,
                                          CONSTRAINT fk_deal_advertisement
                                              FOREIGN KEY(ad_id)
                                                  REFERENCES advertisements(ad_id)
                                                  ON DELETE CASCADE
);