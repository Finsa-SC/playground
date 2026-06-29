import subprocess

DANGER_COMMAND = [
    "sudo",
]

class System:
    def __init__(self):
        self.previous_command = None

    @property
    def previous_command(self) -> str:
        return self._previous_command

    @previous_command.setter
    def previous_command(self, command):
        self._previous_command = command

    def run_command(self, command) -> str:
        if self.danger_command(command):
            return f"[1] Danger Command detected\n"

        prompt = subprocess.run(
            command.split(" "),
            text=True,
            capture_output=True,
        )
        if prompt.returncode == 0:
            self.previous_command = command
            return f"[{prompt.returncode}] {prompt.stdout}"
        else:
            return f"[{prompt.returncode}] Failed to execute command: {prompt.stderr}"

    @staticmethod
    def danger_command(command: str) -> bool:
        for i in DANGER_COMMAND:
            if i in command:
                return True
        return False

if __name__ == "__main__":
    syst = System()
    print(syst.run_command("sudo -i"))
    print(syst.run_command("whoami"))
    print(syst.run_command("uname -r"))
    print(syst.run_command("ambatukam ah ah"))
    print(syst.run_command(syst.previous_command))