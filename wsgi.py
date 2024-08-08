from app.main import app, pg_conn, pg_cursor

if __name__ == '__main__':
    try: 
        app.run()
    finally: 
        pg_conn.close()
        pg_cursor.close()