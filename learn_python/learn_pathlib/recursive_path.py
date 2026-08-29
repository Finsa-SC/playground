from pathlib import Path
import shutil

target = Path("/home/silence-suzuka/Project/playground/learn_python/learn_pathlib/my-dir")

destination = target.parent / "backup_dir"
destination.mkdir(parents=True, exist_ok=True)

# try:
# #     #Copy with pathlib
# #     # target.copy_into(destination)
# #
#     #Copy with shutil
#     shutil.copytree(target, destination, dirs_exist_ok=True)
# except Exception as e:
#     shutil.rmtree(destination)
#     print(f"Error occuered: {e}")
print(shutil.disk_usage(target))
#
# target_file = target / "hello.txt"
# target_file.copy(target / "hello_to.txt")

print(destination)