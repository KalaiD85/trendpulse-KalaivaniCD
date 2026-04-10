import pandas as pd
import matplotlib.pyplot as plt
import os
def Setup (filename):
    # 1. Load the analysed CSV into a DataFrame
    df = pd.read_csv(f"data/{filename}.csv")
    # 2. Create outputs/ folder if it doesn't exist
    os.makedirs("outputs", exist_ok=True)    
    return df

def Top_10_Story(df):
    # top 10 stories by score
    top10 = df.sort_values("score", ascending=False).head(10)
    # Shorten titles longer than 50 characters
    top10["short_title"] = top10["title"].apply(
        lambda t: t if len(t) <= 50 else t[:50]
    )
    # horizontal bar chart
    plt.figure(figsize=(10, 6))
    plt.barh(top10["short_title"], top10["score"], color="steelblue")
    plt.title("Top 10 Stories by Score")
    plt.xlabel("Score")
    plt.ylabel("Story Title")

    # Save before showing
    plt.savefig("outputs/chart1_top_stories.png")
    plt.show()

def Story_by_Category(df):
    # Count stories per category
    category_counts = df["category"].value_counts()
    # bar chart with different colors
    plt.figure(figsize=(8, 6))
    plt.bar(category_counts.index, category_counts.values, color=plt.cm.tab10.colors)
    plt.title("Stories per Category")
    plt.xlabel("Category")
    plt.ylabel("Number of Stories")

    # Save before showing
    plt.savefig("outputs/chart2_categories.png", bbox_inches="tight")
    plt.show()

def Score_vs_Comments(df):
    # scatter plot
    fig, ax = plt.subplots(figsize=(8, 6))
    #non-popular plot
    ax.scatter(df.loc[~df["is_popular"], "score"], df.loc[~df["is_popular"], "num_comments"],
                    color="red", label="Non Popular", alpha=0.7)
    #popular plot
    ax.scatter(df.loc[df["is_popular"], "score"], df.loc[df["is_popular"], "num_comments"],
                    color="green", label="Popular", alpha=0.7)
    # title and axis labels
    plt.title("Score vs Number of Comments")
    plt.xlabel("Score")
    plt.ylabel("Number of Comments")
    plt.legend()

    # Save before showing
    plt.savefig("outputs/chart3_scatter.png", bbox_inches="tight")
    plt.show()

def Combine_Chart(df):

    # Prepare data
    top10 = df.sort_values("score", ascending=False).head(10)
    top10["short_title"] = top10["title"].apply(lambda t: t if len(t) <= 50 else t[:50])
    category_counts = df["category"].value_counts()

    # Create subplots layout (2 rows, 2 cols — leaving one empty)
    fig, axes = plt.subplots(2, 2, figsize=(16, 10))

    # Chart 1: Top 10 stories by score (horizontal bar)
    axes[0, 0].barh(top10["short_title"], top10["score"], color="steelblue")
    axes[0, 0].set_title("Top 10 Stories by Score")
    axes[0, 0].set_xlabel("Score")
    axes[0, 0].set_ylabel("Story Title")

    # Chart 2: Stories per category (bar chart with colors)
    axes[0, 1].bar(category_counts.index, category_counts.values, color=plt.cm.tab10.colors)
    axes[0, 1].set_title("Stories per Category")
    axes[0, 1].set_xlabel("Category")
    axes[0, 1].set_ylabel("Number of Stories")

    # Chart 3: Scatter plot (score vs num_comments)
    #non-popular plot
    axes[1, 0].scatter(df.loc[~df["is_popular"], "score"], df.loc[~df["is_popular"], "num_comments"],
                    color="red", label="Non Popular", alpha=0.7)
    #popular plot
    axes[1, 0].scatter(df.loc[df["is_popular"], "score"], df.loc[df["is_popular"], "num_comments"],
                    color="green", label="Popular", alpha=0.7)

    axes[1, 0].set_title("Score vs Number of Comments")
    axes[1, 0].set_xlabel("Score")
    axes[1, 0].set_ylabel("Number of Comments")
    axes[1, 0].legend()

    # Hide unused subplot
    axes[1, 1].axis("off")

    # title
    fig.suptitle("TrendPulse Dashboard", fontsize=16)
    # Adjust layout for overlapping
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    # Save before showing
    plt.savefig("outputs/dashboard.png", bbox_inches="tight")
    plt.show()


if __name__ == "__main__":
    df = Setup("trends_analysed")
    Top_10_Story(df)
    Story_by_Category(df)
    Score_vs_Comments(df)
    Combine_Chart(df)