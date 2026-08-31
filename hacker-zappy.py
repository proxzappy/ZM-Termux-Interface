import os
import sys
import time
import pty
import select
import termios
import tty
import tempfile
import subprocess
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

# ============================================================
# BLOCK LETTER FONT MAPPING (fixed width = 8 columns, 6 rows)
# ============================================================
BLOCK_FONT = {
    'A': [
        " █████╗ ",
        "██╔══██╗",
        "███████║",
        "██╔══██║",
        "██║  ██║",
        "╚═╝  ╚═╝"
    ],
    'B': [
        "██████╗ ",
        "██╔══██╗",
        "██████╔╝",
        "██╔══██╗",
        "██████╔╝",
        "╚═════╝ "
    ],
    'C': [
        " ██████╗",
        "██╔════╝",
        "██║     ",
        "██║     ",
        "╚██████╗",
        " ╚═════╝"
    ],
    'D': [
        "██████╗ ",
        "██╔══██╗",
        "██║  ██║",
        "██║  ██║",
        "██████╔╝",
        "╚═════╝ "
    ],
    'E': [
        "███████╗",
        "██╔════╝",
        "█████╗  ",
        "██╔══╝  ",
        "███████╗",
        "╚══════╝"
    ],
    'F': [
        "███████╗",
        "██╔════╝",
        "█████╗  ",
        "██╔══╝  ",
        "██║     ",
        "╚═╝     "
    ],
    'G': [
        " ██████╗",
        "██╔════╝",
        "██║  ███╗",
        "██║   ██║",
        "╚██████╔╝",
        " ╚═════╝ "
    ],
    'H': [
        "██╗  ██╗",
        "██║  ██║",
        "███████║",
        "██╔══██║",
        "██║  ██║",
        "╚═╝  ╚═╝"
    ],
    'I': [
        "██╗     ",
        "██║     ",
        "██║     ",
        "██║     ",
        "██║     ",
        "╚═╝     "
    ],
    'J': [
        "     ██╗",
        "     ██║",
        "     ██║",
        "██╗  ██║",
        "╚█████╔╝",
        " ╚════╝ "
    ],
    'K': [
        "██╗  ██╗",
        "██║ ██╔╝",
        "█████╔╝ ",
        "██╔═██╗ ",
        "██║  ██╗",
        "╚═╝  ╚═╝"
    ],
    'L': [
        "██╗     ",
        "██║     ",
        "██║     ",
        "██║     ",
        "███████╗",
        "╚══════╝"
    ],
    'M': [
        "███╗  ██╗",
        "████╗ ██║",
        "██╔████║",
        "██║╚██╔╝",
        "██║ ╚═╝ ",
        "╚═╝     "
    ],
    'N': [
        "███╗  ██╗",
        "████╗ ██║",
        "██╔██╗██║",
        "██║╚███║",
        "██║ ╚██║",
        "╚═╝  ╚═╝"
    ],
    'O': [
        " █████╗ ",
        "██╔══██╗",
        "██║  ██║",
        "██║  ██║",
        "╚█████╔╝",
        " ╚════╝ "
    ],
    'P': [
        "██████╗ ",
        "██╔══██╗",
        "██████╔╝",
        "██╔═══╝ ",
        "██║     ",
        "╚═╝     "
    ],
    'Q': [
        " █████╗ ",
        "██╔══██╗",
        "██║  ██║",
        "██║▄▄██║",
        "╚█████╔╝",
        " ╚══▀▀═╝"
    ],
    'R': [
        "██████╗ ",
        "██╔══██╗",
        "██████╔╝",
        "██╔══██╗",
        "██║  ██║",
        "╚═╝  ╚═╝"
    ],
    'S': [
        "███████╗",
        "██╔════╝",
        "███████╗",
        "╚════██║",
        "███████║",
        "╚══════╝"
    ],
    'T': [
        "████████╗",
        "╚══██╔══╝",
        "   ██║  ",
        "   ██║  ",
        "   ██║  ",
        "   ╚═╝  "
    ],
    'U': [
        "██╗  ██╗",
        "██║  ██║",
        "██║  ██║",
        "██║  ██║",
        "╚█████╔╝",
        " ╚════╝ "
    ],
    'V': [
        "██╗  ██╗",
        "██║  ██║",
        "██║  ██║",
        "╚██╗██╔╝",
        " ╚███╔╝ ",
        "  ╚══╝  "
    ],
    'W': [
        "██╗   ██╗",
        "██║   ██║",
        "██║ █╗██║",
        "██║███╗██║",
        "╚███╔███╔╝",
        " ╚══╝╚══╝ "
    ],
    'X': [
        "██╗  ██╗",
        "╚██╗██╔╝",
        " ╚███╔╝ ",
        " ██╔██╗ ",
        "██╔╝ ██╗",
        "╚═╝  ╚═╝"
    ],
    'Y': [
        "██╗   ██╗",
        "╚██╗ ██╔╝",
        " ╚████╔╝ ",
        "  ╚██╔╝  ",
        "   ██║   ",
        "   ╚═╝   "
    ],
    'Z': [
        "███████╗",
        "╚══███╔╝",
        "  ███╔╝ ",
        " ███╔╝  ",
        "███████╗",
        "╚══════╝"
    ],
    '0': [
        " █████╗ ",
        "██╔══██╗",
        "██║  ██║",
        "██║  ██║",
        "╚█████╔╝",
        " ╚════╝ "
    ],
    '1': [
        " ██╗    ",
        "███║    ",
        "╚██║    ",
        " ██║    ",
        " ██║    ",
        " ╚═╝    "
    ],
    '2': [
        "██████╗ ",
        "╚════██╗",
        "█████╔╝ ",
        "██╔═══╝ ",
        "███████╗",
        "╚══════╝"
    ],
    '3': [
        "██████╗ ",
        "╚════██╗",
        "█████╔╝ ",
        "╚════██╗",
        "██████╔╝",
        "╚═════╝ "
    ],
    '4': [
        "██╗  ██╗",
        "██║  ██║",
        "███████║",
        "╚════██║",
        "    ██║ ",
        "    ╚═╝ "
    ],
    '5': [
        "███████╗",
        "██╔════╝",
        "███████╗",
        "╚════██║",
        "███████║",
        "╚══════╝"
    ],
    '6': [
        " ██████╗",
        "██╔════╝",
        "███████╗",
        "██╔═══██╗",
        "╚██████╔╝",
        " ╚═════╝ "
    ],
    '7': [
        "███████╗",
        "╚════██║",
        "   ██╔╝ ",
        "  ██╔╝  ",
        "  ██║   ",
        "  ╚═╝   "
    ],
    '8': [
        " █████╗ ",
        "██╔══██╗",
        "╚█████╔╝",
        "██╔══██╗",
        "╚█████╔╝",
        " ╚════╝ "
    ],
    '9': [
        " █████╗ ",
        "██╔══██╗",
        "╚██████║",
        " ╚═══██║",
        " █████╔╝",
        " ╚════╝ "
    ],
    ' ': [
        "        ",
        "        ",
        "        ",
        "        ",
        "        ",
        "        "
    ]
}

