import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def create_plots(total_nodes_expanded, total_steps, total_path_length, total_time_taken, algo_list):
    # Creating a list of labels
    labels = algo_list

    # Creating the bar chart
    plt.bar(labels, total_nodes_expanded)
    plt.xlabel('Algorithms')
    plt.ylabel('Nodes expanded')
    plt.title('Comparison of nodes expanded')
    plt.savefig('./images/plot1.png', dpi=85)
    plt.clf()  # Clear the plot

    plt.plot(labels, total_steps, marker='o')
    plt.xlabel('Algorithms')
    plt.ylabel('Steps')
    plt.title('Comparison of total steps taken')
    plt.grid(True)
    plt.savefig('./images/plot2.png', dpi=85)
    plt.clf()  # Clear the plot

    # Creating the bar chart
    plt.bar(labels, total_path_length)
    plt.xlabel('Algorithms')
    plt.ylabel('Nodes expanded')
    plt.title('Comparison of path lengths')
    plt.savefig('./images/plot3.png', dpi=85)
    plt.clf()  # Clear the plot

    plt.plot(labels, total_time_taken, marker='o')
    for i, v in enumerate(total_time_taken):
        plt.text(i, v, "{:.2f}".format(v), ha='center', va='bottom', fontsize=9)
    plt.xlabel('Algorithms')
    plt.ylabel('Completion time')
    plt.title('Comparison of completion time')
    plt.grid(True)
    plt.savefig('./images/plot4.png', dpi=85)
    plt.clf()  # Clear the plot

    # big  comparison

    # Create a list of indices for each label (algorithm), which we'll use as the x-coordinates for the plot
    x = np.arange(len(labels))

    # Define width of a bar
    width = 0.2

    fig, ax1 = plt.subplots()

    # We use the same x values for each line plot, so the lines will be overlaid on the same plot
    ax1.plot(x, total_nodes_expanded, marker='o', label='Nodes expanded')
    ax1.plot(x, total_steps, marker='o', label='Steps')
    ax1.plot(x, total_path_length, marker='o', label='Path length')
    ax1.plot(x, total_time_taken, marker='o', label='Completion time')

    # Adding labels, title and custom x-axis tick labels, etc.
    ax1.set_xlabel('Algorithms')
    ax1.set_ylabel('Values')
    ax1.set_title('Comparison of different metrics')
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels)
    ax1.legend()

    fig.tight_layout()
    plt.savefig('./images/plot5.png', dpi=85)
    plt.clf()  # Clear the plot


