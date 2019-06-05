from bge import logic
from widgets import Widget
import textwrap

class Text(Widget):
    def __init__(self, txtObj, text="", width=None, limit=None):
        super(Text, self).__init__(txtObj)
        self.txtObj = txtObj
        self.width = width
        self.limit = limit
        self.text = text
        self.setText(text)

    def setText(self, text):
        if not self.isParentEnabled():
            return

        if self.limit and len(text) > self.limit:
            text = '%s...' % text[:self.limit]
        
        if self.width:
            text = textwrap.fill(width=self.width,text=text)

        self.txtObj['Text'] = text
        self.text = text

    def tabSpaces(self, units):
        txtspace = '{:>%s}' % units
        txt = txtspace.format(self.text)
        self.setText(txt)