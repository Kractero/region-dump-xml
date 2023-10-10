import requests
import gzip
from io import BytesIO
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET

response = requests.get('https://www.nationstates.net/pages/regions.xml.gz', headers={'User-Agent': 'Kractero'})

if response.status_code == 200:
    with gzip.GzipFile(fileobj=BytesIO(response.content)) as gzipped_file:
        xml_text = gzipped_file.read()
    today_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    with open(f'data/{today_date}-Regions.xml', 'wb') as xml_file:
        xml_file.write(xml_text)

    print('XML file downloaded and saved successfully.')
else:
    print(f'Failed to fetch dump from NationStates with status {response.status_code}')


response = requests.get('https://www.nationstates.net/pages/nations.xml.gz', headers={'User-Agent': 'Kractero'})

if response.status_code == 200:
    with gzip.GzipFile(fileobj=BytesIO(response.content)) as gzipped_file:
        xml_text = gzipped_file.read()
    root = ET.fromstring(xml_text)

    new_root = ET.Element("NATIONS")

    for parent in root.findall('.//NATION'):
        new_nation = ET.SubElement(new_root, "NATION")
        for child in parent:
            if child.tag in ['NAME', 'ENDORSEMENTS']:
                new_nation.append(child)

    tree = ET.ElementTree(new_root)
    modified_xml_text = ET.tostring(new_root, encoding='utf-8')

    today_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    with open(f'data/{today_date}-Nations.xml', 'wb') as xml_file:
        xml_file.write(modified_xml_text)

    print('XML file downloaded and saved successfully.')
else:
    print(f'Failed to fetch dump from NationStates with status {response.status_code}')
