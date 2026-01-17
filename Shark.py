import os
from colorama import Fore, Style, init
import requests
import threading
from concurrent.futures import ThreadPoolExecutor
import time
import asyncio
import aiohttp
init(autoreset=True)  # هذا يخلي اللون يرجع عادي بعد الطباعة
owis = (Fore.CYAN + "Owis")


def boot():
    print("started")
    os.system("clear")
    print("started")
    print(Fore.LIGHTBLUE_EX + "AUTHOUR:", owis)
    
boot()

while True:
    name = input(
        "just for using this tool you agree that is for educational purposes only "
        "if you agree press enter, else Ctrl+Z"
    )
    if name == "":
        break  # ضغط Enter فقط
    else:
        print("\033[91mPlease press Enter only!\033[0m")  # رسالة باللون الأحمر

RED = "\033[91m"
RESET = "\033[0m"
print(Fore.YELLOW + "warning")
print(RED + " you agreed using tool for educational purposes only " + RESET, name)

host = input("target host or url: ")

if not host.startswith(("http://", "https://")):
    host = "https://" + host
    
if not host:
    print(Fore.RED + "you should enter target host or url")
    host = input("target full url: ")
    time.sleep(3)
if not host:
    print(Fore.RED + "you should enter url")
    host = input("target full url: ")
    
if not host:
     print(Fore.RED+ "you should enter url")
     host = input("target full url: ")
ingored1= ("login", "signin", "auth")
valid = {200,301,302,307,401,403,429}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
ingored = (".jpg", ".png", ".css", ".js", ".svg", ".ico")
baseline = None
r = requests.get(host)
print("status ",r.status_code)

wordlist = input("wordlist file: ")
if not wordlist:
    print(Fore.RED + "You should enter an paths file")
    password = input("wordlist file: ") 
word = (Fore.GREEN + " wordlist: ")
base = host.rstrip("/") + "/"
print("trying with url "+ host + word ,wordlist)
sem = asyncio.Semaphore(30)  
def status_color(code):
    if code == 200:
        return Fore.GREEN
    elif code in (301, 302, 307):
        return Fore.YELLOW
    elif code in (429,500):
        return Fore.RED
    elif code in (401, 403):
    
        return Fore.CYAN
    else:
        return Fore.WHITE
                                                
async def check(session, p):
    p = p.strip()
    
    if p.endswith(ingored):
        return
    
    async with sem:
        try:
            async with session.get(base + p.strip(), timeout=aiohttp.ClientTimeout(total=3.7),allow_redirects=False,headers=headers) as r:
                if p.strip().endswith(ingored):
                    return                                                           
                if r.status in (301, 302, 307):
                    location = r.headers.get("Location", "").lower()
                if location in ("/", "/login", "/index.php"):
                    return 
                length = int(r.headers.get("Content-Length", 0))
                if baseline and length == baseline:
                        return   
                if r.status in valid and r.status != 204:
                    color = status_color(r.status)
                    print(f"{color}{base+p} {r.status}{Fore.RESET}")
                
                    
        except Exception as e:
            pass

async def run():
    connector = aiohttp.TCPConnector(limit=0) 
    async with aiohttp.ClientSession(connector=connector) as session:
        with open(wordlist, errors="ignore") as f:
            batch = []
            batch_size = 60

            for line in f:
                batch.append(line)
                if len(batch) == batch_size:
                    await asyncio.gather(*(check(session, p) for p in batch))
                    batch.clear()

            # أي باقي
            if batch:
                await asyncio.gather(*(check(session, p) for p in batch))
           
            
asyncio.run(run())
