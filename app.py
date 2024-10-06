import numpy as np
import plotly.graph_objects as go
import streamlit as st

from exosky.query import DataLoader
from exosky.service import ExoplanetService
from exosky.vizualizer import MollweideVizualizer

service = ExoplanetService(DataLoader(), MollweideVizualizer())

if "is_planet_selected" not in st.session_state:
    st.session_state["is_planet_selected"] = [False, ""]
if "is_distance_chosen" not in st.session_state:
    st.session_state["is_distance_chosen"] = [False, None]


# Add "drawing mode" to session state
if "drawing_mode" not in st.session_state:
    st.session_state["drawing_mode"] = False
if "selected_stars" not in st.session_state:
    st.session_state["selected_stars"] = []


def enable_drawing_mode():
    """Enable or disable drawing mode."""
    if st.session_state["drawing_mode"]:
        st.session_state["drawing_mode"] = False
        st.session_state["selected_stars"] = []
    else:
        st.session_state["drawing_mode"] = True


def welcome_user():
    st.write(
        """
👋 **Welcome to the Exoplanet Explorer!**

Please use the sidebar to set the **distance range** from Earth and click the `Find nearest exoplanets` button to start your search.

You can then select an exoplanet and experience the **sky view** from its perspective. 

Enjoy exploring the universe! 🌌
"""
    )
    st.title("Look at the Sky from Earth 🌍 ")
    fig, ax = service.plot_exoplanet_projection("Earth")
    st.pyplot(fig)
    st.write("Do you want to see the sky from other planet`s perspective?")
    st.markdown("Follow this **demo simulation** for that.")
    st.write("**Step 1:** Set the distance range from Earth.")
    st.write("**Step 2:** Select an exoplanet.")
    st.write("**Step 3:** Click the 'View Sky Perspective' button.")
    st.write("**Step 4:** Enjoy the sky view from the exoplanet's perspective.")


# TODO: Fix Buttons

# TODO: show the view from earth and info about it. then propose user to viw sky from other exoplanets

if not st.session_state["is_planet_selected"][0]:
    st.title("Explore the Exoplanets 🪐")


# choose distance from earth layout
st.sidebar.title("Explore exoplanets 🌌")
st.sidebar.write("Choose distance range from Earth to filter exoplanets")

chosen_distance = st.sidebar.slider(
    "✨ Select distance range (from Earth, in parsecs)",
    min_value=0,
    max_value=8500,
    value=(0, 5),
)

distance_chosen = st.sidebar.button("Find nearest exoplanets")

if chosen_distance and not st.session_state["is_distance_chosen"][0]:
    st.sidebar.markdown(
        '<span style="color:blue;">Click the '
        "Find nearest exoplanets"
        " button to apply your changes.</span>",
        unsafe_allow_html=True,
    )

