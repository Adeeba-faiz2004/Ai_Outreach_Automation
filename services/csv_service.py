"""
CSV Service
-----------
Responsible for loading lead data from CSV files.
"""

import pandas as pd

from models.lead import Lead


class CSVService:
    """
    Handles CSV file operations.
    """

    def load_leads(self, file_path: str) -> list[Lead]:
        """
        Load leads from a local CSV file.
        """

        df = pd.read_csv(file_path)

        return self._convert_dataframe_to_leads(df)

    def load_uploaded_leads(self, uploaded_file) -> list[Lead]:
        """
        Load leads from a Streamlit uploaded CSV file.
        """

        # Reset pointer (important for Streamlit uploads)
        uploaded_file.seek(0)

        df = pd.read_csv(uploaded_file)

        return self._convert_dataframe_to_leads(df)

    def _convert_dataframe_to_leads(
        self,
        df: pd.DataFrame,
    ) -> list[Lead]:
        """
        Convert a pandas DataFrame into a list of Lead objects.
        """

        required_columns = [
            "Name",
            "Company",
            "Position",
            "Industry",
            "Email",
        ]

        # Normalize headers (strip whitespace, match case-insensitively)
        # so a CSV with "name"/"NAME"/" Name " still works instead of
        # rejecting the whole upload.
        column_lookup = {
            str(col).strip().lower(): col for col in df.columns
        }

        rename_map = {}
        missing = []

        for column in required_columns:
            key = column.lower()
            if key in column_lookup:
                rename_map[column_lookup[key]] = column
            else:
                missing.append(column)

        if missing:
            raise ValueError(
                f"Missing required column(s): {', '.join(missing)}"
            )

        df = df.rename(columns=rename_map)

        leads = []
        skipped_rows = 0

        for _, row in df.iterrows():

            name = str(row["Name"]).strip()
            email = str(row["Email"]).strip()

            # Skip rows with no name/email at all instead of silently
            # generating a broken lead (e.g. name="nan", email="nan").
            if not name or name.lower() == "nan" or not email or email.lower() == "nan":
                skipped_rows += 1
                continue

            lead = Lead(
                name=name,
                company=str(row["Company"]).strip(),
                position=str(row["Position"]).strip(),
                industry=str(row["Industry"]).strip(),
                email=email,
            )

            leads.append(lead)

        if skipped_rows:
            print(f"⚠️ Skipped {skipped_rows} row(s) missing a name or email.")

        return leads