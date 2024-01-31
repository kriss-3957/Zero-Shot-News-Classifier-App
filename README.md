
# Zero-Shot News Classifier Application

## Table of Contents

- [Overview](#overview)
- [App Features](#app-features-:)
- [Requirements](#requirements)
- [Installation](#installation)
- [Application Logic](#application-logic)
- [Enhancements](#enhancements)
- [License](#license)

## Overview

This is an End-to-End News Category Classification Application, designed to collect news articles from various RSS feeds, store them into a database, and classify them into predefined categories. The categories include Terrorism/Protest/Political Unrest/Riot, Positive/Uplifting, Natural Disasters, and Others. The classified data is then outputed as a sql dump by the application.

## App Features :

- Parsing of RSS feeds to extract news article information.
- Database storage to store parsed news articles without duplicates.
- Asynchronous processing of new articles using using asyncio, to streamline processing tasks.
- Category classification using a Zero-Shot NLP Classifier.
- Logging and error handling for robustness.

## Requirements

### Required Libraries:

Programming Language: Python
Libraries: Flask, Feedparser, Transformers (HuggingFace),Asyncio, Matplotlib
Database: sqlite3



## Installation



1. Clone the GitHub repository:

```
git clone https://github.com/your-username/news-classification-app.git

cd news-classification-app
```
2. Install dependencies:
For your convenience a requirements.txt is provided, which allows you to install them by using pip:

```
pip install -r requirements.txt
```

3. Run the Flask application:
```
python app4.py
```

### Usage :

1. Visit http://127.0.0.1:5000/ in your web browser.

2. Select the desired RSS feed links from the provided list.

3. Click on the "Fetch Articles" button.

4. View the results, including a table of articles and a category frequency plot.


### Deployed App :

Alternatively, you can directly use the deployed app by visiting the deployed link : 

http://127.0.0.1:5000/ 


## App Demo :




## Application Logic


### Parsing RSS Feeds
The application starts by parsing the selected RSS feeds asynchronously using asyncio. It utilizes the feedparser library to retrieve news articles from the feeds.

###  Database Storage
The parsed articles are stored in a relational database using SQLAlchemy. The database schema is designed to avoid duplicates.

### Asynchronous Processing
Asyncio is used for asynchronous processing. Each news article is processed asynchronously for category classification using a Zero-Shot NLP Classifier.

### Category Classification
The application employs the HuggingFace Zero-Shot NLP Classifier to predict the category of each news article. This is done by creating a pipeline with an explicit tokenizer and model.

### Logging and Error Handling
Proper logging is implemented throughout the application to track events and potential errors. The application gracefully handles parsing errors and network connectivity issues.

### Data Storage
The application stores the parsed news articles into a database using the 'sqlite3' library. The data is stored in a table named news_articles, and duplicates are avoided using database constraints.

### Error Handling
The application handles errors gracefully, providing informative messages in case of parsing errors or other exceptions. Proper logging is implemented to track events and errors.

### Enhancements
Further enhancements of the application may include :
Fine-tuning the Zero-Shot NLP Classifier with additional training data for better category predictions.
Implementing user authentication and personalized feeds.
Adding support for additional RSS feeds and categories.
Optimizing and scaling for larger datasets.
Contributing
Contributions to the project are welcome! Feel free to open issues, submit pull requests, or suggest improvements.



## License

This project is licensed under the MIT License - see the LICENSE file for details. [MIT](https://choosealicense.com/licenses/mit/)