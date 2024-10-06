import pathlib

import pandas as pd
from astroquery.gaia import Gaia
from astroquery.nasa_exoplanet_archive import NasaExoplanetArchive
from astroquery.simbad import Simbad


class DataLoader:

    def load_exoplanet_archive(self) -> pd.DataFrame:
        cache_path = pathlib.Path("tmp/exoplanet_archive_cache")
        if not cache_path.exists():
            cache_path.parent.mkdir(parents=True, exist_ok=True)

            # https://exoplanetarchive.ipac.caltech.edu/docs/API_PS_columns.html
            exoplanets = NasaExoplanetArchive.query_criteria(
                table="PSCompPars",  # The new Planetary Systems (PS) table
                select="pl_name, sy_dist, ra, dec, pl_orbsmax, st_mass, st_rad",
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

            # Add a 'name' column with default values as source_id
            df["name"] = df["SOURCE_ID"].astype(str)

            # Attempt to match with SIMBAD names
            # df["name"] = df["SOURCE_ID"].apply(lambda x: self.match_star_name(str(x)))

            df.to_pickle(cache_path)
        else:
            df = pd.read_pickle(cache_path)

        return df

    # def match_star_name(self, gaia_source_id: str) -> str:
    #     try:
    #         simbad_query = Simbad.query_object(f"Gaia DR3 {gaia_source_id}")
    #         if simbad_query is not None and "MAIN_ID" in simbad_query.colnames:
    #             return simbad_query["MAIN_ID"][
    #                 0
    #             ]  # Return the main ID (common star name)
    #     except Exception as e:
    #         # Handle any issues like network failures or parsing problems
    #         print(f"Error querying SIMBAD for Gaia DR3 {gaia_source_id}: {e}")

    #     # If no name found, return the Gaia source_id
    #     return gaia_source_id
