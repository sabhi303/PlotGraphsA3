import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np


# plot CDF
def plot_CDF(data, title, plt):
    plt.subplot(1, 2, 1)
    counts, bin_edges = np.histogram(data, bins=100, density=True)
    cdf = np.cumsum(counts)
    plt.plot(
        bin_edges[1:],
        cdf,
        linestyle="-",
        linewidth=2,
        marker="o",
        markersize=3,
        color="b",
        label="CDF",
    )
    plt.title(f"{title} CDF")
    plt.xlabel("Values")
    plt.ylabel("Cumulative Probability")
    plt.grid(True)
    plt.legend()


# plt box plot
def plot_box(data, title, plt):
    plt.subplot(1, 2, 2)
    plt.boxplot(
        data,
        patch_artist=True,
        notch=True,
        vert=False,
        meanline=True,
        showmeans=True,
        showcaps=True,
        showbox=True,
        showfliers=True,
    )
    plt.title(f"{title} Boxplot")
    plt.xlabel("Values")
    box_patch = mpatches.Patch(color="lightblue", label="Boxplot")
    median_patch = mpatches.Patch(color="green", label="Median")
    mean_patch = mpatches.Patch(color="red", label="Mean")
    plt.legend(handles=[box_patch, median_patch, mean_patch])
    plt.grid(True)


def plot_graphs(filename, generated_data):
    """Plot CDF and Boxplot and save as PDF files."""
    for distribution, data in generated_data.items():
        # print("Data", data)

        plt.figure(figsize=(10, 5))
        plt.xlabel("Distribution")
        # plt.set_ylabel("Y axis label")

        plot_CDF(data, distribution, plt)
        plot_box(data, distribution, plt)

        plt.tight_layout()

        # plt.show()
        plt.savefig(f"{filename}-{distribution}-CDF-Box.pdf")
        plt.close()
