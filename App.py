import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import os

# Load CSS file
css_file_path = os.path.join(os.path.dirname(__file__), 'styles.css')
if os.path.exists(css_file_path):
    with open(css_file_path) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
else:
    st.error("CSS file not found.")

# Load your dataset
data_url = 'https://raw.githubusercontent.com/zulianizulkoffli/Soil_Studies_Peninsular_Malaysia/main/Data_For_Viz.csv'
data = pd.read_csv(data_url, delimiter=',', encoding='utf-8')

# Correcting the column names
data.columns = data.columns.str.strip()

# Extract necessary columns for the final output
required_columns = ['Location', 'Latitude', 'Longitude', 'Depth (m)', 'Clay (%)', 'Silt (%)', 'Sand (%)', 'Gravels (%)', 'D10', 'D30', 'D60', 'CU', 'CC', '1D inverted resistivity', 'Moisture content (%)', 'pH', 'Soil Type', 'Fine Soil (%)', 'Sand (%)', 'USCS Group Symbol', 'Description', 'Photo Location']

# Check if the required columns exist in the dataset
missing_columns = [col for col in required_columns if col not in data.columns]
if missing_columns:
    st.error(f"Missing columns in the dataset: {missing_columns}")
else:
    filtered_data = data[required_columns]

    # Streamlit app
    st.markdown("<style>h1{margin-top: 0px !important;}</style>", unsafe_allow_html=True)
    st.title("Data Visualization for Soil Classification in Peninsular Malaysia")

    # Adjust layout width
    st.markdown("""
        <style>
        .main .block-container {
            max-width: 80%;
            padding: 1rem;
        }
        .sidebar .sidebar-content {
            background-color: #D0EFFF;
        }
        .table-container {
            width: 50%;
            margin: 0 auto;
            padding: 1rem;
            border-radius: 5px;
            background-color: white;
        }
        .table-content {
            width: 100%;
        }
        .dataframe th, .dataframe td {
            text-align: left;
            padding: 10px;
            font-size: 1.25em;
            font-weight: bold;
        }
        .dataframe.table-no-border th, .dataframe.table-no-border td {
            border: none;
        }
        .dataframe th {
            width: 30%;
        }
        .dataframe td {
            width: 70%;
        }
        .no-input-box {
            display: none;
        }
        .sidebar .sidebar-content .stMarkdown, .sidebar .sidebar-content .stSelectbox {
            font-size: 2em; /* 2 times bigger font size */
        }
        </style>
        """, unsafe_allow_html=True)

    # Initialize session state
    if "location" not in st.session_state:
        st.session_state.location = None
    if "soil_type" not in st.session_state:
        st.session_state.soil_type = None

    # Add a large "Filter Options" title
    st.sidebar.markdown("<div class='filter-options'></div>", unsafe_allow_html=True)
    st.sidebar.markdown(f"""
        <div style='width: 100%; font-size: 2.5em; text-align: justify; padding: 10px; border: bold: none;'>
        {'FILTER OPTIONS'}
        </div>
        """, unsafe_allow_html=True)

    # Location selection
    location_filter = st.sidebar.selectbox("Select Location(s)", ["UTP Perak"] + list(data['Location'].unique()))

    # Filter data based on location selection
    if location_filter:
        st.session_state.location = location_filter
        st.session_state.soil_type = None

    if st.session_state.location:
        filtered_data = data[data['Location'] == st.session_state.location]
        location_info = filtered_data.iloc[0]

        # Display soil type name and other parameters
        st.sidebar.markdown(f"### Soil Type: {location_info['Soil Type']}")
        st.sidebar.markdown(f"### Fine Soil (%): {location_info['Fine Soil (%)']}")
        st.sidebar.markdown(f"### Sand (%): {location_info['Sand (%)']}")
        st.sidebar.markdown(f"### USCS Group Symbol: {location_info['USCS Group Symbol']}")

        # Soil type filter
        st.sidebar.markdown("<br>", unsafe_allow_html=True)
        soil_type_filter = st.sidebar.selectbox("Select Soil Type(s)", [""] + list(data['Soil Type'].unique()), index=0)
        if soil_type_filter:
            st.session_state.soil_type = soil_type_filter
            st.session_state.location = None

        # Display the location name based on soil type selection
        if st.session_state.soil_type:
            filtered_data_by_soil = data[data['Soil Type'] == st.session_state.soil_type]
            st.sidebar.markdown(f"### Locations with {st.session_state.soil_type}:")
            for location in filtered_data_by_soil['Location'].unique():
                st.sidebar.markdown(f"- {location}")

        # Create a folium map centered around UTP Perak
        default_latitude = 4.3828345
        default_longitude = 100.97182
        m = folium.Map(location=[default_latitude, default_longitude], zoom_start=6)

        # Add data points to the map with detailed popups
        for idx, row in filtered_data.iterrows():
            popup_text = (
                f"Location: {row['Location']}<br>"
                f"Soil Type: {row['Soil Type']}<br>"
                f"Fine Soil (%): {row['Fine Soil (%)']}<br>"
                f"Sand (%): {row['Sand (%)']}<br>"
                f"USCS Group Symbol: {row['USCS Group Symbol']}"
            )
            folium.Marker(
                location=[row['Latitude'], row['Longitude']],
                popup=popup_text,
            ).add_to(m)

        # Display the map in Streamlit with centered position
        st.markdown("<div style='display: flex; justify-content: center;'>", unsafe_allow_html=True)
        folium_static(m)
        st.markdown("</div>", unsafe_allow_html=True)

        # Add gap between table and research findings
        st.markdown("<div style='margin-top: 1cm;'></div>", unsafe_allow_html=True)

        # Research introduction elaboration
        st.write("### Preface:")

        # Research elaboration with citations
        st.markdown(f"""
            <div style='width: 80%; font-size: 1.2em; text-align: justify; padding: 10px; border: none;'>
            {location_info['Research Findings']}
            </div>
            """, unsafe_allow_html=True)

        # Add gap between table and research findings
        st.markdown("<div style='margin-top: 2cm;'></div>", unsafe_allow_html=True)

        # Add location information
        st.write(f"### Location Information for {location_filter}")
        st.markdown(f"""
            <div style='width: 80%; font-size: 1.2em; text-align: justify; padding: 10px; border: none;'>
            {location_info['Trivia']}
            </div>
            """, unsafe_allow_html=True)

        # Add location image
        st.markdown("<div style='margin-top: 1.5cm;'>", unsafe_allow_html=True)
        st.image(location_info['Photo Location'], caption=location_filter)

        # Transform and display the filtered dataframe in a vertical format
        st.write("## Filtered Dataset with USCS Classification")
        st.markdown("<div style='margin-top: 1cm;'></div>", unsafe_allow_html=True)
        st.markdown(f"""
              <table class="dataframe table-no-border">
            <tbody>
            <tr><th>Location</th><td>{location_info['Location']}</td></tr>
            <tr><th>Latitude</th><td>{location_info['Latitude']}</td></tr>
            <tr><th>Longitude</th><td>{location_info['Longitude']}</td></tr>
            <tr><th>Depth (m)</th><td>{location_info['Depth (m)']}</td></tr>
            <tr><th>Clay (%)</th><td>{location_info['Clay (%)']}</td></tr>
            <tr><th>Silt (%)</th><td>{location_info['Silt (%)']}</td></tr>
            <tr><th>Sand (%)</th><td>{location_info['Sand (%)']}</td></tr>
            <tr><th>Gravels (%)</th><td>{location_info['Gravels (%)']}</td></tr>
            <tr><th>D10</th><td>{location_info['D10']}</td></tr>
            <tr><th>D30</th><td>{location_info['D30']}</td></tr>
            <tr><th>D60</th><td>{location_info['D60']}</td></tr>
            <tr><th>CU</th><td>{location_info['CU']}</td></tr>
            <tr><th>CC</th><td>{location_info['CC']}</td></tr>
            <tr><th>1D inverted resistivity</th><td>{location_info['1D inverted resistivity']}</td></tr>
            <tr><th>Moisture content (%)</th><td>{location_info['Moisture content (%)']}</td></tr>
            <tr><th>pH</th><td>{location_info['pH']}</td></tr>
            <tr><th>Soil Type</th><td>{location_info['Soil Type']}</td></tr>
            <tr><th>Fine Soil (%)</th><td>{location_info['Fine Soil (%)']}</td></tr>
            <tr><th>Sand (%)</th><td>{location_info['Sand (%)']}</td></tr>
            <tr><th>USCS Group Symbol</th><td>{location_info['USCS Group Symbol']}</td></tr>
            </tbody>
            </table>
            """, unsafe_allow_html=True)
            
            

        # Add gap between table and research findings
        st.markdown("<div style='margin-top: 2cm;'></div>", unsafe_allow_html=True)

        # Explanation and research findings
        st.write(f"### Soil Type for {location_filter} : {location_info['Soil Type']}")

        # Add gap between table and research findings
        st.markdown("<div style='margin-top: 0.5cm;'></div>", unsafe_allow_html=True)

        # Display the description directly from the dataset
        st.markdown(f"""
            <div style='width: 80%; font-size: 1.2em; text-align: justify; padding: 10px; border: none;'>
            {location_info['Description']}
            </div>
            """, unsafe_allow_html=True)

        # Add gaps
        st.markdown("<div style='margin-top: 0.5cm;'></div>", unsafe_allow_html=True)
        
            
  # Title of the app
