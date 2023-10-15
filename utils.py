

def size_str(s: int) -> str:
    unit = ["B", "KB", "MB", "GB", "TB"]
    t = s
    i = 0
    while i < len(unit) - 1 and t > 1024:
        t = t / 1024
        i += 1
    return f"{t:.2f} {unit[i]}"
