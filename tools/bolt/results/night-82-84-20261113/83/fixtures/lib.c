__attribute__((noinline)) static int local_fn(int x) { return x*3+5; }
int bar(int x) { return local_fn(x); }
