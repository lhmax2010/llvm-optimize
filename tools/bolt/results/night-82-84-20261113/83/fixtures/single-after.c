__attribute__((noinline)) int changed(int x) { return x + 9; }
__attribute__((noinline)) int unchanged(int x) { return x * 3; }
int entry(int x) { return changed(x) + unchanged(x); }
