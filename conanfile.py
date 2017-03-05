from conans import ConanFile, AutoToolsBuildEnvironment, tools
import os

class JpegConan(ConanFile):
    name = "jpeg"
    src_version = "9b"
    version = "9.2" # same as 9b
    ZIP_FOLDER_NAME = name + "-" + src_version
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    url="http://github.com/GatorQue/conan-jpeg"
    license="http://www.infai.org/jpeg"
    description="The Independent JPEG Group (IJG) is responsible for the reference implementation of the original JPEG standard."
    
    def source(self):
        zip_name = "%ssrc.v%s.tar.gz" % (self.name, self.src_version)
        tools.download("http://www.infai.org/jpeg/files?get=%s" % zip_name, zip_name)
        tools.unzip(zip_name)
        os.unlink(zip_name)

    def build(self):
        env_build = AutoToolsBuildEnvironment(self)
        env_build.fpic = self.options.shared
        with tools.environment_append(env_build.vars):
            self.run("./configure", cwd=self.ZIP_FOLDER_NAME)
            self.run("make", cwd=self.ZIP_FOLDER_NAME)

    def package(self):
        # Copying include headers
        self.copy("*.h", "include", "%s" % (self.ZIP_FOLDER_NAME), keep_path=False)

        # Copying static and dynamic libs
        if self.settings.os == "Windows":
            if self.options.shared:
                self.copy(pattern="*.dll", dst="bin", src=self.ZIP_FOLDER_NAME, keep_path=False)
                self.copy(pattern="*jpeg.lib", dst="lib", src=self.ZIP_FOLDER_NAME, keep_path=False)
            else:
                self.copy(pattern="*jpeg.*", dst="lib", src=self.ZIP_FOLDER_NAME, keep_path=False)
        else:
            if self.options.shared:
                if self.settings.os == "Macos":
                    self.copy(pattern="*.dylib", dst="lib", src=self.ZIP_FOLDER_NAME, keep_path=False)
                else:
                    self.copy(pattern="*.so*", dst="lib", src=self.ZIP_FOLDER_NAME, keep_path=False)
            else:
                self.copy(pattern="*.a", dst="lib", src=self.ZIP_FOLDER_NAME, keep_path=False)

    def package_info(self):
        self.cpp_info.includedirs = ["include"]
        self.cpp_info.libs = ["jpeg"]
