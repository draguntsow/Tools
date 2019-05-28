import json
import sys
from consolemenu import ConsoleMenu, SelectionMenu
from consolemenu.items import FunctionItem, SubmenuItem, ExternalItem

class Project(object):

    def __init__(self, name, description=''):
        self.name = name
        self.description = description
        self.related = []
        self.notes = []
        self.structure = {}

    def add(self, where, what):
        if where == 'note':
            self.notes.append(what)
        elif where == 'related':
            self.related.append(what)

    def rem(self, where, what):
        try:
            if where == 'note':
                self.notes.pop(what)
            elif where == 'related':
                self.related.pop(what)
        except IndexError:
            return -1

    def change(self, what, to):
        if what == 'name':
            self.name = to
        elif what == 'desc':
            self.description = to

    def addPage(self, url):
        if url in self.structure:
            return -1
        else:
            self.structure[url] = []
    
    def remPage(self, url):
        try: 
            del self.structure[url]
        except KeyError:
            return -1

    def addArg(self, param, url): #param is a tuple from name and value 
        try:
            self.structure[url].append(param)
        except KeyError:
            return -1
    
    def remArg(self, paramID, url): #paramID is a number of param for URL
        try:
            self.structure[url].pop(paramID)
        except KeyError:
            return -1

    def changeArg(self, paramID, param, url): #param is tuple
        try:
            self.structure[url][paramID] = param
        except KeyError:
            return -1

    def show(self, what):
        toShow = ''
        if what == 'notes':
            for i in enumerate(self.notes):
                toShow += (i[0]+') '+i[1])
        elif what == 'meta':
            toShow = self.name+'\n\r'+self.description
        elif what == 'related':
            for i in enumerate(self.related):
                toShow += (i[0]+') '+i[1])
        elif what == 'structure':
            for urlView in self.structure.items:
                toShow+=urlView[0]+'\n\r'
                for param in enumerate(urlView[1]):
                    toShow+='    '+param[0]+') '+param[1][0]+': '+param[1][1]+'\n\r'

        return toShow


class ConsoleInterfaceWrapper(object):
    def wrap(self, funct):
        pass

if __name__ == "__main__":

    name = input('Name: ')
    description = input('Description: ')

    TestWebSite = Project(name, description)


    m_main = ConsoleMenu('WebSiDis console interface')

    m_notes = ConsoleMenu('Notes')
    m_notes.append_item(FunctionItem('Add new note',tinput))
    m_notes.append_item(FunctionItem('Remove existed note',tinput))

    m_related = ConsoleMenu('Sites')
    m_related.append_item(FunctionItem('Add new related site',tinput))
    m_related.append_item(FunctionItem('Remove existed related site',tinput))

    m_structure = ConsoleMenu('Structure')
    m_structure.append_item(FunctionItem('Add new page',tinput))
    m_structure.append_item(FunctionItem('Add parameter to page',tinput))
    m_structure.append_item(FunctionItem('Remove parameter from page',tinput))
    m_structure.append_item(FunctionItem('Change parameter on page',tinput))

    m_main.append_item(SubmenuItem('Notes', m_notes, menu=m_main))
    m_main.append_item(SubmenuItem('Related sites', m_related, menu=m_main))
    m_main.append_item(SubmenuItem('Structure', m_structure, menu=m_main))

    m_main.show()

