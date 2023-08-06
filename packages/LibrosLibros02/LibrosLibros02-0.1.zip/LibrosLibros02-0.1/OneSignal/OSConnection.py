import json

import OneSignal.OSHeader
import OneSignal.OSPayload
import OneSignal.OSResponse
import requests


class OSConnection:

    def __init__(self):
        self.oneSignalUrl = "https://onesignal.com/api/v1/notifications"
        self.appId = "7d02bfcd-e065-42a3-9949-21506a47f788"
        self.header = OneSignal.OSHeader.OSHeader()
        self.payload = OneSignal.OSPayload.OSPayload(self.appId)
        self.response = OneSignal.OSResponse.OSResponse()

    def createNotification(self):
        req = requests.post(self.oneSignalUrl, headers=self.header.getHeader(), data=json.dumps(self.payload.getPayload()))
        print("POST: ",req.status_code, req.reason)
        self.response.response = req.json()
        return self.response

    def cancelNotification(self, notificationId):
        req = requests.delete(self.oneSignalUrl + "/"+notificationId+"?app_id="+self.appId, headers=self.header.getHeader())
        print("DELETE: ",req.status_code, req.reason)
        self.response.response = req.json()
        return self.response