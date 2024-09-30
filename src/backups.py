from datetime import datetime
import os
import zipfile
from config import Config


class Backups:
    def __init__(self, config: Config):
        self.config = config

    def create(self):
        try:
            # Ensure the backup directory exists
            os.makedirs("backups", exist_ok=True)

            # Create a file name based on the current datetime
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            sql_file_name = "data.sql"
            log_backup_file_name = "log_backup.log"
            log_file_name = "app.log"
            zip_file_name = f"{timestamp}.zip"

            # Open the backup file in write mode
            with open(sql_file_name, "w") as f:
                # Iterate through the SQL dump of the database and write to the file
                for line in self.config.con.iterdump():
                    f.write(f"{line}\n")

            # copy the log file to the backup directory
            with open(log_file_name, "r") as f:
                with open(f"{log_backup_file_name}", "w") as backup_file:
                    backup_file.write(f.read())

            # Create a zip file containing the SQL backup
            with zipfile.ZipFile(f"backups/{zip_file_name}", "w") as zipf:
                zipf.write(sql_file_name, arcname=sql_file_name)
                zipf.write(f"{log_backup_file_name}", arcname=log_backup_file_name)

            # Remove the temporary SQL file
            os.remove(sql_file_name)
            os.remove(log_backup_file_name)

            print(f"Backup created successfully: {zip_file_name}")
            return zip_file_name
        except Exception as e:
            print(f"Error creating backup: {e}")

    def restore(self, zip_file_name: str):
        try:
            # Extract the zip file
            with zipfile.ZipFile(f"backups/{zip_file_name}", "r") as zipf:
                zipf.extractall()

            # Ensure the data.sql file exists
            if not os.path.exists("data.sql"):
                raise FileNotFoundError("data.sql not found in the zip file")

            if not os.path.exists("log_backup.log"):
                raise FileNotFoundError("log_backup.log not found in the zip file")

            # Disable foreign key checks to avoid conflicts
            cursor = self.config.con.cursor()
            cursor.execute("PRAGMA foreign_keys = OFF;")
            cursor.close()

            # Get the list of all tables
            cursor = self.config.con.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()

            # Drop all tables
            for table in tables:
                drop_table_sql = f"DROP TABLE IF EXISTS {table[0]}"
                cursor.execute(drop_table_sql)
                print(drop_table_sql)  # Debug print to see the drop statements

            # Commit changes to ensure all tables are dropped
            self.config.con.commit()

            # Open the SQL file in read mode
            with open("data.sql", "r") as f:
                # Execute the script to restore the database
                self.config.con.executescript(f.read())

            # Remove the temporary SQL file
            os.remove("data.sql")

            # Restore log file
            with open("log_backup.log", "r") as f:
                with open("app.log", "w") as log_file:
                    log_file.write(f.read())

            # Remove the temporary log file
            os.remove("log_backup.log")

            print(f"Database restored successfully from {zip_file_name}")
        except Exception as e:
            print(f"Error restoring backup: {e}")
        finally:
            # Re-enable foreign key checks
            cursor = self.config.con.cursor()
            cursor.execute("PRAGMA foreign_keys = ON;")
            cursor.close()

    def list(self):
        return [backup for backup in os.listdir("backups") if backup.endswith(".zip")]
