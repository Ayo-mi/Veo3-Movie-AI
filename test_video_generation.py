#!/usr/bin/env python3
"""
Test script to debug video generation issues
"""

import os
import sys
from google import genai
from google.genai import types

from generate_video import client


def test_api_connection():
    """Test if the API connection works"""
    try:
        if "GEMINI_KEY" not in os.environ:
            print("❌ GEMINI_KEY environment variable is not set!")
            return False
            
        client = genai.Client(api_key=os.environ["GEMINI_KEY"])
        print("✅ API client created successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to create API client: {e}")
        return False

def test_video_generation():
    """Test a simple video generation"""
    try:
        client = genai.Client(api_key=os.environ["GEMINI_KEY"])
        
        print("🔄 Testing video generation with simple prompt...")
        
        # Try a simple prompt first
        operation = client.models.generate_videos(
            model="models/veo-3.0-generate-preview",
            prompt="A simple red circle on a white background",
            config=types.GenerateVideosConfig(negative_prompt="barking, woofing"),
        )
        
        print(f"✅ Operation created: {operation}")
        print(f"Operation type: {type(operation)}")
        print(f"Operation attributes: {[attr for attr in dir(operation) if not attr.startswith('_')]}")
        
        # Check if operation has a name or ID
        if hasattr(operation, 'name'):
            print(f"Operation name: {operation.name}")
        if hasattr(operation, 'id'):
            print(f"Operation ID: {operation.id}")
            
        return operation
        
    except Exception as e:
        print(f"❌ Video generation failed: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_operation_polling(operation):
    """Test polling the operation status"""
    try:
        print("🔄 Testing operation polling...")
        
        # Try to get the operation status
        updated_operation = client.operations.get(operation)
        print(f"✅ Operation retrieved: {updated_operation}")
        print(f"Operation done: {updated_operation.done}")
        
        if hasattr(updated_operation, 'response'):
            print(f"Operation response: {updated_operation.response}")
        if hasattr(updated_operation, 'error'):
            print(f"Operation error: {updated_operation.error}")
            
        return updated_operation
        
    except Exception as e:
        print(f"❌ Operation polling failed: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    print("🧪 Testing Video Generation Setup")
    print("=" * 50)
    
    # Test 1: API Connection
    print("\n1. Testing API Connection...")
    if not test_api_connection():
        sys.exit(1)
    
    # Test 2: Video Generation
    print("\n2. Testing Video Generation...")
    operation = test_video_generation()
    if not operation:
        sys.exit(1)
    
    # Test 3: Operation Polling
    print("\n3. Testing Operation Polling...")
    updated_operation = test_operation_polling(operation)
    if not updated_operation:
        sys.exit(1)
    
    print("\n✅ All basic tests passed!")
    print("\nNext steps:")
    print("1. Run the full video generation script")
    print("2. Check the debug output for any issues")
    print("3. Verify that videos are being saved to the movie_clips directory")
