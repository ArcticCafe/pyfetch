import rich
from rich.table import Table
from rich.text import Text

from pyfetch.info_collector import InfoCollector

logo = r"""[cyan]
          $1▗▄▄▄       $2▗▄▄▄▄    ▄▄▄▖
          $1▜███▙       $2▜███▙  ▟███▛
           $1▜███▙       $2▜███▙▟███▛
            $1▜███▙       $2▜██████▛
     $1▟█████████████████▙ $2▜████▛     $3▟▙
    $1▟███████████████████▙ $2▜███▙    $3▟██▙
           $6▄▄▄▄▖           $2▜███▙  $3▟███▛
          $6▟███▛             $2▜██▛ $3▟███▛
         $6▟███▛               $2▜▛ $3▟███▛
$6▟███████████▛                  $3▟██████████▙
$6▜██████████▛                  $3▟███████████▛
      $6▟███▛ $5▟▙               $3▟███▛
     $6▟███▛ $5▟██▙             $3▟███▛
    $6▟███▛  $5▜███▙           $3▝▀▀▀▀
    $6▜██▛    $5▜███▙ $4▜██████████████████▛
     $6▜▛     $5▟████▙ $4▜████████████████▛
           $5▟██████▙         $4▜███▙
          $5▟███▛▜███▙         $4▜███▙
         $5▟███▛  ▜███▙         $4▜███▙
         $5▝▀▀▀    ▀▀▀▀▘         $4▀▀▀▘
        [/cyan]
"""


class Printer:
    def __init__(self):
        self.console = rich.get_console()

    def print(self, info_dict):

        info = Text()

        server_name = info_dict.get("os_info", {}).get("server_name", "unknown")
        user_name = info_dict.get("os_info", {}).get("user_name", "unknown")
        header = f"{user_name}@{server_name}"

        info.append("\n")
        info.append(f"{header}\n", style="bold cyan")
        info.append("-" * len(header) + "\n")

        for key, dicts in info_dict.items():
            for sub_key, sub_value in dicts.items():
                if sub_key == "server_name":
                    continue
                clean_key = sub_key.replace("_", " ").title()
                info.append(f"{clean_key}: ", style="bold cyan")
                info.append(f"{sub_value}\n")

        grid = Table.grid(padding=(0, 4))
        grid.add_row(logo, info)

        self.console.print(grid)


if __name__ == "__main__":
    printer = Printer()
    collector = InfoCollector()
    printer.print(collector.get_info_dict())
