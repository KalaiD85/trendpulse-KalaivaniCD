import pandas as pd
import json

def Load_JSON_File(filename):
    file_path = f"data/{filename}.json"

    #load from json file
    with open(file_path,"r") as file:
        data = json.load(file)
    df = pd.DataFrame(data)      # convert to DataFrame

    # Print how many rows were loaded
    print(f"Loaded {len(df)} stories from data/{filename}.json ")
    return df

def Clean_the_Data(df):
    # 1. Remove duplicates based on post_id
    df = df.drop_duplicates(subset="post_id")
    print(f"\nAfter removing duplicates: {len(df)}")
    # 2. Drop rows with missing values 
    df = df.dropna(subset=["post_id", "title", "score"])
    print(f"After removing nulls: {len(df)}")
    # 3. Update score and num_comments are integers
    df["score"] = df["score"].astype(int)
    df["num_comments"] = df["num_comments"].astype(int)
    # 4. Remove low-quality stories (score < 5)
    df = df[df["score"] >= 5]
    print(f"After removing low scores: {len(df)}")
    # 5. Strip extra whitespace from title
    df["title"] = df["title"].str.strip()

    # Print number of rows remaining
    print(f"Rows remaining after cleaning: {len(df)}")

    return df

def Save_to_CSV(df):
    import os

    # Save cleaned DataFrame to CSV
    output_path = "data/trends_clean.csv"
    df.to_csv(output_path, index=False)

    # Confirmation message
    if os.path.exists(output_path):
        print(f"Saved {len(df)} rows to {output_path}")

    # Summary: how many stories per category
    print("\nStories per category:")
    #print(df["category"].value_counts())
    # query on category
    counts = df["category"].value_counts()
    for cat, count in counts.items():
        print(f"  {cat:<15} {count}")

if __name__ == "__main__":
    df = Load_JSON_File("trends_20260410")
    df = Clean_the_Data(df)
    Save_to_CSV(df)
