from PIL import Image, ImageDraw, ImageFilter
import math

def create_masked_avatar(input_path, output_path):
    img = Image.open(input_path).convert('RGB')
    
    # Crop to square
    w, h = img.size
    min_dim = min(w, h)
    left = (w - min_dim) / 2
    top = (h - min_dim) / 2
    right = (w + min_dim) / 2
    bottom = (h + min_dim) / 2
    img = img.crop((left, top, right, bottom))
    
    w, h = img.size
    
    # Create an elliptical mask
    # The character's head and shoulders are roughly an inverted triangle or oval
    # We want a mask that is white on the outside, transparent on the inside
    mask = Image.new('L', (w, h), 0)
    draw = ImageDraw.Draw(mask)
    
    # Draw a central ellipse for the head/body
    # We want to keep the bottom center (shoulders) and center (head)
    # bounding box for the ellipse:
    # left, top, right, bottom
    # Make it slightly wider at the bottom? An ellipse is fine.
    draw.ellipse((w*0.1, h*0.05, w*0.9, h*1.1), fill=255)
    
    # Blur the mask so the edges fade softly
    mask = mask.filter(ImageFilter.GaussianBlur(radius=w*0.05))
    
    # Apply the mask: where mask is 255, keep image. Where mask is 0, make white.
    white_bg = Image.new('RGB', (w, h), (255, 255, 255))
    
    # composite
    result = Image.composite(img, white_bg, mask)
    
    result.save(output_path)
    print(f"Masked avatar saved to {output_path}")

if __name__ == '__main__':
    create_masked_avatar('avatar.jpg', 'avatar_masked.jpg')
