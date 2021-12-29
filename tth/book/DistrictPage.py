from BookPage import *
from direct.showbase.DirectObject import DirectObject

class DistrictPage(BookPage,DirectObject):
    def setup(self):
        self.titletext = OnscreenText(text=L10N('BOOK_DIST'),pos=(0,.57),scale=.15,font=BTFont,parent=self.frame)
        
        self.explaintext = OnscreenText(text=L10N('BOOK_DIST_ABOUT'),pos=(.035,.35),parent=self.frame,
                                        align=TextNode.ALeft,scale=.056,wordwrap=.7/.056,font=BTFont)
        
        g_up = (getFriendGuiItem('llUp'),getFriendGuiItem('llUp_'),getFriendGuiItem('llUp_'),getFriendGuiItem('llDN'))
        g_down = (getFriendGuiItem('llUp'),getFriendGuiItem('llUp_'),getFriendGuiItem('llUp_'),getFriendGuiItem('llDN'))
                      
        for g in g_down: g.setP(180)
        
        self.dist_list = DirectScrolledList(parent=self.frame,pos=(-.55,0,.45),
                                        numItemsVisible=16,itemFrame_frameColor=(1,0.0,0.0,1),
                                        decButton_geom = g_up,incButton_geom = g_down,
                                        decButton_relief = None,incButton_relief = None,
                                        decButton_pos = (0,0,.1),incButton_pos = (0,0,-1.05),
                                        #decButton_scale = .6,incButton_scale = .6,
                                        decButton_clickSound=gamebase.sounds['GUI_click'],
                                        decButton_rolloverSound=gamebase.sounds['GUI_rollover'],
                                        incButton_clickSound=gamebase.sounds['GUI_click'],
                                        incButton_rolloverSound=gamebase.sounds['GUI_rollover'],
                                        frameColor=(.9,.9,1,1),frameSize = (-.35, .35, -1, .05))
                                        
        self.dl_items = []
        
        for i,name in enumerate(base.distMgr.names[1:]):
            l = DirectLabel(text = unicode(name.decode('latin-1')),text_scale=(.06),text_align=TextNode.ALeft,
                            frameColor = (0,0,0,0), state=DGG.NORMAL, text_font=BTFont,text_pos=(-.35,0))
            l.bind(DGG.B1PRESS,lambda *a:0)
            l.bind(DGG.WITHIN,self.dist_highlight,[1,i])
            l.bind(DGG.WITHOUT,self.dist_highlight,[0,i])
            l.bind(DGG.B1PRESS,self.dist_go,[i])
            self.dist_list.addItem(l)

            self.dl_items.append(l)
            
            if i+1 == base.distMgr.district:
                self.dist_highlight(1,i,0)
                self.dist_list.selectListItem(l)  
        
        self.accept('shardUpdate',self._update) 
        messenger.send('forceShardUpdate')
        
    def _update(self,sid,toons):
        try:
            i = self.dl_items[sid-1]
            t = i['text'].split()
            
            if t[-1].startswith('('): t.pop()
            
            t = ' '.join(t)
            
            nt = t+' (%s)'%toons
            i['text'] = nt
            
        except: pass

    def dist_highlight(self,hg,index,event):
        self.dl_items[index]['text_fg'] = ((0,0,0,1),(.6,.8,.7,1))[hg]
        
    def dist_go(self,index,event):
        self.book.close(tpRequest = (str(base.distMgr.goToWithMovie(index+1)),))
        
    def destroy(self):  
        BookPage.destroy(self)
        self.ignoreAll()
