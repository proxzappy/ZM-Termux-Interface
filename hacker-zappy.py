import os
import sys
import time
import pty
import tty
import termios
import select
import signal
import subprocess
from pathlib import Path

APP_NAME = "HACKER ZAPPY"

CONTACT_1 = "03702723151"
CONTACT_2 = "03312044136"

CONFIG_DIR = Path.home() / ".hacker-zappy"
USER_FILE = CONFIG_DIR / "username"

RESET = "\033[0m"

BOLD = "\033[1m"
DIM = "\033[2m"
BLINK = "\033[5m"

WHITE = "\033[1;37m"

GREEN = "\033[38;5;46m"
LIGHT_GREEN = "\033[38;5;82m"

YELLOW = "\033[38;5;220m"
RED = "\033[38;5;196m"

CYAN = "\033[38;5;39m"
MAGENTA = "\033[38;5;201m"

def write(text=""):
    sys.stdout.write(text)
    sys.stdout.flush()


def clear_screen():
    write("\033[2J\033[H")


def sleep(seconds):
    time.sleep(seconds)


def terminal_width():
    try:
        return os.get_terminal_size().columns
    except Exception:
        return 78


def line(char="█"):
    width = min(terminal_width(), 78)
    return char * width

def show_banner():

    clear_screen()

    banner = f"""
{GREEN}██╗  ██╗ █████╗  ██████╗██╗  ██╗███████╗██████╗     ███████╗ █████╗ ██████╗ ██████╗ ██╗   ██╗
██║  ██║██╔══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗    ╚══███╔╝██╔══██╗██╔══██╗██╔══██╗╚██╗ ██╔╝
███████║███████║██║     █████╔╝ █████╗  ██████╔╝      ███╔╝ ███████║██████╔╝██████╔╝ ╚████╔╝ 
██╔══██║██╔══██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗     ███╔╝  ██╔══██║██╔═══╝ ██╔═══╝   ╚██╔╝  
██║  ██║██║  ██║╚██████╗██║  ██╗███████╗██║  ██║    ███████╗██║  ██║██║     ██║        ██║   
╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝    ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝        ╚═╝{RESET}

{LIGHT_GREEN}{line()}{RESET}

{YELLOW} [+] OWNER     : {WHITE}HACKER ZAPPY{RESET}
{CYAN} [+] CONTACT   : {WHITE}{CONTACT_1}{RESET}
{CYAN} [+] CONTACT   : {WHITE}{CONTACT_2}{RESET}
{MAGENTA} [+] TERMINAL  : {WHITE}ZAPPY SHELL{RESET}
{GREEN} [+] STATUS    : {BOLD}OPERATIONAL [ONLINE]{RESET}

{LIGHT_GREEN}{line()}{RESET}
"""

    write(banner)


def progress(message, duration=0.8):

    write(f"\n{GREEN}[+] {message}{RESET}\n")

    steps = 20

    for i in range(steps + 1):

        percentage = int((i / steps) * 100)

        filled = "█" * i
        empty = "░" * (steps - i)

        write(
            f"\r{LIGHT_GREEN}[{filled}{empty}] "
            f"{percentage:3d}%{RESET}"
        )

        sleep(duration / steps)

    write("\n")


def startup_animation():

    messages = [
        "Initializing ZAPPY environment...",
        "Loading terminal interface...",
        "Preparing shell runtime...",
        "Checking terminal capabilities..."
    ]

    for msg in messages:
        progress(msg, 0.45)

    write(
        f"\n{GREEN}[✓] ZAPPY terminal environment ready.{RESET}\n"
    )

    sleep(0.4)


def sanitize_username(name):

    name = name.strip()

    if not name:
        return None

    name = "".join(
        char for char in name
        if char.isprintable()
        and char not in "\x1b"
    )

    return name[:32]


def get_saved_username():

    try:

        if USER_FILE.exists():

            name = USER_FILE.read_text(
                encoding="utf-8"
            ).strip()

            return sanitize_username(name)

    except Exception:
        pass

    return None


def save_username(name):

    CONFIG_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    USER_FILE.write_text(
        name,
        encoding="utf-8"
    )


def ask_username():

    write(
        f"\n{YELLOW}"
        f"Enter your name: "
        f"{RESET}"
    )

    while True:

        try:
            name = input().strip()
        except (KeyboardInterrupt, EOFError):
            write("\n")
            sys.exit(0)

        name = sanitize_username(name)

        if name:
            return name

        write(
            f"{RED}[-] Please enter a valid name: {RESET}"
        )


