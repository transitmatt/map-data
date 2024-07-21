from argparse import ArgumentParser
from glob import glob
from pathlib import Path

from tile_renderer import render_tiles
from tile_renderer.types.coord import Vector
from tile_renderer.types.pla2 import Pla2File
from tile_renderer.types.skin import Skin

def main():
    parser = ArgumentParser()
    parser.add_argument("-n", '--namespaces', nargs="+", default=[])
    parser.add_argument("-z", '--zooms', nargs="+", type=int, default=[])
    args = parser.parse_args()

    renders = []
    if args.namespaces:
        for ns in args.namespaces:
            renders.extend(Pla2File.from_file(Path(f"files/{ns}.pla2.msgpack")).components)
    else:
        for file in glob("files/*"):
            renders.extend(Pla2File.from_file(Path(file)).components)
    renders = list({(c.namespace, c.id): c for c in renders}.values())
    
    print(f"Rendering {', '.join(args.namespaces) or 'everything'}")

    for zoom in args.zooms or (0, 1, 2, 3, 4, 5, 6, 7, 8, 9):
        for tile, b in render(
            renders,
            Skin.default(),
            zoom,
            32,
            256,
            Coord(0, 32),
        ).items():
            path = Path(__file__).parent / "tiles" / str(9-tile.z) / str(tile.x) / (str(tile.y)+".webp")
            path.parent.mkdir(exist_ok=True)
            path.write_bytes(b)

if __name__ == "__main__":
    main()
