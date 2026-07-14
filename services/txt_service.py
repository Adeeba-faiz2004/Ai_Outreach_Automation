import os


class TXTService:

    def save_email(self, filename: str, subject: str,content: str) -> None:
    
        """
        Save an email as a TXT file.
        """

        file_path = os.path.join("exports", filename)

        with open(file_path, "w", encoding="utf-8") as file:
         file.write(f"Subject: {subject}\n\n")
         file.write("-" * 50)
         file.write("\n\n")
         file.write(content)

        print(f"{filename} exported successfully.")