import psycopg2
from psycopg2.extras import execute_values
from datetime import datetime, timedelta
import random
import string
from faker import Faker
import os

fake = Faker()

APP_ENV = os.getenv("APP_ENV")
SEED_COUNT = int(os.getenv('SEED_COUNT', 10))

DB_CONFIG = {
    "host": os.getenv("POSTGRES_HOST", "haproxy"),
    "port": os.getenv("POSTGRES_PORT", "5000"),
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
}


def get_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


def check_table_exists(conn, table_name):
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = %s
            );
        """, (table_name,))
        return cursor.fetchone()[0]


def seed_users(conn):
    print("Seeding users...")
    users = []
    user_count = max(5, 20 // SEED_COUNT)

    for i in range(1, user_count + 1):
        username = f'user{i}' if i > 1 else 'admin'
        email = f'user{i}@example.com' if i > 1 else 'admin@example.com'
        phone = f'+123456789{i:02d}'
        password_hash = f'hashed_password_{i}'
        registration_date = fake.date_time_between(start_date='-1y', end_date='now')
        last_login = fake.date_time_between(start_date=registration_date,
                                            end_date='now') if random.random() > 0.2 else None
        is_active = True
        is_blocked = False if i > 1 else False

        users.append((
            username, email, phone, password_hash,
            registration_date, last_login, is_active, is_blocked
        ))

    with conn.cursor() as cursor:
        execute_values(
            cursor,
            """
            INSERT INTO users 
            (username, email, phone, password_hash, registration_date, last_login, is_active, is_blocked)
            VALUES %s
            """,
            users
        )
    conn.commit()


def seed_user_profiles(conn):
    print("Seeding user_profiles...")
    profiles = []
    with conn.cursor() as cursor:
        cursor.execute("SELECT user_id FROM users")
        user_ids = [row[0] for row in cursor.fetchall()]

    for user_id in user_ids:
        first_name = fake.first_name()
        last_name = fake.last_name()
        avatar_url = f'https://example.com/avatars/{user_id}.jpg' if random.random() > 0.3 else None
        about = fake.paragraph(nb_sentences=3) if random.random() > 0.4 else None
        rating = round(random.uniform(1, 5), 2)

        profiles.append((
            user_id, first_name, last_name, avatar_url, about, rating
        ))

    with conn.cursor() as cursor:
        execute_values(
            cursor,
            """
            INSERT INTO user_profiles 
            (user_id, first_name, last_name, avatar_url, about, rating)
            VALUES %s
            """,
            profiles
        )
    conn.commit()


def seed_password_resets(conn):
    print("Seeding password_resets...")
    resets = []
    with conn.cursor() as cursor:
        cursor.execute("SELECT user_id FROM users LIMIT %s", (max(2, 5 // SEED_COUNT),))
        user_ids = [row[0] for row in cursor.fetchall()]

    for user_id in user_ids:
        token = get_random_string(32)
        expiration_date = datetime.now() + timedelta(hours=24)
        is_used = random.choice([True, False])

        resets.append((
            user_id, token, expiration_date, is_used
        ))

    with conn.cursor() as cursor:
        execute_values(
            cursor,
            """
            INSERT INTO password_resets 
            (user_id, token, expiration_date, is_used)
            VALUES %s
            """,
            resets
        )
    conn.commit()


def seed_ad_categories(conn):
    print("Seeding ad_categories...")
    categories = [
        (None, 'Electronics', 'Electronic devices and accessories'),
        (None, 'Real Estate', 'Properties for sale or rent'),
        (None, 'Jobs', 'Job offers'),
        (None, 'Services', 'Various services'),
        (1, 'Phones', 'Smartphones and mobile phones'),
        (1, 'Laptops', 'Laptops and notebooks'),
        (2, 'Apartments', 'Apartments for sale or rent'),
        (2, 'Houses', 'Houses for sale or rent'),
        (3, 'IT', 'IT and programming jobs'),
        (3, 'Marketing', 'Marketing and sales jobs'),
        (4, 'Repair', 'Repair services'),
        (4, 'Cleaning', 'Cleaning services'),
    ]

    with conn.cursor() as cursor:
        execute_values(
            cursor,
            """
            INSERT INTO ad_categories 
            (parent_id, name, description)
            VALUES %s
            """,
            categories
        )
    conn.commit()


def seed_ad_statuses(conn):
    print("Seeding ad_statuses...")
    statuses = [
        ('Active', 'Active advertisement'),
        ('Pending', 'Waiting for moderation'),
        ('Rejected', 'Rejected by moderator'),
        ('Sold', 'Item has been sold'),
        ('Closed', 'Advertisement closed'),
    ]

    with conn.cursor() as cursor:
        execute_values(
            cursor,
            """
            INSERT INTO ad_statuses 
            (name, description)
            VALUES %s
            """,
            statuses
        )
    conn.commit()


def seed_ad_types(conn):
    print("Seeding ad_types...")
    types = [
        ('Product',),
        ('Service',),
        ('Job',),
        ('Real Estate',),
    ]

    with conn.cursor() as cursor:
        execute_values(
            cursor,
            """
            INSERT INTO ad_types 
            (name)
            VALUES %s
            """,
            types
        )
    conn.commit()


def seed_locations(conn):
    print("Seeding locations...")
    locations = [
        (None, 'United States', 'country', None),
        (None, 'United Kingdom', 'country', None),
        (None, 'Germany', 'country', None),
        (1, 'New York', 'city', None),
        (1, 'California', 'state', None),
        (2, 'London', 'city', None),
        (3, 'Berlin', 'city', None),
        (4, 'Manhattan', 'district', None),
        (4, 'Brooklyn', 'district', None),
        (5, 'Los Angeles', 'city', None),
        (5, 'San Francisco', 'city', None),
    ]

    with conn.cursor() as cursor:
        execute_values(
            cursor,
            """
            INSERT INTO locations 
            (parent_id, name, type, coordinates)
            VALUES %s
            """,
            locations
        )
    conn.commit()


def seed_advertisements(conn):
    print("Seeding advertisements...")
    ads = []

    with conn.cursor() as cursor:
        # Get required foreign keys
        cursor.execute("SELECT user_id FROM users")
        user_ids = [row[0] for row in cursor.fetchall()]

        cursor.execute("SELECT category_id FROM ad_categories")
        category_ids = [row[0] for row in cursor.fetchall()]

        cursor.execute("SELECT location_id FROM locations")
        location_ids = [row[0] for row in cursor.fetchall()]

        cursor.execute("SELECT status_id FROM ad_statuses")
        status_ids = [row[0] for row in cursor.fetchall()]

        cursor.execute("SELECT type_id FROM ad_types")
        type_ids = [row[0] for row in cursor.fetchall()]

    ad_count = max(10, 50 // SEED_COUNT)

    for i in range(1, ad_count + 1):
        user_id = random.choice(user_ids)
        category_id = random.choice(category_ids)
        location_id = random.choice(location_ids)
        status_id = random.choice(status_ids)
        type_id = random.choice(type_ids)

        title = fake.sentence(nb_words=6)[:100]
        description = fake.paragraph(nb_sentences=5)
        price = round(random.uniform(10, 10000), 2)
        creation_date = fake.date_time_between(start_date='-6m', end_date='now')
        modification_date = fake.date_time_between(start_date=creation_date,
                                                   end_date='now') if random.random() > 0.5 else None
        views_count = random.randint(0, 1000)

        ads.append((
            user_id, category_id, location_id, status_id, type_id,
            title, description, price, creation_date, modification_date, views_count
        ))

    with conn.cursor() as cursor:
        execute_values(
            cursor,
            """
            INSERT INTO advertisements 
            (user_id, category_id, location_id, status_id, type_id, 
             title, description, price, creation_date, modification_date, views_count)
            VALUES %s
            """,
            ads
        )
    conn.commit()


def seed_ad_photos(conn):
    print("Seeding ad_photos...")
    photos = []

    with conn.cursor() as cursor:
        cursor.execute("SELECT ad_id FROM advertisements")
        ad_ids = [row[0] for row in cursor.fetchall()]

    for ad_id in ad_ids:
        num_photos = random.randint(1, min(5, 5 // SEED_COUNT + 1))
        for i in range(num_photos):
            photo_url = f'https://example.com/ads/{ad_id}/photo_{i}.jpg'
            is_main = (i == 0)
            upload_date = fake.date_time_between(start_date='-6m', end_date='now')

            photos.append((
                ad_id, photo_url, is_main, upload_date
            ))

    with conn.cursor() as cursor:
        execute_values(
            cursor,
            """
            INSERT INTO ad_photos 
            (ad_id, photo_url, is_main, upload_date)
            VALUES %s
            """,
            photos
        )
    conn.commit()


def seed_product_ads(conn):
    print("Seeding product_ads...")
    product_ads = []

    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT a.ad_id 
            FROM advertisements a
            JOIN ad_types t ON a.type_id = t.type_id
            WHERE t.name = 'Product'
        """)
        ad_ids = [row[0] for row in cursor.fetchall()]

    for ad_id in ad_ids:
        brand = fake.company()[:50]
        model = fake.word()[:50]
        condition = random.choice(['New', 'Used', 'Refurbished'])
        warranty = random.choice([True, False])

        product_ads.append((
            ad_id, brand, model, condition, warranty
        ))

    with conn.cursor() as cursor:
        execute_values(
            cursor,
            """
            INSERT INTO product_ads 
            (ad_id, brand, model, condition, warranty)
            VALUES %s
            """,
            product_ads
        )
    conn.commit()


