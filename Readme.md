This is the repository accompanying the project titled: "Triplet prompting: Combining Chain of Thought Prompting with Triplet Generation for Connections in New York Times".

Directory structure:

- data- has all the jsons, intermediate and final jsons used for the project.
- data comparison - has processed jsons for validation and related python scripts.
- Replicated results - has json files, images, graph script cherry picked from paper [4]. The zip was huge and can be found in google drive link in the paper.
- txt files - has input text files and some old data dumps.
- clip.py - has code for (iii)
- clip_text.py - has code for (iv)
- diff.py - to generate images using stable diffusion. Generated in images_sd folder, which also due to huge size was zipped and uploaded to drive. Accidentally commiting this folder blocked me from pushing code regularly because, git always rejected push. Undoing commits and removing files helped me finally push code in last few days.
- google_search_image.py - Code using google-image_search to pull images for given word. However, due to rate limits was not pursued further.
- groq_test.py - File that houses code to make api calls for (v),(vi),(vii). and later part 2 from [4].
- paper_citied_4_part1.py - has code for (i)
- paper_cited_4_part2.py - has code for part 2 based prompt. The json for which is data/paper_cited4_part2_all.json. But due to empty groups in all records, further processing was difficult. Multiple attempts gave same response.
- read_...py - files to mostly read data from various sources. Repeatative code, can be refactored in future.
- semantic_similarity.py - used for sem sim in (ii),(vi).
- utils.py - common code used accross various files.
- wikidata.py - main code for (ii)

Note: I changed directory structure after most of the code is done, so path to excel, csv, txt, json files need to be changed accordingly.
