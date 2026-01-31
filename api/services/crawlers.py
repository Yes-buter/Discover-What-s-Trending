import httpx
import feedparser
from bs4 import BeautifulSoup
from datetime import date, datetime, timedelta
from typing import List, Dict, Any
import asyncio
from api.core.database import supabase
import os

class BaseCrawler:
    async def fetch(self, url: str):
        # Explicitly use trust_env=False to bypass proxy issues if needed, or rely on our global fix
        # But we already patched create_client, not httpx global.
        # Let's check environment vars.
        proxies = None
        if os.environ.get("HTTP_PROXY"):
            proxies = os.environ.get("HTTP_PROXY")
            
        async with httpx.AsyncClient(verify=False, proxy=proxies) as client:
            response = await client.get(url, timeout=30.0)
            return response

class GithubCrawler(BaseCrawler):
    async def get_trending(self, language: str = "") -> List[Dict[str, Any]]:
        url = f"https://github.com/trending/{language}" if language else "https://github.com/trending"
        print(f"Crawling GitHub Trending: {url}")
        
        try:
            response = await self.fetch(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            rows = soup.select('article.Box-row')
            
            projects = []
            for row in rows:
                try:
                    # Get repo name and link
                    h1 = row.select_one('h2.h3 a')
                    if not h1:
                        continue
                        
                    full_name = h1.get_text(strip=True).replace(' ', '').replace('\n', '')
                    repo_url = f"https://github.com{h1['href']}"
                    repo_id = h1['href'].strip('/') # Simple ID
                    
                    parts = full_name.split('/')
                    name = parts[1] if len(parts) > 1 else full_name
                    
                    # Description
                    desc_elem = row.select_one('p.col-9')
                    description = desc_elem.get_text(strip=True) if desc_elem else None
                    
                    # Language
                    lang_elem = row.select_one('span[itemprop="programmingLanguage"]')
                    language_val = lang_elem.get_text(strip=True) if lang_elem else None
                    
                    # Stars and Forks
                    stats = row.select('a.Link--muted')
                    stars_str = stats[0].get_text(strip=True).replace(',', '') if len(stats) > 0 else "0"
                    forks_str = stats[1].get_text(strip=True).replace(',', '') if len(stats) > 1 else "0"
                    
                    stars = int(stars_str)
                    forks = int(forks_str)
                    
                    project = {
                        "repo_id": repo_id,
                        "name": name,
                        "full_name": full_name,
                        "description": description,
                        "language": language_val,
                        "stars": stars,
                        "forks": forks,
                        "url": repo_url,
                        "trending_date": date.today().isoformat()
                    }
                    projects.append(project)
                except Exception as e:
                    print(f"Error parsing row: {e}")
                    continue
                    
            return projects
        except Exception as e:
            print(f"Error crawling GitHub: {e}")
            return []

class ArxivCrawler(BaseCrawler):
    async def get_cv_papers(self, max_results: int = 20) -> List[Dict[str, Any]]:
        # CS.CV is Computer Vision
        url = f"http://export.arxiv.org/api/query?search_query=cat:cs.CV&start=0&max_results={max_results}&sortBy=submittedDate&sortOrder=descending"
        print(f"Crawling ArXiv: {url}")
        
        try:
            # feedparser handles XML fetching and parsing, but it's synchronous. 
            # We can use it with the raw content from httpx if we want async, or run it in executor.
            # Here for simplicity we fetch with httpx then parse string.
            response = await self.fetch(url)
            feed = feedparser.parse(response.text)
            
            papers = []
            
            # Get category ID for 'Computer Vision'
            # In a real app we might cache this or look it up properly
            cats = supabase.table("categories").select("id").eq("slug", "object-detection").execute()
            # Fallback if specific category not found (just use first one or None)
            category_id = cats.data[0]['id'] if cats.data else None
            
            if not category_id:
                # Try to get any category or create one
                cats = supabase.table("categories").select("id").limit(1).execute()
                category_id = cats.data[0]['id'] if cats.data else None

            for entry in feed.entries:
                try:
                    # Extract authors
                    authors = [author.name for author in entry.authors]
                    
                    # Extract PDF link
                    pdf_url = None
                    for link in entry.links:
                        if link.type == 'application/pdf':
                            pdf_url = link.href
                            
                    paper = {
                        "title": entry.title.replace('\n', ' '),
                        "abstract": entry.summary.replace('\n', ' '),
                        "authors": authors,
                        "pdf_url": pdf_url,
                        "published_date": datetime(*entry.published_parsed[:6]).date().isoformat(),
                        "source": "arxiv",
                        "category_id": category_id
                    }
                    papers.append(paper)
                except Exception as e:
                    print(f"Error parsing paper: {e}")
                    continue
                    
            return papers
        except Exception as e:
            print(f"Error crawling ArXiv: {e}")
            return []

class HackerNewsCrawler(BaseCrawler):
    """
    Crawls Hacker News top stories.
    """
    async def get_top_stories(self, limit: int = 20) -> List[Dict[str, Any]]:
        top_stories_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
        print(f"Crawling Hacker News: {top_stories_url}")
        
        try:
            response = await self.fetch(top_stories_url)
            story_ids = response.json()[:limit]
            
            papers = []
            
            # Get a category for HN
            cats = supabase.table("categories").select("id").eq("slug", "hacker-news").execute()
            if not cats.data:
                res = supabase.table("categories").insert({
                    "name": "Hacker News", 
                    "slug": "hacker-news", 
                    "description": "Top stories from Hacker News"
                }).execute()
                category_id = res.data[0]['id']
            else:
                category_id = cats.data[0]['id']
            
            # Fetch details for each story
            # This could be optimized with asyncio.gather
            for sid in story_ids:
                try:
                    item_url = f"https://hacker-news.firebaseio.com/v0/item/{sid}.json"
                    item_resp = await self.fetch(item_url)
                    item = item_resp.json()
                    
                    if not item or item.get('type') != 'story':
                        continue
                        
                    paper = {
                        "title": item.get('title'),
                        "abstract": f"Score: {item.get('score', 0)} | Comments: {item.get('descendants', 0)}",
                        "authors": [item.get('by', 'unknown')],
                        "pdf_url": item.get('url', f"https://news.ycombinator.com/item?id={sid}"), 
                        "published_date": datetime.fromtimestamp(item.get('time')).date().isoformat(),
                        "source": "hackernews", 
                        "category_id": category_id
                    }
                    papers.append(paper)
                except Exception as e:
                    print(f"Error parsing HN story {sid}: {e}")
                    continue
            
            return papers

        except Exception as e:
            print(f"Error crawling Hacker News: {e}")
            return []

class CrawlerService:
    def __init__(self):
        self.github = GithubCrawler()
        self.arxiv = ArxivCrawler()
        self.hn = HackerNewsCrawler()

    async def crawl_all(self):
        print("Starting full crawl...")
        
        # 1. GitHub
        projects = await self.github.get_trending()
        for p in projects:
            try:
                supabase.table("github_projects").upsert(p, on_conflict="repo_id").execute()
            except Exception as e:
                print(f"Failed to save project {p['name']}: {e}")
        print(f"Saved {len(projects)} GitHub projects.")

        # 2. ArXiv
        papers = await self.arxiv.get_cv_papers()
        for p in papers:
            try:
                supabase.table("papers").insert(p).execute()
            except Exception as e:
                # print(f"Failed to save paper {p['title']}: {e}")
                pass # Ignore duplicate inserts for now
        print(f"Saved {len(papers)} ArXiv papers.")
        
        # 3. Hacker News
        hn_items = await self.hn.get_top_stories()
        for n in hn_items:
            try:
                supabase.table("papers").insert(n).execute()
            except Exception as e:
                # print(f"Failed to save HN item {n['title']}: {e}")
                pass
        print(f"Saved {len(hn_items)} HN items.")
        
        return {"status": "success", "message": f"Crawled {len(projects)} projects, {len(papers)} papers, {len(hn_items)} HN items"}

crawler_service = CrawlerService()
