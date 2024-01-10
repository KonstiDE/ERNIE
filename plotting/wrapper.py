import matplotlib.pyplot as plt
import numpy as np

from datetime import datetime


def wrap_plot(x_data, y_data, plot_type="line", color="#007acc", alpha=1, xticks=None, grid=None, legenddata=None, legend=False, xlabel="", ylabel="", vertical_line_date=None):
    fig, ax = plt.subplots()
    fig.patch.set_facecolor('#0c1c23')

    if plot_type == "line":
        ax.plot(x_data, y_data, color=color, alpha=alpha)
    elif plot_type == "bar":
        ax.bar(x_data, y_data, color=color, alpha=alpha)
    elif plot_type == "scatter":
        ax.scatter(x_data, y_data, color=color, alpha=alpha)

    ax.set_facecolor('#122229')
    ax.spines['left'].set_color('#FFFFFF')
    ax.spines['left'].set_linewidth(0.5)

    ax.spines['bottom'].set_color("#3C494F")
    ax.spines['bottom'].set_linewidth(0.3)
    ax.spines['top'].set_color("#3C494F")
    ax.spines['top'].set_linewidth(0.3)
    ax.spines['right'].set_color("#3C494F")
    ax.spines['right'].set_linewidth(0.3)

    ax.tick_params(axis='both', colors='#FFFFFF')

    if xticks is not None:
        ax.set_xticklabels(xticks)

    if grid is not None:
        plt.grid(color="#3C494F", linestyle=grid, linewidth=0.3)

    plt.xticks(rotation=45, ha='right', color="white")
    plt.yticks(color="white")

    if vertical_line_date is not None:
        plt.axvline(x=vertical_line_date, label='Christmas', color="white", linestyle='--', alpha=0.75)

    plt.xlabel(xlabel, color="white", fontweight="bold", fontsize=10)
    plt.ylabel(ylabel, color="white", fontweight="bold", fontsize=10)

    if legend:
        plt.legend(legenddata)

    plt.tight_layout()
    plt.show()


def wrap_plots(x_data, y_datas, colors, plot_type="line", alpha=1, xticks=None, legend=False, legenddata=None, grid=None, xlabel="", ylabel="", vertical_line_date=None):
    assert len(colors) == len(y_datas)

    fig, ax = plt.subplots()
    fig.patch.set_facecolor('#0c1c23')

    if plot_type == "line":
        for idx, y_data in enumerate(y_datas):
            ax.plot(x_data, y_data, color=colors[idx], alpha=alpha)
    elif plot_type == "bar":
        for idx, y_data in enumerate(y_datas):
            ax.bar(x_data, y_data, color=colors[idx], alpha=alpha)
    elif plot_type == "scatter":
        for idx, y_data in enumerate(y_datas):
            ax.scatter(x_data, y_data, color=colors[idx], alpha=alpha)

    ax.set_facecolor('#122229')
    ax.spines['left'].set_color('#FFFFFF')
    ax.spines['left'].set_linewidth(0.5)

    ax.spines['bottom'].set_color("#3C494F")
    ax.spines['bottom'].set_linewidth(0.3)
    ax.spines['top'].set_color("#3C494F")
    ax.spines['top'].set_linewidth(0.3)
    ax.spines['right'].set_color("#3C494F")
    ax.spines['right'].set_linewidth(0.3)

    ax.tick_params(axis='both', colors='#FFFFFF')

    plt.xticks(rotation=45, ha='right', color="white")
    plt.yticks(color="white")

    if xticks is not None:
        ax.set_xticklabels(xticks)

    if grid is not None:
        plt.grid(color="#3C494F", linestyle=grid, linewidth=0.3)

    plt.xlabel(xlabel, color="white", fontweight="bold", fontsize=10)
    plt.ylabel(ylabel, color="white", fontweight="bold", fontsize=10)

    if vertical_line_date is not None:
        plt.axvline(x=vertical_line_date, label='Christmas', color="white", linestyle='--', alpha=0.75)

    if legend:
        plt.legend(legenddata)

    plt.tight_layout()
    plt.show()
