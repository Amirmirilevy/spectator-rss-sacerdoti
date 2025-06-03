import requests
from bs4 import BeautifulSoup
import json
import os

BASE_URL = "https://www.spectator.co.uk/writer/jonathan-sacerdoti/"
HOST_URL = "https://www.spectator.co.uk"

def fetch_articles():
    response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.text, "html.parser")

    articles = []

    titles = soup.select("a.article__title-link")
    images = soup.select("a.article__image-link img")
    descriptions = soup.select("p.article__excerpt-text")
    dates = soup.select("time.archive-entry__timestamp")

    for i in range(len(titles)):
        title = titles[i].text.strip()
        link = titles[i]["href"]
        if not link.startswith("http"):
            link = HOST_URL + link
        image = images[i]["src"]
        description = descriptions[i].text.strip()
        date = dates[i]["datetime"] if dates[i].has_attr("datetime") else dates[i].text.strip()

        articles.append({
            "title": title,
            "link": link,
            "image": image,
            "description": description,
            "date": date
        })

    return articles

def write_json(articles):
    out_path = os.path.join(os.getcwd(), "articles.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(articles, f, indent=2, ensure_ascii=False)

def write_rss(articles):
    items = ""
    for article in articles:
        items += f"""<item>
  <title>{article["title"]}</title>
  <link>{article["link"]}</link>
  <description><![CDATA[{article["description"]}]]></description>
  <pubDate>{article["date"]}</pubDate>
</item>
"""

    rss = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
<channel>
  <title>Jonathan Sacerdoti - Spectator</title>
  <link>{BASE_URL}</link>
  <description>Auto-generated RSS feed of articles</description>
  {items}
</channel>
</rss>
"""

    out_path = os.path.join(os.getcwd(), "feed.xml")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(rss)

if __name__ == "__main__":
    articles = fetch_articles()
    write_json(articles)
    write_rss(articles)
