import psycopg2
import os

conn_details = {
    "host": os.getenv("DATABASE_HOST", "postgres"),
    "database": os.getenv("DATABASE_NAME", "postgres"),
    "user": os.getenv("DATABASE_USER", "postgres"),
    "password": os.getenv("DATABASE_PASSWORD", "Mydatabase1391"),
    "port": os.getenv("DATABASE_PORT", "5432")
}

def admin_change_price(activity, price):
    try:
        conn = psycopg2.connect(**conn_details)
        cur = conn.cursor()
        cur.execute("UPDATE court SET price = %s WHERE activity = %s", (price, activity))
        conn.commit()
        cur.close()
        conn.close()
        return True
    except psycopg2.Error as e:
        print("Error checking login credentials:", e)
        return False

def admin_delete_activity(activity):
    try:
        conn = psycopg2.connect(**conn_details)
        cur = conn.cursor()
        cur.execute("DELETE FROM court WHERE activity = %s", (activity,))
        conn.commit()
        cur.close()
        conn.close()
        return True
    except psycopg2.Error as e:
        print("Error checking login credentials:", e)
        return False         

def admin_add_activity(activity, price):
    try:
        conn = psycopg2.connect(**conn_details)
        cur = conn.cursor()
        cur.execute("INSERT INTO court (activity, price) VALUES (%s, %s)",
                    (activity, price,))
        conn.commit()
        cur.close()
        conn.close()
        return True
    except psycopg2.Error as e:
        print("Error checking login credentials:", e)
        return False  
    
def admin_or_not(email):
    try:
        conn = psycopg2.connect(**conn_details)
        cur = conn.cursor()
        cur.execute("SELECT admin FROM inloggningsuppgifter WHERE email = %s", (email,))
        admin_status = cur.fetchone()[0]
        cur.close()
        conn.close()
        return admin_status
    except psycopg2.Error as e:
        return None

def login_credentials_check(email, password):
    try:
        conn = psycopg2.connect(**conn_details)
        cur = conn.cursor()
        cur.execute("SELECT password, email, admin FROM inloggningsuppgifter WHERE email = %s AND password = %s", (email, password,))
        user_info = cur.fetchall()
        cur.close()
        conn.close()
        if user_info:
            print(user_info)  # Kontrollera om användaren finns i databasen
            return True
        print(user_info)
        return False
    except psycopg2.Error as e:
        print("Error checking login credentials:", e)
        return False