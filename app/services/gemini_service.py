import google.generativeai as genai
import os
from app.config import Config

class GeminiService:
    def __init__(self):
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-pro')

    def generate_diagram_code(self, prompt):
        system_prompt = """
        Generate Python code for creating an architecture diagram using the 'diagrams' package.
        
        IMPORTANT: Return ONLY the Python code, no explanations or additional text.
        The code MUST start with imports and follow this EXACT structure:

        from diagrams import Diagram, Cluster
        from diagrams.aws.compute import EC2
        from diagrams.aws.database import RDS
        from diagrams.aws.network import ELB
        from diagrams.aws.security import SecurityGroup
        from diagrams.aws.network import VPC, PublicSubnet, PrivateSubnet

        def generate_diagram():
            with Diagram("AWS Architecture", show=False, direction="LR"):
                # Your diagram components and connections here
                # Example:
                # lb = ELB("Load Balancer")
                # with Cluster("EC2 Instances"):
                #     servers = [EC2("Server 1"), EC2("Server 2")]
                # db = RDS("Database")
                # lb >> servers >> db

        if __name__ == "__main__":
            generate_diagram()

        RULES:
        1. Include ALL necessary imports at the top
        2. Use proper Python indentation
        3. Make sure all nodes are properly connected using >> or << operators
        4. Group related components using Cluster when appropriate
        5. Give descriptive names to components
        """
        
        full_prompt = f"""
        {system_prompt}

        Create a diagram based on this prompt: {prompt}
        
        Return ONLY the Python code, starting with imports.
        """
        
        try:
            response = self.model.generate_content(full_prompt)
            code = response.text.strip()
            
            # Basic validation
            if not code.startswith("from diagrams import"):
                # Try to extract code if it's wrapped in markdown or other text
                if "```python" in code:
                    code = code.split("```python")[1].split("```")[0].strip()
                elif "```" in code:
                    code = code.split("```")[1].strip()
            
            if not code.startswith("from diagrams import"):
                raise ValueError("Invalid code format. Code must start with proper imports.")
            
            # Validate basic structure
            required_elements = [
                "from diagrams import Diagram",
                "def generate_diagram():",
                'with Diagram(',
                'if __name__ == "__main__":'
            ]
            
            for element in required_elements:
                if element not in code:
                    raise ValueError(f"Missing required code element: {element}")
            
            return code
            
        except Exception as e:
            raise Exception(f"Failed to generate valid diagram code: {str(e)}\nGenerated code:\n{code}") 