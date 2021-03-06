from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
import re

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Speedvid'
        self.__sFileName = self.__sDisplayName
        self.__sHD = ''

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]'+self.__sDisplayName+'[/COLOR] [COLOR khaki]'+self.__sHD+'[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'speedvid'

    def setHD(self, sHD):
        self.__sHD = ''

    def getHD(self):
        return self.__sHD

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return '';
        
    def __getIdFromUrl(self, sUrl):
        sPattern = "http://speedvid.net/([^<]+)"
        oParser = cParser()
        aResult = oParser.parse(sUrl, sPattern)
        if (aResult[0] == True):
            return aResult[1][0]

        return ''

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
    
        oRequest = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequest.request()

        oParser = cParser()
        
        #sPattern = '(eval\(function\(p,a,c,k,e(?:.|\s)+?\))<\/script>'
        sPattern = '(eval\(function\(p,a,c,k,e(?:.|\s)+?\)\)\))'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            for packed in aResult[1]:
                sHtmlContent = cPacker().unpack(packed)
                sHtmlContent = sHtmlContent.replace('\\','')
                if not 'http://www.speedvid.net/hgcd06yxp6hf' in sHtmlContent:
                    break
                
            sPattern = "{file:.([^']+.mp4)"
            aResult = oParser.parse(sHtmlContent, sPattern)
            if (aResult[0] == True):
                api_call = aResult[1][0]

            
        if (api_call):
            return True, api_call
            
        return False, False
