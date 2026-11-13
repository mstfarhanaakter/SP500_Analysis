import os
import re
import requests
import pandas as pd
import yfinance as yf
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from wordcloud import WordCloud
from textblob import TextBlob
import nltk
from nltk.corpus import stopwords

nltk.download("stopwords", quiet=True)

# ==========================================
# অংশ ১: Yahoo Finance থেকে নিউজ Web Scraping
# ==========================================
print("Scraping news from Yahoo Finance for S&P 500...")

# পদ্ধতি ক: Yahoo Finance RSS Feed থেকে S&P 500 (^GSPC) এর নিউজ স্ক্র্যাপ করা
rss_url = "https://finance.yahoo.com/quote/%5EGSPC/news/"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

response = requests.get(rss_url, headers=headers)
soup = BeautifulSoup(response.content, "xml")

news_list = []
for item in soup.find_all("item"):
    title = item.title.text if item.title else ""
    desc = item.description.text if item.description else ""
    pub_date = item.pubDate.text if item.pubDate else ""
    link = item.link.text if item.link else ""
    
    news_list.append({
        "Date": pub_date,
        "Headline": title,
        "Summary": desc,
        "Link": link
    })

# পদ্ধতি খ: আরও বেশি ডেটার জন্য yfinance এর বিল্ট-ইন নিউজ ফিড যুক্ত করা
ticker = yf.Ticker("^GSPC")
for n in ticker.news:
    content = n.get("content", {})
    title = content.get("title", n.get("title", ""))
    summary = content.get("summary", "")
    pub_date = content.get("pubDate", "")
    if title:
        news_list.append({
            "Date": pub_date,
            "Headline": title,
            "Summary": summary,
            "Link": ""
        })

# ডেটাফ্রেম তৈরি ও ডুপ্লিকেট বাদ দেওয়া
df_news = pd.DataFrame(news_list).drop_duplicates(subset=["Headline"]).reset_index(drop=True)

# স্ক্র্যাপ করা ডেটা সেভ করা
raw_folder = r"E:\SP500_Analysis\data\scraped"
os.makedirs(raw_folder, exist_ok=True)
df_news.to_csv(os.path.join(raw_folder, "yahoo_sp500_news.csv"), index=False)
print(f"Total {len(df_news)} unique articles scraped & saved!")

# ==========================================
# অংশ ২: Textual Analysis (Cleaning & Sentiment)
# ==========================================
# Headline এবং Summary একসাথে যুক্ত করে বড় টেক্সট তৈরি করা
df_news["Full_Text"] = df_news["Headline"].fillna("") + " " + df_news["Summary"].fillna("")

stop_words = set(stopwords.words("english"))
custom_stops = {"said", "says", "new", "year", "market", "stock", "stocks", "sp", "500", "yahoo", "finance"}
stop_words.update(custom_stops)

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"http\S+|www\S+", "", text)
    text = re.sub(r"[^a-z\s]", "", text)
    words = [w for w in text.split() if w not in stop_words and len(w) > 2]
    return " ".join(words)

df_news["Cleaned_Text"] = df_news["Full_Text"].apply(clean_text)

def get_sentiment(text):
    score = TextBlob(str(text)).sentiment.polarity
    if score > 0.05:
        return "Positive"
    elif score < -0.05:
        return "Negative"
    else:
        return "Neutral"

df_news["Sentiment"] = df_news["Full_Text"].apply(get_sentiment)

# ==========================================
# অংশ ৩: প্রফেশনাল চার্ট তৈরি ও সেভ
# ==========================================
chart_folder = r"E:\SP500_Analysis\charts"
os.makedirs(chart_folder, exist_ok=True)

# Top 12 Keywords বের করা
all_words = " ".join(df_news["Cleaned_Text"]).split()
word_counts = Counter(all_words).most_common(12)
words_df = pd.DataFrame(word_counts, columns=["Word", "Frequency"])

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6), dpi=300)

# চার্ট ১: Top Keywords
sns.barplot(data=words_df, x="Frequency", y="Word", palette="Blues_r", ax=ax1, zorder=3)
ax1.set_title("Top Keywords in Yahoo Finance S&P 500 News", fontsize=13, fontweight="bold", loc="left", pad=12)
ax1.set_xlabel("Frequency", fontsize=10.5, fontweight="bold")
ax1.set_ylabel("")
ax1.spines["top"].set_visible(False)
ax1.spines["right"].set_visible(False)
ax1.grid(axis="x", linestyle="--", alpha=0.4, zorder=0)

# চার্ট ২: Sentiment Analysis
sentiment_counts = df_news["Sentiment"].value_counts()
sent_colors = {"Positive": "#2E7D32", "Neutral": "#78909C", "Negative": "#C62828"}
bar_colors = [sent_colors.get(x, "#1E88E5") for x in sentiment_counts.index]

bars = ax2.bar(sentiment_counts.index, sentiment_counts.values, color=bar_colors, width=0.5, zorder=3)
for bar in bars:
    yval = bar.get_height()
    pct = (yval / len(df_news)) * 100
    ax2.text(bar.get_x() + bar.get_width()/2, yval + 0.3,
             f"{yval}\n({pct:.1f}%)", ha="center", va="bottom", fontsize=10, fontweight="bold")

ax2.set_title("Market Sentiment Distribution (Yahoo Finance)", fontsize=13, fontweight="bold", loc="left", pad=12)
ax2.set_ylabel("Number of Articles", fontsize=10.5, fontweight="bold")
ax2.set_ylim(0, sentiment_counts.max() * 1.22)
ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)
ax2.grid(axis="y", linestyle="--", alpha=0.4, zorder=0)

plt.tight_layout()
plt.savefig(os.path.join(chart_folder, "07_yahoo_textual_analysis.png"), dpi=300, bbox_inches="tight")
plt.show()

# চার্ট ৩: WordCloud
wc = WordCloud(width=1200, height=600, background_color="white", colormap="viridis", max_words=80).generate(" ".join(df_news["Cleaned_Text"]))
plt.figure(figsize=(12, 6), dpi=300)
plt.imshow(wc, interpolation="bilinear")
plt.axis("off")
plt.title("Word Cloud — S&P 500 Financial News (Yahoo Finance)", fontsize=14, fontweight="bold", pad=15)
plt.savefig(os.path.join(chart_folder, "08_yahoo_wordcloud.png"), dpi=300, bbox_inches="tight")
plt.show()

print("All Yahoo Finance scraping & textual charts saved successfully!")
