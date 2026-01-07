import sqlite3
import appcontext


def insert_into_db(ctx: appcontext.AppContext):
    with sqlite3.connect("appdata.db") as con:
        cur = con.cursor()

        table_name = "measurements"

        # Create table if not already exists
        res = cur.execute(
            """
                CREATE TABLE IF NOT EXISTS measurements(
                measurement_id INTEGER NOT NULL PRIMARY KEY,
                measurement_ts INTEGER NOT NULL UNIQUE,
                temperature REAL NOT NULL,
                humidity REAL NOT NULL,
                create_ts TEXT DEFAULT CURRENT_TIMESTAMP)
            """
        )

        # Insert new data only if there is not already row with this measurement
        cur.execute(
            """
                INSERT OR IGNORE INTO measurements(measurement_ts, temperature, humidity)
                VALUES(?, ?, ?)
            """,
            (ctx.sht4x_ctx.msr.ts, ctx.sht4x_ctx.msr.temp, ctx.sht4x_ctx.msr.rh),
        )

        con.commit()
