import base64
import os
import requests
import sys
from pathlib import Path

import xml.etree.ElementTree as ET

NS_ATOM = {"atom": "http://www.w3.org/2005/Atom"}

def parse(body: str) -> str | None:
    tree = ET.fromstring(body)
    entries = []

    elem_next_link = tree.find('atom:link[@rel="next"]', NS_ATOM)
    if elem_next_link is not None:
        next_href = elem_next_link.attrib.get('href')
    else:
        return None

    for i in tree:
        print(i)
    entries = tree.findall('atom:entry', NS_ATOM)

    for i in entries:
        for j in i:
            print(j)
        print(i.find('atom:title', NS_ATOM).text)
        print(i.find('atom:content', NS_ATOM).text)
        for j in i.findall('atom:link', NS_ATOM):
            print(j.attrib)
    print(entries)

    return (next_href, entries)

def main(hatena_id: str, password: str, blog_id: str):
    output_dir = Path(os.getcwd()) / "out"

    os.makedirs(str(output_dir), exist_ok=True )

    credential = base64.b64encode((hatena_id + ":" + password).encode()).decode()
    authorization = f'Basic {credential}'
    print(authorization)


    # load all entry
    next_href = f'https://blog.hatena.ne.jp/{hatena_id}/{blog_id}/atom/entry'
    all_entries = []
    while next_href is not None:
        print(next_href)
        res = requests.get(next_href, headers={
            "Authorization": authorization
        }, timeout=30)
        (next_href, entries) = parse(res.text)
        all_entries += entries
        break
    return str(output_dir)

if __name__ == '__main__':
    if len(sys.argv) < 4:
        sys.exit(1)
    print(sys.argv)
    print('Hoge')
    main(sys.argv[1], sys.argv[2], sys.argv[3])
