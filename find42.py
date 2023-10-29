import json

with open('./merged_standards.json', 'r') as file:
    standards_data_from_json = json.load(file)

def fetch_details_from_json(key):
    for main_key, main_value in standards_data_from_json.items():
        if key == main_key:
            return main_value
        for sub_key, sub_value in main_value.items():
            if key == sub_key:
                return sub_value
            if key in sub_value:
                return sub_value[key]
    return None

def extract_group_or_class_standards(prefix):
    """Return standards from the JSON data that start with the given prefix."""
    extracted_standards = {}
    for main_key, main_value in standards_data_from_json.items():
        for sub_key, sub_value in main_value.items():
            if isinstance(sub_value, dict):
                for standard, description in sub_value.items():
                    if standard.startswith(prefix):
                        extracted_standards[standard] = description
            else:
                if sub_key.startswith(prefix):
                    extracted_standards[sub_key] = sub_value
    return extracted_standards

standards_data = {
    "Inventive Standards": {
        "Create a new function": {
            "1.1.1": "creating a new interaction",
            "1.1.2": "introduction of new substances inside components",
            "1.1.3": "introduction of new substances attached to components",
            "1.1.4": "using environment as a new component",
            "1.1.5": "using modified environment"
        },
        "Improve effect of insufficient interaction or improve controllability": {
            "Conditions allow introduction of new components to a system": {
                "2.1.1": "introducing a new subsystem",
                "2.1.2": "introducing a new field"
            },
            "Conditions do not allow introduction of new components to a system": {
                "2.2.1": "replacing basic field",
                "2.2.2": "fragmenting substance",
                "2.2.3": "using porous substances",
                "2.2.4": "increasing the degree of dynamics",
                "2.2.5": "structuring existing substances",
                "2.2.6": "structuring existing fields"
            },
            "Group 2.3": "Coordinating rhythms"
        },
        "Provide optimal action": {
            "1.1.6": "using maximum action and removing excess"
        },
        "Provide maximum action under restrictions": {
            "1.1.7": "redirecting action to a new substance"
        },
        "Provide opposite effects by the same interaction": {
            "1.1.8.1": "using protective substance",
            "1.1.8.2": "using amplification substance"
        },
        "Eliminate harmful interaction between two substances": {
            "Direct contact of two substances is not necessary": {
                "1.2.1": "introduction of a new substance",
                "1.2.2": "introduction of a modified substance"
            },
            "Direct contact of two substances must be maintained": {
                "1.2.4": "introduction of a new field"
            }
        },
        "Eliminate harmful interaction between a substance and a field": {
            "1.2.3": "drawing off the negative effect",
            "1.2.5": "using physical effects"
        },
        "Provide measurement/detection": {
            "Class 4": "Measuring and detection of Su-Field"
        },
        "Evolve product/system": {
            "Group 2.4": "Using properties of ferromagnetic substances",
            "Class 3": "Transition to Supersystem and Microlevel"
        }
    }
}
def display_options(options_dict):
    """Display options from the given dictionary with corresponding numbers, 
    their names from the JSON (if available), and return a mapping of numbers to keys."""
    numbered_options = {index+1: key for index, key in enumerate(options_dict.keys())}
    for num, option in numbered_options.items():
        details = fetch_details_from_json(option)  # Fetch the detailed description from JSON
        standard_name = details['StandardName'] if details and 'StandardName' in details else ""
        if standard_name:
            print(f"{num}. {option} - {standard_name}")
        else:
            print(f"{num}. {option}")
    return numbered_options
def search_standards_with_group_class(category):
    """Return the detailed description for a given category from the standards_data."""
    results = standards_data.get("Inventive Standards", {}).get(category, {}).copy()
    
    # Handle "Group" or "Class" entries
    keys_to_remove = []
    additional_standards = {}
    for key, value in results.items():
        if "Group" in key or "Class" in key:
            prefix = key.split(" ")[-1]  # Get the last word (e.g., "2.4" from "Group 2.4")
            standards = extract_group_or_class_standards(prefix)
            additional_standards.update(standards)
            keys_to_remove.append(key)
    
    # Add the new standards and remove the original "Group" or "Class" entries
    results.update(additional_standards)
    for key in keys_to_remove:
        del results[key]

    # Replace the standard number with its detailed description from the JSON data and add the name
    for key in results.keys():
        if isinstance(results[key], dict):
            for subkey in results[key].keys():
                details = fetch_details_from_json(subkey)
                if details:
                    results[key][subkey] = f"{details} ({results[key][subkey]})"
        else:
            details = fetch_details_from_json(key)
            if details:
                results[key] = f"{details} ({results[key]})"
                
    return results


def main_updated():
    print("Available Categories:")
    main_categories = display_options(standards_data["Inventive Standards"])
    
    # Get user's main category choice
    try:
        main_choice_num = int(input("\nEnter a number to choose a category: "))
        main_choice = main_categories[main_choice_num]
    except (ValueError, KeyError):
        print("Invalid choice. Exiting.")
        return
    
    search_results = search_standards_with_group_class(main_choice)
    
    if not search_results:
        print("No results found for the given category.")
        return
    
    # Check if the results have subcategories
    first_key = list(search_results.keys())[0]
    if isinstance(search_results[first_key], dict):
        print("\nAvailable Subcategories:")
        subcategories = display_options(search_results)
        
        # Get user's subcategory choice
        try:
            sub_choice_num = int(input("\nEnter a number to choose a subcategory: "))
            sub_choice = subcategories[sub_choice_num]
        except (ValueError, KeyError):
            print("Invalid choice. Exiting.")
            return
        
        search_results = search_results[sub_choice]
        if not search_results:
            print("No results found for the given subcategory.")
            return
    
    # Display the final results
    print(f"\nResults for {main_choice}:")
    if isinstance(search_results, dict):
        for key, value in search_results.items():
            print(f"  {key}: {value}")
    else:
        print(f"  {search_results}")

if __name__ == "__main__":
    main_updated()

