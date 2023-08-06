import json

import OneSignal.OSHeader
import OneSignal.OSPayload
import OneSignal.OSResponse
import requests

from OneSignal.OSPayload import OSPayload


class OSConnection:

    def __init__(self):
        with open("OneSignal/OneSignal.config") as f:
            content = f.readlines()
        content = [x.strip('\n') for x in content]

        self.oneSignalUrl = content[0]
        self.authToken = content[1]
        self.app_id = content[2]

        self.header = OneSignal.OSHeader.OSHeader(self.authToken)
        self.payload = None
        self.response = OneSignal.OSResponse.OSResponse()

    def createNotification(self, osPayload):
        self.payload = osPayload
        self.payload.app_id = self.app_id
        jsonPayload = json.dumps(self.payload.__dict__, default=OSPayload.encodeFilters, indent=4, sort_keys=True)
        print(jsonPayload)
        req = requests.post(self.oneSignalUrl, headers=self.header.getHeader(), data=jsonPayload)
        print("POST: ",req.status_code, req.reason)
        self.response.response = req.json()
        return self.response

    def cancelNotification(self, notificationId):
        req = requests.delete(self.oneSignalUrl + "/"+notificationId+"?app_id="+self.app_id, headers=self.header.getHeader())
        print("DELETE: ",req.status_code, req.reason)
        self.response.response = req.json()
        return self.response