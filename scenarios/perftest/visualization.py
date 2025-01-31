import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("darkgrid")

def convert_to_ms(time_str: str) -> float:
    if "ms" in time_str:
        return float(time_str.replace("ms", ""))  
    elif "µs" in time_str:
        return float(time_str.replace("µs", "")) / 1000 
    else:
        return np.nan 

def generate_non_cached_plots():
    df = pd.read_csv("perftest.csv", sep='\t',header=0)
 
    plt.figure(figsize=(10, 6))
    for col in ["PTC1", "PTC2", "PTC3", "PTC4", "PTC5"]:
        sns.histplot(df[col], bins=30, kde=True, label=col, alpha=0.3, edgecolor=None)

    plt.xlabel("Execution Time (ms)")
    plt.ylabel("Occurrences")
    plt.title("Distribution of Execution Times")
    plt.legend()

    plt.savefig("execution_time_distribution.pdf", dpi=300, bbox_inches="tight")
    plt.close()

    plt.figure(figsize=(10, 6))

    sns.boxplot(data=df, width=0.5, palette="Set2")

    plt.xlabel("PTC Columns")
    plt.ylabel("Execution Time (ms)")
    plt.title("Whisker Plot of Execution Times")

    plt.savefig("execution_time_whisker_plot.pdf", dpi=300, bbox_inches="tight")
    plt.close()

def generate_cached_plots():
    df = pd.read_csv("perftest_cache.csv", sep='\t',header=0)

    for col in ["PTC1", "PTC2", "PTC3", "PTC4", "PTC5"]:
        df[col] = df[col].apply(convert_to_ms)
    
    plt.figure(figsize=(10, 6))

    sns.lineplot(data=df, x=df.index, y="PTC1", label="PTC1", marker="o")
    sns.lineplot(data=df, x=df.index, y="PTC2", label="PTC2", marker="s")

    plt.yscale("log")

    plt.xlabel("Run Index")
    plt.ylabel("Execution Time (ms)")
    plt.title("Execution Time Over Cached Runs (PTC1 & PTC2)")
    plt.legend()

    plt.savefig("execution_time_line_plot.pdf", dpi=300, bbox_inches="tight")

    plt.close()

def main():
    generate_cached_plots()
    generate_non_cached_plots()
    
if __name__ == '__main__':
    main()