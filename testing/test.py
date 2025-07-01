import os
import psycopg2
import time
from faker import Faker
import random

DB_CONFIG = {
    "host": os.getenv("POSTGRES_HOST", "haproxy"),
    "port": os.getenv("POSTGRES_PORT", "5000"),
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
}

fake = Faker()


def execute_query(query, params=None):
    conn = None
    try:
        conn = psycopg2.connect(
            **DB_CONFIG,
            client_encoding='utf-8'
        )
        cursor = conn.cursor()
        start_time = time.time()
        cursor.execute(query, params or ())
        result = cursor.fetchall()
        execution_time = time.time() - start_time
        print(f"Запрос выполнен за {execution_time:.4f} сек")
        return result, execution_time
    except Exception as e:
        print(f"Ошибка при выполнении запроса: {e}")
        return None, 0
    finally:
        if conn:
            conn.close()


def generate_test_queries():
    queries = []

    queries.append((
        "SELECT user_id, username, email FROM users WHERE is_active = TRUE AND is_blocked = FALSE LIMIT 100;",
        None
    ))

    queries.append((
        """SELECT a.ad_id, a.title, u.username, up.rating 
           FROM advertisements a
           JOIN users u ON a.user_id = u.user_id
           JOIN user_profiles up ON u.user_id = up.user_id
           WHERE a.status_id = 1
           ORDER BY up.rating DESC
           LIMIT 50;""",
        None
    ))

    queries.append((
        """SELECT c.name, COUNT(a.ad_id) as ad_count, AVG(a.price) as avg_price
           FROM advertisements a
           JOIN ad_categories c ON a.category_id = c.category_id
           GROUP BY c.name
           ORDER BY ad_count DESC;""",
        None
    ))

    queries.append((
        """SELECT a.ad_id, a.title, a.price, l.name as location
           FROM advertisements a
           JOIN locations l ON a.location_id = l.location_id
           WHERE a.price BETWEEN %s AND %s
           AND a.category_id = %s
           AND a.creation_date > NOW() - INTERVAL '30 days';""",
        (5000, 20000, random.randint(1, 10))
    ))

    queries.append((
        """SELECT m.message_id, u1.username as sender, u2.username as receiver, 
                  a.title as ad_title, m.send_date
           FROM messages m
           JOIN users u1 ON m.sender_id = u1.user_id
           JOIN users u2 ON m.recipient_id = u2.user_id
           JOIN conversations c ON m.conversation_id = c.conversation_id
           JOIN advertisements a ON c.ad_id = a.ad_id
           WHERE m.send_date > NOW() - INTERVAL '7 days'
           ORDER BY m.send_date DESC
           LIMIT 20;""",
        None
    ))

    queries.append((
        """SELECT u.user_id, u.username, up.rating, ad_counts.ad_count
           FROM users u
           JOIN user_profiles up ON u.user_id = up.user_id
           JOIN (
               SELECT user_id, COUNT(*) as ad_count 
               FROM advertisements 
               GROUP BY user_id
           ) ad_counts ON u.user_id = ad_counts.user_id
           ORDER BY ad_counts.ad_count DESC
           LIMIT 10;""",
        None
    ))

    queries.append((
        """SELECT a.ad_id, a.title, re.property_type, re.area, re.rooms
           FROM advertisements a
           JOIN real_estate_ads re ON a.ad_id = re.ad_id
           WHERE EXISTS (
               SELECT 1 FROM ad_photos p 
               WHERE p.ad_id = a.ad_id
           )
           AND a.price BETWEEN %s AND %s;""",
        (1000000, 5000000)
    ))

    queries.append((
        """SELECT l.name as city, AVG(up.rating) as avg_rating, COUNT(u.user_id) as users
           FROM users u
           JOIN user_profiles up ON u.user_id = up.user_id
           JOIN advertisements a ON u.user_id = a.user_id
           JOIN locations l ON a.location_id = l.location_id
           WHERE l.type = 'city'
           GROUP BY l.name
           HAVING COUNT(u.user_id) > 5
           ORDER BY avg_rating DESC;""",
        None
    ))

    queries.append((
        """SELECT u.username, a.title, d.amount, d.status, d.creation_date
           FROM safe_deals d
           JOIN users u ON d.buyer_id = u.user_id OR d.seller_id = u.user_id
           JOIN advertisements a ON d.ad_id = a.ad_id
           JOIN ad_categories c ON a.category_id = c.category_id
           JOIN locations l ON a.location_id = l.location_id
           WHERE u.user_id = %s
           ORDER BY d.creation_date DESC;""",
        (random.randint(1, 100),)
    ))

    queries.append((
        """SELECT ct.name as complaint_type, u.username, a.title, 
                  c.status, c.creation_date
           FROM complaints c
           JOIN complaint_types ct ON c.complaint_type_id = ct.type_id
           JOIN users u ON c.reporter_id = u.user_id
           JOIN advertisements a ON c.ad_id = a.ad_id
           WHERE c.status = 'pending'
           AND c.creation_date > (SELECT NOW() - INTERVAL '30 days')
           ORDER BY c.creation_date DESC;""",
        None
    ))

    queries.append((
        """SELECT 
               u.user_id,
               u.username,
               COUNT(DISTINCT a.ad_id) as ads_count,
               COUNT(DISTINCT m.message_id) as messages_count,
               COUNT(DISTINCT r.review_id) as reviews_count
           FROM users u
           LEFT JOIN advertisements a ON u.user_id = a.user_id
           LEFT JOIN messages m ON u.user_id = m.sender_id
           LEFT JOIN reviews r ON u.user_id = r.reviewer_id
           GROUP BY u.user_id, u.username
           ORDER BY ads_count DESC
           LIMIT 20;""",
        None
    ))

    queries.append((
        """SELECT a.title, j.position, j.employment_type, 
                  j.salary_from, j.salary_to, l.name as location
           FROM advertisements a
           JOIN job_ads j ON a.ad_id = j.ad_id
           JOIN locations l ON a.location_id = l.location_id
           WHERE j.salary_to >= %s
           AND a.status_id = 1
           ORDER BY j.salary_from DESC;""",
        (50000,)
    ))

    queries.append((
        """WITH RECURSIVE category_tree AS (
               SELECT category_id, name, parent_id, 1 as level
               FROM ad_categories
               WHERE parent_id IS NULL
               UNION ALL
               SELECT c.category_id, c.name, c.parent_id, ct.level + 1
               FROM ad_categories c
               JOIN category_tree ct ON c.parent_id = ct.category_id
           )
           SELECT 
               ct.name as category,
               ct.level,
               COUNT(a.ad_id) as ad_count,
               AVG(a.price) as avg_price
           FROM category_tree ct
           LEFT JOIN advertisements a ON ct.category_id = a.category_id
           GROUP BY ct.category_id, ct.name, ct.level
           ORDER BY ct.level, ct.name;""",
        None
    ))

    queries.append((
        """SELECT 
               a.ad_id,
               a.title,
               a.price,
               c.name as category,
               AVG(a.price) OVER (PARTITION BY a.category_id) as avg_category_price,
               a.price - AVG(a.price) OVER (PARTITION BY a.category_id) as price_diff
           FROM advertisements a
           JOIN ad_categories c ON a.category_id = c.category_id
           WHERE a.status_id = 1
           ORDER BY price_diff DESC
           LIMIT 20;""",
        None
    ))

    queries.append((
        """SELECT 
               a.ad_id, a.title, a.description, a.price, a.creation_date,
               u.username, up.rating,
               c.name as category,
               l.name as location,
               s.name as status,
               t.name as type,
               (SELECT COUNT(*) FROM ad_photos p WHERE p.ad_id = a.ad_id) as photos_count,
               (SELECT COUNT(*) FROM messages m 
                JOIN conversations cv ON m.conversation_id = cv.conversation_id
                WHERE cv.ad_id = a.ad_id) as messages_count
           FROM advertisements a
           JOIN users u ON a.user_id = u.user_id
           JOIN user_profiles up ON u.user_id = up.user_id
           JOIN ad_categories c ON a.category_id = c.category_id
           JOIN locations l ON a.location_id = l.location_id
           JOIN ad_statuses s ON a.status_id = s.status_id
           JOIN ad_types t ON a.type_id = t.type_id
           WHERE a.ad_id = %s;""",
        (random.randint(1, 1000),)
    ))

    return queries


def main():
    print("Запуск тестовых запросов к базе данных...")
    total_time = 0
    queries = generate_test_queries()

    for i, (query, params) in enumerate(queries, 1):
        print(f"\nЗапрос #{i}:")
        print(query[:200] + "..." if len(query) > 200 else query)
        result, exec_time = execute_query(query, params)
        total_time += exec_time
        if result and len(result) > 0:
            print(f"Первые строки результата ({len(result)} всего):")
            for row in result[:3]:
                print(row)

    print(f"\nВсе запросы выполнены за {total_time:.4f} секунд")


if __name__ == "__main__":
    main()