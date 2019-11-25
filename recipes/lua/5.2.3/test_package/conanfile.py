import conans

class TestPackage(conans.ConanFile):

    generators = "cmake"

    def build(self):
        cmake = conans.CMake(self)
        cmake.configure()
        cmake.build()

    def test(self):
        self.run("lua -v", run_environment=True)
        self.run(f"{self.build_folder}/bin/lua_test", run_environment=True)
