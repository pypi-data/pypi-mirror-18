class OSPayload:


    def __init__(self, appId):
        self.appId = appId

    def getPayload(self):
        payload = {"app_id": self.appId,
               "included_segments": ["All"],
               "contents": {"en": "English Message"}}
        return payload