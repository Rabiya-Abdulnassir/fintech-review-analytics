from google_play_scraper import reviews
import pandas as pd

apps = {
    "CBE": "com.combanketh.mobilebanking",
    "BOA": "com.boa.boaMobileBanking",
    "Dashen": "com.dashen.dashensuperapp"
}

all_reviews = []

for bank, app_id in apps.items():

    result, _ = reviews(
        app_id,
        lang='en',
        country='et',
        count=500
    )

    for review in result:
        all_reviews.append({
            "review": review["content"],
            "rating": review["score"],
            "date": review["at"],
            "bank": bank,
            "source": "Google Play"
        })

df = pd.DataFrame(all_reviews)

print(df.head())
print(df.shape)

df.to_csv("data/raw/raw_reviews.csv", index=False)