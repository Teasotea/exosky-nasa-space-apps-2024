from functools import cached_property
from typing import Optional

import astropy.units as u
import numpy as np
import pandas as pd
from astropy.coordinates import (
    CartesianRepresentation,
    Distance,
    SkyCoord,
    SphericalRepresentation,
)


class ExoplanetService:
    """
    from exosky.service import ExoplanetService
    from exosky.vizualizer import MollweideVizualizer
    from exosky.query import DataLoader


    service = ExoplanetService(DataLoader(), MollweideVizualizer())
    service.plot_exoplanet_projection("Earth")
    service.plot_exoplanet_projection("Kepler-138 c")
    service.get_exoplanets_within_distance(0, 100)
    """

    def __init__(self, data_loader, vizualizer):
        self.data_loader = data_loader
        self.vizualizer = vizualizer

    def plot_exoplanet_projection(self, exoplanet_name: str, grid: bool = True):
        df_gaia = self._stars_df

        if exoplanet_name == "Earth":
            return self.vizualizer.plot(
                df_gaia["ra"].values,
                df_gaia["dec"].values,
                df_gaia["phot_g_mean_mag"].values,
                df_gaia["bp_rp"].values,
                grid,
            )

        exoplanet = self.get_exoplanet(exoplanet_name)
        df_gaia = self.get_exoplanet_projection(df_gaia, exoplanet)
        return self.vizualizer.plot(
            df_gaia["new_ra"].values,
            df_gaia["new_dec"].values,
            df_gaia["apparent_magnitude"].values,
            df_gaia["bp_rp"].values,
            grid,
        )

    def get_exoplanets_within_distance(self, min_distance: Optional[float] = None, max_distance: Optional[float] = None) -> pd.DataFrame:
        df_exoplanets = self._explanet_df
        if min_distance:
            df_exoplanets = df_exoplanets[df_exoplanets["sy_dist"] >= min_distance]
        if max_distance:
            df_exoplanets = df_exoplanets[df_exoplanets["sy_dist"] <= max_distance]
        return df_exoplanets

    def get_exoplanet(self, exoplanet_name: str):
        return self._explanet_df[self._explanet_df["pl_name"] == exoplanet_name].iloc[0]

    def get_exoplanet_projection(self, df_gaia, exoplanet):
        exoplanet_coord = SkyCoord(
            ra=exoplanet["ra"] * u.deg,
            dec=exoplanet["dec"] * u.deg,
            distance=Distance(value=exoplanet["sy_dist"], unit=u.pc),
        )

        star_coord = SkyCoord(
            ra=df_gaia["ra"].values * u.deg,
            dec=df_gaia["dec"].values * u.deg,
            distance=Distance(parallax=df_gaia["parallax"].values * u.mas, allow_negative=True),
        )

        star_relative_position = star_coord.transform_to("icrs").represent_as(CartesianRepresentation) - exoplanet_coord.transform_to(
            "icrs"
        ).represent_as(CartesianRepresentation)
        star_from_exoplanet = star_relative_position.represent_as(SphericalRepresentation)

        # Calculate the translated distance
        new_dist = star_from_exoplanet.distance.to(u.parsec).value

        # Extract new RA and Dec
        new_ra = star_from_exoplanet.lon.deg
        new_dec = star_from_exoplanet.lat.deg
        absolute_magnitude = df_gaia["phot_g_mean_mag"] + 5 - 5 * np.log10(1000 / df_gaia["parallax"])
        apparent_magnitude = absolute_magnitude - 5 + 5 * np.log10(new_dist)

        df_gaia["new_ra"] = new_ra
        df_gaia["new_dec"] = new_dec
        df_gaia["apparent_magnitude"] = apparent_magnitude
        return df_gaia

    @cached_property
    def _explanet_df(self):
        return self.data_loader.load_exoplanet_archive()

    @cached_property
    def _stars_df(self):
        return self.data_loader.load_gaia_stars()
