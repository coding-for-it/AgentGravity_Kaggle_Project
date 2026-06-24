import os


class FileMCP:

    def save_report(self, filename, content):

        os.makedirs("reports", exist_ok=True)

        filepath = os.path.join(
            "reports",
            filename
        )

        with open(
            filepath,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(content)

        return filepath

    def read_report(self, filename):

        filepath = os.path.join(
            "reports",
            filename
        )

        with open(
            filepath,
            "r",
            encoding="utf-8"
        ) as file:

            return file.read()