def block_word(word):
    """Convert a word to block letters (fixed width)."""
    rows = [""] * 6
    for ch in word.upper():
        block = BLOCK_FONT.get(ch, BLOCK_FONT[' '])
        for i in range(6):
            rows[i] += block[i]
    return rows

def generate_banner(username=None):
    if not username or username.upper() == "HACKER ZAPPY":
        display_name = "HACKER ZAPPY"
        ascii_art = """
██╗  ██╗ █████╗  ██████╗██╗  ██╗███████╗██████╗ 
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
╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝        ╚═╝          """
    else:
        display_name = username.upper()
        words = display_name.split()
        all_rows = []
        for word in words:
            all_rows.extend(block_word(word))
        ascii_art = "\n" + "\n".join(all_rows)

    return f"""{GREEN}{ascii_art}{RESET}
{LIGHT_GREEN}██████████████████████████████████████████████████████████████████████{RESET}
{YELLOW} [+] OWNER     : {WHITE}{display_name}{RESET}
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
        write(f"\r{LIGHT_GREEN}[{filled}{empty}] {percent:3d}%{RESET}")
        pause(duration / total)
    write("\n")

def startup():
    clear()
    write(generate_banner("HACKER ZAPPY"))
    write("\n")
    progress("Initializing ZAPPY environment...", 0.4)
    progress("Loading terminal interface...", 0.4)
    progress("Preparing shell runtime...", 0.4)
    progress("Checking terminal capabilities...", 0.4)
    write(f"\n{GREEN}[✓] ZAPPY terminal environment ready.{RESET}\n")
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
            return sanitize_name(USER_FILE.read_text(encoding="utf-8"))
    except Exception:
        pass
    return None

def save_username(username):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    USER_FILE.write_text(username, encoding="utf-8")

def ask_username():
    while True:
        write(f"\n{YELLOW}Enter your name: {RESET}")
        try:
            username = input()
        except (KeyboardInterrupt, EOFError):
            write("\n")
            sys.exit(0)
        username = sanitize_name(username)
        if username:
            return username
        write(f"{RED}[-] Please enter a valid name.{RESET}\n")

def set_permanent_terminal():
    while True:
        write(f"\n{YELLOW}Do you want to make this your permanent terminal? (y/n): {RESET}")
        try:
            choice = input().strip().lower()
        except (KeyboardInterrupt, EOFError):
            write("\n")
            sys.exit(0)
        
        if choice == 'y':
            bashrc_path = Path.home() / ".bashrc"
            script_path = os.path.abspath(sys.argv[0])
            
            try:
                if bashrc_path.exists():
                    content = bashrc_path.read_text(encoding="utf-8")
                    if script_path in content:
                        write(f"{GREEN}[+] Already set as default terminal.{RESET}\n")
                        return
            except Exception:
                pass
            
            try:
                with open(bashrc_path, "a", encoding="utf-8") as f:
                    f.write(f"\n# >>> HACKER ZAPPY START >>>\npython3 {script_path}\nexit\n# <<< HACKER ZAPPY END <<<\n")
                write(f"{GREEN}[✓] ZAPPY is now your default permanent terminal!{RESET}\n")
                pause(0.8)
            except Exception as e:
                write(f"{RED}[-] Failed to set as default: {e}{RESET}\n")
            break
        elif choice == 'n':
            write(f"{CYAN}[*] Skipped. Terminal default nahi kiya gaya.{RESET}\n")
            pause(0.8)
            break
        else:
            write(f"{RED}[-] Invalid input! Sirf 'y' ya 'n' likhein.{RESET}\n")

def remove_permanent_terminal():
    """Remove ZAPPY auto-start from .bashrc"""
    bashrc_path = Path.home() / ".bashrc"
    if not bashrc_path.exists():
        print(f"{RED}[-] .bashrc not found.{RESET}")
        return False

    try:
        content = bashrc_path.read_text(encoding="utf-8")
        lines = content.splitlines()
        new_lines = []
        skip = False
        removed = False

        for line in lines:
            if "# >>> HACKER ZAPPY START >>>" in line:
                skip = True
                removed = True
                continue
            if "# <<< HACKER ZAPPY END <<<" in line:
                skip = False
                continue
            if not skip:
                new_lines.append(line)

        if removed:
            bashrc_path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
            print(f"{GREEN}[✓] ZAPPY default terminal removed successfully.{RESET}")
            return True
        else:
            print(f"{YELLOW}[*] ZAPPY default terminal not found in .bashrc.{RESET}")
            return False
    except Exception as e:
        print(f"{RED}[-] Failed to remove: {e}{RESET}")
        return False

def first_setup():
    startup()
    username = ask_username()
    write(f"\n{GREEN}[+] Creating profile for {WHITE}{username}{GREEN}...{RESET}\n")
    pause(0.35)
    progress(f"Loading {username} environment...", 0.7)
    save_username(username)
    
    set_permanent_terminal()
    
    write(f"\n{GREEN}[✓] Welcome, {WHITE}{username}{GREEN}!{RESET}\n")
    pause(0.8)
    # Ab user ka banner dikhayein aur phir terminal start hoga
    clear()
    write(generate_banner(username))
    write("\n")

def returning_user(username):
    clear()
    write(generate_banner(username))
    write("\n")
    write(f"{GREEN}[+] Welcome back, {WHITE}{username}{GREEN}!{RESET}\n")
    total = 12
    for i in range(total + 1):
        filled = "█" * i
        empty = "░" * (total - i)
        write(f"\r{LIGHT_GREEN}[{filled}{empty}] {int((i / total) * 100):3d}%{RESET}")
        pause(0.025)
    write("\n")
    # Ab screen clear nahi karenge, terminal yahin se start hoga
    # pause(0.25)
    # clear()  # isse remove kar diya

def bash_script(username):
    username = username.replace("\\", "\\\\").replace('"', '\\"').replace("$", "\\$").replace("`", "\\`")
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
        self.rcfile_path = None

    def _create_rcfile(self):
        content = bash_script(self.username)
        fd, path = tempfile.mkstemp(suffix=".zappy", text=True)
        with os.fdopen(fd, "w") as f:
            f.write(content)
        self.rcfile_path = path

    def _cleanup_rcfile(self):
        if self.rcfile_path:
            try:
                os.unlink(self.rcfile_path)
            except Exception:
                pass
            self.rcfile_path = None

    def restore_terminal(self):
        if self.original_terminal is None:
            return
        try:
            termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, self.original_terminal)
        except Exception:
            pass

    def set_raw_terminal(self):
        try:
            tty.setraw(sys.stdin.fileno())
        except Exception:
            pass

    def resize_pty(self):
        try:
            import fcntl
            import struct
            rows, cols = os.get_terminal_size()
            size = struct.pack("HHHH", rows, cols, 0, 0)
            fcntl.ioctl(self.fd, 0x5414, size)
        except Exception:
            pass

    def start(self):
        self._create_rcfile()

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
            env["TERM"] = env.get("TERM", "xterm-256color")
            env["COLORTERM"] = "truecolor"
            env["ZAPPY_USER"] = self.username

            args = [shell, "--noprofile", "--rcfile", self.rcfile_path, "-i"]
            os.execvpe(shell, args, env)

        self.original_terminal = termios.tcgetattr(sys.stdin.fileno())
        self.set_raw_terminal()
        self.resize_pty()

    def run(self):
        self.start()
        stdin_fd = sys.stdin.fileno()

        try:
            while True:
                readable, _, _ = select.select([stdin_fd, self.fd], [], [], 0.05)

                if stdin_fd in readable:
                    try:
                        data = os.read(stdin_fd, 8192)
                    except OSError:
                        break
                    if not data:
                        break
                    try:
                        os.write(self.fd, data)
                    except OSError:
                        break

                if self.fd in readable:
                    try:
                        data = os.read(self.fd, 8192)
                    except OSError:
                        break
                    if not data:
                        break
                    try:
                        os.write(sys.stdout.fileno(), data)
                    except OSError:
                        break

        except KeyboardInterrupt:
            try:
                os.write(self.fd, b"\x03")
            except Exception:
                pass
        finally:
            self.restore_terminal()
            self._cleanup_rcfile()

def main():
    if "--remove-default" in sys.argv:
        remove_permanent_terminal()
        sys.exit(0)

    username = load_username()
    if username is None:
        first_setup()
        username = load_username()
        if username is None:
            write(f"{RED}[-] Failed to save profile.{RESET}\n")
            sys.exit(1)
    else:
        returning_user(username)

    terminal = ZappyTerminal(username)
    terminal.run()

if __name__ == "__main__":
    main()
