import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# --- Configuration ---
TREND_DATA_PATH = os.path.join("data", "category_trends.csv")  # Updated from medical_trends.csv
OUTPUT_PLOTS_DIR = "plots"  # Directory to save generated plots

# Ensure the output directory exists
os.makedirs(OUTPUT_PLOTS_DIR, exist_ok=True)

# --- Load Trend Data ---
def load_trend_data(filepath):
    """Loads the category-level trend data."""
    print(f"Loading category trend data from {filepath}...")
    try:
        df = pd.read_csv(filepath)
        df['Year'] = df['Year'].astype(int)
        df.set_index('Year', inplace=True)
        print("Trend data loaded successfully.")
        print("First 5 rows of trend data:")
        print(df.head())
        print("\nTrend data info:")
        df.info()
        return df
    except FileNotFoundError:
        print(f"Error: {filepath} not found. Please ensure category_trends.csv has been generated.")
        return None

# --- Visualize Trends ---
def plot_selected_trends(df, categories_to_plot, title_suffix=""):
    """
    Plots the frequency trends for selected categories over time.

    Args:
        df (pd.DataFrame): DataFrame with years as index and categories as columns.
        categories_to_plot (list): A list of category names to visualize.
        title_suffix (str): An optional suffix for the plot title.
    """
    if df is None:
        return

    existing_categories = [cat for cat in categories_to_plot if cat in df.columns]
    if not existing_categories:
        print(f"None of the specified categories found in the data: {categories_to_plot}")
        return

    print(f"\nPlotting trends for: {existing_categories}...")

    plt.figure(figsize=(12, 7))
    sns.set_style("whitegrid")

    for category in existing_categories:
        plt.plot(df.index, df[category], marker='o', linestyle='-', label=category)

    plt.title(f'Annual Frequency Trends of Medical Categories {title_suffix}', fontsize=16)
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Annual Frequency (Count)', fontsize=12)
    plt.legend(title='Category', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()

    filename_safe = '_'.join(cat.replace(' ', '_') for cat in existing_categories[:3])
    plot_filename = f"selected_category_trends_{filename_safe}.png"
    plt.savefig(os.path.join(OUTPUT_PLOTS_DIR, plot_filename), dpi=300, bbox_inches='tight')
    print(f"Plot saved to {os.path.join(OUTPUT_PLOTS_DIR, plot_filename)}")
    plt.show()

# --- Main Execution ---
if __name__ == "__main__":
    trends_df = load_trend_data(TREND_DATA_PATH)

    if trends_df is not None:
        # Example: Selected categories to visualize
        selected_categories_1 = ['Oncology', 'Genetic therapies', 'Diagnostics']
        plot_selected_trends(trends_df, selected_categories_1, title_suffix="(Core Focus Areas)")

    print("\n--- Phase 3: Category Trend Visualization complete! ---")
    print("Check the 'plots/' directory for saved images.")
