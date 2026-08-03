from PIL import Image
import math
import sys

def image_to_ascii(image_path, width=90):
    img = Image.open(image_path).convert('L')
    
    # Crop to a square in the center for avatar
    w, h = img.size
    min_dim = min(w, h)
    left = (w - min_dim) / 2
    top = (h - min_dim) / 2
    right = (w + min_dim) / 2
    bottom = (h + min_dim) / 2
    img = img.crop((left, top, right, bottom))
    
    aspect_ratio = 0.48 # Typical for JetBrains Mono
    height = int(width * aspect_ratio)
    img = img.resize((width, height), Image.Resampling.LANCZOS)
    
    ramp = " .`:-=+*cs#%@"
    
    pixels = img.getdata()
    
    # Map to ramp based on brightness
    # Brightness is 0-255. 255 is white (space), 0 is black (@)
    ascii_str = ""
    for pixel in pixels:
        # Darkening curve: (v/255)^1.7 as per guide
        normalized = pixel / 255.0
        darkened = math.pow(normalized, 1.7)
        # Reverse because ramp starts with space (lightest)
        index = int(darkened * (len(ramp) - 1))
        # Ensure bounds
        index = max(0, min(len(ramp) - 1, index))
        ascii_str += ramp[index]
        
    lines = [ascii_str[i:i+width] for i in range(0, len(ascii_str), width)]
    return lines

