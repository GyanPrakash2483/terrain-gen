import pyray as rl
import chunkgen as cg

def locIsEq(loc1: rl.Vector3, loc2: rl.Vector3) -> bool:
    return (loc1.x == loc2.x and loc1.y == loc2.y and loc1.z == loc2.z)

def isChunkIn(chunk: cg.Chunk, pos: rl.Vector3, render_distance: int):
    if(chunk.location.x >= pos.x - cg.CHUNK_SIZE * render_distance and chunk.location.x <= pos.x + cg.CHUNK_SIZE * render_distance):
            if(chunk.location.z >= pos.z - cg.CHUNK_SIZE * render_distance and chunk.location.z <= pos.z + cg.CHUNK_SIZE * render_distance):
                return True
    return False
    

rl.init_window(900, 600, "Procedural Terrain Generation")
camera = rl.Camera3D(rl.Vector3(0.01, 256, 0.01), rl.Vector3(0, 0, 0), rl.Vector3(0, 1, 0), 45, rl.CameraProjection.CAMERA_PERSPECTIVE)

rl.disable_cursor()
rl.set_exit_key(rl.KeyboardKey.KEY_NULL)

default_chunk = cg.generateChunk(rl.Vector3(0, 0, 0))

CHUNK_LIST = []
ACTIVE_CHUNKS = []
render_distance = 8

while not rl.window_should_close():

    # Update the list of chunks that should be rendered
    ACTIVE_CHUNKS.clear()
    for i in range(-render_distance + 1, +render_distance):
        for j in range(-render_distance + 1, +render_distance):
            x = camera.position.x + i * cg.CHUNK_SIZE
            z = camera.position.z + j * cg.CHUNK_SIZE
            chunkpos = cg.getChunkPos(rl.Vector3(x, 0, z))
            ACTIVE_CHUNKS.append(chunkpos)

    # Add a chunk to the list if it does not already exist
    for activechunk in ACTIVE_CHUNKS:
        chunkexists = False
        for chunk in CHUNK_LIST:
            if(locIsEq(chunk.location, activechunk)):
                chunkexists = True
                break
        if(not chunkexists):
            CHUNK_LIST.append(cg.generateChunk(activechunk))

    # Remove a chunk from list if it is not active
    CHUNK_LIST = list(filter(lambda chunk: isChunkIn(chunk, camera.position, render_distance), CHUNK_LIST))

    rl.begin_drawing()
    rl.clear_background(rl.BLACK)
    rl.begin_mode_3d(camera)

    # 3d mode - start
    for chunk in CHUNK_LIST:
        cg.renderChunk(chunk)



    # 3d mode - end
    rl.end_mode_3d()

    rl.draw_text(str(rl.get_fps()), 10, 10, 20, rl.GREEN)
    rl.end_drawing()

    rl.update_camera(camera, rl.CameraMode.CAMERA_FIRST_PERSON)

    if(rl.is_key_pressed(rl.KeyboardKey.KEY_ESCAPE)):
        rl.enable_cursor()
    if(rl.is_key_pressed(rl.KeyboardKey.KEY_F11)):
        rl.toggle_fullscreen()
    if(rl.is_key_down(rl.KeyboardKey.KEY_LEFT_SHIFT)):
        camera.position.y -= 1
    if(rl.is_key_down(rl.KeyboardKey.KEY_SPACE)):
        camera.position.y += 1


rl.close_window()