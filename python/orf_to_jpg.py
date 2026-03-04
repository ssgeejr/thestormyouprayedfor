#!/usr/bin/env python3
import sys
import os
from pathlib import Path
import rawpy
import imageio.v3 as iio  # modern imageio style (v3); fallback to imageio.imwrite works too

def main():
    if len(sys.argv) != 2:
        print("Usage: orf_to_jpg.py <directory_path>", file=sys.stderr)
        sys.exit(1)

    folder = Path(sys.argv[1]).resolve()

    if not folder.is_dir():
        print(f"Error: '{folder}' is not a directory or does not exist", file=sys.stderr)
        sys.exit(1)

    orf_files = [p for p in folder.iterdir() if p.is_file() and p.suffix.lower() == '.orf']

    if not orf_files:
        print(f"No .orf files found in '{folder}'", file=sys.stderr)
        sys.exit(0)

    print(f"Found {len(orf_files)} .orf file(s) in '{folder}'")
    converted = 0

    for orf_path in sorted(orf_files):  # sorted for consistent order
        jpg_path = orf_path.with_suffix('.jpg')

        if jpg_path.exists():
            print(f"Skipping (already exists): {jpg_path.name}")
            continue

        try:
            with rawpy.imread(str(orf_path)) as raw:
                # Recommended settings for good-looking JPGs:
                # - use_camera_wb=True → matches camera's own look quite well
                # - output_bps=8 → standard for JPG
                # - no_auto_bright=False (default) → auto-adjusts exposure nicely
                # You can experiment with: use_auto_wb=True, bright=1.0, etc.
                rgb = raw.postprocess(
                    use_camera_wb=True,
                    output_bps=8,
                    # Optional extras you can uncomment/tweak:
                    # demosaic_algorithm=rawpy.DemosaicAlgorithm.AHD,  # default is usually good
                    # no_auto_bright=True,  # if you want zero auto-brightening
                    # output_color=rawpy.ColorSpace.sRGB,
                )

            # Save with decent quality (90-95 is sweet spot for size vs quality)
            iio.imwrite(str(jpg_path), rgb, quality=92)

            print(f"Converted: {orf_path.name} → {jpg_path.name}")
            converted += 1

        except Exception as e:
            print(f"Error processing {orf_path.name}: {e}", file=sys.stderr)

    print(f"\nDone. Successfully converted {converted}/{len(orf_files)} files.")

if __name__ == "__main__":
    main()
