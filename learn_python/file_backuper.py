from pathlib import Path

class BackupSystem:
    def __init__(self, target: str, destination: str = "/tmp", backup_name: str = ""):
        self.target = Path(target)
        self.destination = Path(destination)
        self.backup_name = backup_name if backup_name.strip() else f"{target}_backup"
        self.backup_dir = Path(self.destination / self.backup_name)

    # Check and make destination folder if not exist
    def check_destination(self, make_directory: bool = True) -> None:
        if not self.destination.exists():
            if make_directory:
                self.destination.mkdir(exist_ok=True, parents=True)
            else:
                raise FileNotFoundError(f"Destination {self.destination} not found")

    # Check target existance
    def check_target(self):
        if not self.target.exists():
            raise FileNotFoundError(f"No such directory for {self.target}")

    # Backup file into destination with set name
    def backup_data(self) -> None:
        self.target.copy(self.backup_dir)

    # Check if backup is success or not
    def backup_success(self) -> bool:
        return self.backup_dir.exists()

    # Run all function
    def do_backup(self, make_directory: bool = True) -> str:
        self.check_destination(make_directory=make_directory)
        self.check_target()
        self.backup_data()

        if self.backup_success():
            return f"Success make a backup for {self.target}\n Backup location: {self.backup_dir}"
        return f"Failed to make a backup for {self.target}"

if __name__ == "__main__":
    try:
        # input_target = input("Input your target directory to backup: ")
        # input_destination = input("Input your target directory to backup: ")
        input_target = "/home/silence-suzuka/Pictures"
        input_destination = "/tmp"
        backup = BackupSystem(input_target, input_destination, backup_name="my_backup")

        print(backup.do_backup(make_directory=True))

    except Exception as e:
        print(f"Error occured while trying to backup data: {e}")