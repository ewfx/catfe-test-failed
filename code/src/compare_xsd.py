import xmlschema

def get_elements_from_xsd(file_path):
    schema = xmlschema.XMLSchema(file_path)
    elements = {elem.name: elem for elem in schema.elements.values()}
    return elements

def compare_xsd(old_file, new_file):
    old_elements = get_elements_from_xsd(old_file)
    new_elements = get_elements_from_xsd(new_file)

    added_elements = {k: v for k, v in new_elements.items() if k not in old_elements}
    removed_elements = {k: v for k, v in old_elements.items() if k not in new_elements}
    modified_elements = {
        k: v for k, v in new_elements.items()
        if k in old_elements and old_elements[k] != v
    }

    return added_elements, removed_elements, modified_elements

# Example Usage
old_xsd_path = "C:/projects/wgprt-1/resource/pacs.008.001.13.xsd"
new_xsd_path = "C:/projects/wgprt-1/resource/pacs.008.001.14.xsd"
added, removed, modified = compare_xsd(old_xsd_path, new_xsd_path)

print("Added Elements:", added.keys())
print("Removed Elements:", removed.keys())
print("Modified Elements:", modified.keys())