import json 
import pandas as pd 
def normalize_string(value): 
    words = value.split(",")  # Split by commas 
    sorted_words = sorted(word.strip().lower() for word in words)  # Sort and clean words 
    return ",".join(sorted_words)  # Rejoin into a normalized string 

def compare_and_export_to_excel(base_file, comparison_files, output_excel): 

    """ 

    Compare the base file with multiple comparison files and export results to an Excel file. 

 

    :param base_file: Path to the base JSON file. 

    :param comparison_files: List of paths to comparison JSON files. 

    :param output_excel: Path to the output Excel file. 

    """ 

    try: 

        # Load base JSON file 

        with open(base_file, 'r') as f: 

            base_data = json.load(f) 

 

        # Normalize and store base values by key 

        normalized_base = { 

            key: set(normalize_string(value) for value in values) 

            for key, values in base_data.items() 

        } 

 

        # Prepare data rows for the DataFrame 

        rows = [] 

 

        # Compare each file 

        for key, base_set in normalized_base.items(): 

            row = {'Key': key}  # Start row with the key 

            for comparison_file in comparison_files: 

                with open(comparison_file, 'r') as f: 

                    comparison_data = json.load(f) 

 

                # Normalize comparison values 

                comparison_values = comparison_data.get(key, []) 

                comparison_set = set( 

                    normalize_string(value) for value in comparison_values 

                ) 

 

                # Count matches 

                matches = base_set.intersection(comparison_set) 

                row[comparison_file] = len(matches)  # Add match count for this file 

 

            # Append the row 

            rows.append(row) 

 

        # Create DataFrame 

        result_df = pd.DataFrame(rows) 

 

        # Write to Excel 

        result_df.to_excel(output_excel, index=False) 

        print(f"Results successfully written to {output_excel}") 

 

    except Exception as e: 

        print(f"Error: {e}") 
# Example usage 
base_file_path = 'gold_data_polished.json' 
comparison_files_paths = ['processed_llama_answers.json','clip_similarities.json','clip_text_similarities.json', 'sem_sim_data_all237_minilm.json','sem_sim_wiki.json'] 
output_excel_path = 'comparison_results.xlsx' 

compare_and_export_to_excel(base_file_path, comparison_files_paths, output_excel_path) 

 