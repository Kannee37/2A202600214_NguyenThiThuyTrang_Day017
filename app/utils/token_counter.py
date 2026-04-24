def estimate_tokens(text: str) -> int:
    """
    Estimate đơn giản: 1 token ~ 4 ký tự.
    """
    return max(1, len(text) // 4)