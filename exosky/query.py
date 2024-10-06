import pathlib

import pandas as pd
from astroquery.gaia import Gaia
from astroquery.nasa_exoplanet_archive import NasaExoplanetArchive


class DataLoader:

    def load_exoplanet_archive(self) -> pd.DataFrame:
        cache_path = pathlib.Path("tmp/exoplanet_archive_cache")
        if not cache_path.exists():
            cache_path.parent.mkdir(parents=True, exist_ok=True)

            # https://exoplanetarchive.ipac.caltech.edu/docs/API_PS_columns.html
            exoplanets = NasaExoplanetArchive.query_criteria(
                table="PSCompPars",  # The new Planetary Systems (PS) table
                select="pl_name, ra, dec, sy_dist, pl_orbincl, pl_orbsmax, st_mass, st_rad",
                where="sy_dist IS NOT NULL",
                cache=True,
            )
            df_exoplanets = exoplanets.to_pandas()
            df_exoplanets.to_pickle(cache_path)
        else:
            df_exoplanets = pd.read_pickle(cache_path)

        return df_exoplanets

    def load_gaia_stars(self, number: int = 100000) -> pd.DataFrame:
        cache_path = pathlib.Path("tmp/gaia_cache")
        if not cache_path.exists():

            cache_path.parent.mkdir(parents=True, exist_ok=True)

            job = Gaia.launch_job(
                f"""SELECT TOP {number}
                source_id, ra, dec, parallax, phot_g_mean_mag, bp_rp
                FROM gaiadr3.gaia_source
                WHERE phot_g_mean_mag < 15
                """
            )
            result = job.get_results()
            df = result.to_pandas()
            df.to_pickle(cache_path)
        else:
            df = pd.read_pickle(cache_path)

        return df
