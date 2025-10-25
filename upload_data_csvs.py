#!/usr/bin/env python3
"""
Upload all CSV files from data directory to Supabase
Each CSV file will create a table with the same name as the file

Usage: python upload_data_csvs.py
"""

import pandas as pd
import os
import glob
from supabase_client import supabase
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def upload_csv_to_table(csv_file_path: str, batch_size: int = 100):
    """
    Upload CSV data to Supabase table named after the CSV file
    
    Args:
        csv_file_path (str): Path to the CSV file
        batch_size (int): Number of rows to insert at once (default: 100)
    
    Returns:
        dict: Summary of upload results
    """
    try:
        # Get table name from CSV filename (remove .csv extension)
        table_name = os.path.splitext(os.path.basename(csv_file_path))[0]
        
        # Read CSV file
        print(f"📖 Reading CSV file: {csv_file_path}")
        df = pd.read_csv(csv_file_path)
        print(f"✅ CSV loaded successfully. Found {len(df)} rows")
        
        # Display column information
        print(f"📊 Columns: {list(df.columns)}")
        
        # Convert DataFrame to list of dictionaries
        data_list = df.to_dict('records')
        
        # Upload data in batches
        total_rows = len(data_list)
        successful_inserts = 0
        failed_inserts = 0
        
        print(f"🚀 Starting upload to table '{table_name}'...")
        
        for i in range(0, total_rows, batch_size):
            batch = data_list[i:i + batch_size]
            batch_num = (i // batch_size) + 1
            total_batches = (total_rows + batch_size - 1) // batch_size
            
            try:
                print(f"📦 Processing batch {batch_num}/{total_batches} ({len(batch)} rows)...")
                response = supabase.table(table_name).insert(batch).execute()
                
                if response.data:
                    successful_inserts += len(batch)
                    print(f"✅ Batch {batch_num} uploaded successfully")
                else:
                    print(f"⚠️  Batch {batch_num} - No data returned")
                    failed_inserts += len(batch)
                    
            except Exception as e:
                print(f"❌ Batch {batch_num} failed: {str(e)}")
                failed_inserts += len(batch)
        
        # Summary
        result = {
            "table_name": table_name,
            "total_rows": total_rows,
            "successful_inserts": successful_inserts,
            "failed_inserts": failed_inserts,
            "success_rate": (successful_inserts / total_rows) * 100 if total_rows > 0 else 0
        }
        
        print(f"📊 Upload Summary for '{table_name}':")
        print(f"   Total rows: {result['total_rows']}")
        print(f"   Successful: {result['successful_inserts']}")
        print(f"   Failed: {result['failed_inserts']}")
        print(f"   Success rate: {result['success_rate']:.1f}%")
        
        return result
        
    except FileNotFoundError:
        print(f"❌ Error: CSV file '{csv_file_path}' not found")
        return None
    except Exception as e:
        print(f"❌ Error uploading CSV: {str(e)}")
        return None

def verify_upload(table_name: str, limit: int = 5):
    """
    Verify the uploaded data by fetching from Supabase
    
    Args:
        table_name (str): Name of the table to check
        limit (int): Number of records to fetch
    """
    try:
        print(f"🔍 Verifying upload for table '{table_name}'...")
        response = supabase.table(table_name).select("*").limit(limit).execute()
        
        if response.data:
            print(f"✅ Found {len(response.data)} records in table '{table_name}'")
        else:
            print(f"⚠️  No records found in table '{table_name}'")
            
    except Exception as e:
        print(f"❌ Error verifying upload for '{table_name}': {str(e)}")

def upload_all_csvs_from_data():
    """
    Upload all CSV files from the data directory
    """
    data_dir = "data"
    
    # Check if data directory exists
    if not os.path.exists(data_dir):
        print(f"❌ Error: Directory '{data_dir}' not found")
        print("Please create a 'data' directory and add your CSV files there")
        return
    
    # Find all CSV files in data directory
    csv_files = glob.glob(os.path.join(data_dir, "*.csv"))
    
    if not csv_files:
        print(f"❌ No CSV files found in '{data_dir}' directory")
        print("Please add CSV files to the data directory")
        return
    
    print(f"🚀 Found {len(csv_files)} CSV files in '{data_dir}' directory")
    print("=" * 60)
    
    results = {}
    total_successful = 0
    total_failed = 0
    
    # Upload each CSV file
    for csv_file in csv_files:
        print(f"\n📁 Processing: {csv_file}")
        print("-" * 40)
        
        result = upload_csv_to_table(csv_file)
        
        if result:
            results[result['table_name']] = result
            if result['successful_inserts'] > 0:
                total_successful += result['successful_inserts']
                print(f"✅ {result['table_name']}: {result['successful_inserts']} rows uploaded")
            else:
                total_failed += result['failed_inserts']
                print(f"❌ {result['table_name']}: Upload failed")
        else:
            print(f"❌ Failed to process {csv_file}")
    
    # Overall summary
    print(f"\n🎯 Overall Upload Summary:")
    print("=" * 60)
    print(f"📁 Files processed: {len(csv_files)}")
    print(f"📊 Total successful rows: {total_successful}")
    print(f"📊 Total failed rows: {total_failed}")
    print(f"📋 Tables created: {len(results)}")
    
    # Verify uploads
    print(f"\n🔍 Verifying all uploads...")
    for table_name in results.keys():
        verify_upload(table_name)
    
    print(f"\n🎉 All CSV files from '{data_dir}' directory uploaded successfully!")

def create_sample_data():
    """
    Create sample CSV files in data directory for testing
    """
    data_dir = "data"
    
    # Create data directory if it doesn't exist
    os.makedirs(data_dir, exist_ok=True)
    
    # Sample data for different table types
    sample_datasets = {
        "users.csv": {
            "name": ["John Doe", "Jane Smith", "Bob Johnson", "Alice Brown", "Charlie Wilson"],
            "email": ["john@example.com", "jane@example.com", "bob@example.com", "alice@example.com", "charlie@example.com"],
            "age": [25, 30, 35, 28, 42],
            "city": ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"]
        },
        "products.csv": {
            "product_name": ["Laptop", "Mouse", "Keyboard", "Monitor", "Headphones"],
            "price": [999.99, 29.99, 79.99, 299.99, 149.99],
            "category": ["Electronics", "Accessories", "Accessories", "Electronics", "Accessories"],
            "stock": [50, 200, 150, 30, 75]
        }
    }
    
    print(f"📝 Creating sample CSV files in '{data_dir}' directory...")
    
    for filename, data in sample_datasets.items():
        filepath = os.path.join(data_dir, filename)
        df = pd.DataFrame(data)
        df.to_csv(filepath, index=False)
        print(f"✅ Created: {filepath}")
        print(f"📊 Columns: {list(df.columns)}")
        print(f"📋 Rows: {len(df)}")
    
    print(f"\n🎉 Sample data created in '{data_dir}' directory!")

if __name__ == "__main__":
    print("🚀 Data Directory CSV Uploader for Supabase")
    print("=" * 60)
    
    # Check if data directory exists and has CSV files
    if not os.path.exists("data") or not glob.glob("data/*.csv"):
        print("📝 No data directory or CSV files found. Creating sample data...")
        create_sample_data()
    
    # Upload all CSV files from data directory
    upload_all_csvs_from_data()
