from collections import OrderedDict

class Filterable:
    """Extends functionality of the structure returned by xmltodict. Usage example:
    >>> xmld = Filterable(xmltodict.parse(xml))
    >>> xmld['Project']['Item', '@Name', 'foobar']['Action', '@Type', 'Build']['#text']
    """
    def __init__(self, items):
        self.items = items if isinstance(items, list) else [items]
        
    def __getitem__(self, index):
        if isinstance(index, tuple):
            if len(index) == 2:
                condition = index[1]
            elif len(index) == 3:
                condition = lambda item: item[index[1]] == index[2]
            sel = self.items[0][index[0]]
            sel = sel if isinstance(sel, list) else [sel]
            filtered = list(filter(condition, sel))
            return Filterable(filtered)
        else:
            item = self.items[0][index] 
            if type(item) in (OrderedDict, list):
                return Filterable(item)
            else:
                return item
                
        return Filterable(res)

    def __setitem__(self, index, value):
        self.items[0][index] = value

    def append(self, item):
        self.items.append(item)
