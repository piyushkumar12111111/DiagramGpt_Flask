import os
from diagrams import Diagram
import tempfile
import base64
import traceback

class DiagramService:
    @staticmethod
    def generate_diagram(code, diagram_id):
        try:
            # Create a temporary directory for the diagram
            with tempfile.TemporaryDirectory() as tmpdir:
                # Modify the code to save in the temp directory
                modified_code = code.replace(
                    'with Diagram(',
                    f'with Diagram(filename="{tmpdir}/diagram"'
                )
                
                # Add error handling wrapper
                wrapped_code = f"""
try:
{modified_code}
except Exception as e:
    raise Exception(f"Diagram generation failed: {{str(e)}}")
"""
                
                # Execute the modified code
                local_vars = {}
                exec(wrapped_code, globals(), local_vars)
                
                # Read the generated PNG file
                png_path = f"{tmpdir}/diagram.png"
                if not os.path.exists(png_path):
                    raise Exception("Diagram file was not generated")
                
                with open(png_path, "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read()).decode()
                
                return encoded_string
        except Exception as e:
            error_details = traceback.format_exc()
            raise Exception(f"Error generating diagram: {str(e)}\n{error_details}") 