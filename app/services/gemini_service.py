import google.generativeai as genai
import os
from app.config import Config

class GeminiService:
    def __init__(self):
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-pro')

    def generate_diagram_code(self, prompt):
        system_prompt = """
        You are a Python code generator for architecture diagrams. Generate code using the 'diagrams' package.
        
        Follow this EXACT template and replace the placeholder content:

        from diagrams import Diagram, Cluster
        from diagrams.aws.compute import EC2
        from diagrams.aws.database import RDS
        from diagrams.aws.network import ELB, VPC
        from diagrams.aws.network import PrivateSubnet, PublicSubnet

        def generate_diagram():
            with Diagram("AWS Architecture", direction="LR"):
                with Cluster("VPC"):
                    with Cluster("Public Subnet"):
                        lb = ELB("Load Balancer")
                    
                    with Cluster("Private Subnet"):
                        web = [
                            EC2("Web Server 1"),
                            EC2("Web Server 2")
                        ]
                    
                    with Cluster("Database Subnet"):
                        db = RDS("Database")
                    
                    # Connect components
                    lb >> web >> db

        if __name__ == "__main__":
            generate_diagram()

        IMPORTANT RULES:
        1. Always include ONLY the necessary imports shown above
        2. Always wrap diagram creation in a function called generate_diagram()
        3. Always use Cluster for grouping related components
        4. Always use meaningful names for components
        5. Always connect components using >>
        6. Always include the if __name__ == "__main__" block
        7. Return ONLY the Python code, no explanations
        """

        example_prompt = """
        Here's an example prompt and how to modify the template:
        
        Prompt: "Create AWS architecture with ALB, 2 EC2 instances, and RDS"
        
        Modifications needed:
        1. Keep the imports exactly as shown
        2. Update component names to match the prompt
        3. Update the connections to reflect the architecture
        4. Keep the basic structure intact
        """

        full_prompt = f"""
        # {system_prompt}

        # {example_prompt}

        # Now, generate a diagram based on this prompt: {prompt}
        # Modify ONLY the components, names, and connections while keeping the exact same structure.
        # Return ONLY the Python code.
        """

        try:
            response = self.model.generate_content(full_prompt)
            code = response.text.strip()
            
            # Clean up the code if it's wrapped in markdown
            if "```python" in code:
                code = code.split("```python")[1].split("```")[0].strip()
            elif "```" in code:
                code = code.split("```")[1].strip()
            
            # Validate the code structure
            required_elements = [
                "from diagrams import Diagram",
                "def generate_diagram():",
                'with Diagram(',
                'if __name__ == "__main__":'
            ]
            
            for element in required_elements:
                if element not in code:
                    # If validation fails, return a default template with the user's components
                    return self._generate_default_template(prompt)
            
            return code
            
        except Exception as e:
            # If there's any error, fall back to the default template
            return self._generate_default_template(prompt)

    def _generate_default_template(self, prompt):
        """Generate a safe default template if the AI generation fails."""
        return """
from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB, VPC
from diagrams.aws.network import PrivateSubnet, PublicSubnet

def generate_diagram():
    with Diagram("AWS Architecture", direction="LR"):
        with Cluster("VPC"):
            with Cluster("Public Subnet"):
                lb = ELB("Load Balancer")
            
            with Cluster("Private Subnet"):
                web = [
                    EC2("Web Server 1"),
                    EC2("Web Server 2")
                ]
            
            with Cluster("Database Subnet"):
                db = RDS("Database")
            
            # Connect components
            lb >> web >> db

if __name__ == "__main__":
    generate_diagram()
""".strip() 