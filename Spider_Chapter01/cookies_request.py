# -*- coding:utf-8 -*-

import requests

cookies = '''

ga=GA1.2.1292503945.1523534377; _octo=GH1.1.633811060.1523534377;
SL_GWPT_Show_Hide_tmp=1; 
SL_wptGlobTipTmp=1; _gat=1; logged_in=no; 
_gh_sess=NXFyazlVZ1cvMk5WLzNtVEFEM3dXMjE3RUVrdjQvS2NPUnlrVFNrVis3cz
lDQVdwbzFvQUdiSEV3UmJmajM1NW9lM3Uwd0JyeUZMYzZ6d1VmRU1kVkdzbFlTTFJsQ
VhnbytQallFUkszTm9QTm5RaXZZQjBPZlRscU5yclc1cVpsZjJKd3FZQUxSMDczU3E4
NXBidllRNTBucWJqN1phUTk0SWRCTCtoU2ZwSnk5NFQyVWt2VzlkdXhlWk1penlDcVBT
aGdKbzlET3EwZWdONXdzemRCY2JPVFB0UVJQMW1ma2Yva2VrZW0xRUN5S2xnRW5xVnRi
bzZFNlI5VEFWVXlwVkhOZlVET3d4MXRWWm10YTl2anFBMUk1dXMyUCtBTnR4NEg0Mmw4
cE13V1BjcmxJK1NTRnJwRGpVbHF2dXpyRXN6aGlPUkRsVUVRVVFVWDR1YjBINzBUZzVrR
UZxV2xkMTRkUlBBSE1jdFpDSzhiendvWHowSG02NTFEOGhnSzFzS1N3NUw3WWMwUWdYen
VWeFQ4WGdIenQzZDFpZGhWWUkrMFpXaEFqTT0tLTFwY254MGhuZkc1bTVXVlZtY2pmNFE
9PQ%3D%3D--80ec1cfddaa515f028230199de62504dd5812475
'''


jar = requests.cookies.RequestsCookieJar()

for cookie in cookies.split(';'):
    key,value = cookie.split('=',1)
    jar.set(key,value)

print(jar)