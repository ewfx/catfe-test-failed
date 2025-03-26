import os
from xmlschema import XMLSchema
from langchain.chat_models import init_chat_model
import requests

def parse_xsd_deep(xsd_path):
    """
    Parse the XSD file and return a detailed structure of elements and attributes.
    """
    schema = XMLSchema(xsd_path)
    elements = {}

    def traverse_element(element, path=""):
        """
        Recursively traverse elements and attributes with detailed information.
        """
        element_path = f"{path}/{element.name}" if path else element.name
        element_details = {
            "type": element.type.name if element.type else "unknown",
            "attributes": {},
            "min_occurs": element.min_occurs,
            "max_occurs": element.max_occurs,
            "children": [child.name for child in element.iterchildren()],
            "documentation": element.annotation.documentation if element.annotation else None,
            "constraints": {}
        }

        # Extract constraints for simple types
        if element.type and element.type.is_simple():
            if element.type.is_restriction:
                for facet in element.type.facets.values():

                     if isinstance(facet, list):  # Handle enumeration facets
                        element_details["constraints"].setdefault("enumeration", []).extend(facet)
                     elif facet.__class__.__name__ == "XsdMinLengthFacet":
                        element_details["constraints"]["minLength"] = facet.value
                     elif facet.__class__.__name__ == "XsdMaxLengthFacet":
                        element_details["constraints"]["maxLength"] = facet.value

        # Extract attributes
        element_details["attributes"] = {
            attr.name: {
                "type": attr.type.name if attr.type else "unknown",
                "use": attr.use,  # Required, optional, etc.
                "default": attr.default,
                "fixed": attr.fixed,
            }
            for attr in element.attributes.values()
        }

        elements[element_path] = element_details

        # Recursively process child elements
        for child in element.iterchildren():
            traverse_element(child, element_path)

    # Traverse all root elements in the schema
    for root_element in schema.elements.values():
        traverse_element(root_element)

    return elements


def generate_test_cases(xsd_path):
    """
    Generate test cases based on the detailed XSD structure.
    """
    xsd_structure = parse_xsd_deep(xsd_path)
    prompt = "Generate test cases in BDD format for the following XSD structure:\n"

    for path, details in xsd_structure.items():
        prompt += f"\nElement: {path}\n"
        prompt += f"  Type: {details['type']}\n"
        prompt += f"  Attributes:\n"
        for attr_name, attr_details in details['attributes'].items():
            prompt += f"    - Name: {attr_name}, Type: {attr_details['type']}, Use: {attr_details['use']}, Default: {attr_details['default']}, Fixed: {attr_details['fixed']}\n"
        prompt += f"  Min Occurs: {details['min_occurs']}, Max Occurs: {details['max_occurs']}\n"
        prompt += f"  Children: {', '.join(details['children']) if details['children'] else 'None'}\n"
        if details['documentation']:
            prompt += f"  Documentation: {details['documentation']}\n"
        if details["constraints"]:
            prompt += f"  Constraints:\n"
            if "enumeration" in details["constraints"]:
                prompt += f"    - Enumeration: {', '.join(details['constraints']['enumeration'])}\n"
            if "minLength" in details["constraints"]:
                prompt += f"    - Min Length: {details['constraints']['minLength']}\n"
            if "maxLength" in details["constraints"]:
                prompt += f"    - Max Length: {details['constraints']['maxLength']}\n"

    # Initialize the Groq model
    model = init_chat_model("llama3-8b-8192", model_provider="groq")
    response = model.invoke(prompt)
    return response.content

def generate_api_test_cases(swagger_url):
    """
    Generate automation test cases for REST APIs based on the provided Swagger URL.
    """
    try:
        # Fetch the Swagger JSON from the provided URL
        response = requests.get(swagger_url)
        response.raise_for_status()  # Raise an error for HTTP issues
        swagger_data = response.json()

        # Generate a prompt for the Groq model
        prompt = "Generate automation test cases for the following Swagger API specification:\n"
        prompt += f"{swagger_data}"

        # Initialize the Groq model
        model = init_chat_model("llama3-8b-8192", model_provider="groq")
        response = model.invoke(prompt)
        return response.content
    except Exception as e:
        raise RuntimeError(f"Failed to generate API test cases: {e}")



if __name__ == "__main__":
    # Ensure the API key is set
    if not os.environ.get("GROQ_API_KEY"):
        os.environ["GROQ_API_KEY"] = "your_api_key_here"

    # Path to your XSD file
    xsd_file_path = "E:/Wells-WGPRT-1/Development/resource/pacs.008.001.13.xsd"

    # Generate and print test cases
    try:
        test_cases = generate_test_cases(xsd_file_path)
        print("Test cases generated successfully:\n")
        print(test_cases)
    except Exception as e:
        print(f"An error occurred: {e}")