class OSHeader:

    def __init__(self):
        self.contentType = "application/json; charset=utf-8"
        self.authorization = "Basic NTI1NDBlMTItNzZiZS00ZDhkLTgxM2EtMjE0YzQ3YjI2NWM5"

    def getHeader(self):
        header = { "Content-Type": self.contentType, "Authorization": self.authorization }
        return header