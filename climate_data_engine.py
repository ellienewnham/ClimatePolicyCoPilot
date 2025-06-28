import csv
import json
from data_scrapper import get_data
from data_enricher import enrich_info

def csv_to_json(csv_path):
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return [row for row in reader]

raw_climate_data_file = "./raw_data/partial_raw_climate_data.csv"
rows = csv_to_json(raw_climate_data_file)
additional_info = [{
        "question" : "What companies are impacted by this policy?",
        "column_name" : "who_is_impacted",
        "example_answer" : """The rule would apply to companies that have more than $100 million in public float and meet one of the following criteria:
They have annual greenhouse gas (GHG) emissions of more than 1 million metric tons of carbon dioxide equivalent (CO2e).
They have a global market capitalization of more than $750 million.
They are a registrant in one of the following industries:
Electric utilities
Oil and gas producers
Oil and gas refiners
Coal producers
Transportation companies
Industrial manufacturers
"""
    },
    {
        "question" : "What are key requirements of this policy?",
        "column_name" : "key_requirements",
        "example_answer" : """Carbon accounting for scopes 1, 2, & 3 will be required for all companies (smaller companies exempt from scope 3)
1 fiscal year transition period for reporting
2 fiscal years to scale up to transition requirements
Require GHG emissions accounting attestation
Not limited to public accounting firms
Requirements for the accounting firms
Must meet proposed definition of expertise in accounting, reporting and measuring GHG
Provide standards publicly
Needs to follow prevailing attestation standards
Disclose disaggregated information from climate related risks in the financial statements
"""
    },
    {
        "question" : "What is the timeline of this policy implementation?",
        "column_name" : "timeline_of_policy_implementation",
        "example_answer" : """SEC is now targeting October for release of the final rule. Most likely, litigation will soon follow."""
    }
]
for row in rows:
    url = row["reference"]
    policy = get_data(url)
    for info in additional_info:
        new_data = enrich_info(policy, info["question"], info["example_answer"])
        row[info["column_name"]] = new_data
 
with open("./enriched_climate_data.json", "w", encoding="utf-8") as f:
    json.dump(rows, f, indent=2, ensure_ascii=False)
    


    

