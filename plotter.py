import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np


# plot CDF
def plot_CDF(data, title, plt):
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
    plt.set_title(f"{title.upper()} CDF")
    plt.set_xlabel("Values")
    plt.set_ylabel("Cumulative Probability")
    plt.grid(True)
    plt.legend()


# plt box plot
def plot_box(data, title, plt):
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
    plt.set_title(f"{title.upper()} Boxplot")
    plt.set_xlabel("Values")
    box_patch = mpatches.Patch(color="lightblue", label="Boxplot")
    median_patch = mpatches.Patch(color="green", label="Median")
    mean_patch = mpatches.Patch(color="red", label="Mean")
    plt.legend(handles=[box_patch, median_patch, mean_patch])
    plt.grid(True)


def plot_graphs(filename, generated_data):
    
    # pdf for CDFs
    with PdfPages(filename + "CDF plots.pdf") as pdf:
        for distribution, data in generated_data.items():
            
            figure, ax = plt.subplots(1, figsize=(10, 5))
            plot_CDF(data.get("data"), distribution, ax)
            plt.tight_layout()
            # Save the current figure to the PDF
            pdf.savefig(figure)
            plt.close(figure)

    # pdf for BoxPlots
    with PdfPages(filename + "Box plots.pdf") as pdf:
        for distribution, data in generated_data.items():
            
            figure, ax = plt.subplots(1, figsize=(10, 5))
            plot_box(data.get("data"), distribution, ax)
            plt.tight_layout()
            # Save the current figure to the PDF
            pdf.savefig(figure)
            plt.close(figure)
