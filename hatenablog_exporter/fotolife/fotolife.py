import xml.etree.ElementTree as ET
from urllib.parse import urljoin

NS_DC = "http://purl.org/dc/elements/1.1/"
NS_ATOM = "http://purl.org/atom/ns#"


class TAG:
    class ATOM:
        ENTRY = str(ET.QName(NS_ATOM, "entry"))
        TITLE = str(ET.QName(NS_ATOM, "title"))
        CONTENT = str(ET.QName(NS_ATOM, "content"))
        GENERATOR = str(ET.QName(NS_ATOM, "generator"))

    class DC:
        CATEGORY = str(ET.QName(NS_DC, "category"))


class HatenaFotolife:
    def __init__(self, base_url: str = "http://f.hatena.ne.jp/"):
        self.base_url = base_url

    def composeurl(self, path: str):
        return urljoin(self.base_url, path)

    def post(self, title: str, content_type: str, base64img: str, folder: str = None, tool_name: str = None):
        """
        Post new picture (POST /atom/post)
        """
        root = ET.Element(TAG.ATOM.ENTRY)
        elem_title = ET.SubElement(root, TAG.ATOM.TITLE)
        elem_title.text = title
        elem_content = ET.SubElement(root, TAG.ATOM.CONTENT, {
                                     "mode": "base64", "type": content_type})
        elem_content.text = base64img
        if folder:
            elem_subject = ET.SubElement(root, TAG.DC.CATEGORY)
            elem_subject.text = folder
        if tool_name:
            elem_generator = ET.SubElement(root, TAG.ATOM.GENERATOR)
            elem_generator.text = folder

    def get(self, id: str):
        """
        Get feed (GET /atom/edit/XXXXXXXXXXXX)
        """
        pass

    def put(self, id: str):
        """
        Edit the picture (PUT /atom/edit/XXXXXXXXXXXX)
        """
        pass

    def delete(self, id: str):
        """
        Delete the picture (Delete /atom/edit/XXXXXXXXXXXX)
        """
        pass

    def getall(self):
        """
        Get feed (GET /atom/feed) 
        """
        pass


a = HatenaFotolife()
a.post("Hoge", "folder", "hoge", "Fua")
