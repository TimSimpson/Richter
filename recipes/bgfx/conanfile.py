import conans
import os
import os.path
import pathlib
import shutil


GEN_SRC = pathlib.Path('gen_src')


class BgfxConan(conans.ConanFile):
    name = "bgfx"
    version = "2019-11-27"
    settings = "os", "compiler", "build_type", "arch"

    repos = ["bgfx", "bimg", "bx"]


    @property
    def source_path(self):
        return pathlib.Path(self.source_folder)

    @property
    def build_path(self):
        return pathlib.Path(self.build_folder)

    def source(self):
        # Download the official Lua sources
        for repo in self.repos:
            conans.tools.get(
                **self.conan_data["sources"][f"{repo}/{self.version}"]
            )
            # The unzipped directory takes the form of "{repo}-<some-guid>"
            unzipped_directories = [
                d for d in self.source_path.iterdir()
                if d.name.startswith(f"{repo}-")
            ]
            if len(unzipped_directories) != 1:
                raise RuntimeError("Expected only one unzipped directory.")

            os.rename(unzipped_directories[0], repo)

    def build(self):
        for repo in self.repos:
            shutil.copytree(self.source_path / repo, self.build_path / repo)

        self.run("make", run_environment=True)


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
