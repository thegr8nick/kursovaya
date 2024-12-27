import time


def knuth_morris_pratt(text, pattern):
    start_time = time.time()
    text = text.lower()
    pattern = pattern.lower()
    m, n = len(pattern), len(text)
    lps = [0] * m
    positions = []

    j = 0
    for i in range(1, m):
        while j > 0 and pattern[i] != pattern[j]:
            j = lps[j - 1]
        if pattern[i] == pattern[j]:
            j += 1
            lps[i] = j

    j = 0
    for i in range(n):
        while j > 0 and text[i] != pattern[j]:
            j = lps[j - 1]
        if text[i] == pattern[j]:
            if j == m - 1:
                positions.append(i - m + 1)
                j = lps[j]
            else:
                j += 1

    end_time = time.time()
    execution_time = end_time - start_time
    return positions, execution_time


def rabin_karp(text, pattern):
    start_time = time.time()
    text = text.lower()
    pattern = pattern.lower()
    m, n = len(pattern), len(text)
    d = 256
    q = 101
    pattern_hash = 0
    text_hash = 0
    h = 1
    positions = []

    for i in range(m - 1):
        h = (h * d) % q

    for i in range(m):
        pattern_hash = (d * pattern_hash + ord(pattern[i])) % q
        text_hash = (d * text_hash + ord(text[i])) % q

    for i in range(n - m + 1):
        if pattern_hash == text_hash:
            if text[i:i + m] == pattern:
                positions.append(i)
        if i < n - m:
            text_hash = (d * (text_hash - ord(text[i]) * h) + ord(text[i + m])) % q
            if text_hash < 0:
                text_hash += q

    end_time = time.time()
    execution_time = end_time - start_time
    return positions, execution_time


def boyer_moore(text, pattern):
    start_time = time.time()
    text = text.lower()
    pattern = pattern.lower()
    m, n = len(pattern), len(text)
    last = {}
    positions = []

    for i in range(m):
        last[pattern[i]] = i

    i = 0
    while i <= n - m:
        j = m - 1
        while j >= 0 and pattern[j] == text[i + j]:
            j -= 1
        if j < 0:
            positions.append(i)  # Match found
            i += (m - last.get(text[i + m], -1)) if i + m < n else 1
        else:
            i += max(1, j - last.get(text[i + j], -1))

    end_time = time.time()
    execution_time = end_time - start_time
    return positions, execution_time


def check_plagiarism(text, pattern, algorithm):
    text = text.lower()
    pattern = pattern.lower()

    if algorithm == "kmp":
        positions, execution_time = knuth_morris_pratt(text, pattern)
    elif algorithm == "rk":
        positions, execution_time = rabin_karp(text, pattern)
    elif algorithm == "bm":
        positions, execution_time = boyer_moore(text, pattern)
    else:
        raise ValueError("Unknown algorithm")

    total_occurrences = len(positions)
    total_text_length = len(text)
    pattern_length = len(pattern)

    if total_occurrences == 0:
        return 0.0, execution_time

    total_matched_chars = total_occurrences * pattern_length
    percentage = (total_matched_chars / total_text_length) * 100

    return round(percentage, 2), execution_time