st.markdown(f"""  
    <div style='width: 80%; font-size: 1.2em; text-align: justify; padding: 10px; border: none;'>  
    <b>Soil Texture Classification</b>
    </div>
    """, unsafe_allow_html=True)

# Introduction
st.markdown(f"""  
    <div style='width: 80%; font-size: 1.2em; text-align: justify; padding: 10px; border: none;'>  
    The USDA system classifies soil into 12 primary texture classes based on the percentages of sand, silt, and clay. These texture classes are a standard for understanding and communicating soil composition. Here are the different texture classes:
    </div>
    """, unsafe_allow_html=True)

# Soil texture classes
soil_classes = {
    "<b>Sand</b>": "Contains 85-100% sand, and the percentage of silt plus 1.5 times the percentage of clay is not more than 15.<br>",
    "<b>Loamy Sand</b>": "Contains 70-90% sand, and the percentage of silt plus twice the percentage of clay is 15-30.<br>",
    "<b>Sandy Loam</b>": "Contains less than 30% clay, 50-70% sand, and the remainder is silt.<br>",
    "<b>Loam</b>": "Contains 7-27% clay, less than 52% sand, and 28-50% silt.<br>",
    "<b>Silt Loam</b>": "Contains 50-88% silt, 12-27% clay, and less than 20% sand.<br>",
    "<b>Silt</b>": "Contains 80% or more silt and less than 12% clay.<br>",
    "<b>Sandy Clay Loam</b>": "Contains 20-35% clay, less than 28% silt, and more than 45% sand.<br>",
    "<b>Clay Loam</b>": "Contains 27-40% clay, 20-45% sand, and the remainder is silt.<br>",
    "<b>Silty Clay Loam</b>": "Contains 27-40% clay and 40-73% silt.<br>",
    "<b>Sandy Clay</b>": "Contains 35% or more clay and 45% or more sand.<br>",
    "<b>Silty Clay</b>": "Contains 40% or more clay and 40% or more silt.<br>",
    "<b>Clay</b>": "Contains 40% or more clay, less than 45% sand, and less than 40% silt.<br><br>"
}

