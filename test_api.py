#!/usr/bin/env python3
"""
Simple test script to verify the AUC Digital Archive API is working.
"""

import requests
import json
from auc_archive_chatbot import AUCArchiveAPI

def test_api():
    """Test basic API functionality."""
    print("🧪 Testing AUC Digital Archive API...")
    
    api = AUCArchiveAPI()
    
    # Test 1: Get collections list
    print("\n1. Testing dmGetCollectionList...")
    collections = api.get_collections()
    
    if "error" in collections:
        print(f"❌ Error: {collections['error']}")
        return False
    
    if isinstance(collections, list) and len(collections) > 0:
        print(f"✅ Found {len(collections)} collections")
        print(f"   First collection: {collections[0].get('name', 'Unknown')}")
    else:
        print("❌ No collections found or unexpected response format")
        print(f"Response: {collections}")
        return False
    
    # Test 2: Get collection field info for first collection
    if collections:
        first_collection = collections[0]
        alias = first_collection.get('alias', '')
        
        print(f"\n2. Testing dmGetCollectionFieldInfo for '{alias}'...")
        field_info = api.get_collection_info(alias)
        
        if "error" in field_info:
            print(f"❌ Error: {field_info['error']}")
        elif isinstance(field_info, list):
            print(f"✅ Found {len(field_info)} fields for collection")
        else:
            print(f"⚠️  Unexpected response format: {type(field_info)}")
    
    # Test 3: Browse items in first collection
    if collections:
        alias = collections[0].get('alias', '')
        
        print(f"\n3. Testing dmQuery (browse) for '{alias}'...")
        items = api.browse_collection(alias, max_records=5)
        
        if "error" in items:
            print(f"❌ Error: {items['error']}")
        elif items.get('records'):
            print(f"✅ Found {len(items['records'])} items")
            first_item = items['records'][0]
            print(f"   First item: {first_item.get('title', 'Unknown title')}")
        else:
            print("⚠️  No items found or unexpected response")
            print(f"Response: {items}")
    
    print("\n🎉 API test completed!")
    return True

if __name__ == "__main__":
    test_api()