if distance_chosen:
    with st.spinner("Searching for your exoplanets..."):
        nearest_exoplanets = service.get_exoplanets_within_distance(
            chosen_distance[0], chosen_distance[1]
        )
        nearest_exoplanets = nearest_exoplanets.sort_values(by="sy_dist").reset_index(
            drop=True
        )

    st.sidebar.markdown(
        f"Number of exoplanets within {chosen_distance} parsecs: <span style='color:red'>{len(nearest_exoplanets)}</span>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""Here are the <span style='color:red'>{len(nearest_exoplanets)}</span> nearest exoplanets within {chosen_distance}
        parsecs, sorted by distance to Earth:""",
        unsafe_allow_html=True,
    )

    st.markdown(
        "Select an exoplanet in the **sidebar** to explore 🔭  the stars around it."
    )
    st.dataframe(
        nearest_exoplanets[
            ["pl_name", "sy_dist", "ra", "dec", "pl_orbsmax", "st_mass", "st_rad"]
        ]
    )

    st.markdown(
        """
    **Explanation of Columns:**
    - `pl_name`: Name of the exoplanet.
    - `sy_dist`: Distance to the exoplanet from Earth in parsecs.
    - `ra`: Right Ascension of the exoplanet in the sky.
    - `dec`: Declination of the exoplanet in the sky.
    - `pl_orbsmax`: Semi-major axis of the exoplanet's orbit in AU.
    - `st_mass`: Mass of the host star in solar masses.
    - `st_rad`: Radius of the host star in solar radii.
    """
    )

    st.session_state["is_distance_chosen"] = [True, nearest_exoplanets]

st.sidebar.title("Choose your exoplanet 🌠")

if not st.session_state["is_distance_chosen"][0]:
    st.sidebar.markdown(
        '<span style="color:red;">Please complete all steps above to view sky perspective from exoplanet.</span>',
        unsafe_allow_html=True,
    )
elif (
    st.session_state["is_distance_chosen"][0]
    and not st.session_state["is_planet_selected"][0]
):
    st.sidebar.markdown(
        '<span style="color:blue;">Select an exoplanet to view the sky perspective.</span>',
        unsafe_allow_html=True,
    )

if st.session_state["is_distance_chosen"][0]:
    selected_exoplanet = st.sidebar.selectbox(
        "Select an Exoplanet",
        st.session_state["is_distance_chosen"][1]["pl_name"].unique(),
    )
    is_view_sky = st.sidebar.button("View Sky Perspective")
else:
    selected_exoplanet = None
    is_view_sky = None

if st.session_state["is_distance_chosen"][0] and not is_view_sky:
    st.sidebar.markdown(
        '<span style="color:blue;">Click the '
        "View Sky Perspective"
        " button to apply your changes.</span>",
        unsafe_allow_html=True,
    )
elif st.session_state["is_planet_selected"][0]:
    st.sidebar.markdown(
        """<span style="color:green;">Sky perspective is being displayed. If you want to change the exoplanet, 
        choose it again from dropdown and click the button `View Sky Perspective`.</span>""",
        unsafe_allow_html=True,
    )

if is_view_sky:
    print(selected_exoplanet)
    st.session_state["is_planet_selected"] = [True, selected_exoplanet]

if st.session_state["is_planet_selected"][0]:
    st.write(
        f"💫 **Sky Perspective from Exoplanet {st.session_state['is_planet_selected'][1]}**"
    )
    fig, ax = service.plot_exoplanet_projection(
        st.session_state["is_planet_selected"][1]
    )
    st.pyplot(fig)


if not distance_chosen and not st.session_state["is_planet_selected"][0]:
    print(distance_chosen, st.session_state["is_planet_selected"][0])
    welcome_user()

# Drawing Mode --------------------------------------------------------------------------------

# Button to toggle drawing mode
if st.session_state["is_planet_selected"][0] and not st.session_state["drawing_mode"]:
    st.button("Enable Drawing Mode", on_click=enable_drawing_mode)

if st.session_state["drawing_mode"]:
    st.markdown(
        '<span style="color:blue;">**Drawing Mode Enabled**: Click on stars to create constellations</span>',
        unsafe_allow_html=True,
    )

# --------------------------------------------------------------------------------
# Simulating star positions for example purposes (replace this with real star data)

# Simulated star data (replace with real star data from your app)


def calculate_star_sizes(df, magnitude_threshold=-7):
    mag_arr = df["apparent_magnitude"].to_numpy()
    bright_stars = mag_arr < magnitude_threshold
    sun = mag_arr < -7
    filtered_mag_arr = mag_arr[bright_stars & ~sun]
    size = np.exp(4 - filtered_mag_arr)  # Exponential scaling
    size = np.clip(size, 0, 100)  # Clipping sizes to a maximum of 100
    df["s"] = np.nan
    df.loc[bright_stars & ~sun, "s"] = size
    return df


st.title("Create Your Constellation 🌟")
if st.session_state["is_planet_selected"][1] != "":
    stars = service.get_exoplanet_projection(st.session_state["is_planet_selected"][1])
    stars = stars.dropna(subset=["new_ra", "new_dec", "apparent_magnitude"])
    stars = stars.nsmallest(100, "apparent_magnitude")
    stars = stars[["SOURCE_ID", "new_ra", "new_dec", "apparent_magnitude"]]
    calculate_star_sizes(stars)
    stars = stars.reset_index(drop=True)
    st.dataframe(stars)

# Initialize session state for drawing
if "selected_stars" not in st.session_state:
    st.session_state["selected_stars"] = []


# def plot_star_chart(df, selected_stars):
#     """Plot the star chart and handle drawing mode."""
#     fig = go.Figure()

#     # Plot stars as scatter plot based on real exoplanet data
#     fig.add_trace(
#         go.Scatter(
#             x=df["new_ra"],  # Right Ascension
#             y=df["new_dec"],  # Declination
#             mode="markers",
#             marker=dict(size=10, color="yellow"),
#             text=df["SOURCE_ID"],  # Exoplanet names
#             name="Stars",
#         )
#     )

#     # Draw lines between selected stars
#     if len(selected_stars) > 1:
#         for i in range(len(selected_stars) - 1):
#             star1 = df[df["SOURCE_ID"] == selected_stars[i]].iloc[0]
#             star2 = df[df["SOURCE_ID"] == selected_stars[i + 1]].iloc[0]
#             fig.add_trace(
#                 go.Scatter(
#                     x=[star1["new_ra"], star2["new_ra"]],
#                     y=[star1["new_dec"], star2["new_dec"]],
#                     mode="lines",
#                     line=dict(color="blue", width=2),
#                     name="Constellation",
#                 )
#             )

#     fig.update_layout(
#         xaxis_title="Right Ascension",
#         yaxis_title="Declination",
#         title="Exoplanet Star Chart",
#     )
#     return fig


def plot_star_chart(df, selected_stars):
    """Plot the star chart and handle drawing mode."""
    fig = go.Figure()

    # Plot stars as scatter plot based on real exoplanet data
    fig.add_trace(
        go.Scatter(
            x=df["new_ra"],  # Right Ascension
            y=df["new_dec"],  # Declination
            mode="markers",
            marker=dict(size=df["s"], color="white"),  # Size depends on 's' column
            text=df["source_id"],  # Exoplanet names
            name="Stars",
        )
    )

    # Draw lines between selected stars
    if len(selected_stars) > 1:
        for i in range(len(selected_stars) - 1):
            star1 = df[df["source_id"] == selected_stars[i]].iloc[0]
            star2 = df[df["source_id"] == selected_stars[i + 1]].iloc[0]
            fig.add_trace(
                go.Scatter(
                    x=[star1["new_ra"], star2["new_ra"]],
                    y=[star1["new_dec"], star2["new_dec"]],
                    mode="lines",
                    line=dict(color="yellow", width=2),  # Connection lines in yellow
                    name="Constellation",
                )
            )

    # Update layout for the figure
    fig.update_layout(
        xaxis_title="Right Ascension",
        yaxis_title="Declination",
        title="Exoplanet Star Chart",
        plot_bgcolor="darkblue",  # Dark blue background
        paper_bgcolor="darkblue",  # Dark blue for the paper background
        font=dict(color="white"),  # White font color for titles and labels
        showlegend=True,  # Show legend
    )

    # Set x and y axis properties for better visibility
    fig.update_xaxes(
        showgrid=True, gridcolor="gray", zerolinecolor="gray"
    )  # Optional: add gridlines for clarity
    fig.update_yaxes(
        showgrid=True, gridcolor="gray", zerolinecolor="gray"
    )  # Optional: add gridlines for clarity

    return fig


# Sidebar to select stars
st.sidebar.title("Create Your Constellation")
st.write(
    "Here you can see 100 most bright stars from the exoplanet perspective. You can create constellations from them."
)
if not st.session_state["drawing_mode"]:
    st.sidebar.markdown(
        '<span style="color:red;">Please enable draw mode to create your constellation.</span>',
        unsafe_allow_html=True,
    )

# Dropdown to select stars from the exoplanet DataFrame
selected_star = st.sidebar.selectbox(
    "Select a star (exoplanet) to add to the constellation:", stars["SOURCE_ID"]
)

# Add selected star to the list of stars if the "Add" button is clicked
if st.sidebar.button("Add Star"):
    if selected_star not in st.session_state["selected_stars"]:
        st.session_state["selected_stars"].append(selected_star)

# Display the list of selected stars in the sidebar
st.sidebar.write("Selected stars for the constellation:")
st.sidebar.write(st.session_state["selected_stars"])

# Option to clear the constellation
if st.sidebar.button("Clear Constellation"):
    st.session_state["selected_stars"] = []

# Plot the star chart with the selected stars and drawn lines
st.plotly_chart(plot_star_chart(stars, st.session_state["selected_stars"]))
