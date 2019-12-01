import conans

class TestPackage(conans.ConanFile):

    generators = "cmake_paths"
    requires = (
        "sdl2/2.0.8@bincrafters/stable",
        "sdl2_image/2.0.3@bincrafters/stable",
    )

    def build(self):
        cmake = conans.CMake(self)
        cmake.configure()
        cmake.build()

    def test(self):
        # This is probably not portable, and wouldn't work in some headless
        # environments, so for now I'll just
        pass
        # self.run("./bgfx_test --oneframe", run_environment=True)
