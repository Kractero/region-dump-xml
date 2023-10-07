import Pako from "pako";
import { XMLParser } from "fast-xml-parser";
import { writeFileSync } from "fs";

async function dump(url, filename) {
  const response = await fetch(url,
      {
      headers: {
          'User-Agent': "Kractero"
      }
  });

  const blob = await response.blob();

  const gzippedData = await blob.arrayBuffer();
  const inflate = new Pako.Inflate();
  inflate.push(new Uint8Array(gzippedData), true);

  const xmlText = new TextDecoder().decode(inflate.result);
  const date = new Date();
  date.setDate(date.getDate()-1);
  writeFileSync(`data/${date.toISOString().slice(0, 10)}${filename}.xml`, xmlText);
}

await dump("https://www.nationstates.net/pages/regions.xml.gz", "-Regions")
