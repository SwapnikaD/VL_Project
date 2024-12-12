from rdflib import Graph
from SPARQLWrapper import SPARQLWrapper, JSON, N3
import json
import requests

# src: https://opendata.stackexchange.com/questions/5742/extract-labels-from-wikidata-entity
# src: https://stackoverflow.com/questions/69136904/extracting-rdf-triples-from-wikidata

def save_entry_to_json(entry): 

    try: 
        with open("data_dicts_triplets_wiki.json", 'r') as file: 
                data = json.load(file) 
         
        # Append the new entry 
        data.append(entry) 
         
        # Save back to the file 
        with open("data_dicts_triplets_wiki.json", 'w') as file: 
            json.dump(data, file, indent=4) 
        print(f"Successfully saved entry: {entry}") 
     
    except Exception as e: 
        print(f"Error saving entry to JSON: {e}") 


def getData(keyword):
	list_of_all_triples=[]

	endpoint_url = "https://query.wikidata.org/sparql"
	headers = {'User-Agent': 'Mybot'}


	# keyword = '"Sand"'
	query = "\""+keyword+'\"@en'
	print(keyword)
	print(query)
# query to get top ten most popular results
# 	query_string =  f"""SELECT ?subject ?statements WHERE {{
#   ?subject rdfs:label {query} .
#   ?subject wikibase:statements ?statements .
# }}
# LIMIT 10
# """	
	# generic query
	query_string = f"""
	SELECT * WHERE {{
	?subject rdfs:label {query}
	}}
	LIMIT 10
	"""
    
	# print(query_string)
	
	query_to_get_entity_id = {
		'query': query_string,
		'format': 'json'
	}

	response = requests.get(endpoint_url, params=query_to_get_entity_id, headers=headers)
	data = response.json()
	print(data)
	ids=[]
	for result in data['results']['bindings']:
		ids.append(result["subject"]["value"].replace('http://www.wikidata.org/entity/', ''))

	print(ids)
	
	for id in ids:
		q = f"""  SELECT ?wdLabel ?ooLabel
			WHERE {{
			VALUES (?s) {{( wd:{id})}}
			?s ?wdt ?o .
			?wd wikibase:directClaim ?wdt .
			?wd rdfs:label ?wdLabel .
			OPTIONAL {{
				?o rdfs:label ?oLabel .
				FILTER (lang(?oLabel) = "en")
			}}
			FILTER (lang(?wdLabel) = "en")
			BIND (COALESCE(?oLabel, ?o) AS ?ooLabel)
			}} 
			ORDER BY xsd:integer(STRAFTER(STR(?wd), "http://www.wikidata.org/entity/P")) 
			LIMIT 1
			"""
		query = {
				'query': q,
				'format': 'json'
			}
		response = requests.get(endpoint_url, params=query, headers=headers)
		data = response.json()
		# print(data)
		for result in data['results']['bindings']:
				tripls= [keyword,result["wdLabel"]["value"], result["ooLabel"]["value"]]
				triple = ', '.join(tripls)
				list_of_all_triples.append(triple)
    
	return list_of_all_triples
    				
					
    
    


# keyword = "wade".capitalize()
# getData(keyword)