import requests
import os
import gzip
from io import BytesIO
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
import json

todays_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

def element_to_dict(element, approved_keys, list_key):
    result = {}
    for child in element:
        child_data = element_to_dict(child, approved_keys, list_key)
        if child_data:
            if child.tag in result:
                if type(result[child.tag]) is list:
                    result[child.tag].append(child_data)
                else:
                    result[child.tag] = [result[child.tag], child_data]
            else:
                result[child.tag] = child_data
        else:
            if child.tag in approved_keys:
                if child.tag == list_key:
                    embassies_data = []
                    for sub_child in child:
                        embassies_data.append(sub_child.text)
                    result[list_key] = ",".join(str(embassy) for embassy in embassies_data)
                else:
                    result[child.tag] = child.text
    return result

def download_and_save_xml(url, output_file, approved_keys, iter_str, list_key):
    response = requests.get(url, headers={'User-Agent': 'Kractero'})
    if response.status_code == 200:
        with gzip.GzipFile(fileobj=BytesIO(response.content)) as gzipped_file:
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

        xml_dict = element_to_dict(root, approved_keys, list_key)
        json_data = json.dumps(xml_dict, indent=4)
        with open(output_file.replace(".xml", ".json"), 'w') as json_file:
            json_file.write(json_data)
        print(f'JSON file downloaded and saved successfully: {output_file}')
    else:
        print(f'Failed to fetch dump from NationStates with status {response.status_code}')

def main():
    todays_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    download_and_save_xml('https://www.nationstates.net/pages/regions.xml.gz', f'data/{todays_date}-RegionsTest.xml', ("NAME", "NUMNATIONS", "DELEGATEVOTES", "DELEGATEAUTH", "LASTUPDATE", "FACTBOOK", "EMBASSIES"), "REGION", "EMBASSIES")
    download_and_save_xml('https://www.nationstates.net/pages/nations.xml.gz', f'data/{todays_date}-NationsTest.xml', ("NAME", "ENDORSEMENTS", "LASTACTIVITY"), "NATION", "ENDORSEMENTS")
    previous_date = (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d')

    xml_files = os.listdir('data')

    for xml_file in xml_files:
        file_date = xml_file.split('-R')[0]
        if file_date < previous_date:
            os.remove(os.path.join('data', xml_file))
    
main()