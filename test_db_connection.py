"""
Test script to verify database connection
"""
import os
import psycopg2
from urllib.parse import urlparse

def test_connection():
    """Test database connection"""

    # Get database URL from environment or .env file
    database_url = os.environ.get('DATABASE_URL', 'postgresql://user:password@localhost:5432/your_database_name')

    if 'DATABASE_URL' not in os.environ:
        # Load from .env file
        try:
            with open('.env', 'r') as f:
                for line in f:
                    if line.startswith('DATABASE_URL='):
                        database_url = line.split('=', 1)[1].strip()
                        if database_url.startswith('"') and database_url.endswith('"'):
                            database_url = database_url[1:-1]
                        break
        except FileNotFoundError:
            pass

    if not database_url or database_url.startswith('postgresql://user:password'):
        print("DATABASE_URL environment variable not properly set!")
        print(f"Current value: {database_url}")
        return False

    print(f"Testing connection to database: {database_url}")

    try:
        # Parse the database URL for psycopg2 connection
        parsed = urlparse(database_url)

        # Connect with SSL parameters for Neon
        conn = psycopg2.connect(
            host=parsed.hostname,
            port=parsed.port or 5432,
            database=parsed.path[1:],  # Remove the leading '/'
            user=parsed.username,
            password=parsed.password,
            sslmode='require'  # Add SSL mode for Neon
        )

        print("✓ Successfully connected to database!")

        # Check if tasks table exists
        cursor = conn.cursor()
        cursor.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'tasks');")
        table_exists = cursor.fetchone()[0]

        if table_exists:
            print("✓ Tasks table exists in the database")

            # Check existing columns
            cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'tasks';")
            columns = [row[0] for row in cursor.fetchall()]
            print(f"Current columns in tasks table: {columns}")

            # Check for missing columns
            expected_columns = ['priority', 'due_date', 'reminder_time', 'recurrence_type', 'recurrence_metadata']
            missing_columns = [col for col in expected_columns if col not in columns]
            if missing_columns:
                print(f"Missing columns that need to be added: {missing_columns}")
            else:
                print("✓ All expected columns are already present in the tasks table")
        else:
            print("✗ Tasks table does not exist in the database")

        cursor.close()
        conn.close()
        return True

    except Exception as e:
        print(f"✗ Error occurred during connection test: {e}")
        if 'conn' in locals():
            conn.close()
        return False

if __name__ == "__main__":
    test_connection()