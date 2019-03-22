/***
 * CONSOLE BOOTSTRAP
 */
typedef struct CONSOLE_STRUCT {
    void (*log)(void* self, char* msg);
} Console;

void Console_log(Console* self, char* msg) {
    printf("%s\n", msg);
}

Console* init_console() {
    Console* x = calloc(1, sizeof(struct CONSOLE_STRUCT));
    x->log = Console_log;

    return x;
}

Console* console;
/**
 * END OF CONSOLE BOOTSTRAP
 */
