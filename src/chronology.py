"""Sort only dated activity groups; retain editorial order when dates are unknown."""
import re

def date_key(value):
    text=str(value or '')
    date=re.search(r'(?:(\d{1,2})\.\s*[–-]\s*)?(\d{1,2})\.(\d{2})\.(\d{4})',text)
    if date:return (int(date[4]),int(date[3]),int(date[1] or date[2]))
    month=re.search(r'(?<![\d.])(\d{1,2})\.((?:19|20)\d{2})(?!\d)',text)
    if month and 1<=int(month[1])<=12:return (int(month[2]),int(month[1]),0)
    year=re.search(r'(?<!\d)(?:19|20)\d{2}(?!\d)',text)
    return (int(year[0]),0,0) if year else (0,0,0)

def record_key(node):
    return (bool(node.get('is_new')), *date_key(node.get('sort_date') or node.get('meta')))

def sort_records(records):
    labels=('Publikāc','Projekt','Uzstāšan','Datu kop','Ziņojum','Publicitāt','Raksti kultūras','Dokumentālā')
    for node in records.values():
        for label,ids in node.get('groups',[]):
            if label.startswith(labels):ids.sort(key=lambda id:record_key(records[id]),reverse=True)
    return records
