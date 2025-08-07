from faker import Faker
# Импортируем объекты из новой структуры
from app.database import users_collection, client

# --- Configuration ---
COLLECTION_NAME = "users"
NUM_USERS = 500

# --- Seeder Logic ---
def seed_database():
    try:
        print("--- Database Seeder ---")
        # Теперь нам не нужно создавать client, мы его импортируем
        collection = users_collection

        if collection.count_documents({}) > 0:
            print(f"Collection '{COLLECTION_NAME}' is not empty. Seeding skipped.")
            return

        fake = Faker()
        users_to_insert = []
        for _ in range(NUM_USERS):
            users_to_insert.append({"name": fake.name(), "email": fake.unique.email()})
        
        print(f"Seeding database with {NUM_USERS} users...")
        collection.insert_many(users_to_insert)
        print("Seeding completed successfully!")

    except Exception as e:
        print(f"An error occurred during seeding: {e}")
    finally:
        # Важно закрывать клиент после завершения работы сидера
        client.close()
        print("MongoDB connection closed by seeder.")

if __name__ == "__main__":
    seed_database()
