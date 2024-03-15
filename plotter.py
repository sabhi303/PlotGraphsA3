import matplotlib.pyplot as plt


# plot CDF
def plot_CDF(data, title, plt):
    plt.subplot(1, 2, 1)
    plt.hist(data, bins=100, density=True, cumulative=True, histtype="step", color="b")
    plt.title(f"{title} CDF")


# plt box plot
def plot_box(data, title, plt):
    plt.subplot(1, 2, 2)
    plt.boxplot(data)
    plt.title(f"{title} Boxplot")


def plot_graphs(filename, generated_data):
    """Plot CDF and Boxplot and save as PDF files."""
    for distribution, data in generated_data.items():
        print("Data", data)

        plt.figure(figsize=(10, 5))

        plot_CDF(data, distribution, plt)
        plot_box(data, distribution, plt)

        plt.tight_layout()

        # plt.show()
        plt.savefig(f"{filename}-{distribution}-CDF-Box.pdf")
        plt.close()
