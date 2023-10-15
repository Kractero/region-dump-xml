import requests
import os
import gzip
from io import BytesIO
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET

def download_and_save_xml(xml_content, output_file, approved_keys, iter_str):
    root = ET.fromstring(xml_content)
    for iterable in root.iter(iter_str):
        for element in list(iterable):
            if element.tag not in approved_keys:
                iterable.remove(element)

    filtered_xml_text = ET.tostring(root)
    with open(output_file, 'wb') as xml_file:
        xml_file.write(filtered_xml_text)
    print(f'XML file saved successfully: {output_file}')

def main():
    todays_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

    # Download regions
    region_response = requests.get('https://www.nationstates.net/pages/regions.xml.gz', headers={'User-Agent': 'Kractero'})
    if region_response.status_code == 200:
        with gzip.GzipFile(fileobj=BytesIO(region_response.content)) as gzipped_file:
            download_and_save_xml(gzipped_file.read(), f'data/{todays_date}-Regions.xml', ("NAME", "NUMNATIONS", "DELEGATEVOTES", "DELEGATEAUTH", "LASTUPDATE", "FACTBOOK", "EMBASSIES"), "REGION")
    else:
        print(f'Failed to fetch regions data with status {region_response.status_code}')

    # Download nations
    nation_response = requests.get('https://www.nationstates.net/pages/nations.xml.gz', headers={'User-Agent': 'Kractero'})
    if nation_response.status_code == 200:
        with gzip.GzipFile(fileobj=BytesIO(nation_response.content)) as gzipped_file:
            xml_content = gzipped_file.read()
            download_and_save_xml(xml_content, f'data/{todays_date}-Nations.xml', ("NAME", "ENDORSEMENTS"), "NATION")
            download_and_save_xml(xml_content, f'data/{todays_date}-Nations-LL.xml', ("NAME", "LASTLOGIN"), "NATION")
    else:
        print(f'Failed to fetch nations data with status {nation_response.status_code}')

    previous_date = (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d')

    xml_files = os.listdir('data')

    for xml_file in xml_files:
        file_date = xml_file.split('-R')[0]
        if file_date < previous_date:
            os.remove(os.path.join('data', xml_file))

if __name__ == "__main__":
    main()