def first_run():

    show_banner()

    startup_animation()

    username = ask_username()

    write(
        f"\n{GREEN}[+] Creating user profile...{RESET}\n"
    )

    sleep(0.4)

    progress(
        f"Loading {username} environment...",
        0.7
    )

    save_username(username)

    write(
        f"\n{GREEN}[✓] Welcome, "
        f"{WHITE}{username}{GREEN}!{RESET}\n"
    )

    sleep(0.8)

    clear_screen()


def build_prompt(username):

    cwd = os.getcwd()

    home = str(Path.home())

    if cwd == home:

        location = "~"

    elif cwd.startswith(home + os.sep):

        location = "~" + cwd[len(home):]

    else:

        location = cwd

    return (
        f"\033[38;5;46m"
        f"{username.upper()}"
        f"\033[0m"
        f"@"
        f"\033[38;5;39m"
        f"HACKER-ZAPPY"
        f"\033[0m"
        f":"
        f"\033[38;5;220m"
        f"{location}"
        f"\033[0m"
        f" $ "
    )

SKIP_PROCESSING = {
    "clear",
    "reset",
    "exit",
    "logout"
}


def should_process(command):

    command = command.strip()

    if not command:
        return False

    first = command.split()[0]

    first = os.path.basename(first)

    if first in SKIP_PROCESSING:
        return False

    return True


def processing_animation(command):

    command_display = command.strip()

    if len(command_display) > 45:
        command_display = command_display[:42] + "..."

    write(
        f"\n"
        f"{LIGHT_GREEN}[ZAPPY]{RESET} "
        f"{CYAN}Processing:{RESET} "
        f"{WHITE}{command_display}{RESET}\n"
    )

    frames = [
        "▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒",
        "█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒",
        "███▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒",
        "██████▒▒▒▒▒▒▒▒▒▒▒▒▒▒",
        "█████████▒▒▒▒▒▒▒▒▒▒▒",
        "████████████▒▒▒▒▒▒▒▒",
        "███████████████▒▒▒▒▒",
        "██████████████████▒▒",
        "████████████████████"
    ]

    for frame in frames:

        write(
            f"\r"
            f"{GREEN}[{frame}]{RESET}"
        )

        sleep(0.035)

    write(
        f"\r"
        f"{GREEN}[████████████████████] "
        f"{WHITE}100%{RESET}\n"
    )

    sleep(0.08)


class ZappyShell:

    def __init__(self, username):

        self.username = username

        self.pid = None
        self.fd = None

        self.old_terminal = None


    def spawn(self):

        shell = os.environ.get(
            "SHELL",
            "/data/data/com.termux/files/usr/bin/bash"
        )

        if not os.path.exists(shell):

            shell = "/bin/bash"

        env = os.environ.copy()

        env["TERM"] = env.get(
            "TERM",
            "xterm-256color"
        )

        env["COLORTERM"] = "truecolor"

        env["ZAPPY_USER"] = self.username

        env["PS1"] = ""

        self.pid, self.fd = pty.fork()

        if self.pid == 0:

            os.environ.update(env)

            os.execvpe(
                shell,
                [
                    shell,
                    "--noprofile",
                    "--norc"
                ],
                env
            )

        self.configure_terminal()

    def configure_terminal(self):

        self.old_terminal = termios.tcgetattr(
            sys.stdin
        )

        tty.setraw(sys.stdin)

    def restore_terminal(self):

        if self.old_terminal:

            try:

                termios.tcsetattr(
                    sys.stdin,
                    termios.TCSADRAIN,
                    self.old_terminal
                )

            except Exception:
                pass

    def resize_pty(self):

        try:

            import fcntl
            import struct

            rows, cols = os.get_terminal_size()

            winsize = struct.pack(
                "HHHH",
                rows,
                cols,
                0,
                0
            )

            fcntl.ioctl(
                self.fd,
                0x5414,
                winsize
            )

        except Exception:
            pass

    def run(self):

        self.spawn()

        self.resize_pty()

        command_buffer = b""

        try:

            while True:

                readable, _, _ = select.select(
                    [sys.stdin, self.fd],
                    [],
                    [],
                    0.05
                )

                if sys.stdin in readable:

                    data = os.read(
                        sys.stdin.fileno(),
                        4096
                    )

                    if not data:
                        break

                    if data == b"\x04":

                        os.write(
                            self.fd,
                            data
                        )

                        break

                    if b"\x03" in data:

                        os.write(
                            self.fd,
                            data
                        )

                        command_buffer = b""

                        continue


                    if b"\r" in data or b"\n" in data:

                        parts = data.replace(
                            b"\r\n",
                            b"\n"
                        ).split(b"\n")

                        for index, part in enumerate(parts):

                            if part:
                                command_buffer += part

                            if index < len(parts) - 1:

                                command = (
                                    command_buffer
                                    .decode(
                                        "utf-8",
                                        errors="ignore"
                                    )
                                )

                                command_buffer = b""

                                if should_process(command):

                                    self.restore_terminal()

                                    processing_animation(
                                        command
                                    )

                                    self.configure_terminal()

                                os.write(
                                    self.fd,
                                    b"\n"
                                )

                    else:

                        command_buffer += data

                        os.write(
                            self.fd,
                            data
                        )

                if self.fd in readable:

                    try:

                        output = os.read(
                            self.fd,
                            8192
                        )

                        if not output:
                            break

                        os.write(
                            sys.stdout.fileno(),
                            output
                        )

                    except OSError:

                        break

        except KeyboardInterrupt:

            try:

                os.write(
                    self.fd,
                    b"\x03"
                )

            except Exception:
                pass

        finally:

            self.restore_terminal()

