#include <ctype.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#include "baudot.h"
#include "charmap.c"

Shift state = LTRS;

void reset_shift()
{
    state = LTRS;
}

unsigned char *encode_ita2(char *s)
{
    unsigned char *str = malloc((strlen(s)*2)+1);
    unsigned char *ptr = str;
    reset_shift();
    while (*s) {
        char c = *s;
        if (islower(c))
            c = toupper(c);
        ITA2Char ch = ita2_ascii[(int)c];
        if (state != ch.shift) {
            *ptr++ = ch.shift;
            state = ch.shift;
        }
        *ptr++ = ch.code;
        s++;
    }
    *ptr = '\0';
    return str;
}

char *decode_ita2(unsigned char *s)
{
    char *str = malloc(strlen((char *)s)+1);
    char *ptr = str;
    reset_shift();
    while (*s) {
        if (*s == LTRS || *s == FIGS) {
            state = *s;
        } else {
            if (state == LTRS) {
                *ptr++ = ita2_ltrs2ascii[*s];
            } else {
                *ptr++ = ita2_figs2ascii[*s];
            }
        }
        s++;
    }
    *ptr = '\0';
    return str;
}

void test_roundtrip_ita2()
{
    char *orig_msg = "HELLO, WORLD 123.";
    unsigned char *enc = encode_ita2(orig_msg);
    char *dec_msg = decode_ita2(enc);
    if (strcmp(orig_msg, dec_msg) != 0) {
	    fprintf(stderr, "error decoding: want '%s', got '%s'\n", orig_msg, dec_msg);
    }
}

void test_roundtrip_ita2_all()
{
    char *orig_msg = "E3\nA- S'I8U7\rD\5R4J\aN,F!C:K(T5Z+L)W2H$Y6P0Q1O9B?G&M.X/V;";
    unsigned char *enc = encode_ita2(orig_msg);
    char *dec_msg = decode_ita2(enc);
    if (strcmp(orig_msg, dec_msg) != 0) {
        fprintf(stderr, "error decoding: want '%s', got '%s'\n", orig_msg, dec_msg);
    }
}

int main(int argc, char **argv)
{
    test_roundtrip_ita2();
    test_roundtrip_ita2_all();
    return 0;
}
