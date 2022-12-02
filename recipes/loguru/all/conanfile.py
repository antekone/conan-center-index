import os

from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps, cmake_layout
from conan.tools.files import copy, get

required_conan_version = ">=1.54.0"


class LoguruConan(ConanFile):
    name = "loguru"
    version = "2.1.0"
    settings = "os", "arch", "compiler", "build_type"
    exports_sources = 'CMakeLists.txt'

    options = {
        "use_fmtlib": [True, False],
        "shared": [True, False],
    }

    default_options = {
        "use_fmtlib": False,
        "shared": False,
    }

    def requirements(self):
        if self.options.use_fmtlib:
            self.requires("fmt/9.1.0", transitive_headers=True)

    def validate(self):
        print("validate")
        # TODO: check_min_cppstd(self, 11)

    def source(self):
        get(self, **self.conan_data["sources"][self.version], destination=self.source_folder, strip_root=True)

    def layout(self):
        cmake_layout(self)

    def generate(self):
        tc = CMakeToolchain(self)

        tc.variables["LOGURU_USE_FMTLIB"] = self.options.use_fmtlib
        tc.variables["LOGURU_STATIC"] = not self.options.shared

        tc.generate()
        deps = CMakeDeps(self)
        deps.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        copy(self, pattern='LICENSE.*', src=self.source_folder, dst=os.path.join(self.package_folder, 'licenses'))
        cmake = CMake(self)
        cmake.install()
        copy(self, pattern='loguru.hpp', src=self.source_folder, dst=os.path.join(self.package_folder, 'include'))

    def package_info(self):
        if self.options.use_fmtlib:
            self.cpp_info.components["libloguru"].defines.append("LOGURU_USE_FMTLIB")
            self.cpp_info.components["libloguru"].requires = ["fmt::fmt"]

        if not self.options.shared:
            self.cpp_info.components["libloguru"].defines.append("LOGURU_USE_STATIC")

        self.cpp_info.components["libloguru"].libs = ["loguru"]
        if self.settings.os in ["Linux", "FreeBSD"]:
            self.cpp_info.components["libloguru"].system_libs = ["pthread", "dl"]
