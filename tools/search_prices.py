"""Busca un juego en mathom.es y amazon.es y lista los primeros resultados (título, precio, enlace).

Uso: python3 tools/search_prices.py "harmonies" "skull king" ...
Sirve para elegir a mano la edición en español de cada juego; no escribe nada.
"""
import html, json, re, sys, time, urllib.parse, urllib.request, gzip

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html", "Accept-Language": "es-ES,es;q=0.9", "Accept-Encoding": "gzip"})
    with urllib.request.urlopen(req, timeout=20) as r:
        data = r.read()
        if r.headers.get("Content-Encoding") == "gzip":
            data = gzip.decompress(data)
        return data.decode("utf-8", "ignore")

def price(s):
    s = s.replace("\xa0", " ").replace("€", "").replace(".", "").replace(",", ".").strip()
    try: return float(s)
    except ValueError: return None

def mathom(q, n=6):
    page = get("https://mathom.es/es/buscar?s=" + urllib.parse.quote(q))
    out = []
    for url, title, p in re.findall(r'product-title"><a href="([^"]+)"[^>]*>([^<]+)</a>.*?aria-label="Precio">\s*([^<]+?)\s*<', page, re.S)[:n]:
        out.append({"title": html.unescape(title).strip(), "price": price(p), "url": url})
    return out

def amazon(q, n=6):
    page = get("https://www.amazon.es/s?k=" + urllib.parse.quote(q + " juego de mesa"))
    out = []
    for b in re.split(r'data-component-type="s-search-result"', page)[1:n + 1]:
        t = re.findall(r'<h2[^>]*>.*?<span[^>]*>([^<]+)</span>', b, re.S)
        p = re.findall(r'a-offscreen">([^<]+)<', b)
        asin = re.findall(r'data-asin="([A-Z0-9]{10})"', b) or re.findall(r'/dp/([A-Z0-9]{10})', b)
        if t and asin:
            out.append({"title": html.unescape(t[0]).strip(), "price": price(p[0]) if p else None, "url": f"https://www.amazon.es/dp/{asin[0]}"})
    return out

if __name__ == "__main__":
    res = {}
    for q in sys.argv[1:]:
        res[q] = {"mathom": mathom(q), "amazon": amazon(q)}
        time.sleep(1.5)
    print(json.dumps(res, ensure_ascii=False, indent=1))
