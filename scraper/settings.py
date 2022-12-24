import os
from pprint import pprint

import meilisearch
from dotenv import load_dotenv

load_dotenv()
MEILEI_MASTER_KEY = os.getenv("MEILI_MASTER_KEY")

client = meilisearch.Client("http://localhost:7700", MEILEI_MASTER_KEY)

pprint(client.index("links").get_settings())

# job = client.index("links").update_sortable_attributes(
#     ["title", "description", "tags", "keywords"]
# )
# pprint(job)

# job = client.index("links").update_searchable_attributes(
#     ["title", "description", "link", "tags", "keywords", "body"]
# )
# pprint(job)

job = client.index("links").update_ranking_rules(
    [
        "attribute",
        "words",
        "typo",
        "proximity",
        "sort",
        "exactness",
    ]
)
pprint(job)