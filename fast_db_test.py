"""
Fast test script to verify database connection with timeout
"""
import os
import psycopg2
from urllib.parse import urlparse
import socket

def test_connection():
    """Test database connection with basic verification"""

    # Get database URL from .env file
    try:
        with open('.env', 'r') as f:
            for line in f:
                if line.startswith('DATABASE_URL='):
                    database_url = line.split('=', 1)[1].strip()
                    if database_url.startswith('"') and database_url.endswith('"'):
                        database_url = database_url[1:-1]
                    break
    except FileNotFoundError:
        print("ERROR: .env file not found!")
        return False

    print(f"Database URL: {database_url}")

    try:
        # Parse the database URL
        parsed = urlparse(database_url)
        host = parsed.hostname
        port = parsed.port or 5432

        # Test if we can reach the host:port
        print(f"Testing reachability of {host}:{port}...")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)  # 5 second timeout
        result = sock.connect_ex((host, port))
        sock.close()

        if result == 0:
            print("✓ Host is reachable")
        else:
            print("✗ Host is not reachable - connection timed out or refused")
            return False

        print("Attempting to connect to database...")
        # Connect with a shorter timeout
        conn = psycopg2.connect(
            host=host,
            port=port,
            database=parsed.path[1:],
            user=parsed.username,
            password=parsed.password,
            sslmode='require',
            connect_timeout=10  # 10 second timeout for connection
        )

        print("✓ Successfully connected to database!")

        # Quick check if the tasks table exists
        cursor = conn.cursor()
        cursor.execute("SELECT to_regclass('tasks');")
        table_exists = cursor.fetchone()[0]

        if table_exists:
            print("✓ Tasks table exists")

            # Check if the priority column exists
            cursor.execute("SELECT 1 FROM information_schema.columns WHERE table_name = 'tasks' AND column_name = 'priority';")
            priority_exists = cursor.fetchone() is not None

            if priority_exists:
                print("✓ Priority column already exists in tasks table")
                print("The migration may have already been applied.")
            else:
                print("✗ Priority column does not exist - migration is needed")
        else:
            print("✗ Tasks table does not exist")

        cursor.close()
        conn.close()
        return True

    except psycopg2.OperationalError as e:
        print(f"✗ Database connection failed: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    test_connection()