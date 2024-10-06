## HIGH-LEVEL SUMMARY
Our project aims to bring a unique perspective to stargazing by allowing users to visualize the star sky from the view point of various exoplanets. Using data from the GAIA DR3 dataset and the NASA Exoplanet Archive, we've developed a Python web application that reprojects stars’ positions and characteristics based on an exoplanet's location.


## PROJECT DEMO
N/A
## FINAL PROJECT
N/A
## PROJECT DETAILS

**Features**

Our application features a set of tools for building the star sky vizualization in form of 2D plot:
1. **Dynamic Sky Projection**: Visualizes the star sky from either Earth or an exoplanet's perspective, with a choice between Mollweide or Mercator projections.
2. **Exoplanet Filtering**: Filters the list of exoplanets by their distance from the Solar System, helping users focus on planets within a specific range.
3. **Earth's Position Indicator**: Shows the Earth's location when viewing the star sky from other exoplanets.
4. **Interactive Constellation Drawing**: Allows users to map constellations interactively on the star sky.

**Technical details**
We primarily utilize the following data sources and columns:
- **GAIA DR3 Dataset**: Includes *right ascension (ra)*, *declination (dec)*, *parallax* (for distance calculations), *phot_g_mean_mag* (used to set star sizes, as a proxy value to vizualize brightness), and *bp_rp* (used to infer star color).
- **NASA Exoplanet Archive**: Provides *right ascension (ra)*, *declination (dec)*, and *sy_dist* (distance from the Solar System), allowing us to have an observation points to choose from, and to reposition GAIA data relative to an exoplanet’s coordinates.


Through this project, we tackled a range of challenges and complexities:
1. **Data Integration and Unit Conversion**: Integrated datasets with different measurement units and formats to provide a seamless visualization.
2. **Astronomical Geometry Computation**: Calculated the relative positions using coordinate transformations and apparent magnitudes of stars when viewed from exoplanets, handling complex astronomical geometry, and conversion between different coordinate systems.
2. **Outlier Management**: Addressed plot-distorting outliers, such as stars from the host system of the exoplanet itself, which could skew visual clarity.
3. **Aesthetic and Realistic Plotting**: Mapped magnitude and color values realistically to create visually appealing yet preserve properties representations based on the actual data.

**Future Enhancements**

To elevate the user experience and scientific accuracy, the next steps will be to introduce additional features:
1. **Enhanced Interactivity**: Enable users to zoom in on specific sky regions for detailed views.
2. **Atmospheric Effects**: Incorporate atmospheric properties of the selected planet, adjusting visual effects to simulate local conditions.
3. **Extended Accuracy for Distant Objects**: Refine star data for exoplanets located at far distances.
4. **3D Model Visualization**: Offer a 3D view mode for an immersive spatial understanding of star fields.


## USE OF ARTIFICIAL INTELLIGENCE

We used ChatGPT & Github copilot for development acceleration

## SPACE AGENCY DATA

- [NASA Exoplanet Archive Planetary Systems Composite Data (through astroquery)](https://exoplanetarchive.ipac.caltech.edu/cgi-bin/TblView/nph-tblView?app=ExoTbls&config=PSCompPars)
- [GAIA Data Release 3 (through astroquery)](https://www.cosmos.esa.int/web/gaia/data-release-3)


## REFERENCES

Python libraries used for development:
- https://astroquery.readthedocs.io/en/latest/ - handy wrapper for access to the datasets
- https://www.astropy.org/ - for ease of the astronomical math
- https://matplotlib.org/ - visualization engine
- https://streamlit.io/ - web-app engine

Other resources:
- https://viyaleta.medium.com/how-to-make-a-sky-map-in-python-a362bf722bb2
- https://astronomy.stackexchange.com/questions/54280/how-to-get-star-position-from-the-gaia-data-set
- https://www.omnicalculator.com/physics/luminosity