def seed_service_ads(conn):
    print("Seeding service_ads...")
    service_ads = []

    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT a.ad_id 
            FROM advertisements a
            JOIN ad_types t ON a.type_id = t.type_id
            WHERE t.name = 'Service'
        """)
        ad_ids = [row[0] for row in cursor.fetchall()]

    for ad_id in ad_ids:
        service_type = random.choice(['Repair', 'Cleaning', 'Tutoring', 'Design', 'Transport'])
        experience = random.choice(['<1 year', '1-3 years', '3-5 years', '5+ years'])
        availability = random.choice(['Weekdays', 'Weekends', 'Flexible', 'On demand'])

        service_ads.append((
            ad_id, service_type, experience, availability
        ))

    with conn.cursor() as cursor:
        execute_values(
            cursor,
            """
            INSERT INTO service_ads 
            (ad_id, service_type, experience, availability)
            VALUES %s
            """,
            service_ads
        )
    conn.commit()


def seed_job_ads(conn):
    print("Seeding job_ads...")
    job_ads = []

    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT a.ad_id 
            FROM advertisements a
            JOIN ad_types t ON a.type_id = t.type_id
            WHERE t.name = 'Job'
        """)
        ad_ids = [row[0] for row in cursor.fetchall()]

    for ad_id in ad_ids:
        position = fake.job()[:100]
        employment_type = random.choice(['Full-time', 'Part-time', 'Contract', 'Freelance'])
        experience_required = random.choice(['Entry level', 'Mid level', 'Senior', 'Executive'])
        salary_from = round(random.uniform(1000, 5000), 2)
        salary_to = round(salary_from + random.uniform(1000, 10000), 2)

        job_ads.append((
            ad_id, position, employment_type, experience_required, salary_from, salary_to
        ))

    with conn.cursor() as cursor:
        execute_values(
            cursor,
            """
            INSERT INTO job_ads 
            (ad_id, position, employment_type, experience_required, salary_from, salary_to)
            VALUES %s
            """,
            job_ads
        )
    conn.commit()


