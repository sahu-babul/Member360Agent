import json
from faker import Faker
import random
from datetime import datetime, timedelta
import os

class LocalDataSetup:
    def __init__(self):
        self.data_dir = "data"
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    def generate_sample_data(self):
        fake = Faker()
        
        # Initialize data structures
        members = []
        documents = []
        interactions = []

        # Generate sample members
        for _ in range(50):
            member_id = fake.uuid4()
            member = {
                "id": member_id,
                "firstName": fake.first_name(),
                "lastName": fake.last_name(),
                "email": fake.email(),
                "phone": fake.phone_number(),
                "address": fake.address(),
                "membershipType": random.choice(["Basic", "Premium", "Gold"]),
                "joinDate": fake.date_between(start_date="-5y", end_date="today").isoformat(),
                "status": random.choice(["Active", "Inactive", "Pending"]),
                "lastInteraction": fake.date_between(start_date="-1y", end_date="today").isoformat()
            }
            members.append(member)

            # Generate sample documents for each member
            for _ in range(random.randint(1, 5)):
                document = {
                    "id": fake.uuid4(),
                    "memberId": member_id,
                    "documentType": random.choice(["ID", "Contract", "Invoice", "Statement"]),
                    "uploadDate": fake.date_between(start_date="-1y", end_date="today").isoformat(),
                    "status": random.choice(["Verified", "Pending", "Rejected"]),
                    "url": fake.url()
                }
                documents.append(document)

            # Generate sample interactions for each member
            for _ in range(random.randint(1, 10)):
                interaction = {
                    "id": fake.uuid4(),
                    "memberId": member_id,
                    "type": random.choice(["Call", "Email", "Chat", "Meeting"]),
                    "date": fake.date_between(start_date="-1y", end_date="today").isoformat(),
                    "summary": fake.sentence(),
                    "status": random.choice(["Completed", "Pending", "Follow-up Required"])
                }
                interactions.append(interaction)

        # Save data to JSON files
        with open(os.path.join(self.data_dir, "members.json"), "w") as f:
            json.dump(members, f, indent=2)

        with open(os.path.join(self.data_dir, "documents.json"), "w") as f:
            json.dump(documents, f, indent=2)

        with open(os.path.join(self.data_dir, "interactions.json"), "w") as f:
            json.dump(interactions, f, indent=2)

        print(f"Generated {len(members)} members")
        print(f"Generated {len(documents)} documents")
        print(f"Generated {len(interactions)} interactions")
        print(f"Data saved in the '{self.data_dir}' directory")

if __name__ == "__main__":
    data_setup = LocalDataSetup()
    data_setup.generate_sample_data() 