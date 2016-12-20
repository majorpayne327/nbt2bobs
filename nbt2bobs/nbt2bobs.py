import numpy
import jinja2
from nbt import nbt


MATERIALS_STRING = 'Materials'
LENGTH_STRING = 'Length'  # size along the Z axis
WIDTH_STRING = 'Width'  # size along the X axis
HEIGHT_STRING = 'Height'  # size along the Y axis
SCHEMATIC_MAPPING = 'SchematicaMapping'
BLOCKS_STRING = 'Blocks'
DATA_STRING = 'Data'
ICON_STRING = 'Icon'
ENTITIES_STRING = 'Entities'
TILE_ENTITIES_STRING = 'TileEntities'

IGNORE_BLOCK_ID = -1

env = jinja2.Environment(loader=jinja2.PackageLoader('nbt2bobs', 'templates'))


class Schematic:

    type = ''
    length = 0
    width = 0
    height = 0

    blocks_dictionary = {}
    blocks = []
    layout = []

    @property
    def dimensions(self):
        return self.length, self.width, self.height

    def __repr__(self):
        repr_str = "Type: {0}\n\n".format(self.type)
        repr_str += "Length:{0} x Width:{1} x Height:{2}\n\n".format(self.length, self.width, self.height)
        repr_str += "Dictionary:\n"
        for entry in self.blocks_dictionary.items():
            repr_str += "ID {0}: {1}\n".format(entry[0], entry[1])

        repr_str += "\nBlocks\n"
        for block in self.blocks:
            repr_str += "{0}\n".format(block)

        repr_str += "\nLayout\n"
        for x_layer in self.layout:
            repr_str += "{0}\n".format(x_layer)

        return repr_str


class Block:
    name = ''
    id = 0
    x = 0
    y = 0
    z = 0
    metadata = 0

    @property
    def coordinates(self):
        return self.x, self.y, self.z

    def __init__(self, id, name, x, y, z):
        self.id = id
        self.name = name
        self.x = x
        self.y = y
        self.z = z

    def get_bo3_definition(self):
        return "Block({0}, {1}, {2}, {3}:{4})".format(self.x, self.y, self.z, self.id, self.metadata)

    def __repr__(self):
        return "{0} placed at ({1}, {2}, {3}) with metadata {4:08b}".format(self.name, self.x, self.y, self.z, self.metadata)


def convert_nbt_tag_to_int(tag):
    return int(tag.valuestr())


def retrieve_dimensions(nbt_file):
    length = convert_nbt_tag_to_int(nbt_file.get(LENGTH_STRING))
    width = convert_nbt_tag_to_int(nbt_file.get(WIDTH_STRING))
    height = convert_nbt_tag_to_int(nbt_file.get(HEIGHT_STRING))

    return length, width, height


def retrieve_block_dictionary(nbt_file):
    block_dictionary = {}

    for block in nbt_file.get(SCHEMATIC_MAPPING, []):
        block_id = convert_nbt_tag_to_int(nbt_file.get(SCHEMATIC_MAPPING, [])[block])
        block_dictionary[block_id] = block

    return block_dictionary


def build_block_information(nbt_file, schematic):

    blocks_dictionary = retrieve_block_dictionary(nbt_file)
    nbt_blocks = nbt_file.get(BLOCKS_STRING)
    nbt_data = nbt_file.get(DATA_STRING)

    length, width, height = schematic.dimensions
    blocks = []
    layout = numpy.zeros((width, height, length), dtype=numpy.int16)

    for y in range(0, height):
        for z in range(0, length):
            for x in range(0, width):
                coordinate = (y * length + z) * width + x
                block_id = nbt_blocks[coordinate]
                if block_id != IGNORE_BLOCK_ID:
                    layout[x][y][z] = block_id

                    block = Block(block_id, blocks_dictionary.get(block_id, "NaN"), x, y, z)
                    block.metadata = nbt_data[coordinate]
                    blocks.append(block)
                else:
                    layout[x][y][z] = -1

    schematic.blocks_dictionary = blocks_dictionary
    schematic.blocks = blocks
    schematic.layout = layout

    return schematic


def main():

    filename = input("What is the file you want to load? (.nbt|.schematic) ")
    # IGNORE_BLOCK_ID = int(input("What is the block id you want to ignore? ") or -1)

    nbt_file = nbt.NBTFile(filename, 'rb')

    if nbt_file.filename.split('.')[-1] == 'schematic':
        schematic = Schematic()
        schematic.type = "{0} - {1}".format(nbt_file.get(MATERIALS_STRING, "No Material"), nbt_file.name)
        schematic.length, schematic.width, schematic.height = retrieve_dimensions(nbt_file)

        build_block_information(nbt_file, schematic)

        template = env.get_template('bo3.template')
        bo3 = template.render(author="nbt2bobs", description="Test Description", writemode="WriteDisable",
                              outsidesourceblock='dontPlace', schematic=schematic)

        with open('test_bo3.b03', 'w') as f:
            f.write(bo3)

if __name__ == '__main__':
    main()
