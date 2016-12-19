import numpy
from nbt import nbt


LENGTH_STRING = 'Length'
WIDTH_STRING = 'Width'
HEIGHT_STRING = 'Height'
SCHEMATIC_MAPPING = 'SchematicaMapping'
BLOCKS_STRING = 'Blocks'
DATA_STRING = 'Data'
ICON_STRING = 'Icon'
ENTITIES_STRING = 'Entities'
TILE_ENTITIES_STRING = 'TileEntities'
MATERIALS_STRING = 'Materials'


class Schematic:

    type = ''
    length = 0
    width = 0
    height = 0

    blocks = {}
    layout = []

    @property
    def dimensions(self):
        dim = (self.length, self.width, self.height)
        return dim

    def __repr__(self):
        repr_str = "Type: {0}\n\n".format(self.name)
        repr_str += "Length:{0} x Width:{1} x Height:{2}\n\n".format(self.length, self.width, self.height)
        repr_str += "Dictionary:\n"
        for entry in self.blocks.items():
            repr_str += "ID {0}: {1}\n".format(entry[0], entry[1])

        return repr_str


def retrieve_dimensions(nbt_file):
    length = int(nbt_file.get(LENGTH_STRING).valuestr())
    width = int(nbt_file.get(WIDTH_STRING).valuestr())
    height = int(nbt_file.get(HEIGHT_STRING).valuestr())

    return length, width, height


def retrieve_block_dictionary(nbt_file):
    block_dictionary = {}

    for block in nbt_file.get(SCHEMATIC_MAPPING, []):
        block_id = nbt_file.get(SCHEMATIC_MAPPING, [])[block]
        block_dictionary[block_id] = block

    return block_dictionary


def retrieve_layout(nbt_file, dimensions):
    nbt_layout = nbt_file.get(BLOCKS_STRING)

    length = dimensions[0]
    width = dimensions[1]
    height = dimensions[2]

    layout = numpy.zeros((length, height, width), dtype=numpy.int16)

    for z in range(0, width):
        for x in range(0, length):
            for y in range(0, height):
                coordinate = (y*length + z)*width + x
                layout[x][y][z] = nbt_layout[coordinate]

    return layout


def main():
    filename = input("What is the file you want to load? (.nbt|.schematic) ")
    nbt_file = nbt.NBTFile(filename, 'rb')

    schematic = Schematic()
    schematic.name = nbt_file.name
    schematic.length, schematic.width, schematic.height = retrieve_dimensions(nbt_file)
    schematic.blocks = retrieve_block_dictionary(nbt_file)
    schematic.layout = retrieve_layout(nbt_file, schematic.dimensions)

    print(schematic)


main()
