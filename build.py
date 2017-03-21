from conan.packager import ConanMultiPackager
import platform


if __name__ == "__main__":
    mingw_configurations = [("4.9", "x86_64", "seh", "posix"),
                            ("4.9", "x86_64", "sjlj", "posix"),
                            ("4.9", "x86", "sjlj", "posix"),
                            ("4.9", "x86", "dwarf2", "posix")]
    builder = ConanMultiPackager(mingw_configurations=mingw_configurations, visual_runtimes=["MD","MDd"], vs10_x86_64_enabled=True)
    builder.add_common_builds(shared_option_name="jpeg:shared", pure_c=True)
    builder.run()
