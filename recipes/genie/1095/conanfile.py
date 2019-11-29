import conans
import os
import os.path
import pathlib
import shutil


OSES = [
    "Windows", "Linux", "Macos"
]


class GenieConan(conans.ConanFile):
    name = "genie"
    version = "1095"
    settings = ("os_build",)

    def _use_prebuilt(self):
        return self.settings.os_build in OSES

    def _download_binary(self):
        data = self.conan_data["binaries"][str(self.settings.os_build)]
        if self.settings.os_build == "Windows":
            name = "genie.exe"
        else:
            name = "genie"
        conans.tools.download(
            url=data['url'],
            filename=name
        )
        conans.tools.check_sha256(name, data['sha256'])
        os.makedirs("bin", exist_ok=True)
        shutil.move(name, f"bin/{name}")

    def _download_source(self):
        conans.tools.get(
            **self.conan_data["sources"]["2019-11-14"]
        )
        shutil.move("GENie-84f9352bd2f8bbdb52e931a436423fa3ca473ebb", "src")

    def source(self):
        if self._use_prebuilt():
            self._download_binary()
        else:
            self._download_source()

    def build(self):
        if not self._use_prebuilt():
            shutil.copytree(pathlib.Path(self.source_folder) / "src", "src")
            self.run("make", cwd="src", run_environment=True)

    def package(self):
        # the make file for genie seems to create a "bin" directory, then a
        # directory named after the OS, then the binary, such as
        # `bin/linux/genie`. Since I can't test all the OSes, figure out the
        # name programmatically.

        build = pathlib.Path(self.build_folder)
        bin_dir = build / "src/bin"
        directories = [d for d in bin_dir.iterdir() if d.is_dir() ]
        if len(directories) < 1:
            raise RuntimeError(
                "Can't find output directory. Did the make file run?")
        elif len(directories) > 1:
            raise RuntimeError("Expected only one output directory.")

        binaries = [b for b in directories[0].iterdir() if not b.is_dir() ]

        if len(binaries) < 1:
            raise RuntimeError(
                "Can't find output binary. Did the make file run?")
        elif len(binaries) > 1:
            raise RuntimeError("Expected only one output binary.")

        os.makedirs(pathlib.Path(self.package_folder) / "bin", exist_ok=True)
        shutil.copy(
            binaries[0],
            pathlib.Path(self.package_folder) / "bin" / binaries[0].parts[-1])
