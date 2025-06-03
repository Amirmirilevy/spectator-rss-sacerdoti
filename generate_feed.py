import requests
from bs4 import BeautifulSoup
import json
import os

HOST_URL = "https://www.spectator.co.uk"

def fetch_articles():
    articles = []
    page = 1

    while True:
        url = f"{HOST_URL}/writer/jonathan-sacerdoti/page/{page}/"
        response = requests.get(url)
        if response.status_code != 200:
            break

        soup = BeautifulSoup(response.text, "html.parser")

        titles = soup.select("a.article__title-link")
        images = soup.select("a.article__image-link img")
        descriptions = soup.select("p.article__excerpt-text")
        dates = soup.select("time.archive-entry__timestamp")

        if not titles:
            break

        count = min(len(titles), len(images), len(descriptions), len(dates))
        for i in range(count):
            title = titles[i].text.strip()
            link = titles[i]["href"]
            if not link.startswith("http"):
                link = HOST_URL + link
            image = images[i]["src"]
            description = descriptions[i].text.strip()
            date = dates[i].get("datetime", dates[i].text.strip())

            articles.append({
                "title": title,
                "link": link,
                "image": image,
                "description": description,
                "date": date
            })

        page += 1

    return articles

def write_json(articles):
    out_path = os.path.join(os.getcwd(), "articles.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(articles, f, indent=2, ensure_ascii=False)

def write_rss(articles):
    items = ""
    for article in articles:
        items += f"""<item>
  <title>{article['title']}</title>
  <link>{article['link']}</link>
  <description>{article['description']}</description>
  <pubDate>{article['date']}</pubDate>
</item>
"""

    rss = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
<channel>
  <title>Jonathan Sacerdoti at The Spectator</title>
  <link>{HOST_URL}/writer/jonathan-sacerdoti/</link>
  <description>Latest articles by Jonathan Sacerdoti from The Spectator</description>
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
