import os
import sys
import time
import pty
import select
import termios
import tty
from pathlib import Path

APP_NAME = "HACKER ZAPPY"
CONTACT_1 = "03702723151"
CONTACT_2 = "03312044136"

CONFIG_DIR = Path.home() / ".hacker-zappy"
USER_FILE = CONFIG_DIR / "username"

RESET = "\033[0m"
BOLD = "\033[1m"
WHITE = "\033[1;37m"
GREEN = "\033[38;5;46m"
LIGHT_GREEN = "\033[38;5;82m"
YELLOW = "\033[38;5;220m"
RED = "\033[38;5;196m"
CYAN = "\033[38;5;39m"
MAGENTA = "\033[38;5;201m"

BANNER = f"""
{GREEN}██╗  ██╗ █████╗  ██████╗██╗  ██╗███████╗██████╗ 
██║  ██║██╔══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗
███████║███████║██║     █████╔╝ █████╗  ██████╔╝
██╔══██║██╔══██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗
██║  ██║██║  ██║╚██████╗██║  ██╗███████╗██║  ██║
╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
███████╗ █████╗ ██████╗ ██████╗ ██╗   ██╗       
╚══███╔╝██╔══██╗██╔══██╗██╔══██╗╚██╗ ██╔╝       
  ███╔╝ ███████║██████╔╝██████╔╝ ╚████╔╝        
 ███╔╝  ██╔══██║██╔═══╝ ██╔═══╝   ╚██╔╝         
███████╗██║  ██║██║     ██║        ██║          
╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝        ╚═╝          {RESET}

{LIGHT_GREEN}██████████████████████████████████████████████████████████████████████{RESET}
{YELLOW} [+] OWNER     : {WHITE}HACKER ZAPPY{RESET}
{CYAN} [+] CONTACT   : {WHITE}{CONTACT_1}{RESET}
{CYAN} [+] CONTACT   : {WHITE}{CONTACT_2}{RESET}
{MAGENTA} [+] TERMINAL  : {WHITE}ZM TERMUX INTERFACE{RESET}
{GREEN} [+] STATUS    : {BOLD}OPERATIONAL [ONLINE]{RESET}
{LIGHT_GREEN}██████████████████████████████████████████████████████████████████████{RESET}
"""


def write(text=""):
    sys.stdout.write(text)
    sys.stdout.flush()


def clear():
    write("\033[2J\033[H")


def pause(seconds):
    time.sleep(seconds)


def progress(message, duration=0.5):
    write(f"{GREEN}[+] {message}{RESET}\n")

    total = 20

    for i in range(total + 1):
        filled = "█" * i
        empty = "░" * (total - i)
        percent = int((i / total) * 100)

        write(
            f"\r{LIGHT_GREEN}"
            f"[{filled}{empty}]"
            f" {percent:3d}%"
            f"{RESET}"
        )

        pause(duration / total)

    write("\n")


def startup():
    clear()
    write(BANNER)
    write("\n")

    progress("Initializing ZAPPY environment...", 0.4)
    progress("Loading terminal interface...", 0.4)
    progress("Preparing shell runtime...", 0.4)
    progress("Checking terminal capabilities...", 0.4)

    write(
        f"\n{GREEN}[✓] ZAPPY terminal environment ready.{RESET}\n"
    )

    pause(0.4)


def sanitize_name(name):
    name = name.strip()

    if not name:
        return None

    result = ""

    for char in name:
        if char.isprintable() and char != "\x1b":
            result += char

    result = result.strip()

    if not result:
        return None

    return result[:32]


def load_username():
    try:
        if USER_FILE.exists():
            return sanitize_name(
                USER_FILE.read_text(
                    encoding="utf-8"
                )
            )
    except Exception:
        pass

    return None


def save_username(username):
    CONFIG_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    USER_FILE.write_text(
        username,
        encoding="utf-8"
    )


