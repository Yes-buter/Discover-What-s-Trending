from api.core.database import supabase

def check():
    try:
        res = supabase.table("github_projects").select("*", count="exact").execute()
        print(f"Projects count: {res.count}")
        print(f"Projects: {res.data}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check()
