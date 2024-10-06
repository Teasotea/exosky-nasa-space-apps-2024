import streamlit as st

from exosky.query import DataLoader
from exosky.service import ExoplanetService
from exosky.vizualizer import MollweideVizualizer

service = ExoplanetService(DataLoader(), MollweideVizualizer())

if "is_planet_selected" not in st.session_state:
    st.session_state["is_planet_selected"] = [False, ""]
if "is_distance_chosen" not in st.session_state:
    st.session_state["is_distance_chosen"] = [False, None]


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
    st.title("Explore the Sky from an Exoplanet")


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
        '<span style="color:blue;">Click the ' "Find nearest exoplanets" " button to apply your changes.</span>",
        unsafe_allow_html=True,
    )

if distance_chosen:
    with st.spinner("Searching for your exoplanets..."):
        nearest_exoplanets = service.get_exoplanets_within_distance(chosen_distance[0], chosen_distance[1])
        nearest_exoplanets = nearest_exoplanets.sort_values(by="sy_dist").reset_index(drop=True)

    st.sidebar.markdown(
        f"Number of exoplanets within {chosen_distance} parsecs: <span style='color:red'>{len(nearest_exoplanets)}</span>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""Here are the <span style='color:red'>{len(nearest_exoplanets)}</span> nearest exoplanets within {chosen_distance}
        parsecs, sorted by distance to Earth:""",
        unsafe_allow_html=True,
    )

    st.markdown("Select an exoplanet in the **sidebar** to explore 🔭  the stars around it.")
    st.dataframe(nearest_exoplanets[["pl_name", "sy_dist", "ra", "dec", "pl_orbsmax", "st_mass", "st_rad"]])

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
elif st.session_state["is_distance_chosen"][0] and not st.session_state["is_planet_selected"][0]:
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
        '<span style="color:blue;">Click the ' "View Sky Perspective" " button to apply your changes.</span>",
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
    st.write(f"💫 **Sky Perspective from Exoplanet {st.session_state['is_planet_selected'][1]}**")
    fig, ax = service.plot_exoplanet_projection(st.session_state["is_planet_selected"][1])
    st.pyplot(fig)


if not distance_chosen and not st.session_state["is_planet_selected"][0]:
    print(distance_chosen, st.session_state["is_planet_selected"][0])
    welcome_user()
