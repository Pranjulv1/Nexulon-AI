def detect(text):
    text = text.lower()
    if "device" in text or "performance" in text or "cpu" in text:
        return "PERFORMANCE"
    if "project" in text or "what is this" in text:
        return "PROJECT"
    return "GENERAL"