def ask_username():
    while True:
        write(
            f"\n{YELLOW}"
            f"Enter your name: "
            f"{RESET}"
        )

        try:
            username = input()
        except (KeyboardInterrupt, EOFError):
            write("\n")
            sys.exit(0)

        username = sanitize_name(username)

        if username:
            return username

        write(
            f"{RED}[-] Please enter a valid name.{RESET}\n"
        )


def first_setup():
    startup()

    username = ask_username()

    write(
        f"\n{GREEN}[+] Creating profile for "
        f"{WHITE}{username}"
        f"{GREEN}...{RESET}\n"
    )

    pause(0.35)

    progress(
        f"Loading {username} environment...",
        0.7
    )

    save_username(username)

    write(
        f"\n{GREEN}[✓] Welcome, "
        f"{WHITE}{username}"
        f"{GREEN}!{RESET}\n"
    )

    pause(0.8)
    clear()


def returning_user(username):
    clear()
    write(BANNER)
    write("\n")

    write(
        f"{GREEN}[+] Welcome back, "
        f"{WHITE}{username}"
        f"{GREEN}!{RESET}\n"
    )

    total = 12

    for i in range(total + 1):
        filled = "█" * i
        empty = "░" * (total - i)

        write(
            f"\r{LIGHT_GREEN}"
            f"[{filled}{empty}]"
            f" {int((i / total) * 100):3d}%"
            f"{RESET}"
        )

        pause(0.025)

    write("\n\n")
    pause(0.25)
    clear()


def bash_script(username):
    username = (
        username
        .replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("$", "\\$")
        .replace("`", "\\`")
    )

    return f'''
export ZAPPY_USER="{username}"
export ZAPPY_HOST="HACKER-ZAPPY"

ZAPPY_GREEN=$'\\033[38;5;46m'
ZAPPY_LIGHT_GREEN=$'\\033[38;5;82m'
ZAPPY_CYAN=$'\\033[38;5;39m'
ZAPPY_YELLOW=$'\\033[38;5;220m'
ZAPPY_WHITE=$'\\033[1;37m'
ZAPPY_RESET=$'\\033[0m'

zappy_prompt() {{
    local zappy_pwd="$PWD"

    if [ "$zappy_pwd" = "$HOME" ]; then
        zappy_pwd="~"
    elif [[ "$zappy_pwd" == "$HOME"/* ]]; then
        zappy_pwd="~${{zappy_pwd#$HOME}}"
    fi

    PS1="${{ZAPPY_GREEN}}${{ZAPPY_USER}}${{ZAPPY_RESET}}@${{ZAPPY_CYAN}}HACKER-ZAPPY${{ZAPPY_RESET}}:${{ZAPPY_YELLOW}}${{zappy_pwd}}${{ZAPPY_RESET}} $ "
}}

zappy_process() {{
    local command="$1"

    [ -z "$command" ] && return

    case "$command" in
        zappy_process*|zappy_debug*|zappy_prompt*|local*|trap*|clear|reset|exit|logout)
            return
            ;;
        nano*|vim*|vi*|nvim*|top*|htop*|ssh*|sftp*)
            return
            ;;
    esac

    printf "\\n${{ZAPPY_LIGHT_GREEN}}[ZAPPY]${{ZAPPY_RESET}} ${{ZAPPY_CYAN}}Processing:${{ZAPPY_RESET}} ${{ZAPPY_WHITE}}%s${{ZAPPY_RESET}}\\n" "$command"

    local frames=(
        "▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒"
        "█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒"
        "███▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒"
        "██████▒▒▒▒▒▒▒▒▒▒▒▒▒▒"
        "█████████▒▒▒▒▒▒▒▒▒▒▒"
        "████████████▒▒▒▒▒▒▒▒"
        "███████████████▒▒▒▒▒"
        "██████████████████▒▒"
        "████████████████████"
    )

    local frame

    for frame in "${{frames[@]}}"; do
        printf "\\r${{ZAPPY_GREEN}}[%s]${{ZAPPY_RESET}}" "$frame"
        sleep 0.025
    done

    printf "\\r${{ZAPPY_GREEN}}[████████████████████]${{ZAPPY_RESET}} ${{ZAPPY_WHITE}}100%%${{ZAPPY_RESET}}\\n"
}}

zappy_debug() {{
    # Disable DEBUG trap to prevent recursion
    trap - DEBUG

    local command="$BASH_COMMAND"

    case "$command" in
        zappy_process*|zappy_debug*|zappy_prompt*|local*|trap*)
            ;;
        clear|reset|exit|logout|nano*|vim*|vi*|nvim*|top*|htop*|ssh*|sftp*)
            ;;
        *)
            zappy_process "$command"
            ;;
    esac

    # Re-enable the DEBUG trap
    trap 'zappy_debug' DEBUG
}}

PROMPT_COMMAND="zappy_prompt"
trap 'zappy_debug' DEBUG

zappy_prompt
'''

