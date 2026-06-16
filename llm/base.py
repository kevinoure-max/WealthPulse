class LLMProvider:
    def generate_analysis(self, stats: dict) -> str:
        raise NotImplementedError("Subclasses must implement generate_analysis")
