# Script to 
# - read 1) the BIG directory of URM authors in NLP, 2) the
#   file containing all EACL 2021 paper information;
# - output one json file containing the authors, titles, and links for papers
#   by people in the directory.

import csv
import json

################################################################################

# This file sourced from https://www.virtual2021.eacl.org/papers.json
papers_path = "./2021_eacl_papers.json"

# This file downloaded 2021-04-19 from http://www.winlp.org/big-directory/
big_directory_path = "./2021-04-19-big_directory.csv"

URM_authors_papers_path = "./EACL2021_URM_authors.json".format()

paper_link_pattern = "https://www.virtual2021.eacl.org/paper_{}.html"

URM_authors = set()
URM_papers = []

################################################################################

# Read the file containing URM authors in NLP from the BIG directory
with open(big_directory_path, "r", encoding="utf8") as csv_infile:
    csv_reader = csv.DictReader(csv_infile, delimiter=",")
    for row in csv_reader:
        URM_authors.add(row["Name"])

# Collect EACL 2021 papers, and filter using the URM directory data
with open(papers_path, "r", encoding="utf8") as json_infile:
    paper_data = json.load(json_infile)    
    for this_paper in paper_data:
        current_authors = this_paper["content"]["authors"]
        for a in current_authors:
            if a in URM_authors:
                this_paper_link = paper_link_pattern.format(this_paper["id"])
                URM_papers.append({"Authors": current_authors,
                                "Title": this_paper["content"]["title"],
                                "Talk URL": this_paper_link,
                                "Anthology URL": this_paper["content"]["pdf_url"]})
                break

# Write one json file with all URM-authored EACL 2021 papers.
with open(URM_authors_papers_path, "w", encoding="utf8") as URM_outfile:
    json.dump(URM_papers, URM_outfile, indent=2)