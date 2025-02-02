from xml.etree import ElementTree as ET
from functools import partial
from typing import List, Callable

XML_NAMESPACE = '{http://www.w3.org/XML/1998/namespace}'

def get_text(elem: ET.Element):
    return ''.join(elem.itertext())

def apply_to_all_text(elem: ET.Element, fun: Callable[[str], str], 
                      include_tail: bool = False):
    if elem.text:
        elem.text = fun(elem.text)
    if include_tail and elem.tail:
        elem.tail = fun(elem.tail)
    for child in elem:
        apply_to_all_text(child, fun, include_tail=True)
        
def update_tmx(original_tmx_file: str,
               text_update_rules: List[Callable[[str, str], str]]):

    updated_tmx_file = original_tmx_file.rstrip('.tmx') + '.updated.tmx'

    tree = ET.parse(original_tmx_file)
    root = tree.getroot()
    body = root.find('body')
                 
    # Calling the choice for filter and update functions, and the counter for deleted TUs (NP 03.2022)
    # src_match = ask_src()
    src_removed = 0
                 
    for i, tu in enumerate(body):
      
        assert tu.tag == 'tu', '<body> may only contain <tu> elements.'
        
        for tuv in tu.findall('tuv'):
            lang_code = tuv.attrib[f"{XML_NAMESPACE}lang"]
            segment = tuv.find('seg')
        
      # Searching in the property "Quelle" for given match (NP 03.2022)
        """for tu in body.findall('tu'):
            for prop in tu.findall('prop'):
                if prop.attrib['type'] == 'x-Quelle:SingleString':
                    source = prop.text
                    if source == src_match:
                        src_removed += 1
                        body.remove(tu)  """                 
                
      # Apply the updates rules according to user's choice (original by SL, modified by NP 03.2022)"""
        for text_update_rule in text_update_rules:
            text_update_rule_with_langcode = partial(text_update_rule, lang_code)
            apply_to_all_text(segment, text_update_rule_with_langcode)    

      
    print(f"Original file {original_tmx_file} contained {i} translation units. {i - src_removed} stored in {updated_tmx_file} ({src_removed} removed because of the source).") 
                 
    tree.write(updated_tmx_file, encoding="utf-8", xml_declaration=True)        