def run_zappy(username):

    shell = ZappyShell(username)

    shell.spawn()

    setup = f"""
export PS1=''
export PROMPT_COMMAND=''
export TERM="${{TERM:-xterm-256color}}"
cd "$HOME"
"""

    os.write(
        shell.fd,
        setup.encode()
    )

    shell.resize_pty()

    command_buffer = b""

    try:

        while True:

            if not command_buffer:

                shell.restore_terminal()

                write(
                    build_prompt(username)
                )

                shell.configure_terminal()

            readable, _, _ = select.select(
                [sys.stdin, shell.fd],
                [],
                [],
                0.05
            )

            if sys.stdin in readable:

                data = os.read(
                    sys.stdin.fileno(),
                    4096
                )

                if not data:
                    break

                if data == b"\x04":

                    os.write(
                        shell.fd,
                        b"exit\n"
                    )

                    break

                if b"\x03" in data:

                    os.write(
                        shell.fd,
                        b"\x03"
                    )

                    command_buffer = b""

                    continue

                if b"\r" in data or b"\n" in data:

                    normalized = data.replace(
                        b"\r\n",
                        b"\n"
                    )

                    pieces = normalized.split(b"\n")

                    for i, piece in enumerate(pieces):

                        if piece:

                            command_buffer += piece

                        if i < len(pieces) - 1:

                            command = (
                                command_buffer
                                .decode(
                                    "utf-8",
                                    errors="ignore"
                                )
                            )

                            command_buffer = b""

                            command_clean = command.strip()


                            if command_clean in (
                                "exit",
                                "logout"
                            ):

                                shell.restore_terminal()

                                write(
                                    f"\n"
                                    f"{GREEN}[✓] "
                                    f"Leaving ZAPPY SHELL...{RESET}\n"
                                )

                                return

                            if command_clean == "clear":

                                os.write(
                                    shell.fd,
                                    b"clear\n"
                                )

                                continue

                            if should_process(
                                command
                            ):

                                shell.restore_terminal()

                                processing_animation(
                                    command
                                )

                                shell.configure_terminal()

                            os.write(
                                shell.fd,
                                command.encode()
                                + b"\n"
                            )

                else:
                    command_buffer += data

                    os.write(
                        shell.fd,
                        data
                    )
            if shell.fd in readable:

                try:

                    output = os.read(
                        shell.fd,
                        8192
                    )

                    if not output:

                        break

                    os.write(
                        sys.stdout.fileno(),
                        output
                    )

                except OSError:

                    break

    except KeyboardInterrupt:

        try:

            os.write(
                shell.fd,
                b"\x03"
            )

        except Exception:
            pass

    finally:

        shell.restore_terminal()
def main():
    username = get_saved_username()

    if not username:

        first_run()

        username = get_saved_username()

        if not username:

            write(
                f"{RED}[-] Could not create user profile.{RESET}\n"
            )

            sys.exit(1)

    run_zappy(username)


if __name__ == "__main__":

    main()
