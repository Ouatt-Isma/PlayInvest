import os, time, datetime as dt
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from sqlalchemy import create_engine, text
import re
import os
from urllib.parse import urlparse
from hashlib import sha1

BASE = "https://www.sikafinance.com"
LIST_URL = "https://www.sikafinance.com/marches/actualites_bourse_brvm"

# --- DB setup (use env vars) ---
# DB_URL = os.getenv(
#     "DATABASE_URL",
#     "postgresql+psycopg://user:password@localhost:5432/mydb"
# )
# engine = create_engine(DB_URL, future=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; SikaScraper/1.0; +https://example.com/bot)"
}

import json
from urllib.parse import urljoin, urlparse
from hashlib import sha1

def extract_body(soup):
    # Find the main text container
    container = soup.find("div", class_="inarticle")
    if not container:
        container = soup.find("article") or soup

    paragraphs = []
    for p in container.find_all("p"):
        txt = p.get_text(" ", strip=True)
        if not txt:
            continue
        # Skip unwanted lines
        if any(skip in txt for skip in [
            "CONNECTEZ-VOUS",
            "Identifiant oublié",
            "Créer un compte gratuit",
            "Liste de valeurs",
            "Portefeuille virtuel",
            "Mon compte",
            "Se déconnecter",
            "Pour poster un commentaire"
        ]):
            continue
        # Optional: skip 'Voir aussi - ...' or keep only the plain part
        if txt.startswith("Voir aussi"):
            continue
        # Stop if it's just author or published date
        if re.match(r"^Publié le\s", txt) or re.match(r"^[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+$", txt):
            continue
        paragraphs.append(txt)

    return "\n\n".join(paragraphs) if paragraphs else None


def parse_jsonld_image(soup, page_url):
    # Find the NewsArticle JSON-LD and pull image.url if present
    for tag in soup.find_all("script", attrs={"type":"application/ld+json"}):
        try:
            data = json.loads(tag.string or "")
        except Exception:
            continue
        if isinstance(data, dict) and data.get("@type") in ("NewsArticle","Article"):
            img = data.get("image")
            # image can be string, dict, or list
            if isinstance(img, str):
                return urljoin(page_url, img)
            if isinstance(img, dict) and img.get("url"):
                return urljoin(page_url, img["url"])
            if isinstance(img, list) and img:
                first = img[0]
                if isinstance(first, str):
                    return urljoin(page_url, first)
                if isinstance(first, dict) and first.get("url"):
                    return urljoin(page_url, first["url"])
    return None

def parse_og_image(soup, page_url):
    for prop in ["og:image:url","og:image","twitter:image"]:
        tag = soup.find("meta", attrs={"property": prop}) or soup.find("meta", attrs={"name": prop})
        if tag and tag.get("content"):
            return urljoin(page_url, tag["content"].strip())
    return None

def parse_article_image(soup, page_url):
    # Prefer the in-article handler first
    article = soup.find("article") or soup
    # 1) direct handler img (your example)
    img = article.find("img", src=re.compile(r"handlers/image_news_get\.ashx", re.I))
    if img and img.get("src"):
        return urljoin(page_url, img["src"])

    # 2) any other <img> in the article (src/srcset/lazy)
    img = article.find("img")
    if img:
        for k in ["src", "data-src", "data-original", "data-lazy", "data-srcset", "srcset"]:
            v = img.get(k)
            if not v:
                continue
            if "srcset" in k:
                v = v.split(",")[0].strip().split(" ")[0]
            if v:
                return urljoin(page_url, v.strip())

    return None

def pick_image_url(soup, page_url):
    # 1) article handler
    url = parse_article_image(soup, page_url)
    if url:
        return url
    # 2) JSON-LD
    url = parse_jsonld_image(soup, page_url)
    if url:
        return url
    # 3) OG/Twitter
    url = parse_og_image(soup, page_url)
    return url


def get_soup(url):
    r = requests.get(url, headers=HEADERS, timeout=20)
    r.raise_for_status()
    return BeautifulSoup(r.text, "lxml")

