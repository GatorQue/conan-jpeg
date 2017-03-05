#include <stdio.h>
#include <jpeglib.h>

int main(int argc, char **argv)
{
    struct jpeg_decompress_struct cinfo;
    struct jpeg_error_mgr jerr;

    printf("JPEG Version: %d.%d\n", JPEG_LIB_VERSION_MAJOR, JPEG_LIB_VERSION_MINOR);
    cinfo.err = jpeg_std_error(&jerr);
    jpeg_create_decompress(&cinfo);

    return jerr.num_warnings ? 1 : 0;
}
