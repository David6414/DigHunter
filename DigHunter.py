import sys
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor

VERDE = "\033[1;32m"
AZUL = "\033[1;34m"
ROJO = "\033[1;31m"
AMARILLO = "\033[1;33m"
GRIS = "\033[0;37m"
RESET = "\033[0m"

WORDLIST = [
    "admin", "administrator", "login", "dashboard", "config", 
    "backup", "db", "api", "v1", "v2", "test", "server-status", 
    "robots.txt", "sitemap.xml", "uploads", "images", "css", 
    "js", "assets", "secret", "private", "index", "home",
    "register", "signup", "user", "users", "panel", "phpmyadmin"
]

EXTENSIONS = ["", ".php", ".html", ".txt", ".bak", ".zip"]

def banner():
    print(VERDE + r"""
  ____  _      _   _             _            
 |  _ \(_)_ __| | | |_   _ _ __ | |_ ___ _ __ 
 | | | | | '__| |_| | | | | '_ \| __/ _ \ '__|
 | |_| | | |  |  _| | |_| | | | | ||  __/ |   
 |____/|_|_|  |_| |_|\__,_|_| |_|\__\___|_|   
    [ DirHunter - Security Fuzzer ]
    """ + RESET)
    
    print(AMARILLO + "--------------------------------------------------------")
    print(" [!] AVISO: Uso exclusivo para auditorías éticas y educación.")
    print(" [!] El autor no se hace responsable de usos malintencionados.")
    print("--------------------------------------------------------" + RESET)

def check_url(url):
    try:
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        with urllib.request.urlopen(req, timeout=3) as res:
            code = res.getcode()
            if code == 200:
                print(VERDE + f"  [200 OK]      -> {url}" + RESET)
            elif code in [301, 302, 307]:
                print(AMARILLO + f"  [{code} REDIRECT] -> {url}" + RESET)
    except urllib.error.HTTPError as e:
        if e.code == 403:
            print(AMARILLO + f"  [403 FORBIDDEN] -> {url}" + RESET)
    except Exception:
        pass

def main():
    banner()
    print(GRIS + "Introduce una URL o escribe 'exit' para salir.\n" + RESET)

    while True:
        try:
            target = input(AZUL + "[Escaneo Forzoso] URL -> " + RESET).strip()
        except (KeyboardInterrupt, EOFError):
            print(VERDE + "\nSaliendo..." + RESET)
            break

        if not target:
            continue

        if target.lower() == "exit":
            print(VERDE + "Hasta luego." + RESET)
            break

        if not target.startswith("http"):
            target = "http://" + target
        target = target.rstrip('/')

        print(VERDE + f"\n[*] Analizando: {target}..." + RESET)
        
        urls = [f"{target}/{word}{ext}" for word in WORDLIST for ext in EXTENSIONS]

        try:
            with ThreadPoolExecutor(max_workers=5) as ex:
                ex.map(check_url, urls)
        except KeyboardInterrupt:
            print(ROJO + "\n[!] Detenido." + RESET)

        print(AZUL + "\n[*] Finalizado.\n" + RESET)

if __name__ == "__main__":
    main()
