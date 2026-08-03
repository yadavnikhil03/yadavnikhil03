import sys
import os

def main():
    # Read the font style from the reference SVG
    style_content = ""
    try:
        with open('temp_andriidrok1/ascii.svg', 'r', encoding='utf-8') as f:
            svg_content = f.read()
        start_idx = svg_content.find('<style>')
        end_idx = svg_content.find('</style>')
        if start_idx != -1 and end_idx != -1:
            style_content = svg_content[start_idx:end_idx+8]
    except FileNotFoundError:
        pass # Handle if temp was already deleted

    # Read the user's ASCII art
    try:
        with open(r'C:\Users\Nikhil\Downloads\ascii-art.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("ASCII art file not found.")
        sys.exit(1)
        
    lines = [l.replace('\n', '').replace('\r', '') for l in lines]
    
    # Calculate dimensions
    max_len = max(len(l) for l in lines) if lines else 0
    width = int(max_len * 7.74 + 28)
    height = int(len(lines) * 15 + 43)
    
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" font-family="JBMono,ui-monospace,SFMono-Regular,Menlo,Consolas,&apos;Liberation Mono&apos;,monospace">')
    if style_content:
        svg.append(style_content)
    else:
        # Fallback if no style found
        svg.append('<style>.a{fill:#6e7681}@media(prefers-color-scheme:dark){.a{fill:#c9d1d9}}</style>')
    
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
    print(f"Generated ascii.svg successfully with {len(lines)} lines.")

if __name__ == '__main__':
    main()
