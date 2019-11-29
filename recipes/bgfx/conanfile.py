import conans
import os
import os.path
import pathlib
import shutil


GEN_SRC = pathlib.Path('gen_src')


class BgfxConan(conans.ConanFile):
    name = "bgfx"
    version = "2019-11-25"
    # settings = "os", "compiler", "build_type", "arch"
    # exports = ["conanfile.py", "CMakeLists.txt"]
    # lua_dir = pathlib.Path(f'lua-{version}')

    # Where the extract file contents end up.
    lua_dir = pathlib.Path(f'lua-{version}')

    projects = ["bgfx", "bimg", "bx"]


    def source(self):
        # Download the official Lua sources
        for project in self.projects:
            # conans.tools.get(
            #     **self.conan_data["sources"][f"{project}/{self.version}"]
            # )
            os.rename(f"{project}-master", project)



        # shutil.copy(pathlib.Path(__file__).parent / "CMakeLists.txt",
        #             self.lua_dir / "CMakeLists.txt")
        # shutil.copy(pathlib.Path(__file__).parent / "Config.cmake.in",
        #             self.lua_dir / "Config.cmake.in")

    # def _configed_cmake(self):
    #     cmake = conans.CMake(self)
    #     lua_dir = pathlib.Path(self.source_folder) / self.lua_dir
    #     cmake.configure(source_folder=str(lua_dir))
    #     return cmake

    # def build(self):
    #     cmake = self._configed_cmake()
    #     cmake.build()

    # def package(self):
    #     cmake = self._configed_cmake()
    #     cmake.install()

    #     # self.copy(pattern="*.h", dst="include", src=os.path.join(self.lua_dir, "src"))
    #     # self.copy(pattern="*.lib", dst="lib", src="lib")
    #     # self.copy(pattern="*.a", dst="lib", src="lib")

    # def package_info(self):
    #     self.cpp_info.libs = ["lua_lib"]
    #     self.cpp_info.includedirs = [f"include/lua{self.version}"]
