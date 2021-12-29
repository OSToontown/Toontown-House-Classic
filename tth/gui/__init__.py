from panda3d.core import TextNode

def UnicodeText(text,parent,pos=(0,0,0),scale=.1,fg=(0,0,0,1),align=0,font=None,enc="latin-1"):
            Text = TextNode('unicodetext')
            if font: Text.setFont(font)
            Text.setAlign(align)
            Text.setWtext(unicode(text))
            TextNp = parent.attachNewNode(Text)
            TextNp.setPos(pos)
            TextNp.setColor(fg)              
            TextNp.setScale(scale)
            
            return (Text,TextNp)
            
