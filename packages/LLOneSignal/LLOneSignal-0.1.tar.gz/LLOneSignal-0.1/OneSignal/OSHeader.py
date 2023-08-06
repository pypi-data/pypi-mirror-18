class OSHeader:

    def __init__(self, authToken):
        self.contentType = "application/json; charset=utf-8"
        self.authorization = "Basic " + authToken

    def getHeader(self):
        header = { "Content-Type": self.contentType, "Authorization": self.authorization }
        return header