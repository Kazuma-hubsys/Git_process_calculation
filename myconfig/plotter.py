import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

plt.rcParams["font.family"] = "Arial"
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['font.size'] = 18

plt.rcParams["mathtext.cal"]     = "serif"            # 数式フォントの設定（カリグラフィ）
plt.rcParams["mathtext.rm"]      = "serif"            # 数式フォントの設定（ロマン体）
plt.rcParams["mathtext.it"]      = "serif:italic"     # 数式フォントの設定（斜体）
plt.rcParams["mathtext.bf"]      = "serif:bold"       # 数式フォントの設定（太字）
plt.rcParams["mathtext.fontset"] = "cm"               # 数式フォント（cmはComputer Modern）

plt.rcParams["axes.labelsize"] = 18  # 軸ラベルのフォントサイズ
plt.rcParams["axes.linewidth"] = 2.0       # グラフ囲う線の太さ
plt.rcParams["axes.grid"]      = False     # グリッドを表示するかどうか

# Legend
plt.rcParams["legend.loc"]        = "best"   # 凡例の位置、"best"でいい感じのところ
plt.rcParams["legend.frameon"]    = False     # 凡例を囲うかどうか、Trueで囲う、Falseで囲わない
plt.rcParams["legend.framealpha"] = 0.5      # 透過度、0.0から1.0の値を入れる
plt.rcParams["legend.facecolor"]  = "white"  # 背景色
plt.rcParams["legend.edgecolor"]  = "black"  # 囲いの色
plt.rcParams["legend.fancybox"]   = False    # Trueにすると囲いの四隅が丸くなる

def plot_formatting(axes, x_label="x", y_label="y", title="title"):
    axes_new = axes
    wid = 2
    for ax in [axes_new]:
        for s in ax.spines:
            pass
            ax.spines[s].set_color('k')
            # ax.spines[s].set_linewidth(wid)
    axes_new.get_xaxis().set_tick_params(pad=10)
    axes_new.get_yaxis().set_tick_params(pad=10)
    axes_new.set_title(title)
    axes_new.set_xlabel(x_label)
    axes_new.set_ylabel(y_label)
    return axes_new

def make_ax(x_label, y_label, title):
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_alpha(0)
    ax = plot_formatting(ax, x_label, y_label, title)
    return ax

def save_figure(title, save_dir):
    DATA_DIR = Path(__file__).resolve().parent.parent / "DATA"
    plot_dir = DATA_DIR / save_dir
    plot_dir.mkdir(exist_ok=True)
    save_path = plot_dir / f"{title}.png"
    plt.tight_layout()
    plt.savefig(save_path)

###############
## Line plot ##
###############

def plot_line(x, y_list, legend_label=[], x_label="x", y_label="y", title="title", save_dir="plots", legend_on=True):
    ax = make_ax(x_label, y_label, title)
    if not legend_label:
        legend_label = [str(i) for i in range(len(y_list))]
    
    for i in range(len(y_list)):
       y = y_list[i]
       label = legend_label[i]
       ax.plot(x, y, label=label)
    if legend_on:
        ax.legend(bbox_to_anchor=(1.01, 0.5), loc="center left", frameon=False)

    print(f"Plotted: {title}")
    save_figure(title, save_dir)
    plt.show()

##############
## Bar plot ##
##############

def plot_bar(y_list, label_list=[], x_label="", y_label="y", title="title", save_dir="plots"):
    ax = make_ax(x_label, y_label, title)

    x = ["Bar" + str(i+1) for i in range(len(y_list))]
    tick_label = label_list if (len(label_list) == len(y_list)) else x
    ax.bar(tick_label, y_list, tick_label=tick_label)

    print(f"Plotted: {title}")
    save_figure(title, save_dir)
    plt.show()

def plot_stack_bar(y_list, label_list=[], x_label="", y_label="y", title="title", save_dir="plots"):
    ax = make_ax(x_label, y_label, title)

    x = ["Bar" + str(i+1) for i in range(len(y_list))]
    tick_label = label_list if (len(label_list) == len(y_list)) else x
    
    # y_list内の各リストの最大長を取得
    max_len = max(len(y) for y in y_list)
    
    # 各段（層）ごとに積み上げ棒をプロット
    bottom = np.zeros(len(y_list))
    for layer in range(max_len):
        heights = []
        for y in y_list:
            if layer < len(y):
                heights.append(y[layer])
            else:
                heights.append(0)
        ax.bar(tick_label, heights, bottom=bottom, label=f"Layer {layer + 1}")
        bottom += np.array(heights)
    
    ax.legend(bbox_to_anchor=(1.01, 0.5), loc="center left", frameon=False)
    print(f"Plotted: {title}")
    save_figure(title, save_dir)
    plt.show()

##################
## Scatter plot ##
##################

def plot_scatter(x, y, x_label="x", y_label="y", title="title", save_dir="plots"):
    ax = make_ax(x_label, y_label, title)

    x_list = x
    y_list = y
    ax.scatter(x_list, y_list)

    print(f"Plotted: {title}")
    save_figure(title, save_dir)
    plt.show()

######################
## Combination plot ##
######################

def plot_line_and_scatter(x_line, y_line, x_scat, y_scat, legend_label=[],  x_label="x", y_label="y", title="title", save_dir="plots", legend_on=True):
    ax = make_ax(x_label, y_label, title)
    if legend_on and (not legend_label):
        legend_label = [str(i) for i in range(len(y_line))]

    ax.scatter(x_scat, y_scat)

    for i in range(len(y_line)):
       y = y_line[i]
       label = legend_label[i]
       ax.plot(x_line, y, label=label)
    ax.legend(bbox_to_anchor=(1.01, 0.5), loc="center left", frameon=False)

    print(f"Plotted: {title}")
    save_figure(title, save_dir)
    plt.show()

if __name__ == "__main__":
    
    # x = np.linspace(- 2 * np.pi, 2 * np.pi, 100)
    # y_list = [np.sin(x), np.cos(x)]
    # legend_label = ["sin(x)", "cos(x)"]
    # plot_line(x, y_list, legend_label=legend_label)

    # x = np.linspace(- 2 * np.pi, 2 * np.pi, 100)
    # y_list = [np.sin(x), np.cos(x)]
    # x_scat = [-2, 0, 2]
    # y_scat = [np.sin(-2), 0, np.sin(2)]
    # legend_label = ["sin(x)", "cos(x)"]
    # plot_line_and_scatter(x_line=x, y_line=y_list, x_scat=x_scat, y_scat=y_scat, legend_label=legend_label)

    # y_list = np.array([5, 3, 7, 4, 6])
    # plot_bar(y_list)

    # 各barが異なるリストの値を積み上げる
    y_list = [[2, 1, 3], [1, 4, 2], [3, 2, 1], [2, 3, 2]]
    plot_stack_bar(y_list)