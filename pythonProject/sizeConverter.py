import re

class SizeConverter:
    def __init__(self):
        pass

    @staticmethod
    def get_mb_size(base_size: float, size_type: str) -> float:
        base = 1_024

        match size_type:
            case "B":
                return base_size / base
            case "KB":
                return base_size * base
            case "MB":
                return base_size
            case "GB":
                return base_size * base
            case "TB":
                return base_size * base * base
            case _:
                return 0

    def get_clean_format(self, base_size: str) -> tuple[float, str]:
        regex_to_clean = r"^(\d*)([a-zA-Z]{2})$"
        match = re.search(regex_to_clean, base_size, re.IGNORECASE)

        if match:
            clean_size = match.group(1)
            size_suffix = match.group(2)
        else:
            exit 1
        clean_size =
        return

    def format_size(self, base_size):
