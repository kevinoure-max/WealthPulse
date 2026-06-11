class LLMProvider:
    def generated_analysis(self, stats: dict) -> str:
        raise NotImplementedError("Subclasses must implement generate_analysis")
