import asyncio
from api.core.database import supabase
from datetime import date, datetime

async def seed_data():
    print("Seeding data...")

    # Seed GitHub Projects
    projects = [
        {
            "repo_id": "1",
            "name": "fastapi",
            "full_name": "tiangolo/fastapi",
            "description": "FastAPI framework, high performance, easy to learn, fast to code, ready for production",
            "language": "Python",
            "stars": 65000,
            "forks": 5000,
            "url": "https://github.com/tiangolo/fastapi",
            "trending_date": date.today().isoformat()
        },
        {
            "repo_id": "2",
            "name": "react",
            "full_name": "facebook/react",
            "description": "A declarative, efficient, and flexible JavaScript library for building user interfaces.",
            "language": "JavaScript",
            "stars": 213000,
            "forks": 45000,
            "url": "https://github.com/facebook/react",
            "trending_date": date.today().isoformat()
        },
        {
            "repo_id": "3",
            "name": "rust",
            "full_name": "rust-lang/rust",
            "description": "Empowering everyone to build reliable and efficient software.",
            "language": "Rust",
            "stars": 85000,
            "forks": 11000,
            "url": "https://github.com/rust-lang/rust",
            "trending_date": date.today().isoformat()
        }
    ]

    for p in projects:
        try:
            supabase.table("github_projects").upsert(p, on_conflict="repo_id").execute()
            print(f"Upserted project: {p['name']}")
        except Exception as e:
            print(f"Error upserting project {p['name']}: {e}")

    # Seed Papers
    # First get categories
    cats = supabase.table("categories").select("*").execute()
    cat_id = cats.data[0]['id'] if cats.data else None

    papers = [
        {
            "title": "Attention Is All You Need",
            "abstract": "The dominant sequence transduction models are based on complex recurrent or convolutional neural networks that include an encoder and a decoder...",
            "authors": ["Ashish Vaswani", "Noam Shazeer", "Niki Parmar"],
            "pdf_url": "https://arxiv.org/pdf/1706.03762.pdf",
            "published_date": date.today().isoformat(),
            "source": "arxiv",
            "category_id": cat_id
        },
        {
            "title": "YOLOv8: A State-of-the-Art Real-time Object Detection System",
            "abstract": "We present YOLOv8, a new state-of-the-art computer vision model built by Ultralytics.",
            "authors": ["Ultralytics"],
            "code_url": "https://github.com/ultralytics/ultralytics",
            "published_date": date.today().isoformat(),
            "source": "github",
            "category_id": cat_id
        }
    ]

    for p in papers:
        try:
            supabase.table("papers").insert(p).execute()
            print(f"Inserted paper: {p['title']}")
        except Exception as e:
            print(f"Error inserting paper {p['title']}: {e}")

    print("Seeding complete!")

if __name__ == "__main__":
    asyncio.run(seed_data())
