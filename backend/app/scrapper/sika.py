import os, time, datetime as dt
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from sqlalchemy import create_engine, text
import re
import os
from urllib.parse import urlparse
from hashlib import sha1
from typing import Optional, Tuple
from app.core.paths import MEDIA_DIR, MEDIA_URL

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

def parse_article(url, *, download=True):
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
            image_path = download_image_png(image_url)
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


import os, io, hashlib, requests
from PIL import Image

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; SikaScraper/1.0)",
    # "Referer": page_url,  # uncomment and pass if the site requires it
    "Accept": "image/avif,image/webp,image/apng,image/*;q=0.8,*/*;q=0.5",
}

ALLOWED_FORMATS = {
    "JPEG": ".jpg",
    "PNG":  ".png",
    "WEBP": ".webp",
    "GIF":  ".gif",   # keep if you need gifs; otherwise re-encode to webp/jpg
}

MIME_TO_EXT = {
    "image/jpeg": ".jpg",
    "image/jpg":  ".jpg",
    "image/png":  ".png",
    "image/webp": ".webp",
    "image/gif":  ".gif",
    # optionally: "image/avif": ".avif",
}



# def download_image_safely(
#     image_url: str,
#     *,
#     max_bytes: int = 10_000_000,
#     max_side: int = 4096,
#     page_url: Optional[str] = None
# ) -> Tuple[str, str]:
#     """
#     Downloads, type-sniffs, sanitizes, and saves an image.
#     Returns (file_path, public_url). Never uses '.ashx' — picks a real extension.
#     """
#     os.makedirs(MEDIA_DIR, exist_ok=True)
#     headers = dict(HEADERS)
#     if page_url:
#         headers["Referer"] = page_url

#     # 1) fetch bytes with a size cap
#     r = requests.get(image_url, headers=headers, timeout=20, stream=True)
#     r.raise_for_status()

#     content_type = r.headers.get("Content-Type", "").split(";")[0].strip().lower()
#     guessed_ext = MIME_TO_EXT.get(content_type, None)

#     buf = io.BytesIO()
#     total = 0
#     for chunk in r.iter_content(8192):
#         if not chunk:
#             continue
#         total += len(chunk)
#         if total > max_bytes:
#             raise ValueError("image too large")
#         buf.write(chunk)
#     buf.seek(0)

#     # 2) decode to verify & learn real format
#     im = Image.open(buf)
#     im.load()  # force decode
#     fmt = (im.format or "").upper()

#     # 3) choose extension
#     ext = guessed_ext or ALLOWED_FORMATS.get(fmt)
#     if not ext:
#         # Fallback: re-encode to WEBP (safe & compact)
#         fmt = "WEBP"
#         ext = ".webp"

#     # 4) resize huge images (defense)
#     w, h = im.size
#     if max(w, h) > max_side:
#         scale = max_side / float(max(w, h))
#         im = im.resize((int(w * scale), int(h * scale)))

#     # 5) sanitize / re-encode (strips EXIF)
#     # If original fmt allowed, keep it; else convert to webp/jpg
#     if fmt not in ALLOWED_FORMATS:
#         im = im.convert("RGB")
#         fmt = "WEBP"
#         ext = ".webp"

#     # deterministic filename based on source URL
#     name = hashlib.sha1(image_url.encode("utf-8")).hexdigest() + ext
#     file_path = os.path.join(MEDIA_DIR, name)

#     save_kwargs = {}
#     if fmt in ("JPEG", "WEBP"):
#         save_kwargs = {"quality": 85, "optimize": True}
#     im.save(file_path, fmt, **save_kwargs)


#     public_url = f"{MEDIA_DIR}/{name}"
    

#     return  public_url
def download_image_png(image_url):
    """
    Saves to the ../media folder and returns:
    (file_system_path, public_url)
    """
    MEDIA_DIR.mkdir(parents=True, exist_ok=True)

    resp = requests.get(image_url, timeout=20)
    resp.raise_for_status()

    img = Image.open(io.BytesIO(resp.content))
    if img.mode not in ("RGB", "RGBA"):
        img = img.convert("RGB")

    filename = hashlib.sha1(image_url.encode("utf-8")).hexdigest() + ".png"
    file_path = MEDIA_DIR / filename
    img.save(file_path, format="PNG", optimize=True)

    public_url = f"{MEDIA_URL}/{filename}"
    return public_url

def download_image(image_url, dest_dir="media"):
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


def get_all():
    items = parse_listing()
    results = []
    for i, it in enumerate(items, start=1):
        try:
            title, author, pub, body, image_url, image_path = parse_article(it["url"])
            row = {
                "url": it["url"],
                "title": title or it["title"],
                "published_at": pub or it["published_at"],
                "author": author,
                "body": body,
                "image_url": image_url,
                "image_path": image_path,  # may be None if download=False
                "category": "Afrique", 
            }
            results.append(row)
        except Exception as e:
            print(f"Error on {it['url']}: {e}")
    return results

# if __name__ == "__main__":
#     main()