def parse_listing():
    soup = get_soup(LIST_URL)
    items = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        # normalize to absolute URL
        url = urljoin(BASE, href)

        # keep only article-like URLs and ensure they end with _<digits>
        if "/marches/" in href and re.search(r'_\d+(?:$|\?)', href):
            title = a.get_text(strip=True)

            # try to find a nearby timestamp like "08/08/2025 14:53"
            parent_text = a.parent.get_text(" ", strip=True) if a.parent else ""
            m = re.search(r"(\d{2}/\d{2}/\d{4}\s+\d{2}:\d{2})", parent_text)
            ts = None
            if m:
                ts = dt.datetime.strptime(m.group(1), "%d/%m/%Y %H:%M")

            items.append({"title": title, "url": url, "published_at": ts})

    # de-dupe by URL
    seen, unique = set(), []
    for it in items:
        if it["url"] not in seen:
            seen.add(it["url"])
            unique.append(it)
    return unique

def parse_article(url, *, download=False):
    soup = get_soup(url)

    # Title
    h1 = soup.find(["h1", "h2"])
    title = h1.get_text(strip=True) if h1 else None

    # Author
    author = None
    pub_node = soup.find(string=re.compile(r"Publié le"))
    if not author:
        sig = soup.find("p", class_="dt_sign")
        if sig and not sig.get_text(strip=True).startswith("Publié"):
            author = sig.get_text(strip=True)

    # Date
    published_at = None
    if pub_node:
        m = re.search(r"(\d{2}/\d{2}/\d{2,4}\s+\d{2}:\d{2})", pub_node)
        if m:
            fmt = "%d/%m/%y %H:%M" if len(m.group(1).split("/")[-1].split()[0]) == 2 else "%d/%m/%Y %H:%M"
            published_at = dt.datetime.strptime(m.group(1), fmt)

    # Body (cleaned)
    body = extract_body(soup)

    # Image
    image_url = pick_image_url(soup, url)
    image_path = None
    if download and image_url:
        try:
            image_path = download_image(image_url)
        except Exception:
            pass

    return title, author, published_at, body, image_url, image_path

# def upsert_article(row):
#     with engine.begin() as conn:
#         conn.execute(text("""
#             INSERT INTO news (url, title, published_at, author, body, source)
#             VALUES (:url, :title, :published_at, :author, :body, 'sikafinance')
#             ON CONFLICT (url) DO UPDATE SET
#               title = EXCLUDED.title,
#               published_at = COALESCE(EXCLUDED.published_at, news.published_at),
#               author = COALESCE(EXCLUDED.author, news.author),
#               body = COALESCE(EXCLUDED.body, news.body)
#         """), row)


def download_image(image_url, dest_dir="images"):
    os.makedirs(dest_dir, exist_ok=True)
    # keep extension if present; default to .jpg
    parsed = urlparse(image_url)
    name = os.path.basename(parsed.path)
    ext = os.path.splitext(name)[1].lower() or ".jpg"
    # deterministic filename from URL
    fn = sha1(image_url.encode("utf-8")).hexdigest() + ext
    path = os.path.join(dest_dir, fn)

    r = requests.get(image_url, headers=HEADERS, timeout=30, stream=True)
    r.raise_for_status()
    with open(path, "wb") as f:
        for chunk in r.iter_content(8192):
            if chunk:
                f.write(chunk)
    return path


def main():
    items = parse_listing()
    for i, it in enumerate(items, start=1):
        # try:
            title, author, pub, body, image_url, image_path = parse_article(it["url"])
            row = {
                "url": it["url"],
                "title": title or it["title"],
                "published_at": pub or it["published_at"],
                "author": author,
                "body": body,
                "image_url": image_url,
                "image_path": image_path,  # may be None if download=False
            }
            print(row)
            if(i==2):
                raise NotImplementedError
            # upsert_article(row)
            # print(f"[{i}/{len(items)}] Saved: {row['title']}")
            # time.sleep(1.2)  # be polite
        # except Exception as e:
        #     print(f"Error on {it['url']}: {e}")

if __name__ == "__main__":
    main()
