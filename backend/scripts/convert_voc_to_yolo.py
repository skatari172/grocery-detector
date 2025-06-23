import os
import xml.etree.ElementTree as ET
from PIL import Image
import argparse

def convert_voc_to_yolo(xml_dir, img_dir, output_dir, classes_file):
    """
    Convert VOC XML annotations to YOLO format
    
    Args:
        xml_dir: Directory containing XML annotation files
        img_dir: Directory containing corresponding images
        output_dir: Directory to save YOLO format annotations
        classes_file: Path to classes.txt file
    """
    
    # Read classes
    if not os.path.exists(classes_file):
        print(f"❌ Classes file not found: {classes_file}")
        return
    
    with open(classes_file, 'r') as f:
        CLASSES = [c.strip() for c in f.readlines()]
    
    print(f"📋 Found {len(CLASSES)} classes: {CLASSES}")
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Process XML files
    xml_files = [f for f in os.listdir(xml_dir) if f.endswith('.xml')]
    print(f"🔍 Found {len(xml_files)} XML files to convert")
    
    converted = 0
    for xml_file in xml_files:
        try:
            xml_path = os.path.join(xml_dir, xml_file)
            tree = ET.parse(xml_path)
            root = tree.getroot()
            
            # Get image size
            size = root.find("size")
            if size is None:
                print(f"⚠️  No size info in {xml_file}, skipping...")
                continue
                
            w = float(size.find("width").text)
            h = float(size.find("height").text)
            
            # Prepare output .txt file
            txt_filename = xml_file.replace(".xml", ".txt")
            txt_path = os.path.join(output_dir, txt_filename)
            
            with open(txt_path, "w") as out:
                for obj in root.findall("object"):
                    cls_name = obj.find("name").text
                    
                    # Skip if class not in our list
                    if cls_name not in CLASSES:
                        print(f"⚠️  Unknown class '{cls_name}' in {xml_file}, skipping...")
                        continue
                    
                    cls_id = CLASSES.index(cls_name)
                    bb = obj.find("bndbox")
                    
                    if bb is None:
                        continue
                        
                    x1 = float(bb.find("xmin").text)
                    y1 = float(bb.find("ymin").text)
                    x2 = float(bb.find("xmax").text)
                    y2 = float(bb.find("ymax").text)
                    
                    # Convert to YOLO format (normalized coordinates)
                    cx = ((x1 + x2) / 2) / w
                    cy = ((y1 + y2) / 2) / h
                    bw = (x2 - x1) / w
                    bh = (y2 - y1) / h
                    
                    # Write YOLO format: class_id center_x center_y width height
                    out.write(f"{cls_id} {cx:.6f} {cy:.6f} {bw:.6f} {bh:.6f}\n")
            
            converted += 1
            if converted % 10 == 0:
                print(f"✅ Converted {converted}/{len(xml_files)} files...")
                
        except Exception as e:
            print(f"❌ Error converting {xml_file}: {e}")
    
    print(f"🎉 Conversion complete! Converted {converted}/{len(xml_files)} files")
    print(f"📁 YOLO annotations saved to: {output_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert VOC XML to YOLO format")
    parser.add_argument("--xml_dir", required=True, help="Directory containing XML files")
    parser.add_argument("--img_dir", required=True, help="Directory containing images")
    parser.add_argument("--output_dir", required=True, help="Output directory for YOLO annotations")
    parser.add_argument("--classes", default="classes.txt", help="Path to classes.txt file")
    
    args = parser.parse_args()
    
    convert_voc_to_yolo(args.xml_dir, args.img_dir, args.output_dir, args.classes)
