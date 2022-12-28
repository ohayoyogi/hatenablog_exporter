
from dataclasses import dataclass
import xml.etree.ElementTree as ET
import requests
from urllib.parse import urljoin

from .auth import WSSEAuthenticator


NS_W3C_ATOM = "http://www.w3.org/2005/Atom"
NS_W3C_APP = "http://www.w3.org/2007/app"

NS_ATOM = {
    "atom": NS_W3C_ATOM,
    "app": NS_W3C_APP
}


class TAG:
    class ATOM:
        ID = str(ET.QName(NS_W3C_ATOM, "id"))
        TITLE = str(ET.QName(NS_W3C_ATOM, "title"))
        CONTENT = str(ET.QName(NS_W3C_ATOM, "content"))
        LINK = str(ET.QName(NS_W3C_ATOM, "link"))
        CATEGORY = str(ET.QName(NS_W3C_ATOM, "category"))

    class APP:
        CATEGORIES = str(ET.QName(NS_W3C_APP, "categories"))


@dataclass
class HatenaBlogArticle:
    id: str
    title: str
    content: str
    links: list[dict]

    @classmethod
    def parseelement(cls, elem: ET.Element):
        def gettext(e: ET.Element | None, d: str = ""):
            return e.text or d if e is not None else d

        elem_id = elem.find(TAG.ATOM.ID)
        elem_title = elem.find(TAG.ATOM.TITLE)
        elem_content = elem.find(TAG.ATOM.CONTENT)
        elem_link = elem.findall(TAG.ATOM.LINK)

        return HatenaBlogArticle(
            id=gettext(elem_id),
            title=gettext(elem_title),
            content=gettext(elem_content),
            links=[e.attrib for e in elem_link]
        )


class HatenaBlog:
    def __init__(self, hatena_id: str, api_key: str, blog_id: str) -> None:
        self.auth = WSSEAuthenticator(hatena_id, api_key)
        self.hatena_id = hatena_id
        self.blog_id = blog_id
        self.base_url = f"https://blog.hatena.ne.jp/{hatena_id}/{blog_id}/"

    def composeurl(self, path: str):
        return urljoin(self.base_url, path)

    def getcategories(self):
        url = self.composeurl("atom/category")
        key, val = self.auth.generateheader()
        res = requests.get(url, headers={key: val}, timeout=30)

        tree = ET.fromstring(res.text)
        elem_categories = tree.findall(f'{TAG.ATOM.CATEGORY}')
        return [e.attrib.get('term') for e in elem_categories]

    def getall(self, depth: int):

        def parse(body: str) -> tuple[str | None, list[HatenaBlogArticle]]:
            tree = ET.fromstring(body)
            entries = []

            elem_next_link = tree.find('atom:link[@rel="next"]', NS_ATOM)
            if elem_next_link is not None:
                next_href = elem_next_link.attrib.get('href')
            else:
                next_href = None

            entries = tree.findall('atom:entry', NS_ATOM)

            return (next_href, [HatenaBlogArticle.parseelement(i) for i in entries])

        # load all entry
        next_href = self.composeurl("atom/entry")
        all_entries: list[HatenaBlogArticle] = []
        cnt = 0
        while next_href is not None:
            key, val = self.auth.generateheader()
            res = requests.get(next_href, headers={
                key: val
            }, timeout=30)
            (next_href, entries) = parse(res.text)
            all_entries += entries
            cnt += 1
            if depth >= 0 and cnt > depth:
                break

        return all_entries
