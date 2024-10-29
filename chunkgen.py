import pyray as rl
import addimages as ai


class Chunk:
    def __init__(self, model, texture, location: rl.Vector3):
        self.model = model
        self.texture = texture
        self.location = location


CHUNK_SIZE = 64
CHUNK_HEIGHT = 32

def getChunkPos(position: rl.Vector3) -> rl.Vector3:
    return rl.Vector3(
        position.x // CHUNK_SIZE * CHUNK_SIZE,
        0,
        position.z // CHUNK_SIZE * CHUNK_SIZE
    )


def generateChunk(position: rl.Vector3) -> Chunk:
    offset = getChunkPos(position)
    perlin_image_1 = rl.gen_image_perlin_noise(
        int(CHUNK_SIZE), int(CHUNK_SIZE), int(offset.x), int(offset.z), 5)
    perlin_image_2 = rl.gen_image_perlin_noise(
        int(CHUNK_SIZE), int(CHUNK_SIZE), int(offset.x), int(offset.z), 3)
    perlin_image_final = ai.addImages(perlin_image_1, perlin_image_2)

    mesh = rl.gen_mesh_heightmap(perlin_image_final, rl.Vector3(
        CHUNK_SIZE, CHUNK_HEIGHT, CHUNK_SIZE))
    model = rl.load_model_from_mesh(mesh)
    texture = rl.load_texture_from_image(perlin_image_final)
    model.materials[0].maps[rl.MaterialMapIndex.MATERIAL_MAP_ALBEDO].texture = texture

    rl.unload_image(perlin_image_1)
    rl.unload_image(perlin_image_2)

    return Chunk(model, texture, offset)


def unloadChunk(chunk: Chunk) -> None:
    rl.unload_model(chunk.model)
    rl.unload_texture(chunk.texture)


def renderChunk(chunk: Chunk) -> None:
    rl.draw_model(chunk.model, chunk.location, 1, rl.GREEN)
    rl.draw_cube(rl.Vector3(chunk.location.x + CHUNK_SIZE // 2, 16,
                 chunk.location.z + CHUNK_SIZE // 2), CHUNK_SIZE, 1, CHUNK_SIZE, rl.BLUE)

