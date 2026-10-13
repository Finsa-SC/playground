from dataclasses import dataclass

@dataclass(frozen=True)
class Color:
    RESET: str = "\033[0m"

    # --- Styles ---
    BOLD: str = "\033[1m"
    DIM: str = "\033[2m"
    ITALIC: str = "\033[3m"
    UNDERLINE: str = "\033[4m"
    BLINK: str = "\033[5m"
    REVERSE: str = "\033[7m"

    # --- Foreground (Standard) ---
    BLACK: str = "\033[30m"
    RED: str = "\033[31m"
    GREEN: str = "\033[32m"
    YELLOW: str = "\033[33m"
    BLUE: str = "\033[34m"
    MAGENTA: str = "\033[35m"
    CYAN: str = "\033[36m"
    WHITE: str = "\033[37m"

    # --- Foreground (Bright) ---
    BRIGHT_BLACK: str = "\033[90m"  # Gray
    BRIGHT_RED: str = "\033[91m"
    BRIGHT_GREEN: str = "\033[92m"
    BRIGHT_YELLOW: str = "\033[93m"
    BRIGHT_BLUE: str = "\033[94m"
    BRIGHT_MAGENTA: str = "\033[95m"
    BRIGHT_CYAN: str = "\033[96m"
    BRIGHT_WHITE: str = "\033[97m"

    # --- Background (Standard) ---
    BG_BLACK: str = "\033[40m"
    BG_RED: str = "\033[41m"
    BG_GREEN: str = "\033[42m"
    BG_YELLOW: str = "\033[43m"
    BG_BLUE: str = "\033[44m"
    BG_MAGENTA: str = "\033[45m"
    BG_CYAN: str = "\033[46m"
    BG_WHITE: str = "\033[47m"

    # --- Background (Bright) ---
    BG_BRIGHT_BLACK: str = "\033[100m"
    BG_BRIGHT_RED: str = "\033[101m"
    BG_BRIGHT_GREEN: str = "\033[102m"
    BG_BRIGHT_YELLOW: str = "\033[103m"
    BG_BRIGHT_BLUE: str = "\033[104m"
    BG_BRIGHT_MAGENTA: str = "\033[105m"
    BG_BRIGHT_CYAN: str = "\033[106m"
    BG_BRIGHT_WHITE: str = "\033[107m"


class PrintLog:
    # --- Reset ---

    def __init__(self, text: str):
        self.text = text
        self.__text_color = Color.RESET
        self.__background_color = Color.RESET

    def __str__(self) -> str:
        return (f"{self.__text_color}"
                f"{self.__background_color}"
                f"{self.text}"
                f"{Color.RESET}"
                )

    def color(self, color: str) -> "PrintLog":
        self.__text_color = color
        return self

    def background(self, color: str) -> "PrintLog":
        self.__background_color = color
        return self

    def reset(self):
        self.__background_color = Color.RESET
        self.__text_color = Color.RESET


agus = PrintLog("Hello")
agus.color(Color.BLUE).background(Color.BG_BRIGHT_YELLOW)
print(agus)
agus.reset()

