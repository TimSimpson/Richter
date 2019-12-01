#include <iostream>
#include <memory>
#include <stdexcept>
#include <SDL2/SDL.h>
#include <SDL2/SDL_syswm.h>
#include <bx/bx.h>
#include <bgfx/bgfx.h>
#include <bgfx/platform.h>

// I hobbled this together from the following better examples:
// https://github.com/jpcy/bgfx-minimal-example/blob/master/helloworld.cpp
// https://gist.github.com/zlash/abf8d4bc2efb795a02361e4820a2da10

class BgfxStuff {
public:
    BgfxStuff(SDL_Window * window, int width, int height);
    ~BgfxStuff();
    void change_size(int width, int height);
    void render();
private:
    int width, height;
    int old_width, old_height;
    const bgfx::ViewId clear_view;
};

BgfxStuff::BgfxStuff(SDL_Window * window, int width, int height)
:   width(width), height(height), old_width(width), old_height(height),
    clear_view(0)
{
    bgfx::renderFrame();

    SDL_SysWMinfo window_info;
    SDL_VERSION(&window_info.version);
    if (!SDL_GetWindowWMInfo(window, &window_info)) {
        throw std::runtime_error("Whoops, couldn't get window info. Good-bye.");
    }

    bgfx::Init init;

    #if BX_PLATFORM_LINUX || BX_PLATFORM_BSD
        init.platformData.ndt = window_info.info.x11.display;
        init.platformData.nwh = (void*)(uintptr_t)window_info.info.x11.window;
    #elif BX_PLATFORM_OSX
        init.platformData.ndt = nullptr;
        init.platformData.nwh = window_info.info.cocoa.window;
    #elif BX_PLATFORM_WINDOWS
        init.platformData.ndt = nullptr;
        init.platformData.nwh = window_info.info.win.window;
    #else
        #error "Unhandled platform."
    #endif


    init.resolution.width = width;
    init.resolution.height = height;
    init.resolution.reset = BGFX_RESET_VSYNC;

    if (!bgfx::init(init)) {
        throw std::runtime_error("Could not initialize BGFX.");
    }
    bgfx::reset(width, height, BGFX_RESET_VSYNC);

    bgfx::setDebug(BGFX_DEBUG_TEXT);

    bgfx::setViewClear(this->clear_view, BGFX_CLEAR_COLOR);
    bgfx::setViewRect(this->clear_view, 0, 0, bgfx::BackbufferRatio::Equal);
}

BgfxStuff::~BgfxStuff() {
    bgfx::shutdown();
}

void BgfxStuff::change_size(int width, int height) {
    this->width = width;
    this->height = height;
}

void BgfxStuff::render() {
    if (this->width != this->old_width) {
        bgfx::reset((uint32_t)width, (uint32_t)height, BGFX_RESET_VSYNC);
        bgfx::setViewRect(this->clear_view, 0, 0, bgfx::BackbufferRatio::Equal);
        this->old_width = this->width;
        this->old_height = this->height;
    }

    bgfx::touch(clear_view);
    bgfx::dbgTextClear();
    bgfx::dbgTextPrintf(0, 1, 0x0f, "Hello world!");
    const bgfx::Stats* stats = bgfx::getStats();
    bgfx::dbgTextPrintf(0, 2, 0x0f, "Backbuffer %dW x %dH in pixels, debug text %dW x %dH in characters.", width, height, stats->textWidth, stats->textHeight);
    bgfx::setDebug(BGFX_DEBUG_TEXT);
    bgfx::frame();
}

int main(int argc, char **argv) {
    const bool one_frame = (argc == 2 && strcmp(argv[1], "--oneframe") == 0);

    std::cout << "Hey, wassup?\n";

    SDL_Init(SDL_INIT_VIDEO);

    int width = 640;
    int height = 640;

    SDL_Window * window = SDL_CreateWindow(
        "SDL2",
        SDL_WINDOWPOS_CENTERED,
        SDL_WINDOWPOS_CENTERED,
        width,
        height,
        SDL_WINDOW_SHOWN|SDL_WINDOW_RESIZABLE
    );

    BgfxStuff bgfx_stuff(window, width, height);

    bool exit = one_frame;
    SDL_Event event;
    do {
        bgfx_stuff.render();
        while (SDL_PollEvent(&event)) {
            switch (event.type) {
                case SDL_QUIT: {
                    exit = true;
                    break;
                }
                case SDL_WINDOWEVENT: {
                    switch (event.window.event) {
                        case SDL_WINDOWEVENT_RESIZED:
                        case SDL_WINDOWEVENT_SIZE_CHANGED:
                            width = event.window.data1;
                            height = event.window.data2;
                            bgfx_stuff.change_size(width, height);
                            break;
                        case SDL_WINDOWEVENT_CLOSE:
                            exit = true;
                            break;
                        default:
                            break;
                        }
                    break;
                }
                default:
                    break;
            }
        }
    } while(!exit);
    return 0;
}
