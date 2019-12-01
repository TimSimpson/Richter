import conans
import os
import os.path
import pathlib
import shutil


GEN_SRC = pathlib.Path('gen_src')


class BgfxConan(conans.ConanFile):
    name = "bgfx"
    version = "2019-09-27"
    # settings = "os", "compiler", "build_type", "arch"
    settings = "arch",

    submodules = ["bgfx", "bimg", "bx"]

    # options = {
    #     'build_tools': [True, False]
    # }

    @property
    def _source_path(self):
        return pathlib.Path(self.source_folder)

    @property
    def _build_path(self):
        return pathlib.Path(self.build_folder)

    def _find_unzipped_path(self, name):
        # The zip files from GitHub take the form of "{repo}-<some-guid>"
        unzipped_directories = [
            d for d in self._source_path.iterdir()
            if d.name.startswith(f"{name}-")
        ]
        if len(unzipped_directories) != 1:
            raise RuntimeError("Expected only one unzipped directory.")

        return unzipped_directories[0]

    def source(self):
        # Download the official Lua sources

        conans.tools.get(
            **self.conan_data["sources"][f"bgfx.cmake/{self.version}"]
        )
        main_module_directory = self._find_unzipped_path("bgfx.cmake")
        os.rename(main_module_directory, "root")

        for submodule in self.submodules:
            conans.tools.get(
                **self.conan_data["sources"][f"{submodule}/{self.version}"]
            )
            unzipped_directory = self._find_unzipped_path(submodule)
            os.rename(unzipped_directory,
                      self._source_path / "root" / submodule)

    def _configed_cmake(self):
        cmake = conans.CMake(self)

        # The source CMake file could possibly be updated to build these tools
        # using a toolchain on the build OS rather than the destination OS
        # somehow, but just work around it in Emscripten.
        arch = self.settings.get_safe('arch')
        if arch.startswith("asm.js"):
            cmake.definitions["BGFX_BUILD_TOOLS"] = "FALSE"

        cmake.configure(source_folder=str(self._source_path / "root"))
        return cmake

    def build(self):
        cmake = self._configed_cmake()


        cmake.build()

    def package(self):
        cmake = self._configed_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["lib"]
        self.cpp_info.includedirs = ["include"]
