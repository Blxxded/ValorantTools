#!/usr/bin/python
# -*- coding: utf-8 -*-

# ︾︾︾︾︾︾︾︾︾︾︾︾︾︾︾︾︾︾︾︾︾︾
# 💨 | ValorantTools » Imports & Functions
# ︽︽︽︽︽︽︽︽︽︽︽︽︽︽︽︽︽︽︽︽︽︽

import json, os, ssl, urllib3
try:
	import requests
except ImportError:
	os.system("pip install requests")

def clearScreen(title=None):
	if os.name == "nt":
		os.system("mode 180,23")
		os.system("cls")
	if title == True:
		print("\u001b[31m\n\n\n\n\n\n           //                     /,          \n           ////                 ///,               ██████╗ ██╗     ██╗  ██╗██╗  ██╗██████╗ ██████╗  █████╗ ███╗   ██╗████████╗     ██████╗██╗     ██╗███████╗███╗   ██╗████████╗\n           //////             /////,               ██╔══██╗██║     ╚██╗██╔╝╚██╗██╔╝██╔══██╗██╔══██╗██╔══██╗████╗  ██║╚══██╔══╝    ██╔════╝██║     ██║██╔════╝████╗  ██║╚══██╔══╝\n           ////////         ///////,               ██████╔╝██║      ╚███╔╝  ╚███╔╝ ██║  ██║██████╔╝███████║██╔██╗ ██║   ██║       ██║     ██║     ██║█████╗  ██╔██╗ ██║   ██║   \n            .////////     ////////                 ██╔══██╗██║      ██╔██╗  ██╔██╗ ██║  ██║██╔══██╗██╔══██║██║╚██╗██║   ██║       ██║     ██║     ██║██╔══╝  ██║╚██╗██║   ██║   \n              .////////                            ██████╔╝███████╗██╔╝ ██╗██╔╝ ██╗██████╔╝██║  ██║██║  ██║██║ ╚████║   ██║       ╚██████╗███████╗██║███████╗██║ ╚████║   ██║   \n                .////////                          ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝        ╚═════╝╚══════╝╚═╝╚══════╝╚═╝  ╚═══╝   ╚═╝   \n                  .////////                   \n\n\n\n\n\u001b[0m")
	else:
		os.system("clear")
		print("\u001b[31mError! This script can only be executed on Windows.\n\u001b[0m")
		input("\u001b[0mPress enter to exit...")
		exit()

# ︾︾︾︾︾︾︾︾︾︾︾︾︾︾︾︾︾
# 💨 | ValorantTools » Main Code
# ︽︽︽︽︽︽︽︽︽︽︽︽︽︽︽︽︽

clearScreen(True)
urllib3.disable_warnings()

try:
	lockfile = "".join([os.getenv("LOCALAPPDATA"), r"\Riot Games\Riot Client\Config\lockfile"])
	with open(lockfile, "r") as f:
		data = f.read().split(":")
except:
	print("\u001b[31mError loading data! Please make sure you have the Riot Client and Valorant running.\n\u001b[0m")
	input("\u001b[0mPress enter to exit...")
	exit()

base_url = f"{data[4]}://127.0.0.1:{data[2]}"
s = requests.Session()
s.auth = ("riot", data[3])

try:
	PlayerUUID = s.get(f"https://127.0.0.1:{data[2]}/chat/v1/session", verify=ssl.CERT_NONE).json()["puuid"]
	RegionRequest = s.get(f"https://127.0.0.1:{data[2]}/product-session/v1/external-sessions", verify=ssl.CERT_NONE).json()
	RegionKey = list(RegionRequest.keys())
	Region = RegionRequest[RegionKey[0]]["launchConfiguration"]["arguments"][3].split("=")[-1]
except Exception as e:
	print("\u001b[31mError loading data! Please make sure you have Valorant running.\n\u001b[0m")
	input("\u001b[0mPress enter to exit...")
	exit()

Token = s.get(f"https://127.0.0.1:{data[2]}/entitlements/v1/token", verify=ssl.CERT_NONE).json()["accessToken"]
Entitlement = requests.post("https://entitlements.auth.riotgames.com/api/token/v1", headers={"Authorization": f"Bearer {Token}", "Content-Type": "application/json"}).json()["entitlements_token"]
DefaultInventory = requests.get("https://valorant-tools.blxxded.com/data_files/default_inventory.json").json()
ResetInventory = requests.put(f"https://pd.{Region}.a.pvp.net/personalization/v2/players/{PlayerUUID}/playerloadout", headers={"X-Riot-Entitlements-JWT": f"{Entitlement}", "Authorization": f"Bearer {Token}"}, json=DefaultInventory)
if ResetInventory.status_code == 200:
	print("\u001b[32mYour inventory has been reseted, please restart Valorant to apply changes.\n\u001b[0m")
else:
	print("\u001b[31mAn error has ocurred reseting your inventory, please try again later or contact with Blxxded#0303 on Discord.\n\u001b[0m")
input("\u001b[0mPress enter to exit...")
