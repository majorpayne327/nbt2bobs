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

    length = 0
    width = 0
    height = 0

    block_dictionary = {}

    @property
    def dimensions(self):
        return [self.length, self.width, self.height]

    def __repr__(self):
        repr_str = "Schematic:\n\n"
        repr_str += "Length:{0} x Width:{1} x Height:{2}\n\n".format(self.length, self.width, self.height)
        repr_str += "Dictionary:\n"
        for entry in self.block_dictionary.items():
            repr_str += "ID {0}: {1}\n".format(entry[0], entry[1])

        return repr_str


def retrieve_dimensions(nbt_file):
    length = nbt_file.get(LENGTH_STRING)
    width = nbt_file.get(LENGTH_STRING)
    height = nbt_file.get(HEIGHT_STRING)

    return length, width, height


def retrieve_block_dictionary(nbt_file):
    block_dictionary = {}

    for block in nbt_file.get(SCHEMATIC_MAPPING, []):
        block_id = nbt_file.get(SCHEMATIC_MAPPING, [])[block]
        block_dictionary[block_id] = block

    return block_dictionary


def main():
    filename = input("What is the file you want to load? (.nbt|.schematic) ")
    nbt_file = nbt.NBTFile(filename, 'rb')

    schematic = Schematic()

    schematic.length, schematic.width, schematic.height = retrieve_dimensions(nbt_file)
    schematic.block_dictionary = retrieve_block_dictionary(nbt_file)

    print(schematic)


main()
