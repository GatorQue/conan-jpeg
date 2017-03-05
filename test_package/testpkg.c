#include <stdio.h>
#include <jpeglib.h>
#include <jversion.h>

int main(int argc, char **argv)
{
    struct jpeg_decompress_struct cinfo;
    struct jpeg_error_mgr jerr;

    printf("JPEG Version: %s\n", JVERSION);
    cinfo.err = jpeg_std_error(&jerr);
    jpeg_create_decompress(&cinfo);

    return jerr.num_warnings ? 1 : 0;
}
