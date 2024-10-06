import streamlit as st
from exosky.utils import get_exoplanet_data, filter_exoplanets_within_distance
# import plotly.graph_objects as go
# from astropy.coordinates import SkyCoord
# from astropy import units as u


def welcome_user():
    st.write("👋 Welcome to the Exoplanet Explorer!")
    st.write("Please use the sidebar to set the maximum distance from Earth and click the 'Find nearest exoplanets' button to start your search.")
    st.write("You can then select an exoplanet to view its position in the sky and explore the stars around it.")
    st.write("You can also create your own constellations by selecting stars from the list.")
    st.write("Enjoy exploring the universe! 🌌")    
# idea. show the view from earth and info about it. then propose user to viw sky from other exoplanets


# Streamlit app layout
st.title("Explore the Sky from an Exoplanet")


# choose distance from earth layout
st.sidebar.title("Choose your exoplanet 🌌")
st.sidebar.write("Enter max distance from Earth to filter stars")
chosen_distance = st.sidebar.slider("✨ Max Distance (parsecs)", 0, 8500, 10)

distance_chosen = st.sidebar.button("Find nearest exoplanets")

if distance_chosen:
    with st.spinner('Searching for your exoplanets...'):
        if "exoplanet_data" not in st.session_state:
            st.session_state["exoplanet_data"] = get_exoplanet_data()

        exoplanet_data = st.session_state["exoplanet_data"]
        nearest_exoplanets = filter_exoplanets_within_distance(exoplanet_data, chosen_distance)    
  
    st.sidebar.markdown(f"Number of exoplanets within {chosen_distance} parsecs: <span style='color:red'>{len(nearest_exoplanets)}</span>", unsafe_allow_html=True)
    # button view details will show a table dataframe with info about all nearest exoplanets
    if st.sidebar.button("View Details"):
        st.write(nearest_exoplanets.to_csv())
    st.sidebar.write("Select an exoplanet to view its position in the sky and explore the stars around it.")
    selected_exoplanet = st.sidebar.selectbox("Select an Exoplanet", nearest_exoplanets['pl_name'].unique())

    
else:
    welcome_user()

# if st.sidebar.button("View Planets"):
#         selected_exoplanet = st.selectbox("Select an Exoplanet", exoplanet_data['pl_name'].unique())
    
#         exoplanet_info = exoplanet_data[exoplanet_data['pl_name'] == selected_exoplanet].iloc[0]
#         exoplanet_ra = exoplanet_info['ra']
#         exoplanet_dec = exoplanet_info['dec']
#         exoplanet_dist = exoplanet_info['sy_dist']
    
#         st.write(f"Exoplanet: {selected_exoplanet}")
#         st.write(f"RA: {exoplanet_ra}°, Dec: {exoplanet_dec}°, Distance: {exoplanet_dist} parsecs")


# User selection of exoplanet
# selected_exoplanet = st.selectbox(
#     "Select an Exoplanet",
#     exoplanet_data['pl_name'].unique()
# )

# exoplanet_info = exoplanet_data[exoplanet_data['pl_name'] == selected_exoplanet].iloc[0]
# exoplanet_ra = exoplanet_info['ra']
# exoplanet_dec = exoplanet_info['dec']
# exoplanet_dist = exoplanet_info['sy_dist']

# st.write(f"Exoplanet: {selected_exoplanet}")
# st.write(f"RA: {exoplanet_ra}°, Dec: {exoplanet_dec}°, Distance: {exoplanet_dist} parsecs")

# Convert star coordinates relative to the exoplanet
# x, y, z = convert_star_coordinates(exoplanet_ra, exoplanet_dec, exoplanet_dist, star_data)

# # Create a 3D scatter plot for the stars
# fig = go.Figure(data=[go.Scatter3d(
#     x=x,
#     y=y,
#     z=z,
#     mode='markers',
#     marker=dict(
#         size=5,
#         color=star_data['dist'],  # Color by distance
#         colorscale='Viridis',
#         opacity=0.8
#     ),
#     text=star_data['star_name'],  # Hover text
#     hoverinfo='text'
# )])

# # Customize the layout for the 3D plot
# fig.update_layout(
#     scene=dict(
#         xaxis_title='X (parsecs)',
#         yaxis_title='Y (parsecs)',
#         zaxis_title='Z (parsecs)',
#         aspectmode='cube'
#     ),
#     title=f"3D Map of Stars Visible from {selected_exoplanet}",
#     margin=dict(l=0, r=0, b=0, t=40),
# )

# Display the 3D plot
# st.plotly_chart(fig)

# Optional: Constellation creation tool (user selects stars to form constellations)
# selected_stars = st.multiselect("Select Stars", star_data['star_name'])

# # Draw constellation if at least two stars are selected
# if len(selected_stars) > 1:
#     # Filter the selected stars
#     selected_stars_data = star_data[star_data['star_name'].isin(selected_stars)]
    
#     # Convert their coordinates relative to the exoplanet
#     const_x, const_y, const_z = convert_star_coordinates(exoplanet_ra, exoplanet_dec, exoplanet_dist, selected_stars_data)
    
#     # Add lines between the selected stars to form a constellation
#     fig.add_trace(go.Scatter3d(
#         x=const_x,
#         y=const_y,
#         z=const_z,
#         mode='lines',
#         line=dict(color='blue', width=3),
#         name='Constellation',
#         hoverinfo='skip'
#     ))

#     # Update the plot with constellation lines
#     st.plotly_chart(fig)

