#!/usr/bin/env python3
"""Historical synthetic generator, copied unchanged from bench_compiler.py.

Seed 73419; scale 1: 320 template instances / 400 functions / 3000 blocks.
Original generate() source lines 337-370; see provenance.json for hashes.
"""
import argparse
import hashlib
import json
from pathlib import Path
import random

SEED = 73419

def write(path, data):
    Path(path).write_text(data)

def save(path, data):
    Path(path).write_text(json.dumps(data, indent=2) + "\n")

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def generate(out, scale=1):
    out.mkdir(parents=True, exist_ok=True)
    rng = random.Random(SEED)
    counts = [max(1, round(n * scale)) for n in (320, 400, 3000)]
    headers = 'algorithm array atomic bitset chrono complex deque functional future iomanip iterator limits list map memory mutex numeric optional queue random regex set shared_mutex sstream stack string tuple type_traits unordered_map unordered_set utility variant vector'.split()
    a = ['// Synthetic A: parsing and unique standard-library template instantiation.\n']
    a += ['#include <' + h + '>\n' for h in headers]
    a += ['template<int N> struct Tag { unsigned char bytes[1+N%11]; };\n',
          'template<int N> struct Front { using T=Tag<N>;\n',
          'using P=std::tuple<std::vector<T>,std::map<int,T>,std::variant<T,std::array<T,7>>,std::unordered_map<int,T>,std::deque<T>>;\n',
          'P value; static_assert(std::is_default_constructible<P>::value, "constructible"); };\n']
    a += [f'static_assert(sizeof(Front<{i}>)>0, "instantiate");\n' for i in range(counts[0])]
    a += ['extern "C" unsigned frontend_anchor(unsigned x) { return x+1; }\n']
    b = ['// Synthetic B: many independent medium functions, no external headers.\n']
    for i in range(counts[1]):
        constants = [rng.randrange(1, 65535) | 1 for _ in range(6)]
        b.append(f'extern "C" __attribute__((noinline)) unsigned mid_{i}(unsigned *p, unsigned n, unsigned x) {{\n')
        b.append('for (unsigned j=0;j<n;++j) { unsigned y=p[j&255];\n')
        for k, val in enumerate(constants):
            b.append(f'x=(x^{val}u)+(y*{val+2}u); x=(x<<{k+1})|(x>>{31-k}); if ((x&31)=={k}) y^=x>>3;\n')
        b.append('p[(j+17)&255]=x^y; } return x; }\n')
    c = ['// Synthetic C: a single large data-dependent function, unsigned arithmetic.\n',
         'extern "C" __attribute__((noinline)) unsigned giant(unsigned *p,unsigned x) {\n']
    for i in range(counts[2]):
        val = rng.randrange(1, 65535) | 1
        c.append(f'x^=p[{i%256}]+{val}u; x=(x<<5)|(x>>27); if ((x&15)=={i%16}) x+=p[{(i*7)%256}]; p[{(i*11)%256}]=x;\n')
    c.append('return x; }\n')
    result = {}
    for name, content in zip(('A', 'B', 'C'), (a, b, c)):
        p = out / (name + '.cpp')
        write(p, ''.join(content))
        result[name] = {'sha256': sha(p), 'bytes': p.stat().st_size}
    save(out / 'generator.json', {'seed': SEED, 'scale': scale, 'counts': counts, 'sources': result})
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("--scale", type=float, default=1)
    args = parser.parse_args()
    if args.scale <= 0:
        parser.error("scale must be positive")
    generate(args.output, args.scale)
