# src/plot_results.py

import matplotlib.pyplot as plt


def plot_monte_carlo(results_list):

    undervoltages = [r["undervoltage_percent"] for r in results_list]
    overloads = [r["max_line_loading"] for r in results_list]

    plt.figure()
    plt.hist(undervoltages, bins=10)
    plt.title("Undervoltage Risk Distribution")
    plt.xlabel("Undervoltage %")
    plt.ylabel("Frequency")
    plt.show()

    plt.figure()
    plt.hist(overloads, bins=10)
    plt.title("Max Line Loading Distribution")
    plt.xlabel("Loading %")
    plt.ylabel("Frequency")
    plt.show()