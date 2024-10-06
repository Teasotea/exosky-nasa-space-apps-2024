import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
from matplotlib.patches import Circle


class MollweideVizualizer:

    def __init__(self, magnitude_treshold: float = 10):
        self.cmap = plt.get_cmap("coolwarm")  # A colormap going from blue to red
        self.norm = plt.Normalize(
            vmin=-5, vmax=7
        )  # Normalize 'bp_rp' values for color mapping
        self.magnitude_treshold = magnitude_treshold

    def plot(
        self,
        ra_arr,
        dec_arr,
        mag_arr,
        bp_rp_arr,
        grid: bool = True,
        mollweide: bool = False,
        earth: tuple[float, float, float] | None = None,
    ):
        bright_starts = mag_arr < self.magnitude_treshold
        local_sun = mag_arr < -7
        ra_arr = ra_arr[bright_starts & ~local_sun]
        dec_arr = dec_arr[bright_starts & ~local_sun]
        mag_arr = mag_arr[bright_starts & ~local_sun]
        bp_rp_arr = bp_rp_arr[bright_starts & ~local_sun]

        # Create a figure
        fig = plt.figure(figsize=(20, 12))
        ax = fig.add_subplot(111, projection="mollweide" if mollweide else None)
        ax.margins(x=0, y=0, tight=True)
        ax.grid(grid)

        # Using Mollweide projection for RA/DEC
        ra_rad = np.radians(ra_arr - 180)
        dec_rad = np.radians(dec_arr)

        # Adjust star sizes with exponential scaling
        size = np.exp(4 - mag_arr)
        size = np.clip(size, 0, 100) * 2
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
        # ax.set_xlabel("Right Ascension (degrees)", color="black")
        # ax.set_ylabel("Declination (degrees)", color="black")
        # ax.set_title("Star Map from Gaia Data (Mollweide Projection)", color="black")

        # Adjust axis labels and ticks to white to contrast with the dark projection background
        ax.set_xticks(
            np.radians(
                [-180, -150, -120, -90, -60, -30, 0, 30, 60, 90, 120, 150, 180][::1]
            )
        )
        ax.set_yticks(np.radians([-80, -60, -40, -20, 0, 20, 40, 60, 80][::1]))
        ax.xaxis.label.set_color("white")
        ax.yaxis.label.set_color("white")
        ax.tick_params(axis="both", colors="white")
        ax.xaxis.set_ticklabels([])
        ax.yaxis.set_ticklabels([])

        if earth:
            axins = self._add_earth_subplot(ax, earth)

            earth_mag = (
                4.83 - 5 + 5 * np.log10(earth[2])
            )  # 4.83 is a sun absolute magnitude

            axins.scatter(
                np.radians(earth[0]),
                np.radians(earth[1]),
                s=np.clip(np.exp(4 - earth_mag) * 30, 0, 100),
                c="white",
                # cmap=self.cmap,
                # norm=self.norm,
                alpha=0.75,
            )
            axins.scatter(
                ra_rad,
                dec_rad,
                s=size * 30,
                c=bp_rp_arr,
                cmap=self.cmap,
                norm=self.norm,
                alpha=0.75,
            )
            ax.scatter(
                np.radians(earth[0]),
                np.radians(earth[1]),
                s=np.clip(np.exp(4 - earth_mag), 0, 100),
                c="white",
                # cmap=self.cmap,
                # norm=self.norm,
                alpha=0.75,
            )
            ax.indicate_inset_zoom(axins, edgecolor="white", linewidth=2)

        return fig, ax

    def _add_earth_subplot(self, ax, earth):

        inset_coord = [0, 0, 30, 30]

        if earth[0] < 30:
            inset_coord[0] = 30

        if earth[1] < 30:
            inset_coord[1] = 30

        axins = ax.inset_axes(
            np.radians(inset_coord),
            xlim=np.radians((earth[0] - 5, earth[0] + 5)),
            ylim=np.radians((earth[1] - 5, earth[1] + 5)),
            xticklabels=[],
            yticklabels=[],
        )
        circle = Circle(
            np.radians(earth[:2]),
            np.radians(0.25),
            fill=False,
            color="red",
            linewidth=3,
        )

        axins.add_patch(circle)

        axins.set_facecolor("#000033")
        return axins

    def plot_star_chart(self, df, selected_stars):
        """Plot the star chart and handle drawing mode."""
        fig = go.Figure()

        # Plot stars as scatter plot based on real exoplanet data
        fig.add_trace(
            go.Scatter(
                x=df["new_ra"],  # Right Ascension
                y=df["new_dec"],  # Declination
                mode="markers",
                marker=dict(size=df["s"], color="white"),  # Size depends on 's' column
                text=df["SOURCE_ID"],  # Exoplanet names
                name="Stars",
            )
        )

        # Draw lines between selected stars
        if len(selected_stars) > 1:
            for i in range(len(selected_stars) - 1):
                star1 = df[df["SOURCE_ID"] == selected_stars[i]].iloc[0]
                star2 = df[df["SOURCE_ID"] == selected_stars[i + 1]].iloc[0]
                fig.add_trace(
                    go.Scatter(
                        x=[star1["new_ra"], star2["new_ra"]],
                        y=[star1["new_dec"], star2["new_dec"]],
                        mode="lines",
                        line=dict(
                            color="yellow", width=2
                        ),  # Connection lines in yellow
                        name="Constellation",
                    )
                )

        # Update layout for the figure
        fig.update_layout(
            xaxis_title="Right Ascension (RA)",
            yaxis_title="Declination (DEC)",
            title="Exoplanet Star Chart",
            title_font=dict(size=20, color="white"),
            title_x=0.35,
            plot_bgcolor="darkblue",  # Dark blue background
            paper_bgcolor="darkblue",  # Dark blue for the paper background
            font=dict(color="white"),  # White font color for titles and labels
            showlegend=False,  # Show legend
        )

        # Set x and y axis properties for better visibility
        fig.update_xaxes(
            showgrid=True, gridcolor="gray", zerolinecolor="gray"
        )  # Optional: add gridlines for clarity
        fig.update_yaxes(
            showgrid=True, gridcolor="gray", zerolinecolor="gray"
        )  # Optional: add gridlines for clarity

        return fig
