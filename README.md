# InterIIT-Task

## Demo

[!Demo](https://user-images.githubusercontent.com/17357089/209448060-5338deb9-027f-4a6a-b33a-6273bb20f83d.webm)


## Implementation Process

The task was to implement a closed search engine (a knowledge base) where the user can search any data from pages defined in a [specified file](scraper/saved_links.json).

My implementation uses a one-time Python scraper which extracts metadata information and content from each of the URLs, and stores them in a search-engine database. Of the alternatives available, I chose MeiliSearch due to the ease of implementation and available features (primarily, typo tolerancy, field weights, and orderable ranking rules).

The body content is used as a fallback if the meta description tag is not present. Currently, this just directly converts the page into plaintext which is stored.

To improve the speed, the scraper processes requests asynchronously, upto 10 at a time together.

The frontend directly fetches data from the databsae and displays it in a material-ish fashion.

### Possible Improvements

- The search engine can be finetuned further to improve accuracy of matches. I did a basic optimization, and I am sure better ranking rules and weights can be obtained by further finetuning the settings.
- A page rank of the website can be fetched from the internet via some services available online. I did not implement this cause (1) they are usually paid, and (2) it might skew the results (ex. the user might find some pages with low rankings more useful).
- Currently, the body text is parsed as-is by stripping the HTML tags and scripts. However, this results in some ugly text for websites that are not properly built (especially the ones which do not have better meta attributes, and are heavily JavaScript reliant). A better option will be to run a neural network, maybe a BERT, to generate a description or atleast tags for the HTML content. Also, a better scraper can be implemented by scraping by executing the JavaScript, since React/similar-based sites do not have any proper HTML unless they are rendered server-side.
- The frontend can probably be improved but I am not a frontend guy, so I don't know.

## Installation

The entire application (excluding the scraper) is dockerized. To run it, simply bring the containers up with `docker compose up --build`.

The scraper is intentionally not dockerized, since it is a one-time setup, and configuring the settings needs changes to the source code. Additionally, the scraper can be run on any system, not necesarily the computer which runs the search engine server.

To install the dependencies for the scraper inside a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Please scrape the data before running the application, otherwise the frontend will return 0 results.

## Scraping Data

To scrape the data, run `python scraper/main.py`.

To finetune the search engine, edit `scraper/settings.py` to your liking and run the file via `python scraper/settings.py`.
