class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_colored(text: str, *colors: Colors):
    print(colored_string(text, *colors))


def colored_string(text: str, *colors: Colors):
    output = text
    for color in colors:
        output = f"{color}{output}{Colors.ENDC}"
    return output
