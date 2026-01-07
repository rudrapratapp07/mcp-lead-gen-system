import requests
import time
import sys

BASE_URL = "http://localhost:8000"

def test_pipeline():
    print("1. Testing Connection...")
    try:
        requests.get(f"{BASE_URL}/tools/get_stats")
    except:
        print("Error: Backend not running at http://localhost:8000")
        sys.exit(1)

    print("2. Generating Leads...")
    res = requests.post(f"{BASE_URL}/tools/generate_leads", json={"count": 5})
    data = res.json()
    print(f"   Generated {data['count']} leads. IDs: {data['ids']}")
    lead_ids = data['ids']

    print("3. Processing Leads...")
    for lid in lead_ids:
        print(f"   Processing Lead {lid}...")
        
        # Enrich
        res = requests.post(f"{BASE_URL}/tools/enrich_lead", json={"lead_id": lid})
        if res.json()['status'] != 'success':
            print(f"Failed to enrich {lid}")
            continue
            
        # Message
        res = requests.post(f"{BASE_URL}/tools/generate_messages", json={"lead_id": lid})
        if res.json()['status'] != 'success':
            print(f"Failed to message {lid}")
            continue

        # Send
        res = requests.post(f"{BASE_URL}/tools/send_message", json={"lead_id": lid, "mode": "dry_run"})
        if res.json()['status'] != 'success':
            print(f"Failed to send {lid}")
            continue
            
    print("4. Verifying Stats...")
    stats = requests.get(f"{BASE_URL}/tools/get_stats").json()
    print("   Stats:", stats)
    
    if stats['sent'] >= len(lead_ids):
        print("SUCCESS: Pipeline verified.")
    else:
        print("WARNING: Stats might not match expected count (could be previous data).")

if __name__ == "__main__":
    test_pipeline()
