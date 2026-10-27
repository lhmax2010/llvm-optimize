unsigned bolt_probe(unsigned x, unsigned y) { return (x * 33u) ^ (y + (x >> 3)); }
int bolt_branch(int x) { return x < 0 ? -x : x * 7 + 1; }
