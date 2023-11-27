import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

text_color = "000000"

plt.rcParams.update({
    'font.size': 16,
    'text.color': text_color,
    'axes.edgecolor': text_color,
    'xtick.color': text_color,
    'ytick.color': text_color,
    'axes.labelcolor': text_color,
})

plt.rc('figure', dpi=100)
plt.rc('text', usetex=True)
plt.rc('font', family='serif')
plt.rc('text.latex', preamble=r'\usepackage{textgreek}')


def to_df(t, x, control, labels):
    model_labels = labels[0]
    control_labels = labels[1]

    x_dict = {"t": t}
    control_dict = {}

    for i in range(len(x)):
        x_dict[model_labels[i]] = x[i]

    for i in range(len(control)):
        control_dict[control_labels[i]] = control[i]

    return pd.concat([pd.DataFrame(x_dict), pd.DataFrame(control_dict)], axis=1)


def plot_x(df, workdir, measure_labels=None):
    for i in range(1, df.shape[1]):
        fig, ax = plt.subplots()

        if df.iloc[0::, i].name == 'V_f':
            ax.plot(df.iloc[1::, 0], np.zeros(df.shape[0] - 1), linewidth=3.0, color="red", alpha=0.8)

        ax.set_ylim(np.min(df.iloc[0::, i]), np.max(df.iloc[0::, i]) * 1.2)

        ax.plot(df.iloc[0::, 0], df.iloc[0::, i], linewidth=2.0, color="black")

        # ylimit = max(df.iloc[0::, i]) * 1.2
        # ax.set_ylim(min(df.iloc[1::, i]), ylimit)

        ax.set_xlabel("$t$, days", loc="right")
        if measure_labels is None:
            ax.text(.01, .97, "$" + str(df.columns[i]) + "(t)$", ha='left', va='top', transform=ax.transAxes)
        else:
            ax.text(.01, .97, "$" + str(df.columns[i]) + "(t)$, " + measure_labels[i],
                    ha='left', va='top', transform=ax.transAxes)

        fig.tight_layout()
        fig.savefig(workdir + "png/" + str(df.columns[i]) + ".png")
        fig.savefig(workdir + "svg/" + str(df.columns[i]) + ".svg")
        # plt.show()
        plt.close()


def plot_two_one_axes(df1, df2, workdir, measure_labels=None):
    max_shape = max(df1.shape[1], df2.shape[1])

    for i in range(1, max_shape):

        # if df1.iloc[1::, 0].name == df2.iloc[1::, 0].name
        fig, ax = plt.subplots()

        ax.plot(df1.iloc[1::, 0], df1.iloc[1::, i], linestyle="-", linewidth=1.9, color="black", alpha=0.85)
        ax.plot(df2.iloc[1::, 0], df2.iloc[1::, i], linestyle="-", linewidth=1.9, color="red", alpha=0.85)

        # ax.spines['left'].set_color('red')
        # ax.spines['right'].set_color('darkturquoise')

        if df1.iloc[1::, i].name == 'V_f':
            ax.plot(df1.iloc[1::, 0], np.zeros(df1.shape[0] - 1), linewidth=3.0, color="red", alpha=0.8)

        # if df1.iloc[1::, i].name == 'u':
        #     ax.set_ylim(0, np.max(df1.iloc[1::, i] + df2.iloc[1::, i]) * 1.1)
        #else:
        #   ax.set_ylim(np.min(df1.iloc[1::, i] + df2.iloc[1::, i]), np.max(df1.iloc[1::, i] + df2.iloc[1::, i]) * 1.1)

        # ax.set_ylim(np.min(df1.iloc[1::, i] + df2.iloc[1::, i]),
        #            np.max(df1.iloc[1::, i] + df2.iloc[1::, i]) * 1.2)

        ax.set_ylim(np.min(np.concatenate((df1.iloc[1::, i], df2.iloc[1::, i]))), np.max(np.concatenate((df1.iloc[1::, i], df2.iloc[1::, i]))) * 1.2)

        ax.set_xlabel("$t$, days", loc="right")

        if measure_labels is None:
            ax.text(.01, .97, "$" + str(df1.columns[i]) + "(t)$", ha='left', va='top', transform=ax.transAxes)
        else:
            ax.text(.01, .97, "$" + str(df1.columns[i]) + "(t)$, " + measure_labels[i],
                    ha='left', va='top', transform=ax.transAxes)

        fig.tight_layout()
        fig.savefig(workdir + "png/" + str(df1.columns[i]) + ".png")
        fig.savefig(workdir + "svg/" + str(df1.columns[i]) + ".svg")
        # plt.show()
        plt.close()


def plot_two(df1, df2, workdir):
    # if df1.shape[1] != df2.shape[1]:
    #     raise Exception("Can't ffs")

    for i in range(1, df1.shape[1]):
        fig, ax1 = plt.subplots()
        ax2 = ax1.twinx()

        ax1.plot(df1.iloc[0::, 0], df1.iloc[0::, i], linestyle="-", linewidth=1.5, color="black", alpha=0.85)
        ax2.plot(df2.iloc[0::, 0], df2.iloc[0::, i], linestyle="--", linewidth=1.5, color="black", alpha=0.85)

        # ax2.spines['left'].set_color('red')
        # ax2.spines['right'].set_color('black')
        ax1.spines['left'].set(linestyle='--')

        if i == 1:
            ax2.plot(df1.iloc[1::, 0], np.zeros(df1.shape[0] - 1), linewidth=3.0, color="red", alpha=0.8)

        ax1.set_ylim(min(df1.iloc[0::, i]), max(df1.iloc[0::, i]) * 1.2)
        ax2.set_ylim(min(df2.iloc[0::, i]), max(df2.iloc[0::, i]) * 1.2)

        ax1.set_xlabel("$t$, days", loc="right")
        ax1.text(.01, .97, "$" + str(df1.columns[i]) + "(t)$", ha='left', va='top', transform=ax1.transAxes)

        fig.tight_layout()
        fig.savefig(workdir + "png/" + str(df1.columns[i]) + ".png")
        fig.savefig(workdir + "svg/" + str(df1.columns[i]) + ".svg")
        # plt.show()
        plt.close()
