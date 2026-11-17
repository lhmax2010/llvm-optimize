TOKENS = ("clang-bolt-helper.py post ", "BOLT_POST_GATE_PASS", "disk-report post")
def check_post(body, enabled):
    counts = {token: body.count(token) for token in TOKENS}
    expected = 1 if enabled else 0
    if any(value != expected for value in counts.values()):
        raise AssertionError("post macro expected=%d counts=%s" % (expected, counts))
    return counts
