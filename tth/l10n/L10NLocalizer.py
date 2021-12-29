badAttrs = ("languages","_sleeve","buildDB","db","module","sc_buildDB","sc_db",
            "cog_buildDB","cog_db","sc_fetch","cog_fetch","getSleeveTexture","tip",
            "cogSpeechAI","setLanguage","language","buildName")

def getModule(language):
    print ':L10N: Running in language: %s' % language
    l = {}
    g = {}
    m = __import__('tth.l10n.L10NLocalizer'+language.title(), g, l, ['tth.l10n'])
    
    for x in dir(m):
        if x.startswith('__'): pass
        if x in badAttrs:
            raise AttributedError("%s defines a non-allowed symbol: %s" % ('L10NLocalizer'+language.title(),x))
    
    return (m,g,l)