def lines_to_svg(lines):
    # Read font style from existing script or fallback
    style_content = '<style>.a{fill:#6e7681}@media(prefers-color-scheme:dark){.a{fill:#c9d1d9}}</style>'
    try:
        with open('scripts/txt_to_svg.py', 'r') as f:
            for l in f:
                if '<style>' in l and '</style>' in l:
                    style_content = l.strip().strip("svg.append('").strip("')").replace("\\'", "'")
    except Exception:
        pass

    # Use hardcoded font style from the guide
    style_content = "<style>@font-face{font-family:JBMono;font-style:normal;font-weight:400;font-display:block;src:url(data:font/woff2;base64,d09GMgABAAAAAAT4AA4AAAAACXwAAASmAAJN0wAAAAAAAAAAAAAAAAAAAAAAAAAAGhYbIBwqBmAAgQwRCAqIGIZQATYCJAM8CyAABCAFhCYHIBufByg+DNhkyEL73hCPSpDQcO3wJH4sGfunsjwyWl9JPDwv59e5byT3dCUxGbGVVBkrFc22Pz/Yvb5Avg8p5uFDuKQAJ2rXJGDr2rk2u/3qL2jONDcItMqJsqdHHkQYZ1BLICjLshaHF38jpGzByRmo+P4HQOeYM2ZolZP992Oz8jAPVbRBaEQykRJJYv8jYskk2ZbMs2byQnJNI82u76jTisLcwKzRs+J0BASKA0JIQggUVV27rK6D4ygUyg+5XECgqIbYsqndlc9wkXFoZMHV+dOQrN0KkLakIQD6aCfHKJBGR4BEEYNmOLN3ZwCPqi2T70/eR5pILHKI1DB9R235SMiH8nKE9lG5lgCVVcpRWG00DDxCWgbdnDwyOfFr4RI83f3pn5B77pWXLmhRGHSUVatSQBGFrjA5cioFCDX/Xx5EV4A4gsJfbsshOWmJAtJGsVk6FFtUz81fPEclE0OEGuOzxm59K5H9ols/7aInPnPLR8h80q1fvNjHj0SuWOaVpu1vJDto0N3P4ca0WIruec10j5fIdBv4RuYjI3Q1AD1MBu/L3JtsUR/SOXgQcfDWPHG3a++EnX7Q9pyIKCZzqPI+GoMx9NTtevqGDUTxAzfzruup2ODiLGCVoCwoSi8msMXdYskqMzgoQ455Hax4DLQP3/LW48iXi97R6o93eknQsu1aRPZB0S33yNyfSJEFMP8Q/F33xxpSVr4sIXn4PpVnViyyKaSBYoZtvbXt3o//oBJMVjRhUcK9xz39xF4H6csmzPQetVo32Nu5t5P6dOoeDc2cTZA+qCs0wjs7bmaaJXxphD3UXbi3ghnGu4bdMwR/2jvZZWllcPhCDV07tKPGa3JiAmoFXpEGL+o1eNIgO6zeI832cooKeznlevaYXgIuTeoq7rbeeOrqtziN1TIZYeUtjY0M1qxAV9TgIytCdRGXwd1U/+2qfyncOOcutjMt70LVg/4NXwzu5Kacd3WK6qh7iQ/hFI5Ym7LHikuP2VqHu6fh/6inD3t460ZdGLB7+sL0+R+Jsn07O/YeLuspc3b3hM7io53v3Uzs9KFmvY6eDlp74+95T6HOcNIYsbPQ1d9ObRkdbV+8nKr/KrZysH+tccCmXXtWzVu7dl6pScw8OoITQ+TowHQ3x7EtuzuGmqbNnkwQ9YbTtvgYVcDczVP+ESYe5QtvN3Rel97qnbkNFFIiDQGQcCStjwU5VbKQ+r3Kt+Zs59EV+v8J+f6DX99S7cmv+ynv9Df/A1BQAsH/4UtDGHquDYQBlfL7wQxgBAw+wgegAw22A7h7KCgXCEBe73GdECgVt8yyScEDnPmaRCHD9En5i+AeuSRUd1mSlPRVkk9b3yX5NY+6kgIGxORwBTWNI7pISFoiLSQgiISQEkMcgdrBh0fbUSP1SnMJictATEiIS0BMS0sI8/EgIXrMIwUlpGUg2IJIpKQMLRGRgBA35nluQh4JMSJHTe2xHb58ztXis3yx6rwolzSpooyYnM7Zi9PafBHBBtOPF0PyJM73cGeIWogc7kQ+Iunn+qJkQjBykm3rAgkhNYBcUUVAwbtTbpzrBnMM+uUmkgIB) format('woff2')}.a{fill:#6e7681}@media(prefers-color-scheme:dark){.a{fill:#c9d1d9}}</style>"

    max_len = max(len(l) for l in lines) if lines else 0
    width = int(max_len * 7.74 + 28)
    height = int(len(lines) * 15 + 43)
    
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" font-family="JBMono,ui-monospace,SFMono-Regular,Menlo,Consolas,&apos;Liberation Mono&apos;,monospace">')
    svg.append(style_content)
    
    for i, line in enumerate(lines):
        line_esc = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        y_text = 25.2 + i * 15
        y_rect = 15 + i * 15
        dur = 0.09
        begin = i * dur
        w = len(line) * 7.74
        clip_id = f"c{i}"
        
        svg.append(f'<clipPath id="{clip_id}">')
        svg.append(f'  <rect x="14" y="{y_rect-1}" height="15" width="0">')
        svg.append(f'    <animate attributeName="width" from="0" to="{w:.1f}" begin="{begin:.2f}s" dur="{dur:.2f}s" fill="freeze"/>')
        svg.append(f'  </rect>')
        svg.append(f'</clipPath>')
        
        svg.append(f'<g clip-path="url(#{clip_id})">')
        svg.append(f'  <text xml:space="preserve" x="14" y="{y_text:.1f}" class="a" font-size="12.9">{line_esc}</text>')
        svg.append(f'</g>')
        
        svg.append(f'<rect y="{y_rect}" width="6" height="12" class="a" opacity="0">')
        svg.append(f'  <animate attributeName="x" from="14" to="{14+w:.1f}" begin="{begin:.2f}s" dur="{dur:.2f}s" fill="freeze"/>')
        svg.append(f'  <set attributeName="opacity" to="0.8" begin="{begin:.2f}s"/>')
        svg.append(f'  <set attributeName="opacity" to="0" begin="{begin+dur:.2f}s"/>')
        svg.append(f'</rect>')
        
    svg.append('</svg>')
    
    with open('ascii.svg', 'w', encoding='utf-8') as f:
        f.write('\n'.join(svg))
    print(f"Generated new ascii.svg successfully with {len(lines)} lines.")

if __name__ == '__main__':
    lines = image_to_ascii('avatar.jpg', width=90)
    lines_to_svg(lines)
