#!/usr/bin/env python3
import sys
import os
from pathlib import Path
import rawpy
import imageio

def main():
    # Check argument count
    if len(sys.argv) != 2:
        print("Usage: orf_to_jpg.py <path_to_orf_file>", file=sys.stderr)
        sys.exit(1)
    
    orf_path = sys.argv[1]
    
    # Check if file exists
    if not os.path.exists(orf_path):
        print(f"Error: File '{orf_path}' does not exist", file=sys.stderr)
        sys.exit(1)
    
    # Check file extension (case-insensitive)
    if not orf_path.lower().endswith('.orf'):
        print(f"Error: File '{orf_path}' is not an ORF file", file=sys.stderr)
        sys.exit(1)
    
    # Create output directory if needed
    output_dir = Path('/tmp/jpgexport')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate output path
    basename = os.path.basename(orf_path)
    name_without_ext = os.path.splitext(basename)[0]
    jpg_path = output_dir / (name_without_ext + '.jpg')
    
    try:
        # Read ORF and convert to RGB
        with rawpy.imread(orf_path) as raw:
            rgb = raw.postprocess()
        
        # Write as JPG
        imageio.imwrite(str(jpg_path), rgb)
        print(jpg_path)
    except Exception as e:
        print(f"Error converting ORF to JPG: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()