import re
import requests

# URL de ejemplo (reemplázala por la real)
url = "https://serialgo.tv/home"  # ⚠️ Cambia esto por la URL correcta

# Encabezados para evitar ser bloqueado
headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10)"
}

try:
    response = requests.get(url, headers=headers)
    html = response.text

    # Encuentra bloques <div class="flw-item">...</div>
    blocks = re.findall(r'<div class="flw-item">.*?</div>\s*</div>', html, re.DOTALL)

    for block in blocks:
        # Buscar imagen
        img_match = re.search(r'<img[^>]+data-src="(https:\/\/[^"]+\.jpg)"', block)
        img_url = img_match.group(1) if img_match else "No encontrada"

        # Buscar href
        href_match = re.search(r'<a[^>]+href="([^"]+)"', block)
        href = href_match.group(1) if href_match else "No encontrado"

        # Buscar título
        title_match = re.search(r'<h3 class="film-name">.*?<a[^>]*>([^<]+)</a>', block, re.DOTALL)
        title = title_match.group(1).strip() if title_match else "No encontrado"

        print("---------")
        print("Título:", title)
        print("Enlace:", href)
        print("Imagen:", img_url)

except requests.RequestException as e:
    print("Error al hacer la solicitud:", e)
