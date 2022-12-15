import pysdl2

# Initialize the SDL2 library
pysdl2.SDL_Init()

# Create a window and renderer
window = pysdl2.SDL_CreateWindow(b'VSGB', 100, 100, 640, 480, pysdl2.SDL_WINDOW_SHOWN)
renderer = pysdl2.SDL_CreateRenderer(window, -1, pysdl2.SDL_RENDERER_ACCELERATED)

# Create a texture to hold the framebuffer data
texture = pysdl2.SDL_CreateTexture(renderer, pysdl2.SDL_PIXELFORMAT_ARGB1555, pysdl2.SDL_TEXTUREACCESS_STREAMING, 640, 480)

# Update the texture with the framebuffer data
pysdl2.SDL_UpdateTexture(texture, None, framebuffer, 640 * 2)

# Clear the renderer
pysdl2.SDL_RenderClear(renderer)

# Copy the texture to the renderer
pysdl2.SDL_RenderCopy(renderer, texture, None, None)

# Present the rendered image
pysdl2.SDL_RenderPresent(renderer)

# Clean up
pysdl2.SDL_DestroyTexture(texture)
pysdl2.SDL_DestroyRenderer(renderer)
pysdl2.SDL_DestroyWindow(window)
pysdl2.SDL_Quit()
