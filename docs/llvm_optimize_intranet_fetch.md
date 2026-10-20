# llvm_optimize 内网可断点续传源码包

状态（2026-10-20）：**PASS**。第 2 步 spec 与 8 个补丁逐字节相同；Release 已发布；整包 **425,114,069 字节，5 片**；第 6 步从 GitHub 实际回下、检出、HEAD/TREE/UPSTREAM/ABBREV 核对及再次 GBS 导出全部通过。没有修改源码、构建或推送 Gerrit。

Release：[src-llvm-optimize-6e9d4f2](https://github.com/lhmax2010/llvm-optimize/releases/tag/src-llvm-optimize-6e9d4f2)。下载下方脚本使用的具名 `.partNN` 资产；GitHub 自动生成的 “Source code (zip/tar.gz)” 属于文档仓库，**不是 LLVM 交付包**。

## 1. 本轮裁决与上轮前 5 处差异原文

上轮 8 个 patch 共有 29 行 `index` 缩写长度差异。前 5 处如下，每处列参考 12 位与浅克隆 9 位两行；原文来自 `temp/llvm-optimize-intranet-20261020/tag-export-full.diff`：

```diff
-index 00c352b458c3..0e7107a1964e 100644
+index 00c352b45..0e7107a19 100644
-index eb3f9cbea284..109bfd55923e 100644
+index eb3f9cbea..109bfd559 100644
-index d525b417b4ea..8a8a755a136c 100644
+index d525b417b..8a8a755a1 100644
-index e5aefa012f67..6dcbdb631205 100644
+index e5aefa012..6dcbdb631 100644
-index 9c83abeeb3b1..4a3f8bbac59a 100644
+index 9c83abeeb..4a3f8bbac 100644
```

本轮只在浅克隆 `temp/llvm-optimize-intranet-20261020/llvm` 执行 `git config core.abbrev 12`，写入该仓库 `.git/config`；全局 Git 配置未改。本地 upstream 继续指向 `ca7933e47d3a3451d81e72ac174dcb5aa28b59d1`。固定长度后的原命令导出全部同字节，见 §4。

**本地 upstream 与 `core.abbrev=12` 是为了让 GBS 导出与指定 QB 交付参考一致，不要改动，也不要 fetch 覆盖 upstream。以后要更新代码时，只拉 `sandbox/lhmax2025/llvm_optimize` 分支。** 本轮没有更新远端代码；未来 HEAD 变化后，本页冻结摘要不能直接用于新版本。

历史停止报告：[native 回退，7bab0df](https://github.com/lhmax2010/llvm-optimize/blob/7bab0df9193cab894c6efa3a84c7eda7e84a1b98/docs/llvm_optimize_intranet_fetch.md)、[缩写差异，1759dd5](https://github.com/lhmax2010/llvm-optimize/blob/1759dd57ac57974c4786c828150f2828b3271e05/docs/llvm_optimize_intranet_fetch.md)。历史判定保持原样，本轮按新裁决重新验证。

## 2. 内网服务器直接粘贴

前提：Bash、Git、curl、tar/gzip 与标准 coreutils 已可用，目标路径可写。脚本不需要 Gerrit 连接或输入账号。

- 固定目标：`/home/linhao/toolchain/development/llvm_optimize/llvm`。若已有该目录或同名条目，打印提示并退出，不覆盖。
- 日志：`~/llvm_optimize_fetch.log`，全部输出经 tee 追加。整段在独立 Bash 中运行，不会因失败退出用户的交互 shell。
- 分片保存在目标上级的 `.download-6e9d4f2` 中。每片最多 10 轮，网络中断保留未完成片并断点续传；完整片长度或 SHA 错误则删除重下。全部校验成功后才解包和检出。
- 成功应看到 5 个 `PART_OK`，以及 `HEAD OK`、`TREE OK`、`UPSTREAM OK`、`ABBREV OK`。包中只有 `.git`，工作区文件由 `git checkout -f llvm_optimize` 恢复。

```bash
bash <<'EOF'
cd ~ || exit 1
exec > >(tee -a "$HOME/llvm_optimize_fetch.log") 2>&1
set -u
set -o pipefail
fail() { printf 'ERROR: %s\n' "$*" >&2; exit 1; }
printf '\n=== llvm_optimize fetch: %s ===\n' "$(date -Is)"
TARGET=/home/linhao/toolchain/development/llvm_optimize
if [[ -e "$TARGET/llvm" || -L "$TARGET/llvm" ]]; then
    printf '目标已有 llvm 目录或同名条目，不覆盖：%s/llvm\n' "$TARGET"
    exit 0
fi
for cmd in curl sha256sum stat cat tar git tee mkdir rm mv date; do
    command -v "$cmd" >/dev/null || fail "缺少命令：$cmd"
done
mkdir -p "$TARGET/.download-6e9d4f2" || fail '无法创建下载目录'
cd "$TARGET/.download-6e9d4f2" || fail '无法进入下载目录'
mapfile -t manifest <<'PART_MANIFEST'
llvm_optimize-6e9d4f2-shallow-git.tar.gz.part00 104857600 d20fb365842f98b1903fc78b83d331fce9ee9e38839bedfdba14ba1a7dbae81a https://github.com/lhmax2010/llvm-optimize/releases/download/src-llvm-optimize-6e9d4f2/llvm_optimize-6e9d4f2-shallow-git.tar.gz.part00
llvm_optimize-6e9d4f2-shallow-git.tar.gz.part01 104857600 c67917d83047e87c38ea41b0ab4ccf4866fa729f27086492e8b4e6906f6a8e10 https://github.com/lhmax2010/llvm-optimize/releases/download/src-llvm-optimize-6e9d4f2/llvm_optimize-6e9d4f2-shallow-git.tar.gz.part01
llvm_optimize-6e9d4f2-shallow-git.tar.gz.part02 104857600 6ec8e1ff0b02e32bef49932d8cc58feef74ade94e7524db0374053b7c0047ab5 https://github.com/lhmax2010/llvm-optimize/releases/download/src-llvm-optimize-6e9d4f2/llvm_optimize-6e9d4f2-shallow-git.tar.gz.part02
llvm_optimize-6e9d4f2-shallow-git.tar.gz.part03 104857600 eca80fc527cce125437c114d011884d8c10d99600400bc10a9ae112527b39b3a https://github.com/lhmax2010/llvm-optimize/releases/download/src-llvm-optimize-6e9d4f2/llvm_optimize-6e9d4f2-shallow-git.tar.gz.part03
llvm_optimize-6e9d4f2-shallow-git.tar.gz.part04 5683669 46ba3f46de4d7a364ef43a9542d66290bc1353cb20b4c2f166daf59bbc1c3939 https://github.com/lhmax2010/llvm-optimize/releases/download/src-llvm-optimize-6e9d4f2/llvm_optimize-6e9d4f2-shallow-git.tar.gz.part04
PART_MANIFEST
check_part() {
    local file=$1 bytes=$2 hash=$3
    [[ -f "$file" && ! -L "$file" ]] || return 1
    [[ "$(stat -Lc %s -- "$file")" == "$bytes" ]] || return 1
    printf '%s  %s\n' "$hash" "$file" | sha256sum --check --status
}
parts=()
for row in "${manifest[@]}"; do
    read -r part bytes hash url <<< "$row"
    parts+=("$part")
    ok=0
    for ((round=1; round<=10; round++)); do
        if check_part "$part" "$bytes" "$hash"; then
            ok=1
            break
        fi
        [[ ! -L "$part" ]] || fail "拒绝写入软链接：$part"
        if [[ -f "$part" ]] && (( $(stat -Lc %s -- "$part") >= bytes )); then
            printf '完整片长度或 SHA 不符，删除重下：%s\n' "$part"
            rm -- "$part" || fail "无法删除损坏片：$part"
        fi
        printf 'DOWNLOAD %s round=%d/10\n' "$part" "$round"
        curl --fail -L -C - --retry 20 --retry-delay 10 --max-time 900 \
             --output "$part" "$url"
        rc=$?
        if check_part "$part" "$bytes" "$hash"; then
            ok=1
            break
        fi
        if (( rc == 0 )) || { [[ -f "$part" ]] && (( $(stat -Lc %s -- "$part") >= bytes )); }; then
            printf '片下载完成但长度或 SHA 不符，删除重下：%s\n' "$part"
            rm -f -- "$part" || fail "无法删除损坏片：$part"
        else
            printf 'curl exit=%d；保留未完成片，下轮断点续传：%s\n' "$rc" "$part"
        fi
    done
    (( ok == 1 )) || fail "$part 超过 10 轮仍未通过校验"
    printf 'PART_OK %s %s bytes %s\n' "$part" "$bytes" "$hash"
done
ARCHIVE=llvm_optimize-6e9d4f2-shallow-git.tar.gz
cat -- "${parts[@]}" > "$ARCHIVE.tmp" || fail '拼接失败'
[[ "$(stat -Lc %s -- "$ARCHIVE.tmp")" == '425114069' ]] || fail '整包长度不符'
printf '%s  %s\n' 'cebfeb3cbda216be11f4e760336a2afc3a8d40ad26906482a849225559777f46' "$ARCHIVE.tmp" \
    | sha256sum --check --status || fail '整包 SHA256 不符'
mv -- "$ARCHIVE.tmp" "$ARCHIVE" || fail '保存整包失败'
printf 'ARCHIVE_OK %s\n' 'cebfeb3cbda216be11f4e760336a2afc3a8d40ad26906482a849225559777f46'
tar -tzf "$ARCHIVE" > tar-members.txt || fail '无法读取整包'
while IFS= read -r entry; do
    case "$entry" in llvm/.git|llvm/.git/|llvm/.git/*) ;; *) fail "包内非 .git 条目：$entry";; esac
    [[ "$entry" != *'/../'* ]] || fail "包内路径越界：$entry"
done < tar-members.txt
[[ ! -e "$TARGET/llvm" && ! -L "$TARGET/llvm" ]] || fail '目标 llvm 在下载期间被创建，停止'
tar -xzf "$ARCHIVE" -C "$TARGET" --no-same-owner || fail '解包失败'
git -C "$TARGET/llvm" checkout -f llvm_optimize || fail '检出失败'
head=$(git -C "$TARGET/llvm" rev-parse HEAD) || fail '读取 HEAD 失败'
[[ "$head" == '6e9d4f2bc77e20ba96d586680bb4f4c25eace7d2' ]] || fail "HEAD 不符：$head"
printf 'HEAD OK %s\n' "$head"
tree=$(git -C "$TARGET/llvm" rev-parse 'HEAD^{tree}') || fail '读取 tree 失败'
[[ "$tree" == '80a6fd231c4564a3b762f4ec288cf2c41f9d2e20' ]] || fail "tree 不符：$tree"
printf 'TREE OK %s\n' "$tree"
upstream=$(git -C "$TARGET/llvm" rev-parse refs/heads/upstream) || fail '读取本地 upstream 失败'
[[ "$upstream" == 'ca7933e47d3a3451d81e72ac174dcb5aa28b59d1' ]] || fail "upstream 不符：$upstream"
ancestor=$(git -C "$TARGET/llvm" merge-base HEAD upstream) || fail '查找 upstream 共同祖先失败'
[[ "$ancestor" == "$upstream" ]] || fail "merge-base 不符：$ancestor"
printf 'UPSTREAM OK %s\n' "$upstream"
abbrev=$(git -C "$TARGET/llvm" config --local --get core.abbrev) || fail '读取局部 core.abbrev 失败'
[[ "$abbrev" == '12' ]] || fail "core.abbrev 不符：$abbrev"
printf 'ABBREV OK %s\n' "$abbrev"
remote=$(git -C "$TARGET/llvm" remote get-url origin) || fail '读取 origin 失败'
[[ "$remote" == 'ssh://lhmax2025@review.tizen.org:29418/platform/upstream/llvm' ]] || fail 'origin URL 不符'
state=$(git -C "$TARGET/llvm" status --porcelain) || fail '读取工作区状态失败'
[[ -z "$state" ]] || fail '工作区不干净'
git -C "$TARGET/llvm" remote -v || fail 'remote -v 失败'
git -C "$TARGET/llvm" log --oneline -3 || fail 'git log 失败'
printf '完成：%s/llvm；完整日志：%s/llvm_optimize_fetch.log\n' "$TARGET" "$HOME"
EOF
```

此代码块与本机实际运行的 `E/intranet-fetch.sh` 完全相同，脚本 SHA256：`94aa3a3fa69d4ac31a38a6a8d7569f896c4c802b2a0830b7b5b90ca623ea2ea1`。外层及内层 Bash 语法检查 PASS；完整实跑证据见 §5。

## 3. 冻结身份与资产清单

| 项目 | 值 |
| --- | --- |
| LLVM HEAD | `6e9d4f2bc77e20ba96d586680bb4f4c25eace7d2` |
| tree | `80a6fd231c4564a3b762f4ec288cf2c41f9d2e20` |
| parent | `67619ec8bbbac7238a6cfc33a481ccfbcd12206f` |
| 检出分支 | 本地 `llvm_optimize` |
| local upstream / merge-base HEAD upstream | 均为 `ca7933e47d3a3451d81e72ac174dcb5aa28b59d1` |
| 局部 core.abbrev | `12`，打包前与回下后均核对 |
| origin | `ssh://lhmax2025@review.tizen.org:29418/platform/upstream/llvm` |
| 浅仓库 / 工作区 | true / clean；无外部 objects/info/alternates |
| GitHub Release tag | `src-llvm-optimize-6e9d4f2` |
| Release tag 所指文档仓库提交 | `1759dd57ac57974c4786c828150f2828b3271e05`；与包内 LLVM HEAD 是两个仓库的身份 |

repack 后只打包 `llvm/.git`（80 个 tar 条目，无检出的工作区文件）；`split -b 100M -d -a 2` 中 100M = 104,857,600 字节。前四片各 100 MiB，最后一片 5,683,669 字节。

| 资产 | 字节数 | SHA256 |
| --- | ---: | --- |
| `llvm_optimize-6e9d4f2-shallow-git.tar.gz` | 425,114,069 | `cebfeb3cbda216be11f4e760336a2afc3a8d40ad26906482a849225559777f46` |
| `llvm_optimize-6e9d4f2-shallow-git.tar.gz.part00` | 104,857,600 | `d20fb365842f98b1903fc78b83d331fce9ee9e38839bedfdba14ba1a7dbae81a` |
| `llvm_optimize-6e9d4f2-shallow-git.tar.gz.part01` | 104,857,600 | `c67917d83047e87c38ea41b0ab4ccf4866fa729f27086492e8b4e6906f6a8e10` |
| `llvm_optimize-6e9d4f2-shallow-git.tar.gz.part02` | 104,857,600 | `6ec8e1ff0b02e32bef49932d8cc58feef74ade94e7524db0374053b7c0047ab5` |
| `llvm_optimize-6e9d4f2-shallow-git.tar.gz.part03` | 104,857,600 | `eca80fc527cce125437c114d011884d8c10d99600400bc10a9ae112527b39b3a` |
| `llvm_optimize-6e9d4f2-shallow-git.tar.gz.part04` | 5,683,669 | `46ba3f46de4d7a364ef43a9542d66290bc1353cb20b4c2f166daf59bbc1c3939` |

Release 同时提供 [SHA256SUMS](https://github.com/lhmax2010/llvm-optimize/releases/download/src-llvm-optimize-6e9d4f2/SHA256SUMS) 与 [manifest.json](https://github.com/lhmax2010/llvm-optimize/releases/download/src-llvm-optimize-6e9d4f2/manifest.json)。整包与各片都已上传，服务器端资产大小/SHA256核对通过。所有大文件只在 Release 与本机 temp 中，不进入 Git 分支。

## 4. 导出与打包证据

W=`/home/linhao/Toolchain/development/llvm-optimize`；E=`W/temp/llvm-optimize-intranet-20261020`；S=`E/llvm`。原 W/gbs_llvm.conf SHA 为 `28f1caf93cd39738a7da1e0da8d5f945f7372963bb9823a507f9157294272169`，用户原有修改保留。

第 2 步实际命令（与上轮只差新的输出目录）：

```bash
TMPDIR="$E/tmp" gbs \
  -c /home/linhao/Toolchain/development/llvm-optimize/gbs_llvm.conf export \
  --spec llvm.spec \
  --commit 6e9d4f2bc77e20ba96d586680bb4f4c25eace7d2 \
  --outdir-directly --outdir "$E/export-abbrev12" "$S"
```

GBS exit 0；完整日志没有 native 回退。参考为 `E/reference-export.json` 及 `W/temp/hybrid-sandbox-20261019/patch-export`；逐字节比较之外，还逐项重算 SHA。回下仓库再导出结果列在同一表中：

| 文件 | 字节数 | 参考、第 2 步与第 6 步共同 SHA256 | 第 2 步 / 第 6 步 |
| --- | ---: | --- | --- |
| `llvm.spec` | 23,428 | `1da77fe8dfe45134bf7ae558ef366da2cfda6eccd917740449b85557b00e7f07` | PASS / PASS |
| `0001-Add-support-for-Tizen-toolchain-vendor.patch` | 5,537 | `a71a7503e851f4ebe1c192326d832c28f79a81ff1c9db43696d0487c118d587c` | PASS / PASS |
| `0002-Link-libclang_rt.asan.so-against-libatomic-when-nece.patch` | 1,122 | `cefb73ec25a64f8c70cc0e585dfc688a23eb44b740093755ffaf8ee86f7e716e` | PASS / PASS |
| `0003-Fix-armv7l-build-when-compiler-is-clang.patch` | 1,408 | `9ce436eb2f73e01b112cfeb10d6108e33c719b1db54a8fc404abdc10c367102b` | PASS / PASS |
| `0004-clang-add-support-for-LLVM-gold-plugin-in-case-of-ac.patch` | 2,175 | `45d68e84754f93ebe10ba80725e6cbb28826890e344f0ae910e061690105e944` | PASS / PASS |
| `0005-Merge-MLGO-AOT-compilation-support-and-optimization-.patch` | 5,546 | `da2cacae22ef8ececf808596b14ff53b6741db23e3f34d7fc5e07a75fa3543c2` | PASS / PASS |
| `0006-libcxxabi-declare-__gnu_unwind_frame-in-cxa_personal.patch` | 1,426 | `f52129a2f008603a3cf74fc1bf448d984b0f1827a48a9597f346223d87b98062` | PASS / PASS |
| `0007-libcxx-backport-EH-ABI-forced-unwind-handling.patch` | 28,278 | `b2d657339c18c5c1416bc9b3890afd39394b9ce46af061c1db809315ad4746d3` | PASS / PASS |
| `0008-cmake-use-hybrid-LLVM-linkage-on-x86_64.patch` | 7,392 | `5bce5e43b16cf6fc8494ae4db489adf77e19489af8375144c524a8d70732c67e` | PASS / PASS |

打包命令：

```bash
git -C "$S" -c pack.threads=1 -c pack.windowMemory=256m \
  -c pack.deltaCacheSize=128m repack -a -d
tar -C "$E" -czf "$E/assets/llvm_optimize-6e9d4f2-shallow-git.tar.gz" llvm/.git
split -b 100M -d -a 2 \
  "$E/assets/llvm_optimize-6e9d4f2-shallow-git.tar.gz" \
  "$E/assets/llvm_optimize-6e9d4f2-shallow-git.tar.gz.part"
```

pack 的三个 `-c` 仅限制本次 repack 的并发和内存，不写入配置。打包前确认 core.abbrev=12、upstream/merge-base、干净状态；从 tar 中读取 `.git/config` 与原件比对相同。`E/tar-members.txt` 保存完整 tar 清单。

使用 `gh release create` 发布具名整包、5 片、SHA256SUMS 与 manifest.json，明确 `--target 1759dd57… --latest=false`；没有创建或更新 Gerrit 分支。GitHub 已登录 lhmax2010，无需浏览器登录，凭据不进入资产或报告。Release 元数据见 `E/abbrev-published-release.json`，CLI 原文见 `E/abbrev-release.log`。

## 5. GitHub 实际回下与再导出

测试前固定目标不存在。本机从 GitHub Release 的公开资产 URL 下载全部 5 片，没有以本地资产代替网络下载；按 §2 完整脚本拼接、检出，返回 0。成功输出原文：

```text
PART_OK llvm_optimize-6e9d4f2-shallow-git.tar.gz.part00 104857600 bytes d20fb365842f98b1903fc78b83d331fce9ee9e38839bedfdba14ba1a7dbae81a
PART_OK llvm_optimize-6e9d4f2-shallow-git.tar.gz.part01 104857600 bytes c67917d83047e87c38ea41b0ab4ccf4866fa729f27086492e8b4e6906f6a8e10
PART_OK llvm_optimize-6e9d4f2-shallow-git.tar.gz.part02 104857600 bytes 6ec8e1ff0b02e32bef49932d8cc58feef74ade94e7524db0374053b7c0047ab5
PART_OK llvm_optimize-6e9d4f2-shallow-git.tar.gz.part03 104857600 bytes eca80fc527cce125437c114d011884d8c10d99600400bc10a9ae112527b39b3a
PART_OK llvm_optimize-6e9d4f2-shallow-git.tar.gz.part04 5683669 bytes 46ba3f46de4d7a364ef43a9542d66290bc1353cb20b4c2f166daf59bbc1c3939
ARCHIVE_OK cebfeb3cbda216be11f4e760336a2afc3a8d40ad26906482a849225559777f46
HEAD OK 6e9d4f2bc77e20ba96d586680bb4f4c25eace7d2
TREE OK 80a6fd231c4564a3b762f4ec288cf2c41f9d2e20
UPSTREAM OK ca7933e47d3a3451d81e72ac174dcb5aa28b59d1
ABBREV OK 12
```

origin URL、parent、工作区干净、本地 upstream、merge-base 和局部 core.abbrev 再次独立核对。恢复路径就是 `/home/linhao/toolchain/development/llvm_optimize/llvm`，未覆盖原开发工作区（注意两路径大小写和 `-` / `_` 不同）。

第 6 步再导出实际命令，配置、spec、commit、outdir-directly 与第 2 步相同，只替换输入仓库和新输出目录：

```bash
TMPDIR="$E/tmp" gbs \
  -c /home/linhao/Toolchain/development/llvm-optimize/gbs_llvm.conf export \
  --spec llvm.spec \
  --commit 6e9d4f2bc77e20ba96d586680bb4f4c25eace7d2 \
  --outdir-directly --outdir "$E/export-roundtrip-abbrev12" \
  /home/linhao/toolchain/development/llvm_optimize/llvm
```

再次 export exit 0，无 native；spec + 8 patch 与参考及第 2 步逐字节一致。证据：`E/abbrev-download.log`、`~/llvm_optimize_fetch.log`、`E/abbrev-roundtrip-verification.json`、`E/abbrev-roundtrip-export.log`、`E/abbrev-roundtrip-export-comparison.json`。没有执行构建。

## 6. 资源、边界与收尾

本轮 Git/export/打包/传输为轻任务，沿用 6 GiB 准入、18 GiB cap、MemorySwapMax=0、nice19/ionice3；每 2 秒检查宿主可用 2 GiB 与目标文件系统可用 30 GiB 底线。全部写入 /home；不进入 BOLT 资产或已交接的 x86 构建树，没有触发资源保护。

| 阶段 | 开始时间（UTC+08） | 外层 wall（秒） | exit |
| --- | --- | ---: | ---: |
| abbrev-export | 2026-10-20T21:08:16.589041+08:00 | 70.028 | 0 |
| abbrev-repack | 2026-10-20T21:09:45.654245+08:00 | 30.008 | 0 |
| abbrev-package | 2026-10-20T21:10:42.930594+08:00 | 16.004 | 0 |
| abbrev-release | 2026-10-20T21:11:59.286370+08:00 | 104.027 | 0 |
| abbrev-download | 2026-10-20T21:16:05.898602+08:00 | 98.022 | 0 |
| abbrev-roundtrip-export | 2026-10-20T21:18:08.380380+08:00 | 64.015 | 0 |

191 个采样点，最低宿主 MemAvailable **6856261632 B**，最低 /home 可用 **230656983040 B**。这是资源保护记录，不作性能结论。scope/采样器已回收，项目锁释放，无本任务残留进程或挂载；见 `E/abbrev-resource-summary.json`、`abbrev-final-audit.json`、`abbrev-lock-released.json`。

源码/spec/候选补丁、W/gbs_llvm.conf 和全局 Git 配置未改；唯一仓库配置变更是用户授权的局部 core.abbrev=12。两个历史停止报告和原证据保留。GitHub main 仅提交本页与 STATUS，署名 Hao Lin，不改全局身份；Release/tag 与文档更新均属本次授权，不推 Gerrit。
