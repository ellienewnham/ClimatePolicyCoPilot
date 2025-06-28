import http.client
import json


def get_data(input_url, output_file):
    conn = http.client.HTTPSConnection("api.apify.com")
    payload = json.dumps({
        "aggressivePrune": False,
        "blockMedia": True,
        "clickElementsCssSelector": "[aria-expanded=\"False\"]",
        "clientSideMinChangePercentage": 15,
        "crawlerType": "playwright:adaptive",
        "debugLog": False,
        "debugMode": False,
        "expandIframes": True,
        "ignoreCanonicalUrl": False,
        "ignoreHttpsErrors": False,
        "keepUrlFragments": False,
        "proxyConfiguration": {
            "useApifyProxy": True
        },
        "readableTextCharThreshold": 100,
        "removeCookieWarnings": True,
        "removeElementsCssSelector": "nav, footer, script, style, noscript, svg, img[src^='data:'],\n[role=\"alert\"],\n[role=\"banner\"],\n[role=\"dialog\"],\n[role=\"alertdialog\"],\n[role=\"region\"][aria-label*=\"skip\" i],\n[aria-modal=\"True\"]",
        "renderingTypeDetectionPercentage": 10,
        "respectRobotsTxtFile": True,
        "saveFiles": False,
        "saveHtml": False,
        "saveHtmlAsFile": False,
        "saveMarkdown": True,
        "saveScreenshots": False,
        "startUrls": [
            {
                "url": input_url,
                "method": "GET"
            }
        ],
        "useSitemaps": False
    })
    headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': 'Bearer apify_api_Kh60iZYQwT5OGo9Pqc9XnDROcGwQIM167Kl2'
    }
    conn.request("POST", "/v2/acts/apify~website-content-crawler/run-sync-get-dataset-items", payload, headers)
    res = conn.getresponse()
    data = res.read()
    items = json.loads(data.decode("utf-8"))
    texts = [item.get("text", "") for item in items if "text" in item]
    with open(output_file, "w", encoding="utf-8") as f:
        for text in texts:
            f.write(text.strip() + "\n\n")

get_data("https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32019R2088", "./eur_lex.txt")
get_data("https://www.finance.gov.au/government/climate-action-government-operations/commonwealth-climate-disclosure-policy", "./finance_au.txt")
