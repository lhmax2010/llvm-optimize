static int twice(int x) { return x * 2; }
int probe(int *p, int n) { int s=0; for (int i=0;i<n;++i) s += twice(p[i]) + i; return s; }
