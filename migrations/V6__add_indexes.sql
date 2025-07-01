BEGIN;

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_registration_date ON users(registration_date);
CREATE INDEX idx_users_active ON users(is_active) WHERE is_active = TRUE;

CREATE INDEX idx_user_profiles_user_id ON user_profiles(user_id);
CREATE INDEX idx_user_profiles_rating ON user_profiles(rating);

CREATE INDEX idx_advertisements_user_id ON advertisements(user_id);
CREATE INDEX idx_advertisements_category_id ON advertisements(category_id);
CREATE INDEX idx_advertisements_status_id ON advertisements(status_id);
CREATE INDEX idx_advertisements_type_id ON advertisements(type_id);
CREATE INDEX idx_advertisements_location_id ON advertisements(location_id);
CREATE INDEX idx_advertisements_price ON advertisements(price);
CREATE INDEX idx_advertisements_creation_date ON advertisements(creation_date);
CREATE INDEX idx_advertisements_views ON advertisements(views_count);
CREATE INDEX idx_advertisements_price_category ON advertisements(category_id, price);


CREATE INDEX idx_product_ads_brand ON product_ads(brand);
CREATE INDEX idx_product_ads_model ON product_ads(model);
CREATE INDEX idx_product_ads_condition ON product_ads(condition);

CREATE INDEX idx_service_ads_service_type ON service_ads(service_type);
CREATE INDEX idx_service_ads_experience ON service_ads(experience);

CREATE INDEX idx_job_ads_position ON job_ads(position);
CREATE INDEX idx_job_ads_salary_range ON job_ads(salary_from, salary_to);
CREATE INDEX idx_job_ads_employment_type ON job_ads(employment_type);

CREATE INDEX idx_real_estate_ads_property_type ON real_estate_ads(property_type);
CREATE INDEX idx_real_estate_ads_rooms ON real_estate_ads(rooms);
CREATE INDEX idx_real_estate_ads_price_range ON real_estate_ads(area, rooms);

CREATE INDEX idx_messages_sender_id ON messages(sender_id);
CREATE INDEX idx_messages_recipient_id ON messages(recipient_id);
CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX idx_messages_send_date ON messages(send_date);
CREATE INDEX idx_conversations_ad_id ON conversations(ad_id);

CREATE INDEX idx_reviews_reviewer_id ON reviews(reviewer_id);
CREATE INDEX idx_reviews_reviewed_user_id ON reviews(reviewed_user_id);
CREATE INDEX idx_reviews_ad_id ON reviews(ad_id);
CREATE INDEX idx_reviews_rating ON reviews(rating);

CREATE INDEX idx_safe_deals_buyer_id ON safe_deals(buyer_id);
CREATE INDEX idx_safe_deals_seller_id ON safe_deals(seller_id);
CREATE INDEX idx_safe_deals_ad_id ON safe_deals(ad_id);
CREATE INDEX idx_safe_deals_status ON safe_deals(status);

COMMIT;
