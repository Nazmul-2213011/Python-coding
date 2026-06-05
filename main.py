import tkinter as tk
from tkinter import messagebox, filedialog
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import math


class LinePlotterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Scientific Multi Graph Plotter")

        self.graphs = []

        # ---------------- GRAPH INPUTS ----------------
        for i in range(4):
            frame = tk.LabelFrame(root, text=f"Graph {i+1}", padx=10, pady=10)
            frame.grid(row=i, column=0, columnspan=2, sticky="w", pady=5)

            tk.Label(frame, text="X datasets (; separated)").grid(row=0, column=0)
            x_data = tk.Entry(frame, width=60)
            x_data.grid(row=0, column=1)

            tk.Label(frame, text="Y datasets (; separated)").grid(row=1, column=0)
            y_data = tk.Entry(frame, width=60)
            y_data.grid(row=1, column=1)

            tk.Label(frame, text="X-axis label").grid(row=2, column=0)
            x_label = tk.Entry(frame, width=40)
            x_label.grid(row=2, column=1)

            tk.Label(frame, text="Y-axis label").grid(row=3, column=0)
            y_label = tk.Entry(frame, width=40)
            y_label.grid(row=3, column=1)

            tk.Label(frame, text="Legend names (, separated)").grid(row=4, column=0)
            legend = tk.Entry(frame, width=60)
            legend.grid(row=4, column=1)

            tk.Label(frame, text="Figure title").grid(row=5, column=0)
            title = tk.Entry(frame, width=60)
            title.grid(row=5, column=1)

            self.graphs.append((x_data, y_data, x_label, y_label, legend, title))

        # ---------------- BUTTONS ----------------
        tk.Button(root, text="HELP", command=self.help).grid(row=5, column=0)
        tk.Button(root, text="PLOT", command=self.plot).grid(row=5, column=1)

        tk.Button(root, text="SAVE JPG", command=self.save_jpg).grid(row=6, column=0)
        tk.Button(root, text="SAVE PDF", command=self.save_pdf).grid(row=6, column=1)

        self.last_fig = None

    # ---------------- HELP ----------------
    def help(self):
        msg = r"""
========================
HOW TO USE THIS APP
========================

✔ HOW TO PLOT:
X datasets:
  1,2,3; 1,2,3

Y datasets:
  2,4,6; 3,6,9

Use ';' to separate curves

------------------------
✔ MATHEMATICAL FORMAT ($...$)
------------------------

$x^2$, $CO_2$, $x_1$

------------------------
✔ DEVELOPED BY:
Nazmul Hasan
Email: nazmulhasan25350@gmail.com
"""
        messagebox.showinfo("Help", msg)

    # ---------------- ACTIVE ----------------
    def get_active_graphs(self):
        return [g for g in self.graphs if g[0].get().strip()]

    # ---------------- PLOT (FIXED GRID) ----------------
    def create_plot(self):
        try:
            active = self.get_active_graphs()

            if not active:
                messagebox.showwarning("No Data", "Please enter at least one graph.")
                return None

            n = len(active)

            fig = plt.figure(figsize=(12, 8))

            # 🔥 GRID FIX (TRUE CENTERING)
            if n == 1:
                gs = gridspec.GridSpec(1, 1)
            elif n == 2:
                gs = gridspec.GridSpec(1, 2)
            elif n == 3:
                gs = gridspec.GridSpec(2, 2)
            else:
                gs = gridspec.GridSpec(2, 2)

            axes = []

            if n == 1:
                axes.append(fig.add_subplot(gs[0, 0]))

            elif n == 2:
                axes.append(fig.add_subplot(gs[0, 0]))
                axes.append(fig.add_subplot(gs[0, 1]))

            elif n == 3:
                axes.append(fig.add_subplot(gs[0, 0]))
                axes.append(fig.add_subplot(gs[0, 1]))

                # 🔥 THIS IS THE KEY FIX (CENTER FULL WIDTH)
                axes.append(fig.add_subplot(gs[1, :]))

            else:
                axes.append(fig.add_subplot(gs[0, 0]))
                axes.append(fig.add_subplot(gs[0, 1]))
                axes.append(fig.add_subplot(gs[1, 0]))
                axes.append(fig.add_subplot(gs[1, 1]))

            # ---------------- PLOT DATA ----------------
            for i, graph in enumerate(active):
                ax = axes[i]

                x_str, y_str, xlab, ylab, legend_str, title_str = graph

                x_sets = x_str.get().split(";")
                y_sets = y_str.get().split(";")
                legends = legend_str.get().split(",")

                legend_used = False

                for j in range(min(len(x_sets), len(y_sets))):
                    x = list(map(float, x_sets[j].strip().split(",")))
                    y = list(map(float, y_sets[j].strip().split(",")))

                    label = legends[j].strip() if j < len(legends) else ""

                    if label:
                        legend_used = True

                    ax.plot(x, y, marker="o", linestyle="-",
                            label=label if label else None)

                ax.set_xlabel(xlab.get())
                ax.set_ylabel(ylab.get())

                ax.text(0.5, -0.25, title_str.get(),
                        transform=ax.transAxes, ha="center", fontsize=10)

                if legend_used:
                    ax.legend()

                ax.grid(True)

            plt.tight_layout()
            return fig

        except Exception as e:
            messagebox.showerror("Error", str(e))
            return None

    # ---------------- ACTIONS ----------------
    def plot(self):
        fig = self.create_plot()
        if fig:
            self.last_fig = fig
            plt.show()

    def save_jpg(self):
        if self.last_fig:
            file = filedialog.asksaveasfilename(defaultextension=".jpg")
            if file:
                self.last_fig.savefig(file, dpi=300)
                messagebox.showinfo("Saved", "JPG saved")

    def save_pdf(self):
        if self.last_fig:
            file = filedialog.asksaveasfilename(defaultextension=".pdf")
            if file:
                self.last_fig.savefig(file)
                messagebox.showinfo("Saved", "PDF saved")


# ---------------- RUN ----------------
root = tk.Tk()
app = LinePlotterApp(root)
root.mainloop()