# Displaying the soil classes
for texture, description in soil_classes.items():
    st.markdown(f"<div style='width: 80%; font-size: 1.2em; text-align: justify; padding: 10px; border: none;'>{texture}: {description}</div>", unsafe_allow_html=True)


# Soil Texture Triangle
st.markdown(f"""  
<div style='width: 80%; font-size: 1.2em; text-align: justify; padding: 10px; border: none;'>  
<b>Using the Soil Texture Triangle</b><br><br>
- The Soil Texture Triangle is a tool used to classify the texture class of a soil based on its sand, silt, and clay percentages.<br><br>
- The triangle is divided into various zones, each representing a different texture class.<br><br>
- To classify a soil, plot the percentage of sand on the horizontal axis, the percentage of clay on the left vertical axis, and the percentage of silt on the right vertical axis. The intersection of these three lines indicates the soil's texture class.<br><br>
</div>
""", unsafe_allow_html=True)

# Implications of Soil Texture
st.markdown(f"""  
<div style='width: 80%; font-size: 1.2em; text-align: justify; padding: 10px; border: none;'>  
<b>Implications of Soil Texture</b><br><br>
- <b>Water Holding Capacity:</b> Clay soils have high water-holding capacity, while sandy soils have low. This affects the soil’s ability to support plant growth.<br><br>
- <b>Aeration and Drainage:</b> Sandy soils are well-aerated and well-drained, whereas clay soils may suffer from poor drainage and aeration, affecting root development.<br><br>
- <b>Nutrient Availability:</b> Clay and silt soils are better at holding nutrients than sandy soils, influencing fertilizer management practices.<br><br>
- <b>Workability:</b> Sandy soils are easier to cultivate than clay soils, which can be hard and cloddy when dry and sticky when wet.<br><br>
- <b>Erosion Risk:</b> Sandy soils are more prone to erosion than clay or silt soils, impacting land management strategies.<br><br>
</div>
""", unsafe_allow_html=True)



# Embedding the image and centering the text with slight adjustment to the left
st.markdown(f"""  
    <div style='width: 80%; text-align: center; padding: 10px; border: none;'>  
    <h3>Soil Texture Triangle Image</h3>
    <img src="https://raw.githubusercontent.com/zulianizulkoffli/Soil_Studies_Peninsular_Malaysia/main/Texture_Triangle_USDA.jpg" alt="USDA Soil Texture Triangle" style='max-width: 70%; height: auto;'>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown(f"""  
    <div style='width: 80%;text-align: center; font-size: 1.2em; text-align: justify; padding: 10px; border: none;'>  
    ---
    This image provides a quick reference to the USDA soil texture classification system.
    </div>
    """, unsafe_allow_html=True)


# Add gap 
st.markdown("<div style='margin-top: 0.5cm;'></div>", unsafe_allow_html=True)

# Display the disclaimer directly from the dataset
st.markdown(f"""  
<div style='width: 80%; font-size: 1.2em; text-align: justify; padding: 10px; border: none;'>DISCLAIMER NOTE: 
{location_info['Disclaimer']}
</div>
""", unsafe_allow_html=True)

# Add gap between table and research findings
st.markdown("<div style='margin-top: 5cm;'></div>", unsafe_allow_html=True)