class ZappyTerminal:

    def __init__(self, username):
        self.username = username
        self.pid = None
        self.fd = None
        self.original_terminal = None

    def restore_terminal(self):
        if self.original_terminal is None:
            return

        try:
            termios.tcsetattr(
                sys.stdin.fileno(),
                termios.TCSADRAIN,
                self.original_terminal
            )
        except Exception:
            pass

    def set_raw_terminal(self):
        try:
            tty.setraw(
                sys.stdin.fileno()
            )
        except Exception:
            pass

    def resize_pty(self):
        try:
            import fcntl
            import struct

            rows, cols = os.get_terminal_size()

            size = struct.pack(
                "HHHH",
                rows,
                cols,
                0,
                0
            )

            fcntl.ioctl(
                self.fd,
                0x5414,
                size
            )
        except Exception:
            pass

    def start(self):
        shell = os.environ.get("SHELL")

        if not shell:
            candidates = [
                "/data/data/com.termux/files/usr/bin/bash",
                "/bin/bash"
            ]

            for candidate in candidates:
                if os.path.exists(candidate):
                    shell = candidate
                    break

        if not shell:
            shell = "/bin/sh"

        self.pid, self.fd = pty.fork()

        if self.pid == 0:
            env = os.environ.copy()

            env["TERM"] = env.get(
                "TERM",
                "xterm-256color"
            )

            env["COLORTERM"] = "truecolor"
            env["ZAPPY_USER"] = self.username

            os.execvpe(
                shell,
                [
                    shell,
                    "--noprofile",
                    "--norc",
                    "-i"
                ],
                env
            )

        self.original_terminal = termios.tcgetattr(
            sys.stdin.fileno()
        )

        self.set_raw_terminal()
        self.resize_pty()

    def send_setup(self):
        script = bash_script(
            self.username
        )

        os.write(
            self.fd,
            script.encode("utf-8")
        )

        os.write(
            self.fd,
            b"\n"
        )

    def run(self):
        self.start()
        self.send_setup()

        stdin_fd = sys.stdin.fileno()

        try:
            while True:

                readable, _, _ = select.select(
                    [
                        stdin_fd,
                        self.fd
                    ],
                    [],
                    [],
                    0.05
                )

                if stdin_fd in readable:
                    try:
                        data = os.read(
                            stdin_fd,
                            8192
                        )
                    except OSError:
                        break

                    if not data:
                        break

                    try:
                        os.write(
                            self.fd,
                            data
                        )
                    except OSError:
                        break

                if self.fd in readable:
                    try:
                        data = os.read(
                            self.fd,
                            8192
                        )
                    except OSError:
                        break

                    if not data:
                        break

                    try:
                        os.write(
                            sys.stdout.fileno(),
                            data
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


def main():
    username = load_username()

    if username is None:
        first_setup()
        username = load_username()

        if username is None:
            write(
                f"{RED}"
                f"[-] Failed to save profile."
                f"{RESET}\n"
            )
            sys.exit(1)

    else:
        returning_user(username)

    terminal = ZappyTerminal(
        username
    )

    terminal.run()


if __name__ == "__main__":
    main()
