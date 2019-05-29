import json
import sys

from consolemenu import ConsoleMenu, SelectionMenu
from consolemenu.items import FunctionItem, SubmenuItem, ExternalItem

class Project(object):

    def __init__(self, name='', description=''):
        self.name = name
        self.description = description
        self.related = []
        self.notes = []
        self.structure = {}

    def save(self):
        with open(self.name+'_websidis.json', 'w') as file_project:
            project = {'name':self.name, 'description':self.description, 
                       'related':self.related, 'notes':self.notes, 'structure':self.structure}

            json.dump(project, file_project)

    def load(self, path):
        with open(path) as file_project:
            project = json.load(file_project)
            self.name = project['name']
            self.description = project['description']
            self.related = project['related']
            self.notes = project['notes']
            self.structure = project['structure']

    def add(self, where, what):
        if where == 'note':
            self.notes.append(what)
        elif where == 'related':
            self.related.append(what)

    def rem(self, where, what):
        try:
            if where == 'note':
                self.notes.pop(what) #pop works properly
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
            self.structure[url] = {} #UPDATE in 0.0.2
    
    def remPage(self, url):
        try: 
            self.structure.pop(url)
        except KeyError:
            return -1

    def addArg(self, url, method, key, value): #UPDATE in 0.0.2
        try:
            self.structure[url]
        except KeyError:
            return -1
        try:
            self.structure[url][method].append((key,value))
        except KeyError:
            self.structure[url][method] = []
            self.structure[url][method].append((key,value))
    
    def remArg(self, url, method, paramID): #paramID is a number of param for URL
        try:
            self.structure[url][method].pop(paramID)
        except KeyError:
            return -1

    def changeArg(self, url, method, paramID, key, value):
        try:
            self.structure[url][method][paramID] = (key,value)
        except KeyError:
            return -1

    def show(self, what): #Show function is working properly! Structure: {'url':{'method1':[(key,value),(key,value)], 'method2':[(key,value),(key,value)]}}
        toShow = ''
        if what == 'notes':
            for i in enumerate(self.notes):
                toShow += (str(i[0])+') '+i[1]+'\n\r')
        elif what == 'meta':
            toShow = self.name+'\n\r'+self.description+'\n\r'
        elif what == 'related':
            for i in enumerate(self.related):
                toShow += (str(i[0])+') '+i[1]+'\n\r')
        elif what == 'structure':
            for urlView in self.structure.items():
                toShow+=urlView[0]+'\n\r' #print url 
                for methodView in urlView[1].items():
                    toShow+='    '+methodView[0]+'\n\r'
                    for paramPair in enumerate(methodView[1]):
                        toShow+='        '+str(paramPair[0])+') '+paramPair[1][0]+': '+paramPair[1][1]+'\n\r'

        return toShow


#this is not related to the framework itself and is only needed to enpower console interface
class ConsoleInterfaceWrapper(object):

    def __init__(self, project):
        self.project = project

    def wrapAddNote(self):
        text = input('Text:')
        self.project.add('note', text)

    def wrapAddRelated(self):
        text = input('URL:')
        self.project.add('related', text)

    def wrapRemNote(self):
        print(self.project.show('notes'))
        NoteID = input('Note ID:')
        try:
            self.project.rem('note', int(NoteID))
        except ValueError:
            return -1

    def wrapRemRelated(self):
        print(self.project.show('related'))
        UrlID = input('URL ID:')
        try:
            self.project.rem('related', int(UrlID))
        except ValueError:
            return -1

    def wrapChangeMeta(self):
        name = input('Name: ')
        description = input('Description: ')
        self.project.change(name, description)

    def wrapAddPage(self):
        url = input("URL: ")
        self.project.addPage(url)

    def wrapRemPage(self):
        print(self.project.show('structure'))
        UrlID = input("URL ID: ")
        try:
            self.project.remPage(int(UrlID))
        except ValueError:
            return -1

    def wrapAddArg(self):
        url = input("For Page: ")
        method = input("For method: ")
        key = input("Parameter name: ")
        value = input("Parameter value: ")
        self.project.addArg(url, method, key, value)

    def wrapRemArg(self):
        print(self.project.show('structure'))
        url = input("For Page: ")
        method = input("For method: ")
        pid = input('Parameter ID: ')
        self.project.remArg(url, method, int(pid))

    def wrapChangeArg(self):
        print(self.project.show('structure'))
        url = input("For Page: ")
        method = input("For method: ")
        pid = input("Parameter ID: ")
        key = input("Parameter name: ")
        value = input("Parameter value: ")
        self.project.changeArg(url, method, int(pid), key, value)

    def wrapShow(self, what):
        try:
            print(self.project.show(what))
        except:
            print(sys.exc_info())
        input('Press any key to back')

    def wrapSave(self):
        self.project.save()


if __name__ == "__main__":

    discovering_website = Project()
    load_or_new = input('Do you want to load a project from disk? (y/n) ')
    if load_or_new == 'y':
        path = input('Path: ')
        discovering_website.load(path)
    else:
        name = input('Name: ')
        description = input('Description: ')
        discovering_website = Project(name, description)

    interface = ConsoleInterfaceWrapper(discovering_website)


    m_main = ConsoleMenu('WebSiDis console interface')

    m_notes = ConsoleMenu('Notes')
    m_notes.append_item(FunctionItem('Add new note', interface.wrapAddNote))
    m_notes.append_item(FunctionItem('Remove existed note', interface.wrapRemNote))
    m_notes.append_item(FunctionItem('Show notes', interface.wrapShow, ['notes']))

    m_related = ConsoleMenu('Sites')
    m_related.append_item(FunctionItem('Add new related site', interface.wrapAddRelated))
    m_related.append_item(FunctionItem('Remove existed related site', interface.wrapRemRelated))
    m_related.append_item(FunctionItem('Show related sites', interface.wrapShow, ['related']))

    m_structure = ConsoleMenu('Structure')
    m_structure.append_item(FunctionItem('Add new page', interface.wrapAddPage))
    m_structure.append_item(FunctionItem('Remove page', interface.wrapRemPage))
    m_structure.append_item(FunctionItem('Add parameter to page', interface.wrapAddArg))
    m_structure.append_item(FunctionItem('Remove parameter from page', interface.wrapRemArg))
    m_structure.append_item(FunctionItem('Change parameter on page',interface.wrapChangeArg))
    m_structure.append_item(FunctionItem('Show structure', interface.wrapShow, ['structure']))

    m_main.append_item(SubmenuItem('Notes', m_notes, menu=m_main))
    m_main.append_item(SubmenuItem('Related sites', m_related, menu=m_main))
    m_main.append_item(SubmenuItem('Structure', m_structure, menu=m_main))
    m_main.append_item(FunctionItem('Save project', interface.wrapSave))

    m_main.show()

