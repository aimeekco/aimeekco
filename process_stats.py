import json
import matplotlib.pyplot as plt
import numpy as np

def load_stats():
    with open("nyt_stats.json", "r") as f:
        return json.load(f)
    
def process_stats(stats):
    results = stats["results"]["stats"]
    streaks = stats["results"]["streaks"]

    # markdown content
    content = "## NYT Crossword Stats\n"
    content += f"- **Puzzles Solved:** {results['puzzles_solved']}\n"
    content += f"- **Solve Rate:** {results['solve_rate'] * 100:.1f}%\n"
    content += f"- **Current Streak:** {streaks['current_streak']}\n"
    content += f"- **Longest Streak:** {streaks['longest_streak']}\n\n"

    # daily solve times
    content += "### Daily Solve Times\n"
    for day in results["stats_by_day"]:
        content += f"- **{day['label']}:** Best: {day['best_time']}s, Avg: {day['avg_time']}s, Latest: {day['latest_time']}s\n"

    return content

def generate_graphs(stats):
    stats_by_day = stats["results"]["stats"]["stats_by_day"]
    
    days = [day["label"] for day in stats_by_day]
    best_times = [day["best_time"] / 60 for day in stats_by_day]
    avg_times = [day["avg_time"] / 60 for day in stats_by_day]
    latest_times = [day["latest_time"] / 60 for day in stats_by_day]

    bar_width = 0.3
    x = np.arange(len(days))

    plt.figure(figsize=(10, 5), facecolor="#1e1e1e")

    bars1 = plt.bar(x - bar_width, best_times, width=bar_width, color="#4CAF50", alpha=0.8, label="best")
    bars2 = plt.bar(x, latest_times, width=bar_width, color="#2196F3", alpha=0.8, label="today")

    for bar, time in zip(bars1, best_times):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() / 2, f"{time:.1f} min",
                 ha='center', va='center', fontsize=10, color="white", rotation=90)
        
    for bar, time in zip(bars2, latest_times):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() / 2, f"{time:.1f} min",
                 ha='center', va='center', fontsize=10, color="white", rotation=90)

    plt.xticks(x, days, fontsize=12, fontweight='bold', color="white")
    plt.yticks(fontsize=10)

    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)
    plt.gca().spines['bottom'].set_visible(False)
    plt.gca().yaxis.set_visible(False)
    plt.gca().tick_params(axis='y', which='both', left=False)
    plt.gca().set_facecolor("#1e1e1e")

    plt.tight_layout()

    # Save the graph
    plt.savefig("nyt_stats_graph.png", dpi=300, bbox_inches='tight', facecolor="#1e1e1e")
    print("Graph saved as nyt_stats_graph.png")

if __name__ == "__main__":
    stats = load_stats()
    generate_graphs(stats)

