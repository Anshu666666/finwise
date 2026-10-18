import urllib.request, re, ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

with open(r'report/finwise_ieee_report.html', 'r', encoding='utf-8') as f:
    text = f.read()

refs_block = re.search(r'<ul class="references-list">(.*?)</ul>', text, re.DOTALL)
if refs_block:
    links = re.findall(r'href="([^"]+)"', refs_block.group(1))
    for url in links:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        try:
            with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
                print(f"[STATUS {resp.status}] {url}")
        except Exception as e:
            print(f"[FAIL: {e}] {url}")
