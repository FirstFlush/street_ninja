

class TokenNavigator:

    def __init__(self, tokens:list[str]):
        self.tokens = tokens
        self.tokens_length = len(tokens)
    
    def get_before(self, token_index: int, count: int=1) -> str | None:
        """Gets the token `count` positions before the given index."""
        if token_index >= count:
            return self.tokens[token_index - count]

    def get_after(self, token_index: int, count: int=1) -> str | None:
        """Gets the token `count` positions after the given index."""
        if token_index < self.tokens_length - count:
            return self.tokens[token_index + count]
