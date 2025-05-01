from azure.cosmos import CosmosClient, PartitionKey
import os
from dotenv import load_dotenv

load_dotenv()

class CosmosDBSetup:
    def __init__(self):
        self.endpoint = os.getenv("AZURE_COSMOS_ENDPOINT")
        self.key = os.getenv("AZURE_COSMOS_KEY")
        self.client = CosmosClient(self.endpoint, self.key)
        self.database_name = "Member360DB"
        self.database = self.client.create_database_if_not_exists(id=self.database_name)

    def setup_containers(self):
        # Members container
        members_container = self.database.create_container_if_not_exists(
            id="Members",
            partition_key=PartitionKey(path="/id")
        )

        # Documents container
        documents_container = self.database.create_container_if_not_exists(
            id="Documents",
            partition_key=PartitionKey(path="/memberId")
        )

        # Interactions container
        interactions_container = self.database.create_container_if_not_exists(
            id="Interactions",
            partition_key=PartitionKey(path="/memberId")
        )

        return {
            "members": members_container,
            "documents": documents_container,
            "interactions": interactions_container
        }

    def generate_sample_data(self):
        from faker import Faker
        import random
        from datetime import datetime, timedelta

        fake = Faker()
        containers = self.setup_containers()

        # Generate sample members
        for _ in range(50):
            member = {
                "id": fake.uuid4(),
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
            containers["members"].create_item(body=member)

            # Generate sample documents for each member
            for _ in range(random.randint(1, 5)):
                document = {
                    "id": fake.uuid4(),
                    "memberId": member["id"],
                    "documentType": random.choice(["ID", "Contract", "Invoice", "Statement"]),
                    "uploadDate": fake.date_between(start_date="-1y", end_date="today").isoformat(),
                    "status": random.choice(["Verified", "Pending", "Rejected"]),
                    "url": fake.url()
                }
                containers["documents"].create_item(body=document)

            # Generate sample interactions for each member
            for _ in range(random.randint(1, 10)):
                interaction = {
                    "id": fake.uuid4(),
                    "memberId": member["id"],
                    "type": random.choice(["Call", "Email", "Chat", "Meeting"]),
                    "date": fake.date_between(start_date="-1y", end_date="today").isoformat(),
                    "summary": fake.sentence(),
                    "status": random.choice(["Completed", "Pending", "Follow-up Required"])
                }
                containers["interactions"].create_item(body=interaction)

if __name__ == "__main__":
    db_setup = CosmosDBSetup()
    db_setup.generate_sample_data() 