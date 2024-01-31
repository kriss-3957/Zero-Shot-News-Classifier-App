from flask import Flask, render_template, request
import pandas as pd
from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer
import feedparser
import asyncio
import nest_asyncio
import sqlite3
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)

# Sample RSS feed links
sample_rss_feeds = [
    'http://rss.cnn.com/rss/cnn_topstories.rss',
    'http://qz.com/feed',
    'http://feeds.foxnews.com/foxnews/politics',
    'http://feeds.reuters.com/reuters/businessNews',
    'http://feeds.feedburner.com/NewshourWorld',
    'https://feeds.bbci.co.uk/news/world/asia/india/rss.xml'
]

# Load the locally saved model
local_model_name = "local_model_weights"
tokenizer = AutoTokenizer.from_pretrained(local_model_name)
model = AutoModelForSequenceClassification.from_pretrained(local_model_name)

# Create a zero-shot classification pipeline with an explicit tokenizer
classifier = pipeline("zero-shot-classification", model=model, tokenizer=tokenizer)

# Patch the event loop for Flask
nest_asyncio.apply()

async def parse(url):
    return feedparser.parse(url)

async def get_articles_async(entry):
    article_url = entry.link
    news_data = Article(article_url)

    try:
        # Download and parse the article content
        news_data.download()
        news_data.parse()

        # Extract information from the Article object
        title = news_data.title
        authors = news_data.authors
        publish_date = news_data.publish_date
        text = news_data.text

        # Extract natural language processing features (optional)
        # news_data.nlp()

        # Return the extracted information as a dictionary
        return {
            'Title': title,
            'Authors': authors,
            'Content': text,
            'Publication Date': publish_date,
            'Source URL': article_url
        }

    except Exception as e:
        print(f"Error processing article at {article_url}: {e}")
        return None

    
    
    
# ... (previous code)

async def predict_category_async(title):
    # Define categories
    categories = ["Terrorism/Protest/Political Unrest/Riot", "Positive/Uplifting", "Natural Disasters", "Others"]

    # Zero-shot classification
    zero_shot_result = classifier(title, categories)

    # Find the category with the highest confidence
    max_confidence_index = zero_shot_result['scores'].index(max(zero_shot_result['scores']))
    final_prediction = zero_shot_result['labels'][max_confidence_index]

    return final_prediction, zero_shot_result['scores'][max_confidence_index]

# ... (remaining code)


async def process_article_async(article):
    # Simulate processing time
    await asyncio.sleep(1)

    # Predict category asynchronously
    category, confidence = await predict_category_async(article['title'])
    return {
        'Title': article['title'],
        'Content': article.get('summary', ''),
        'Publication Date': article.get('published', ''),
        'Source URL': article.get('link', ''),
        'Category': category,
        'Confidence': confidence
    }

def generate_sql_dump(articles_df):
    # Convert datetime columns to string format (modify based on your datetime format)
    articles_df['Publication Date'] = articles_df['Publication Date'].astype(str)

    # Create a SQLite database connection
    conn = sqlite3.connect('news_articles.db')

    # Write the DataFrame to a SQL table
    articles_df.to_sql('news_articles', conn, index=False, if_exists='replace')

    # Close the database connection
    conn.close()

async def process_rss_feed(rss_url):
    parsed_feed = await parse(rss_url)
    tasks = [process_article_async(entry) for entry in parsed_feed.entries]
    return await asyncio.gather(*tasks)

@app.route('/', methods=['GET', 'POST'])
async def index():
    if request.method == 'POST':
        # Get selected RSS feed links from the form
        rss_links = request.form.getlist('rss_link')

        # List to store tasks
        tasks = []

        for rss_url in rss_links:
            # Step 1: Parse the RSS feed asynchronously
            tasks.append(process_rss_feed(rss_url))

        # Run tasks concurrently
        results = await asyncio.gather(*tasks)

        # Flatten the list of results
        articles_list = [item for sublist in results for item in sublist]

        # Create a DataFrame from the results
        articles_df = pd.DataFrame(articles_list)

        # Display the DataFrame
        df_html = articles_df[['Title', 'Category', 'Confidence']].to_html()

        # Generate SQL dump
        generate_sql_dump(articles_df)

        # Read the SQL dump into a DataFrame
        conn = sqlite3.connect('news_articles.db')
        Articles_df = pd.read_sql('SELECT * FROM news_articles', conn)
        conn.close()

        # Count the occurrences of each category
        category_counts = Articles_df['Category'].value_counts()

        # Plot the frequency
        plt.bar(category_counts.index, category_counts.values, color='skyblue')
        plt.title('Category Frequency Plot')
        plt.xlabel('Category')
        plt.ylabel('Frequency')

        # Rotate x-axis labels for better readability
        plt.xticks(rotation=45, ha='right')

        # Add some space at the bottom
        plt.subplots_adjust(bottom=0.5)

        # Save the plot as an image
        img = BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)

        # Encode the image to base64 for displaying in HTML
        img_base64 = base64.b64encode(img.read()).decode('utf-8')
        plt.close()

        return render_template('index.html', df_html=df_html, img_base64=img_base64, rss_feeds=sample_rss_feeds)

    return render_template('index.html', rss_feeds=sample_rss_feeds)

if __name__ == '__main__':
    app.run(debug=True)
