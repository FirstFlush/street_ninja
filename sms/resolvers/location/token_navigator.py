class TokenNavigator:
    """
    Utility class for navigating and accessing tokens in a list with positional awareness.

    Used by location expanders to scan backward and forward around a "hot" token index
    when resolving structured phrases like addresses, intersections, or landmarks.

    Provides safe access to tokens before or after a given index, as well as 
    methods to retrieve windows or ranges of tokens for multi-word phrase detection.
    """
    def __init__(self, tokens: list[str]):
        self.tokens = tokens
        self.tokens_length = len(tokens)

    def get_before(self, token_index: int, count: int = 1) -> str | None:
        if token_index >= count:
            return self.tokens[token_index - count]

    def get_after(self, token_index: int, count: int = 1) -> str | None:
        if token_index < self.tokens_length - count:
            return self.tokens[token_index + count]

    def get_prev(self, token_index: int) -> str | None:
        return self.get_before(token_index)

    def get_next(self, token_index: int) -> str | None:
        return self.get_after(token_index)

    def get_window(self, token_index: int, before: int = 0, after: int = 0) -> list[str]:
        start = max(0, token_index - before)
        end = min(self.tokens_length, token_index + after + 1)
        return self.tokens[start:end]

    def get_range(self, start: int, end: int) -> list[str]:
        return self.tokens[max(0, start):min(end, self.tokens_length)]
