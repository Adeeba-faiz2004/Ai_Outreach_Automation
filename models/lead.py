class Lead:
    """
    Represents a single outreach lead.
    """

    def __init__(
        self,
        name: str,
        company: str,
        position: str,
        industry: str,
        email:str,
    ):

        self.name = name
        self.company = company
        self.position = position
        self.industry = industry
        self.email = email