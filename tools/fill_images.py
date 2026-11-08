"""Rellena el campo "image" de los juegos que no tengan imagen.

Uso: python3 tools/fill_images.py ../boardgames-data/games.json

Orden de búsqueda: página de Mathom del juego → búsqueda en Mathom por nombre
(solo si el título coincide) → página de Amazon del juego. Usa miniaturas pequeñas.
"""
import html, json, re, sys, time, unicodedata, urllib.parse
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from search_prices import get

def norm(s):
    s = unicodedata.normalize('NFD', s.lower())
    return re.sub(r'[^a-z0-9]+', ' ', ''.join(c for c in s if unicodedata.category(c) != 'Mn')).strip()

def mathom_thumb(url):
    # PrestaShop: .../70037-large_default/x.jpg -> .../70037-home_default/x.jpg (273x312)
    return re.sub(r'-(large|medium|small|thickbox)_default/', '-home_default/', url)

def from_mathom_page(url):
    m = re.search(r'<meta property="og:image" content="([^"]+)"', get(url))
    return mathom_thumb(m.group(1)) if m else None

def from_mathom_search(names):
    for name in names:
        page = get("https://mathom.es/es/buscar?s=" + urllib.parse.quote(name))
        for img, title in re.findall(r'data-full-size-image-url="([^"]+)".*?product-title"><a[^>]*>([^<]+)</a>', page, re.S):
            if norm(html.unescape(title)) == norm(name):
                return mathom_thumb(img)
    return None

def from_amazon_page(url):
    page = get(url)
    m = re.search(r'"hiRes":"(https://m\.media-amazon\.com/images/I/[^"]+)"', page) or \
        re.search(r'id="landingImage"[^>]*src="(https://m\.media-amazon\.com/images/I/[^"]+)"', page)
    if not m: return None
    # ask Amazon for a ~300px version
    return re.sub(r'\._[^/]*_\.', '._AC_SX300_.', m.group(1)) if '._' in m.group(1) else m.group(1).replace('.jpg', '._AC_SX300_.jpg')

def main(path):
    data = json.load(open(path, encoding='utf-8'))
    for g in data['games']:
        if g.get('deleted') or g.get('image'): continue
        names = [n for n in (g.get('name'), g.get('originalName')) if n]
        img = None
        for step in (
            lambda: g.get('mathomUrl') and from_mathom_page(g['mathomUrl']),
            lambda: from_mathom_search(names),
            lambda: g.get('amazonUrl') and from_amazon_page(g['amazonUrl']),
        ):
            try: img = step()
            except Exception as e: print('  error', g['name'], e)
            if img: break
            time.sleep(1)
        print(('OK  ' if img else '--  ') + g['name'], img or '')
        if img: g['image'] = img
    json.dump(data, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    open(path, 'a').write('\n')

if __name__ == '__main__':
    main(sys.argv[1])
