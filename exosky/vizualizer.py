import matplotlib.pyplot as plt
import numpy as np


class MollweideVizualizer:

    def __init__(self, magnitude_treshold: float = 10):
        self.cmap = plt.get_cmap("coolwarm")  # A colormap going from blue to red
        self.norm = plt.Normalize(
            vmin=-5, vmax=7
        )  # Normalize 'bp_rp' values for color mapping
        self.magnitude_treshold = magnitude_treshold

    def plot(self, ra_arr, dec_arr, mag_arr, bp_rp_arr, grid: bool = True):
        bright_starts = mag_arr < self.magnitude_treshold
        sun = mag_arr < -7
        ra_arr = ra_arr[bright_starts & ~sun]
        dec_arr = dec_arr[bright_starts & ~sun]
        mag_arr = mag_arr[bright_starts & ~sun]
        bp_rp_arr = bp_rp_arr[bright_starts & ~sun]

        # Create a figure
        fig = plt.figure(figsize=(10, 6))
        ax = fig.add_subplot(111, projection="mollweide")

        ax.grid(grid)

        # Using Mollweide projection for RA/DEC
        ra_rad = np.radians(ra_arr - 180)
        dec_rad = np.radians(dec_arr)

        # Adjust star sizes with exponential scaling
        size = np.exp(4 - mag_arr)
        size = np.clip(size, 0, 100)
        # size = 100 * 10 ** (mag_arr / -2.5)

        ax.set_facecolor("#000033")

        ax.scatter(
            ra_rad,
            dec_rad,
            s=size,
            c=bp_rp_arr,
            cmap=self.cmap,
            norm=self.norm,
            alpha=0.75,
        )

        # Add labels and title
        ax.set_xlabel("Right Ascension (degrees)", color="black")
        ax.set_ylabel("Declination (degrees)", color="black")
        # ax.set_title("Star Map from Gaia Data (Mollweide Projection)", color="black")

        # Adjust axis labels and ticks to white to contrast with the dark projection background
        ax.xaxis.label.set_color("white")
        ax.yaxis.label.set_color("white")
        ax.tick_params(axis="both", colors="white")
        ax.xaxis.set_ticklabels([])
        ax.yaxis.set_ticklabels([])
        return fig, ax
