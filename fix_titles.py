import os
import re

d = r'c:\Users\Sebas\Downloads\veterinaria\veterinaria\templates'

for r, _, fs in os.walk(d):
    for f in fs:
        if f.endswith('.html'):
            p = os.path.join(r, f)
            with open(p, 'r', encoding='utf-8') as fp:
                c = fp.read()
            
            # Quitar el div interior que contiene el <h1> y <p> en page-header
            # \s*<div>\s*<[hH][12].*?</[hH][12]>.*?(?:</p>)?\s*</div>
            # Nos aseguramos de capturar el page-header y reemplazamos
            pattern = re.compile(r'(<div class="page-header"[^>]*>)\s*<div[^>]*>\s*<h[12][^>]*>.*?</h[12]>.*?(?:</p>)?\s*</div>', re.DOTALL)
            nc = pattern.sub(r'\1', c)
            
            # Si el page header queda vacio (solo espacios), borrarlo todo
            nc = re.sub(r'<div class="page-header"[^>]*>\s*</div>', '', nc)
            
            if nc != c:
                with open(p, 'w', encoding='utf-8') as fp:
                    fp.write(nc)
                print(f"Updated {f}")
