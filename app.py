import plotly.io as pio
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
    grid = st.checkbox("Show grid", value=True)
    mollwide = st.checkbox("Mollwide", value=False)
    fig, _ = service.plot_exoplanet_projection("Earth", grid=grid, mollweide=mollwide)
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
    st.title(
        f"💫 **Sky Perspective from Exoplanet {st.session_state['is_planet_selected'][1]}**"
    )
    grid = st.checkbox("Show grid", value=True)
    mollwide = st.checkbox("Mollwide", value=False)
    if not mollwide:
        show_earth = st.checkbox("Show Earth", value=True)
    else:
        show_earth = False
    fig, _ = service.plot_exoplanet_projection(
        st.session_state["is_planet_selected"][1],
        grid=grid,
        mollweide=mollwide,
        display_earth=show_earth,
    )
    st.pyplot(fig)


if not distance_chosen and not st.session_state["is_planet_selected"][0]:
    print(distance_chosen, st.session_state["is_planet_selected"][0])
    welcome_user()

# Drawing Mode --------------------------------------------------------------------------------


st.sidebar.title("Create Your Constellation")
if not st.session_state["drawing_mode"]:
    st.sidebar.markdown(
        '<span style="color:red;">Please enable draw mode to create your constellation.</span>',
        unsafe_allow_html=True,
    )

if st.session_state["is_planet_selected"][0] and not st.session_state["drawing_mode"]:
    st.sidebar.button("Enable Drawing Mode", on_click=enable_drawing_mode)

if st.session_state["is_planet_selected"][0] and st.session_state["drawing_mode"]:
    st.sidebar.markdown(
        '<span style="color:blue;">Here you can choose the brightest stars from the exoplanet perspective and create constellations from them.</span>',
        unsafe_allow_html=True,
    )
    st.title("Create Your Constellation 🌟")

    n = st.sidebar.number_input(
        "Enter N — number of brightest stars to display (recommended: 10 to 1000):",
        min_value=0,
        max_value=10000,
        value=100,
    )
    # n = st.sidebar.slider(
    #     "Enter N — number of brightest stars to display (from 5 to 10000):",
    #     min_value=5,
    #     max_value=10000,
    #     value=100,
    # )

    stars = service.get_exoplanet_projection(st.session_state["is_planet_selected"][1])
    stars = stars.dropna(subset=["new_ra", "new_dec", "apparent_magnitude"])
    stars = stars.nsmallest(n, "apparent_magnitude")
    stars = stars[["name", "new_ra", "new_dec", "apparent_magnitude"]]
    stars["s"] = stars["apparent_magnitude"].apply(lambda x: 35 * 10 ** (x / -2.5))
    stars = stars.reset_index(drop=True)
    # st.dataframe(stars)

    selected_star = st.sidebar.selectbox(
        "Select a star (exoplanet) to add to the constellation:", stars["name"]
    )

    add_star = st.sidebar.button("Add Star")
    if add_star and selected_star not in st.session_state["selected_stars"]:
        st.session_state["selected_stars"].append(selected_star)
        add_star = None

    st.sidebar.write("Selected stars for the constellation:")
    st.sidebar.write(st.session_state["selected_stars"])

    is_clear = st.sidebar.button("Clear Constellation")
    if is_clear:
        st.session_state["selected_stars"] = []
        is_clear = None

    fig = service.plot_star_chart(stars, st.session_state["selected_stars"])
    st.plotly_chart(fig)

    const_name = st.sidebar.text_input("Like your constellation? Give it a name:")

    if const_name:
        st.sidebar.write(f"Do you want to save it as: {const_name}.png ?")

        if st.sidebar.button("Save"):
            # pio.write_image(fig, f"{const_name}.png")
            st.success(f"Plot saved as {const_name}.png")


if st.session_state["drawing_mode"]:
    st.sidebar.button("Disable Drawing Mode", on_click=enable_drawing_mode)
