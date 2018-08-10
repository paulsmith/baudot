typedef enum Shift {
    LTRS = 31,
    FIGS = 27
} Shift;

typedef struct ITA2Char {
    char code;
    Shift shift;
} ITA2Char;