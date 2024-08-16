import os
import gzip
from io import BytesIO
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
from urllib.request import urlopen, Request
import json

todays_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

def download_and_save_xml(url, output_file, approved_keys, iter_str):
    try:
        with urlopen(Request(url, headers={'User-Agent': 'Kractero'})) as response:
            if response.status == 200:
                with gzip.GzipFile(fileobj=BytesIO(response.read())) as gzipped_file:
                    xml_text = gzipped_file.read()

                root = ET.fromstring(xml_text)

                for iterable in root.iter(iter_str):
                    for element in list(iterable):
                        if element.tag not in approved_keys:
                            iterable.remove(element)

                filtered_xml_text = ET.tostring(root)

                with open(output_file, 'wb') as xml_file:
                    xml_file.write(filtered_xml_text)

                print(f'XML file downloaded and saved successfully: {output_file}')
            else:
                print(f'Failed to fetch dump from NationStates with status {response.status}')
    except Exception as e:
        print(f'An error occurred: {e}')

def main():
    todays_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    download_and_save_xml('https://www.nationstates.net/pages/regions.xml.gz', f'data/{todays_date}-Regions.xml', ("NAME", "NUMNATIONS", "UNNATIONS", "DELEGATEVOTES", "DELEGATEAUTH", "LASTUPDATE", "FACTBOOK", "EMBASSIES"), "REGION")
    download_and_save_xml('https://www.nationstates.net/pages/nations.xml.gz', f'data/{todays_date}-Nations.xml', ("NAME", "ENDORSEMENTS"), "NATION")
    previous_date = (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d')

    xml_files = os.listdir('data')

    with open('cards.txt', 'r') as file:
        card_names = set(line.strip() for line in file if line.strip())

    tree = ET.parse(f'data/{todays_date}-Nations.xml')
    root = tree.getroot()
    names_in_xml = set()
    for nation in root.iter('NATION'):
        name = nation.find('NAME').text
        names_in_xml.add(name)

    cards = {}

    for name in card_names:
        cards[name] = 'false' if name in names_in_xml else 'true'

    with open(f'data/{todays_date}-cards.json', 'w') as json_file:
        json.dump(cards, json_file, indent=2)

    for xml_file in xml_files:
        file_date = xml_file.split('-R')[0]
        if file_date < previous_date:
            os.remove(os.path.join('data', xml_file))

main()
