import os
import sys
import string
import random
import base64
import requests
from random_user_agent.user_agent import UserAgent

if sys.platform == "linux":
    clear = lambda: os.system("clear")
else:
    clear = lambda: os.system("cls")

class Misc:

    def discord_headers():
        fingerprint = requests.get("https://discord.com/api/v9/experiments").json()["fingerprint"]
        ua = UserAgent(limit=100).get_random_user_agent()
        super = base64.b64encode(str({
            "os": "Windows",
            "browser": "Chrome",
            "device": "",
            "system_locale": "en-US",
            "browser_user_agent": ua,
            "browser_version": "91.0.4472.101",
            "os_version": "10",
            "referrer": f"https://discord.com/register",
            "referring_domain": "",
            "referrer_current": "",
            "referring_domain_current": "",
            "release_channel": "stable",
            "client_build_number": 87598,
            "client_event_source": None
        }).encode()).decode()
        return {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US",
            "authorization": "undefined",
            "content-length": None,
            "content-type": "application/json",
            "origin": "https://discord.com",
            "referer": "https://discord.com/register",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "sec-gpc": "1",
            "user-agent": ua,
            "x-fingerprint": fingerprint,
            "x-super-properties": super,
        }

class Capmonster:

    def __init__(self, apikey: str, **options):
        self.apikey = apikey
        self.config = options
        self.session = requests.session()

        if self.config.get("host") is None:
            raise KeyError("\"host\" is a required argument.")
        if self.config.get("sitekey") is None:
            raise KeyError("\"sitekey\" is a required argument.")

        self.host = self.config.get("host") 
        self.sitekey = self.config.get("sitekey")

    def _balance(self):
        try:
            json = {
                "clientKey": self.apikey
            }
            r = self.session.post("https://api.capmonster.cloud/getBalance", json=json)
            if r.json()["errorId"] == 0:
                return r.json()["balance"]
            else:
                return
        except Exception:
            return

    def _new_task(self):
        try:
            json = {
                "clientKey": self.apikey,
                "task": {
                    "type": "HCaptchaTaskProxyless",
                    "websiteURL": self.host,
                    "websiteKey": self.sitekey,
                    "minScore": 0.5
                }
            }
            r = self.session.post("https://api.capmonster.cloud/createTask", json=json)
            if r.json()["errorId"] == 0:
                return r.json()["taskId"]
            else:
                return
        except Exception:
            return

    def _task_result(self, tid: str):
        try:
            json = {
                "clientKey": self.apikey,
                "taskId": tid
            }
            r = self.session.post("https://api.capmonster.cloud/getTaskResult", json=json)
            if r.json()["errorId"] == 0:
                if r.json()["status"] != "ready":
                    return r.json()["solution"]["gRecaptchaResponse"]
                else:
                    return
            else:
                return False
        except Exception:
            return False

    def start(self):
        balance = self._balance()
        if balance == None:
            raise ValueError("invalid apikey for capmonster.cloud")
        if init(balance) == 0:
            raise ValueError("no balance, please purchase more at capmonster.cloud")

        tid = self._new_task()
        if tid == None:
            raise Exception("failed to create new task.")

        result = self._task_result(tid)
        while result is None:
            result = self._task_result(tid)
            if result == False:
                break

        return result

print(Misc.discord_headers())