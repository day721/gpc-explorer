import streamlit as st
import json

# Set Page Config
st.set_page_config(page_title="GPC Hierarchy Explorer", layout="wide")

# Load the JSON Data
@st.cache_data
def load_data():
    with open('GPC as of November 2025 v20251127 GB.json', 'r') as f:
        return json.load(f)

try:
    data = load_data()
    schema = data.get('Schema', [])
except FileNotFoundError:
    st.error("Data file not found. Please ensure the JSON file is in the same directory.")
    st.stop()

st.title("📦 GPC Product Groups Explorer")
st.write(f"**Language:** {data.get('LanguageCode')} | **Updated:** {data.get('DateUtc')}")

# Sidebar for Hierarchical Filtering
st.sidebar.header("Navigate Groups")

# Level 1: Segment
segments = {s['Title']: s for s in schema}
seg_choice = st.sidebar.selectbox("1. Select Segment", ["All"] + list(segments.keys()))

if seg_choice != "All":
    selected_seg = segments[seg_choice]
    
    # Level 2: Family
    families = {f['Title']: f for f in selected_seg.get('Childs', [])}
    fam_choice = st.sidebar.selectbox("2. Select Family", ["All"] + list(families.keys()))
    
    if fam_choice != "All":
        selected_fam = families[fam_choice]
        
        # Level 3: Class
        classes = {c['Title']: c for c in selected_fam.get('Childs', [])}
        class_choice = st.sidebar.selectbox("3. Select Class", ["All"] + list(classes.keys()))
        
        if class_choice != "All":
            selected_class = classes[class_choice]
            
            # Level 4: Brick
            bricks = {b['Title']: b for b in selected_class.get('Childs', [])}
            brick_choice = st.sidebar.selectbox("4. Select Brick", list(bricks.keys()))
            
            # DISPLAY SELECTED DATA
            item = bricks[brick_choice]
            st.header(f"Brick: {item['Title']}")
            st.info(f"**Code:** {item['Code']}")
            st.write(f"**Definition:** {item['Definition']}")
            if item.get('DefinitionExcludes'):
                st.warning(f"**Excludes:** {item['DefinitionExcludes']}")
            
            # Show Attributes (Level 5/6)
            if item.get('Childs'):
                with st.expander("View Attributes & Values"):
                    for attr in item['Childs']:
                        st.markdown(f"**{attr['Title']}** ({attr['Code']})")
                        values = [val['Title'] for val in attr.get('Childs', [])]
                        st.write(", ".join(values))
        else:
            st.subheader(f"Families in {seg_choice} > {fam_choice}")
            st.write(list(classes.keys()))
    else:
        st.subheader(f"Families in {seg_choice}")
        st.write(list(families.keys()))
else:
    st.info("Select a Segment in the sidebar to begin exploring product groups.")
    # Show summary of all segments
    st.write("### All Available Segments")
    for s in schema:
        st.write(f"- {s['Title']} ({s['Code']})")
