import base64, os

class SessionStore:
    
    def __init__(self):
        self.sessions = {}    #dictionary: keys are session ID, values are dictionaries

    def generateSessionId(self):
        rnum = os.urandom(32)
        rstr = base64.b64encode(rnum).decode("utf-8")
        return rstr

    def createSession(self):
        sessionId = self.generateSessionId()
        self.sessions[sessionId] = {}
        return sessionId
    
    def getSessionData(self, sessionId):
        #dictionary inside of dictionary.
        #make sure that the sessionId is valid first.
        if sessionId in self.sessions:
            return self.sessions[sessionId]
        else:
            return None
    
    #optional
    def setSessionData(self, sessionId, data):
        pass
