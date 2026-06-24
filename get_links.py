import requests
import sys
import io
import os
from dotenv import load_dotenv

load_dotenv()

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

PREFERENCES = {
    "position_title": "Full Stack Developer",
    "location": "Philippines"
}

ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID", "ab6d6b10")
ADZUNA_API_KEY = os.getenv("ADZUNA_API_KEY", "74c6ed0544b5db7fe0a65f75ae85f482")

ATS_DOMAINS = {"lever.co", "greenhouse.io", "ashbyhq.com"}


def search_adzuna():
    if not ADZUNA_APP_ID or not ADZUNA_API_KEY:
        return []
    countries = ["sg", "au", "gb", "in"]
    what = PREFERENCES["position_title"]
    all_jobs = []
    for country in countries:
        url = f"https://api.adzuna.com/v1/api/jobs/{country}/search/1"
        params = {"app_id": ADZUNA_APP_ID, "app_key": ADZUNA_API_KEY, "results_per_page": 50, "what": what, "max_days_old": 30}
        try:
            resp = requests.get(url, params=params, timeout=30)
            if resp.status_code != 200:
                continue
            data = resp.json()
            count = data.get("count", 0)
            print(f"[{country}] {count} jobs")
            for job in data.get("results", []):
                ru = job.get("redirect_url", "")
                if ru:
                    all_jobs.append({
                        "title": job.get("title", ""),
                        "company": job.get("company", {}).get("display_name", ""),
                        "country": country,
                        "redirect_url": ru,
                    })
        except Exception as e:
            print(f"[{country}] err: {e}")
    return all_jobs


def resolve_redirects(jobs):
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})
    found = set()
    for i, job in enumerate(jobs):
        title_s = job["title"].encode("ascii", "replace").decode()[:40]
        company_s = job["company"].encode("ascii", "replace").decode()[:20]
        print(f"  [{i+1}/{len(jobs)}] {title_s} @ {company_s}...", end=" ", flush=True)
        try:
            r = session.get(job["redirect_url"], allow_redirects=True, timeout=10)
            final = r.url.lower()
            matched = [d for d in ATS_DOMAINS if d in final]
            if matched:
                found.add(r.url)
                print(f"ATS: {r.url}")
            else:
                domain = r.url.split("/")[2] if "//" in r.url else r.url[:60]
                print(f"-> {domain}")
        except Exception as e:
            print(f"err: {e}")

    if found:
        print(f"\nATS URLs found via Adzuna: {len(found)}")
        for u in sorted(found):
            print(f"  {u}")
    else:
        print("\nNo ATS URLs found via Adzuna (Adzuna redirects go to adzuna.sg pages, not directly to Lever/GH)")
    return found


def getURLs():
    print(f"Searching Adzuna for '{PREFERENCES['position_title']}'...")
    jobs = search_adzuna()
    if not jobs:
        print("No jobs found.")
        return set()

    print(f"\nResolving {len(jobs)} redirect URLs...")
    urls = resolve_redirects(jobs)
    return urls


if __name__ == "__main__":
    getURLs()
