import streamlit as st
import requests
import base64
from PIL import Image
import io
import json

st.set_page_config(
    page_title="Architecture Diagram Generator",
    page_icon="🔧",
    layout="wide"
)

def main():
    st.title("Architecture Diagram Generator 🏗️")
    
    # Sidebar
    st.sidebar.header("About")
    st.sidebar.info(
        "This application generates architecture diagrams based on your text descriptions "
        "using AI and the Python Diagrams package."
    )
    
    # Main content
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Enter Your Description")
        prompt = st.text_area(
            "Describe the architecture you want to visualize",
            height=150,
            placeholder="Example: Create an AWS architecture diagram showing a web application with an Application Load Balancer, two EC2 instances in a private subnet, and an RDS database in a separate subnet"
        )
        
        if st.button("Generate Diagram", type="primary"):
            if prompt:
                with st.spinner("Generating diagram..."):
                    try:
                        # Make request to Flask backend
                        response = requests.post(
                            "http://localhost:5000/api/diagrams/generate",
                            json={"prompt": prompt}
                        )
                        
                        if response.status_code == 200:
                            data = response.json()
                            
                            # Store data in session state
                            st.session_state.diagram_code = data['diagram_code']
                            st.session_state.diagram_image = data['diagram_image']
                            st.session_state.diagram_id = data['id']
                            
                            st.success("Diagram generated successfully!")
                        else:
                            error_msg = response.json().get('error', 'Unknown error occurred')
                            st.error(f"Error: {error_msg}")
                            
                    except Exception as e:
                        st.error(f"Error connecting to backend: {str(e)}")
            else:
                st.warning("Please enter a description first!")

    with col2:
        st.subheader("Generated Diagram")
        if 'diagram_image' in st.session_state:
            # Display the diagram
            image_bytes = base64.b64decode(st.session_state.diagram_image)
            image = Image.open(io.BytesIO(image_bytes))
            st.image(image, use_column_width=True)
            
            # Download button
            st.download_button(
                label="Download Diagram",
                data=image_bytes,
                file_name="architecture_diagram.png",
                mime="image/png"
            )
    
    # Display generated code
    if 'diagram_code' in st.session_state:
        st.subheader("Generated Python Code")
        st.code(st.session_state.diagram_code, language="python")

    # Display diagram history
    st.subheader("Previous Diagrams")
    if st.button("Refresh History"):
        try:
            response = requests.get("http://localhost:5000/api/diagrams/history")
            if response.status_code == 200:
                diagrams = response.json()
                
                for diagram in diagrams:
                    with st.expander(f"Diagram {diagram['id']} - {diagram['created_at']}"):
                        st.write(f"**Prompt:** {diagram['prompt']}")
                        st.write(f"**Status:** {diagram['status']}")
                        if diagram.get('error_message'):
                            st.error(f"Error: {diagram['error_message']}")
        except Exception as e:
            st.error(f"Error fetching history: {str(e)}")

if __name__ == "__main__":
    main() 