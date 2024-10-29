import pyray as rl
import cffi
ffi = cffi.FFI()

def addImages(image1: rl.Image, image2: rl.Image) -> rl.Image:
    colors1 = ffi.unpack(ffi.cast("struct {unsigned char r; unsigned char g; unsigned char b; unsigned char a;} *", image1.data), image1.height * image1.width)
    colors2 = ffi.unpack(ffi.cast("struct {unsigned char r; unsigned char g; unsigned char b; unsigned char a;} *", image2.data), image2.height * image2.width)

    colors = ffi.new("struct {unsigned char r; unsigned char g; unsigned char b; unsigned char a;} []", image1.height * image1.width)

    for i in range(0, image1.height * image1.width):
        colors[i].r = ffi.cast("unsigned char", (colors1[i].r + colors2[i].r) / 2)
        colors[i].g = ffi.cast("unsigned char", (colors1[i].g + colors2[i].g) / 2)
        colors[i].b = ffi.cast("unsigned char", (colors1[i].b + colors2[i].b) / 2)
        colors[i].a = ffi.cast("unsigned char", (colors1[i].a + colors2[i].a) / 2)


    finalimage = rl.Image(colors, image1.width, image1.height, image1.mipmaps, image1.format)
    return finalimage