def seed_real_estate_ads(conn):
    print("Seeding real_estate_ads...")
    real_estate_ads = []

    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT a.ad_id 
            FROM advertisements a
            JOIN ad_types t ON a.type_id = t.type_id
            WHERE t.name = 'Real Estate'
        """)
        ad_ids = [row[0] for row in cursor.fetchall()]

    for ad_id in ad_ids:
        property_type = random.choice(['Apartment', 'House', 'Condo', 'Villa', 'Townhouse'])
        area = round(random.uniform(30, 300), 2)
        rooms = random.randint(1, 5)
        floor = random.randint(1, 25) if property_type == 'Apartment' or property_type == 'Condo' else 1
        total_floors = random.randint(1, 30) if property_type == 'Apartment' or property_type == 'Condo' else 1

        real_estate_ads.append((
            ad_id, property_type, area, rooms, floor, total_floors
        ))

    with conn.cursor() as cursor:
        execute_values(
            cursor,
            """
            INSERT INTO real_estate_ads 
            (ad_id, property_type, area, rooms, floor, total_floors)
            VALUES %s
            """,
            real_estate_ads
        )
    conn.commit()


def seed_conversations(conn):
    print("Seeding conversations...")
    conversations = []

    with conn.cursor() as cursor:
        cursor.execute("SELECT ad_id FROM advertisements")
        ad_ids = [row[0] for row in cursor.fetchall()]

    conversation_count = max(5, 20 // SEED_COUNT)
    for ad_id in random.sample(ad_ids, min(conversation_count, len(ad_ids))):
        start_date = fake.date_time_between(start_date='-3m', end_date='now')
        last_message_date = fake.date_time_between(start_date=start_date,
                                                   end_date='now') if random.random() > 0.3 else None

        conversations.append((
            ad_id, start_date, last_message_date
        ))

    with conn.cursor() as cursor:
        execute_values(
            cursor,
            """
            INSERT INTO conversations 
            (ad_id, start_date, last_message_date)
            VALUES %s
            """,
            conversations
        )
    conn.commit()


def seed_messages(conn):
    print("Seeding messages...")
    messages = []

    with conn.cursor() as cursor:
        cursor.execute("SELECT conversation_id FROM conversations")
        conversation_ids = [row[0] for row in cursor.fetchall()]

        cursor.execute("SELECT user_id FROM users")
        user_ids = [row[0] for row in cursor.fetchall()]

    for conversation_id in conversation_ids:
        num_messages = random.randint(1, max(3, 10 // SEED_COUNT))
        participants = random.sample(user_ids, 2)
        sender, recipient = participants[0], participants[1]

        for i in range(num_messages):
            if i % 2 == 0:
                current_sender = sender
                current_recipient = recipient
            else:
                current_sender = recipient
                current_recipient = sender

            content = fake.sentence(nb_words=random.randint(5, 20))
            send_date = fake.date_time_between(start_date='-3m', end_date='now')
            is_read = random.choice([True, False])

            messages.append((
                current_sender, current_recipient, conversation_id, content, send_date, is_read
            ))

    with conn.cursor() as cursor:
        execute_values(
            cursor,
            """
            INSERT INTO messages 
            (sender_id, recipient_id, conversation_id, content, send_date, is_read)
            VALUES %s
            """,
            messages
        )
    conn.commit()


def seed_reviews(conn):
    print("Seeding reviews...")
    reviews = []

    with conn.cursor() as cursor:
        cursor.execute("SELECT user_id FROM users")
        user_ids = [row[0] for row in cursor.fetchall()]

        cursor.execute("SELECT ad_id, user_id FROM advertisements")
        ad_user_pairs = [(row[0], row[1]) for row in cursor.fetchall()]

    review_count = max(5, 30 // SEED_COUNT)
    for ad_id, seller_id in random.sample(ad_user_pairs, min(review_count, len(ad_user_pairs))):
        possible_reviewers = [uid for uid in user_ids if uid != seller_id]
        if not possible_reviewers:
            continue

        reviewer_id = random.choice(possible_reviewers)
        rating = random.randint(1, 5)
        comment = fake.paragraph(nb_sentences=2) if random.random() > 0.3 else None
        creation_date = fake.date_time_between(start_date='-3m', end_date='now')

        reviews.append((
            reviewer_id, seller_id, ad_id, rating, comment, creation_date
        ))

    with conn.cursor() as cursor:
        execute_values(
            cursor,
            """
            INSERT INTO reviews 
            (reviewer_id, reviewed_user_id, ad_id, rating, comment, creation_date)
            VALUES %s
            """,
            reviews
        )
    conn.commit()


def seed_complaint_types(conn):
    print("Seeding complaint_types...")
    complaint_types = [
        ('Spam', 'Advertisement is spam'),
        ('Fraud', 'Advertisement is fraudulent'),
        ('Inappropriate', 'Advertisement contains inappropriate content'),
        ('Wrong Category', 'Advertisement is in wrong category'),
        ('Duplicate', 'Duplicate advertisement'),
    ]

    with conn.cursor() as cursor:
        execute_values(
            cursor,
            """
            INSERT INTO complaint_types 
            (name, description)
            VALUES %s
            """,
            complaint_types
        )
    conn.commit()


def seed_complaints(conn):
    print("Seeding complaints...")
    complaints = []

    with conn.cursor() as cursor:
        cursor.execute("SELECT type_id FROM complaint_types")
        type_ids = [row[0] for row in cursor.fetchall()]

        cursor.execute("SELECT user_id FROM users")
        user_ids = [row[0] for row in cursor.fetchall()]

        cursor.execute("SELECT ad_id FROM advertisements")
        ad_ids = [row[0] for row in cursor.fetchall()]

    complaint_count = max(3, 15 // SEED_COUNT)
    for _ in range(complaint_count):
        reporter_id = random.choice(user_ids)
        ad_id = random.choice(ad_ids)
        complaint_type_id = random.choice(type_ids)
        description = fake.paragraph(nb_sentences=2)
        status = random.choice(['Pending', 'Resolved', 'Rejected'])
        creation_date = fake.date_time_between(start_date='-2m', end_date='now')
        resolution_date = fake.date_time_between(start_date=creation_date,
                                                 end_date='now') if status == 'Resolved' else None

        complaints.append((
            reporter_id, ad_id, complaint_type_id, description, status, creation_date, resolution_date
        ))

    with conn.cursor() as cursor:
        execute_values(
            cursor,
            """
            INSERT INTO complaints 
            (reporter_id, ad_id, complaint_type_id, description, status, creation_date, resolution_date)
            VALUES %s
            """,
            complaints
        )
    conn.commit()


def seed_safe_deals(conn):
    print("Seeding safe_deals...")
    safe_deals = []

    with conn.cursor() as cursor:
        cursor.execute("SELECT user_id FROM users")
        user_ids = [row[0] for row in cursor.fetchall()]

        cursor.execute("SELECT ad_id, user_id FROM advertisements")
        ad_seller_pairs = [(row[0], row[1]) for row in cursor.fetchall()]

    deal_count = max(3, 10 // SEED_COUNT)
    for ad_id, seller_id in random.sample(ad_seller_pairs, min(deal_count, len(ad_seller_pairs))):
        possible_buyers = [uid for uid in user_ids if uid != seller_id]
        if not possible_buyers:
            continue

        buyer_id = random.choice(possible_buyers)

        with conn.cursor() as cursor:
            cursor.execute("SELECT price FROM advertisements WHERE ad_id = %s", (ad_id,))
            price = cursor.fetchone()[0]

        # Fixed line - using Solution 1
        amount = round(float(price) * random.uniform(0.9, 1.1), 2)

        status = random.choice(['Pending', 'Completed', 'Cancelled'])
        creation_date = fake.date_time_between(start_date='-1m', end_date='now')
        completion_date = fake.date_time_between(start_date=creation_date,
                                                 end_date='now') if status == 'Completed' else None

        safe_deals.append((
            buyer_id, seller_id, ad_id, amount, status, creation_date, completion_date
        ))

    with conn.cursor() as cursor:
        execute_values(
            cursor,
            """
            INSERT INTO safe_deals 
            (buyer_id, seller_id, ad_id, amount, status, creation_date, completion_date)
            VALUES %s
            """,
            safe_deals
        )
    conn.commit()


def seed_database():
    conn = None
    try:
        conn = psycopg2.connect(**DB_PARAMS)

        if check_table_exists(conn, 'users'):
            seed_users(conn)

        if check_table_exists(conn, 'user_profiles'):
            seed_user_profiles(conn)

        if check_table_exists(conn, 'password_resets'):
            seed_password_resets(conn)

        if check_table_exists(conn, 'ad_categories'):
            seed_ad_categories(conn)

        if check_table_exists(conn, 'ad_statuses'):
            seed_ad_statuses(conn)

        if check_table_exists(conn, 'ad_types'):
            seed_ad_types(conn)

        if check_table_exists(conn, 'locations'):
            seed_locations(conn)

        if check_table_exists(conn, 'advertisements'):
            seed_advertisements(conn)

        if check_table_exists(conn, 'ad_photos'):
            seed_ad_photos(conn)

        if check_table_exists(conn, 'product_ads'):
            seed_product_ads(conn)

        if check_table_exists(conn, 'service_ads'):
            seed_service_ads(conn)

        if check_table_exists(conn, 'job_ads'):
            seed_job_ads(conn)

        if check_table_exists(conn, 'real_estate_ads'):
            seed_real_estate_ads(conn)

        if check_table_exists(conn, 'conversations'):
            seed_conversations(conn)

        if check_table_exists(conn, 'messages'):
            seed_messages(conn)

        if check_table_exists(conn, 'reviews'):
            seed_reviews(conn)

        if check_table_exists(conn, 'complaint_types'):
            seed_complaint_types(conn)

        if check_table_exists(conn, 'complaints'):
            seed_complaints(conn)

        if check_table_exists(conn, 'safe_deals'):
            seed_safe_deals(conn)

        print("Database seeding completed successfully!")

    except Exception as e:
        print(f"Error seeding database: {e}")
    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    seed_database()