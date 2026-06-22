from db import supabase

# INSERT — keys must match column names
supabase.table("knowledge_base").insert({"category": "author", "verified", "usage_count ", "created_a}).execute()

# SELECT with a filter, sorted, capped
resp = supabase.table("knowledge_base") \
    .select("*") \
    .eq("category", category) \
    .eq("verified", True) \
    .order("usage_count", desc=True) \
    .limit(1) \
    .execute()

resp.data   # -> a LIST of row dicts; [] if nothing matched