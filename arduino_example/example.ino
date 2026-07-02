#include <MD_MAX72xx.h>
#include <SPI.h>

#include "eight_bit.h"

#define HARDWARE_TYPE MD_MAX72XX::FC16_HW
#define MAX_DEVICES 4

MD_MAX72XX mx(HARDWARE_TYPE, 9, MAX_DEVICES);

void drawChar(int x, char c)
{
    if (c < eight_bit_font_start_char || c > eight_bit_font_end_char)
        return;

    uint8_t index = c - eight_bit_font_start_char;

    uint16_t start = pgm_read_word(&eight_bit_font_offsets[index]);
    uint16_t end   = pgm_read_word(&eight_bit_font_offsets[index + 1]);

    uint8_t width = end - start;

    for (uint8_t col = 0; col < width; col++)
    {
        uint8_t bits = pgm_read_byte(&eight_bit_font_data[start + col]);

        if (x + col >= 0 && x + col < 32)
            mx.setColumn(31 - (x + col), bits);
    }
}

void drawString(const char *str)
{
    mx.clear();

    int x = 0;

    while (*str)
    {
        drawChar(x, *str);

        uint8_t idx = *str - eight_bit_font_start_char;
        uint8_t w = pgm_read_word(&eight_bit_font_offsets[idx + 1]) -
                    pgm_read_word(&eight_bit_font_offsets[idx]);

        x += w + 1;      //one column spacing

        str++;

        if (x >= 32)
            break;
    }

    mx.update();
}

void setup()
{
    mx.begin();
    mx.control(MD_MAX72XX::INTENSITY, 2);

    drawString("HELLO");
}

void loop()
{

}