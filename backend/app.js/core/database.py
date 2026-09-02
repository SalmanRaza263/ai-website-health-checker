from supabase import create_client, Client
from app.core.config import config

supabase: Client = None

def get_supabase() -> Client:
    global supabase
    if supabase is None:
        supabase = create_client(config.SUPABASE_URL, config.SUPABASE_ANON_KEY)
    return supabase

def save_scan_result(scan_data: dict):
    """Save scan result to Supabase"""
    client = get_supabase()
    if client:
        try:
            result = client.table("scans").insert(scan_data).execute()
            return result.data
        except Exception as e:
            print(f"Error saving to Supabase: {e}")
    return None

def get_scan_history(user_id: str = None):
    """Get scan history from Supabase"""
    client = get_supabase()
    if client:
        try:
            query = client.table("scans").select("*").order("created_at", desc=True)
            if user_id:
                query = query.eq("user_id", user_id)
            result = query.execute()
            return result.data
        except Exception as e:
            print(f"Error getting history: {e}")
    return []