import os
from diagrams import Diagram
import tempfile
import base64
import traceback
import sys
from pathlib import Path
import textwrap
import re

class DiagramService:
    @staticmethod
    def generate_diagram(code, diagram_id):
        try:
            # Create a temporary directory for the diagram
            with tempfile.TemporaryDirectory() as tmpdir:
                # Create a Path object for better path handling
                diagram_path = Path(tmpdir) / "diagram"
                diagram_path = str(diagram_path).replace("\\", "/")
                
                # Extract and format the diagram content
                try:
                    # Use regex to extract the content between the outermost with block
                    match = re.search(r'with\s+Diagram.*?:\s*(.*?)(?=if\s+__name__|$)', 
                                    code, re.DOTALL)
                    if not match:
                        raise ValueError("Could not extract diagram content")
                    
                    # Get the content and clean it up
                    diagram_content = match.group(1).strip()
                    
                    # Split into lines and remove empty lines at start/end
                    lines = [line for line in diagram_content.splitlines() if line.strip()]
                    
                    # Find the base indentation level
                    base_indent = len(lines[0]) - len(lines[0].lstrip())
                    
                    # Remove the base indentation from all lines and add proper indentation
                    cleaned_lines = []
                    for line in lines:
                        if line.startswith(' ' * base_indent):
                            line = line[base_indent:]
                        cleaned_lines.append(' ' * 12 + line)  # 12 spaces = 3 levels of indentation
                    
                    # Join lines back together
                    diagram_content = '\n'.join(cleaned_lines)
                    
                except Exception as e:
                    print(f"Error extracting diagram content: {str(e)}")
                    raise
                
                # Create the modified code with the correct diagram parameters
                modified_code = f"""
import os
import sys
from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB
from diagrams.aws.network import VPC, PrivateSubnet, PublicSubnet
from diagrams.aws.network import ALB, ELB

def generate_diagram():
    try:
        with Diagram(
            "AWS Architecture",
            filename=r"{diagram_path}",
            show=False,
            outformat="png",
            direction="LR"
        ):
{diagram_content}
    except Exception as e:
        print(f"Error in diagram generation: {{str(e)}}", file=sys.stderr)
        raise

if __name__ == "__main__":
    generate_diagram()
"""
                
                # Debug the generated code
                print("Generated code:")
                print(modified_code)
                print("\nDiagram content:")
                print(diagram_content)
                
                # Create a new Python file in the temp directory
                temp_py_file = os.path.join(tmpdir, "diagram_gen.py")
                with open(temp_py_file, "w", encoding='utf-8') as f:
                    f.write(modified_code)
                
                # Execute the Python file as a separate process
                import subprocess
                result = subprocess.run(
                    [sys.executable, temp_py_file],
                    capture_output=True,
                    text=True,
                    cwd=tmpdir,  # Set working directory to temp dir
                    env={**os.environ, 'PATH': f"{os.environ['PATH']};C:\\Program Files\\Graphviz\\bin"}  # Add Graphviz to PATH
                )
                
                if result.returncode != 0:
                    print("Error output:", result.stderr)
                    raise Exception(f"Diagram generation failed: {result.stderr}")
                
                # Read the generated PNG file
                png_path = f"{diagram_path}.png"
                
                # Debug information
                print(f"Looking for diagram at: {png_path}")
                print(f"Directory contents: {os.listdir(tmpdir)}")
                
                if not os.path.exists(png_path):
                    raise Exception(f"Diagram file was not generated at {png_path}")
                
                with open(png_path, "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read()).decode()
                
                return encoded_string
                
        except Exception as e:
            error_details = traceback.format_exc()
            print(f"Error details: {error_details}", file=sys.stderr)
            raise Exception(f"Error generating diagram: {str(e)}\n{error_details}") 