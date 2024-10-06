# import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from astroquery.nasa_exoplanet_archive import NasaExoplanetArchive
from astroquery.gaia import Gaia


def get_exoplanet_data():
    exoplanets = NasaExoplanetArchive.query_criteria(
        table="PSCompPars",  # The new Planetary Systems (PS) table
        select="pl_name, ra, dec, sy_dist, pl_orbincl, pl_orbsmax, st_mass, st_rad",
        where="sy_dist IS NOT NULL"  # Filter to get systems with known distances
    )
    df_exoplanets = exoplanets.to_pandas()
    return df_exoplanets


# write a func to filter exoplanets available within a certain distance from earth
def filter_exoplanets_within_distance(df_exoplanets, max_distance=100):
    return df_exoplanets[df_exoplanets["sy_dist"] <= max_distance]


def compute_star_properties_from_exoplanet(df_gaia, exoplanet):
    # Get exoplanet's coordinates and distance
    exoplanet_ra = np.radians(exoplanet["ra"])  # Convert to radians
    exoplanet_dec = np.radians(exoplanet["dec"])
    exoplanet_distance = exoplanet["sy_dist"]  # * 206265  # Convert parsecs to AU

    # Calculate distances for Gaia stars from parallax
    parallax = df_gaia["parallax"] / 1000  # Parallax in arcseconds
    d = np.where(
        parallax > 0, 1 / parallax, np.inf
    )  # Distance in parsecs; inf for zero or negative parallax

    # Convert Gaia stars to Cartesian coordinates\
    # TODO: CHECK IF THIS IS CORRECT, NOT SURE ABOUT GAIA MEASUREMENT UNITS
    x_gaia = d * np.cos(np.radians(df_gaia["dec"])) * np.cos(np.radians(df_gaia["ra"]))
    y_gaia = d * np.cos(np.radians(df_gaia["dec"])) * np.sin(np.radians(df_gaia["ra"]))
    z_gaia = d * np.sin(np.radians(df_gaia["dec"]))

    # Calculate the position of the exoplanet in Cartesian coordinates
    x_exoplanet = exoplanet_distance * np.cos(exoplanet_dec) * np.cos(exoplanet_ra)
    y_exoplanet = exoplanet_distance * np.cos(exoplanet_dec) * np.sin(exoplanet_ra)
    z_exoplanet = exoplanet_distance * np.sin(exoplanet_dec)

    # Adjust Gaia star positions relative to the exoplanet
    star_x = x_gaia - x_exoplanet
    star_y = y_gaia - y_exoplanet
    star_z = z_gaia - z_exoplanet

    # Convert back to spherical coordinates (RA, Dec)
    r = np.sqrt(star_x**2 + star_y**2 + star_z**2)

    # Avoid division by zero
    r[r == 0] = 1e-10

    new_dec = np.arcsin(star_z / r)  # New declination
    new_ra = np.arctan2(star_y, star_x)  # New right ascension

    # Convert back to degrees
    new_dec = np.degrees(new_dec)
    new_ra = np.degrees(new_ra)

    # Normalize RA to be between 0 and 360
    new_ra = (new_ra + 360) % 360

    # Compute apparent magnitudes
    apparent_magnitudes = []
    for index, row in df_gaia.iterrows():

        absolute_magnitude = (
            row["phot_g_mean_mag"] + 5 - 5 * np.log10(1000 / row["parallax"])
        )

        # absolute_magnitude = row['phot_g_mean_mag']  # G-band mean magnitude

        # Calculate the distance from the exoplanet to the star
        distance_from_exoplanet = r[index]

        # Calculate the apparent magnitude using the distance modulus
        # Check to avoid division by zero or log of zero
        apparent_magnitude = (
            absolute_magnitude - 5 + 5 * np.log10(distance_from_exoplanet)
        )

        apparent_magnitudes.append(apparent_magnitude)

    # Add the new RA, Dec, and apparent magnitudes to the DataFrame
    df_gaia["new_ra"] = new_ra
    df_gaia["new_dec"] = new_dec
    df_gaia["apparent_magnitude"] = apparent_magnitudes

    return df_gaia


def query_magnitude_range(x=10000):
    # Query a region of the sky or specific magnitude range
    query = f"SELECT TOP {x} source_id, ra, dec, parallax, phot_g_mean_mag, bp_rp FROM gaiadr3.gaia_source WHERE phot_g_mean_mag < 15"
    job = Gaia.launch_job(query)
    result = job.get_results()

    # Convert to DataFrame
    df = result.to_pandas()
    return df


def plot_smth(ra_arr, dec_arr, mag_arr, bp_rp_arr):
    # Create a figure
    plt.figure(figsize=(10, 6))

    # Using Mollweide projection for RA/DEC
    ra_rad = np.radians(ra_arr - 180)  # Center the map at RA = 180°
    dec_rad = np.radians(dec_arr)

    # Adjust star sizes with exponential scaling
    size = np.exp(4 - mag_arr)  # Exponential scaling for sizes

    # Use the 'bp_rp' values to map colors of stars (use colormap that transitions from blue to red)
    cmap = plt.get_cmap('coolwarm')  # A colormap going from blue to red
    norm = plt.Normalize(vmin=-5, vmax=7)  # Normalize 'bp_rp' values for color mapping

    # Create the subplot with Mollweide projection
    ax = plt.subplot(111, projection="mollweide")

    # Set the face color of the projection (ellipse region) to deep blue
    ax.set_facecolor('#000033')

    # Plot stars using scatter
    sc = ax.scatter(ra_rad, dec_rad, s=size, c=bp_rp_arr, cmap=cmap, norm=norm, alpha=0.75)

    # Add labels and title
    ax.set_xlabel('Right Ascension (degrees)', color='white')
    ax.set_ylabel('Declination (degrees)', color='white')
    ax.set_title('Star Map from Gaia Data (Mollweide Projection)', color='white')

    # Adjust axis labels and ticks to white to contrast with the dark projection background
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.tick_params(axis='both', colors='white')

    # Show the plot
    plt.show()
    
    return sc

