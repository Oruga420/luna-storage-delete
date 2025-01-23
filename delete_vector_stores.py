import os
from openai import OpenAI
from dotenv import load_dotenv
import argparse
import time

# Load environment variables from the specific .env file
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

class VectorStoreDeleter:
    def __init__(self):
        self.api_key = os.getenv('LUNAS_OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("LUNAS_OPENAI_API_KEY not found in environment variables")
        
        self.client = OpenAI(api_key=self.api_key)

    def delete_vector_store(self, vector_store_id):
        """Delete a specific vector store by ID"""
        try:
            print(f"\nAttempting to delete vector store: {vector_store_id}")
            response = self.client.beta.vector_stores.delete(vector_store_id=vector_store_id)
            print(f"Successfully deleted vector store: {vector_store_id}")
            return response
        except Exception as e:
            print(f"Error deleting vector store {vector_store_id}: {str(e)}")
            return None

    def list_vector_stores(self):
        """List all vector stores"""
        try:
            print(f"\nChecking available vector stores...")
            response = self.client.beta.vector_stores.list()
            return response
        except Exception as e:
            print(f"Error listing vector stores: {str(e)}")
            return None

    def delete_specific_vector_stores(self, vector_store_ids):
        """Delete specific vector stores by their IDs"""
        print(f"Attempting to delete {len(vector_store_ids)} vector stores...")
        for vector_store_id in vector_store_ids:
            result = self.delete_vector_store(vector_store_id.strip())
            if result:
                print(f"✓ Vector store {vector_store_id} deleted successfully")
            else:
                print(f"✗ Failed to delete vector store {vector_store_id}")
            print("-" * 50)

    def delete_all_vector_stores(self):
        """Delete all vector stores"""
        vector_stores = self.list_vector_stores()
        if not vector_stores:
            print("No vector stores found or unable to list vector stores")
            return

        for store in vector_stores.data:
            self.delete_vector_store(store.id)

    def interactive_delete(self):
        """Interactive mode to delete vector stores"""
        print("\nEnter vector store IDs to delete (one per line)")
        print("Press Enter twice to start deletion")
        print("----------------------------------------")
        
        vector_store_ids = []
        while True:
            id_input = input("\nEnter vector store ID (or press Enter to finish): ").strip()
            if id_input == "":
                if len(vector_store_ids) == 0:
                    print("No IDs entered. Exiting...")
                    return
                break
            vector_store_ids.append(id_input)
            print(f"Added ID: {id_input} to deletion list")
        
        print(f"\nYou entered {len(vector_store_ids)} IDs:")
        for vid in vector_store_ids:
            print(f"- {vid}")
        
        confirm = input("\nDo you want to proceed with deletion? (y/N): ").strip().lower()
        if confirm == 'y':
            self.delete_specific_vector_stores(vector_store_ids)
        else:
            print("Deletion cancelled.")

def main():
    # Initialize OpenAI client with API key
    client = OpenAI(api_key=os.getenv('LUNAS_OPENAI_API_KEY'))
    
    # Get vector store IDs from user
    vector_store_ids = input("Enter the vector store IDs to delete (separated by commas): ").strip()
    
    # Split the input into individual IDs and clean them
    ids = [id.strip() for id in vector_store_ids.split(',') if id.strip()]
    
    print(f"\nPreparing to delete {len(ids)} vector stores...")
    print("Vector stores to delete:")
    for id in ids:
        print(f"- {id}")
    
    confirm = input("\nDo you want to proceed with deletion? (y/N): ").strip().lower()
    if confirm != 'y':
        print("Deletion cancelled.")
        return
        
    print("\nStarting deletion process...")
    for i, vector_store_id in enumerate(ids, 1):
        try:
            print(f"\n[{i}/{len(ids)}] Deleting vector store: {vector_store_id}")
            deleted_vector_store = client.beta.vector_stores.delete(
                vector_store_id=vector_store_id
            )
            print(f"✓ Successfully deleted vector store: {vector_store_id}")
            print(f"Response: {deleted_vector_store}")
            
            # Add cooldown between deletions (except for the last one)
            if i < len(ids):
                print(f"Waiting 2 seconds before next deletion...")
                time.sleep(2)
                
        except Exception as e:
            print(f"✗ Error deleting vector store {vector_store_id}: {str(e)}")
            
            # Still wait before next deletion even if there was an error
            if i < len(ids):
                print(f"Waiting 2 seconds before next deletion...")
                time.sleep(2)
    
    print("\nDeletion process completed!")

if __name__ == "__main__":
    main() 
