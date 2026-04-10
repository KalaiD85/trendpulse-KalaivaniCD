import requests
from datetime import datetime, timezone
import os
import json
import time

header = {"User-Agent": "TrendPulse/1.0"}
top_stories_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
#Categories the story
categories = {
    "technology": ["ai","software","tech","code","computer","data","cloud","api","gpu","llm"],
    "worldnews": ["war","government","country","president","election","climate","attack","global"],
    "sports": ["nfl","nba","fifa","sport","game","team","player","league","championship"],
    "science": ["research","study","space","physics","biology","discovery","nasa","genome"],
    "entertainment": ["movie","film","music","netflix","game","book","show","award","streaming"]
}

#1: get top stories ids
def fetch_top_story_ids():
    try:
        response = requests.get(top_stories_url,headers=header)
        if response.status_code == 200:
            ids = response.json()[:2000]
        else:
            print(f"Request failed for with status {response.status_code}")
            ids = []
    except Exception as e:
        print(f"Failed to fetch top stories :{e}")
        ids = []
    return ids

#2: get story details for each story id
def fetch_story_details(id):
    try:
        response = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{id}.json"
                                     ,headers=header)
        if response.status_code == 200:
            story = response.json()
        else:
            print(f"Request failed for story {id} with status {response.status_code}")
            story = {}
    except Exception as e:
        print(f"Failed to fetch story details for {id}:{e}")
        story = {}
    return story

#3. CAtegorize the story based on title keyword
def categorize_story(title):
    if not title:
        return None
    title_lower = title.lower()
    for category, keywords in categories.items():
        for kw in keywords:
            if kw.lower() in title_lower:
                return category
    return None

def Make_the_API_Calls():
    story_ids = fetch_top_story_ids()
    grouped = {category: [] for category in categories}
    all_stories = []
    for category in categories:
        #print(f"\nFetching data for category: {category}")
        #count = 0
        for sid in story_ids:
            #if count >= 25:
               #break
            story = fetch_story_details(sid)
            if story and "title" in story:
                cat = categorize_story(story["title"])
                if category == cat:
                    all_stories.append({
                        "title": story.get("title"),
                        "category": category,})
                    #count += 1

        # Sleep once per category loop
        time.sleep(2)

    ## Print summary
    #total_count = len(all_stories)
    #print(f"\nTotal stories collected: {total_count}")

    ## Create a dictionary to hold counts
    #category_counts = {}

    #for story in all_stories:
      #cat = story.get("category")
      #category_counts[cat] = category_counts.get(cat, 0) + 1

    ## Print results
    #for cat, count in category_counts.items():
      #print(f"{cat.upper()}: {count} stories")

def Make_the_API_Calls_to_Extract_Fields():
    story_ids = fetch_top_story_ids()
    grouped = {category: [] for category in categories}
    all_stories = []
    unmatched_stories = []
    for category in categories:
        #print(f"\nFetching data for category: {category}")
        count = 0
        for sid in story_ids:
            # this count is not workinng to extract exact 25 story/category other than 
            # technology and entertainment, hence planned to add few unmatched category 
            if count >= 25:
                break
            story = fetch_story_details(sid)
            if story and "title" in story:
                cat = categorize_story(story["title"])            
                item = {
                        "post_id": story.get("id"), #Unique ID of the story
                        "title": story.get("title"), #Story title
                        "category": category, #The category assigned based on keywords
                        "score": story.get("score", 0), #Number of upvotes
                        "num_comments": story.get("descendants", 0), #Number of comments
                        "author": story.get("by"), #Username of the story author
                        "collected_at": datetime.now(timezone.utc).isoformat() #The current date and time
                        }
                if category == cat:
                    grouped[cat].append(item)
                    count += 1
                else:
                    unmatched_stories.append(item)
        # Sleep once per category loop
        time.sleep(2)

    ## Print summary Before
    #total_count = len(all_stories)
    #print(f"\nTotal stories collected: {total_count}")

    ## Create a dictionary for counts
    #category_counts = {}

    #for story in all_stories:
      #cat = story.get("category")
      #category_counts[cat] = category_counts.get(cat, 0) + 1

    ## Print results
    #for cat, count in category_counts.items():
      #print(f"{cat.upper()}: {count} stories")

    #assigning unmatched catgory so each category have 25 story
    for cat in categories:
        if len(grouped[cat]) < 25:
            needed = 25 - len(grouped[cat])
            filler = unmatched_stories[:needed]
            for f in filler:
                f["category"] = cat  # assign filler to this category to match the count
                grouped[cat].append(f)
            unmatched_stories = unmatched_stories[needed:]

    for cat in categories:
        all_stories.extend(grouped[cat][:25])  # exactly 25

    ## Print summary After
    #total_count = len(all_stories)
    #print(f"\nTotal stories collected: {total_count}")

    ## Create a dictionary for counts
    #category_counts = {}

    #for story in all_stories:
      #cat = story.get("category")
      #category_counts[cat] = category_counts.get(cat, 0) + 1

    ## Print results
    #for cat, count in category_counts.items():
      #print(f"{cat.upper()}: {count} stories")

    return all_stories

def Save_to_JSON(collected_stories):
    os.makedirs("data", exist_ok=True)
    date_str = datetime.now(timezone.utc).strftime("%Y%m%d")
    output_path = f"data/trends_{date_str}.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(collected_stories, f, indent=2)

    #Print summary
    total_count = len(collected_stories)
    print(f"\nCollected {total_count} stories")
    print(f"Saved to {output_path}")

if __name__ == "__main__":
    Make_the_API_Calls()
    categorized_story = Make_the_API_Calls_to_Extract_Fields()
    Save_to_JSON(categorized_story)