import psycopg2


class DataBaseFunctions:
    def __init__(self, driver, hostname, username, password, database, port):
        self.driver = driver
        self.hostname = hostname
        self.username = username
        self.password = password
        self.database = database
        self.port = port
        self.conn = None

    def connect(self):
        try:
            self.conn = psycopg2.connect(
                host=self.hostname,
                user=self.username,
                password=self.password,
                dbname=self.database,
                port=self.port
            )
        except psycopg2.OperationalError as e:
            print("Error de conexión:", e)
            raise

    def close(self):
        try:
            if self.conn is not None:
                self.conn.close()
        except Exception as e:
            print("Error al cerrar la conexión:", e)

    def execute_query(self, query, values=None, fetch_results=True, commit=False):
        if self.conn is None:
            self.connect()

        with self.conn, self.conn.cursor() as cur:
            try:
                if values is not None:
                    cur.execute(query, values)
                else:
                    cur.execute(query)

                if commit:
                    self.conn.commit()

                if fetch_results:
                    return cur.fetchall()
            except Exception as e:
                if commit:
                    self.conn.rollback()
                raise e
