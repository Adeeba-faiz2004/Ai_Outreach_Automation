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

        # Validate CSV columns
        for column in required_columns:

            if column not in df.columns:

                raise ValueError(
                    f"Missing required column: {column}"
                )

        leads = []

        for _, row in df.iterrows():

            lead = Lead(
                name=str(row["Name"]).strip(),
                company=str(row["Company"]).strip(),
                position=str(row["Position"]).strip(),
                industry=str(row["Industry"]).strip(),
                email=str(row["Email"]).strip(),
            )

            leads.append(lead)

        return leads