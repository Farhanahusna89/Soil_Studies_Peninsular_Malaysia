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
            <div style='width: 80%; font-size: 1.5em; text-align: justify; padding: 10px; border: none;'>
            {location_info['Research Findings']}
            </div>
            """, unsafe_allow_html=True)

        # Add gap between table and research findings
        st.markdown("<div style='margin-top: 2cm;'></div>", unsafe_allow_html=True)

        # Add location information
        st.write(f"### Location Information for {location_filter}")
        st.markdown(f"""
            <div style='width: 80%; font-size: 1.5em; text-align: justify; padding: 10px; border: none;'>
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
            <div style='width: 80%; font-size: 1.5em; text-align: justify; padding: 10px; border: none;'>
            {location_info['Description']}
            </div>
            """, unsafe_allow_html=True)

        # Add gaps
        st.markdown("<div style='margin-top: 0.5cm;'></div>", unsafe_allow_html=True)
        
        
        # Add gap 
        st.markdown("<div style='margin-top: 0.5cm;'></div>", unsafe_allow_html=True)

        # Display the disclaimer directly from the dataset
        st.markdown(f"""  
            <div style='width: 80%; font-size: 1.5em; text-align: justify; padding: 10px; border: none;'>NOTE: 
            {location_info['Disclaimer']}
            </div>
            """, unsafe_allow_html=True)

        # Add gap between table and research findings
        st.markdown("<div style='margin-top: 5cm;'></div>", unsafe_allow_html=True)

        # References (You can add your references here in APA style format)
        # st.write("**References:**")
        # st.markdown("- Pozdnyakova, L. (1999). Relationship between geo-electrical resistivity and soil properties. *Journal of Geotechnical and Geoenvironmental Engineering*, 125(4), 345-353.")
        # st.markdown("- Samouelian, A., Cousin, I., Tabbagh, A., Bruand, A., & Richard, G. (2005). Electrical resistivity survey in soil science: a review. *Soil and Tillage Research*, 83(2), 173-193.")
        # st.markdown("- Telford, W. M., Geldart, L. P., & Sheriff, R. E. (1990). *Applied Geophysics*. Cambridge University Press.")

