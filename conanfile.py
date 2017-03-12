from conans import CMake, ConanFile, AutoToolsBuildEnvironment, tools
import os
import shutil

class JpegConan(ConanFile):
    name = "jpeg"
    src_version = "9b"
    version = "9.2" # same as 9b
    ZIP_FOLDER_NAME = name + "-" + src_version
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    exports = ["CMakeLists.txt"]
    url="http://github.com/GatorQue/conan-jpeg"
    license="http://www.infai.org/jpeg"
    description="The Independent JPEG Group (IJG) is responsible for the reference implementation of the original JPEG standard."
    
    def source(self):
        zip_name = "%ssrc.v%s.tar.gz" % (self.name, self.src_version)
        tools.download("http://www.infai.org/jpeg/files?get=%s" % zip_name, zip_name)
        tools.unzip(zip_name)
        os.unlink(zip_name)
        if self.settings.os == "Windows":
            shutil.move("CMakeLists.txt", "%s/CMakeLists.txt" % self.ZIP_FOLDER_NAME)

    def build(self):
        if self.settings.os == "Windows":
            cmake = CMake(self.settings)

            cmake_options = []
            cmake_options.append("-DCMAKE_INSTALL_PREFIX:PATH=../install")
            # JPEG sources can't create shared libraries for Windows when
            # using Visual Studio compilers
            if self.options.shared == True and self.settings.compiler == "gcc":
                cmake_options.append("-DBUILD_SHARED_LIBS=ON")

            self.run("IF not exist build mkdir build")
            cd_build = "cd build"
            self.output.warn('%s && cmake ../%s %s %s' % (cd_build, self.ZIP_FOLDER_NAME, cmake.command_line, " ".join(cmake_options)))
            self.run('%s && cmake ../%s %s %s' % (cd_build, self.ZIP_FOLDER_NAME, cmake.command_line, " ".join(cmake_options)))
            self.output.warn('%s && cmake --build . --target install %s' % (cd_build, cmake.build_config))
            self.run('%s && cmake --build . --target install %s' % (cd_build, cmake.build_config))
        else:
            env_build = AutoToolsBuildEnvironment(self)
            env_build.fpic = self.options.shared

            if self.settings.os == "Macos":
                old_str = '-install_name \$rpath/\$soname'
                new_str = '-install_name \$soname'
                tools.replace_in_file("./%s/configure" % self.ZIP_FOLDER_NAME, old_str, new_str)

            conf_options = []
            conf_options.append("--prefix=/")
            if self.options.shared == True:
                conf_options.append("--enable-shared")
                conf_options.append("--disable-static")
            else:
                conf_options.append("--disable-shared")
                conf_options.append("--enable-static")

            with tools.environment_append(env_build.vars):
                self.run("./configure %s" % " ".join(conf_options), cwd=self.ZIP_FOLDER_NAME)
                self.run("make", cwd=self.ZIP_FOLDER_NAME)
                self.run("make install DESTDIR=%s/install" % self.conanfile_directory, cwd=self.ZIP_FOLDER_NAME)

    def package(self):
        self.copy("*", dst="include", src="install/include")
        self.copy("*", dst="lib", src="install/lib")
        self.copy("*", dst="bin", src="install/bin")

    def package_info(self):
        self.cpp_info.includedirs = ["include"]
        self.cpp_info.libs = ["jpeg"]
