import matplotlib.pyplot as plt
import numpy as np


class MollweideVizualizer:

    def __init__(self):
        self.cmap = plt.get_cmap("coolwarm")  # A colormap going from blue to red
        self.norm = plt.Normalize(vmin=-5, vmax=7)  # Normalize 'bp_rp' values for color mapping

    def plot(self, ra_arr, dec_arr, mag_arr, bp_rp_arr, grid: bool = True):
        # Create a figure
        fig = plt.figure(figsize=(10, 6))
        ax = fig.add_subplot(111, projection="mollweide")

        ax.grid(grid)

        # Using Mollweide projection for RA/DEC
        ra_rad = np.radians(ra_arr - 180)
        dec_rad = np.radians(dec_arr)

        # Adjust star sizes with exponential scaling
        size = np.exp(4 - mag_arr)
        ax.set_facecolor("#000033")

        ax.scatter(ra_rad, dec_rad, s=size, c=bp_rp_arr, cmap=self.cmap, norm=self.norm, alpha=0.75)

        # Add labels and title
        ax.set_xlabel("Right Ascension (degrees)", color="black")
        ax.set_ylabel("Declination (degrees)", color="black")
        ax.set_title("Star Map from Gaia Data (Mollweide Projection)", color="black")

        # Adjust axis labels and ticks to white to contrast with the dark projection background
        ax.xaxis.label.set_color("white")
        ax.yaxis.label.set_color("white")
        ax.tick_params(axis="both", colors="white")
        ax.xaxis.set_ticklabels([])
        ax.yaxis.set_ticklabels([])
        return fig, ax
