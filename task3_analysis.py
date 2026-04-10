import pandas as pd
import numpy as np
import os
def Load_n_Explore(filename):
    # Load the cleaned CSV
    df = pd.read_csv(f"data/{filename}.csv")
    # Print the shape (rows, columns)
    print("Loaded data:", df.shape)    
    # Print the first 5 rows
    print("\nFirst 5 rows:")
    print(df.head().to_string(index=False))
    # Print average score and average num_comments
    avg_score = df["score"].mean()
    avg_comments = df["num_comments"].mean()
    print(f"\nAverage score    : {avg_score:.2f}")
    print(f"Average comments : {avg_comments:.2f}")
    return df

def Analyse_with_Numpy(df):
    # Convert relevant columns to NumPy arrays
    scores = df["score"].to_numpy()
    comments = df["num_comments"].to_numpy()
    print("\n--- NumPy Stats ---")

     # 1. Mean, median, and standard deviation of score
    print(f"Mean score   : {np.mean(scores):.2f}")
    print(f"Median score : {np.median(scores)}")
    print(f"Std deviation: {np.std(scores):.2f}")
    # 2. Highest and lowest score
    print(f"Max score    : {np.max(scores)}")
    print(f"Min score    : {np.min(scores)}")
    # 3. Category with the most stories
    print(f"\nMost stories in: {df["category"].value_counts().idxmax()} ({df["category"].value_counts().max()} stories)")
    # 4. Story with the most comments
    max_comments_idx = np.argmax(comments)
    print(f'\nMost commented story: "{df.iloc[max_comments_idx]["title"]}" — {df.iloc[max_comments_idx]["num_comments"]} comments')


def Add_New_Col(df):
    # 1. engagement = num_comments / (score + 1)
    df["engagement"] = df["num_comments"] / (df["score"] + 1)
    # 2. is_popular = True if score > average score, else False
    df["is_popular"] = df["score"] > df["score"].mean()
    return df
    
def Save_the_Result(df):    
    output_path = "data/trends_analysed.csv"
    df.to_csv(output_path, index=False)
    # Confirmation message    
    if os.path.exists(output_path):
        print(f"\nSaved to {output_path}")
        #print(f"Saved {len(df)} rows to {output_path}")

if __name__ == "__main__":
    df = Load_n_Explore("trends_clean")
    Analyse_with_Numpy(df)
    updated_df = Add_New_Col(df)
    Save_the_Result(updated_df)

