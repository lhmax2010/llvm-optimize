Name: bolt-validation-d
Version: 1
Release: 1
Summary: BOLT full strip with a1410e3d install and post helpers
License: Apache-2.0
Group: Development/Tools
Source0: clang-22
Source1: control
Source2: control.c
%description
Minimal local postprocessing qualification, not a full LLVM build.
%debug_package

%prep
mkdir -p %{_builddir}
cp %{SOURCE2} %{_builddir}/control.c
%build
%install
set -x
mkdir -p %{buildroot}/usr/bin
install -m 0755 /home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/bin/clang-22 %{buildroot}/usr/bin/clang-22
install -m 0755 %{SOURCE1} %{buildroot}/usr/bin/bolt-control
ln -s clang-22 %{buildroot}/usr/bin/clang
ln -s clang-22 %{buildroot}/usr/bin/clang++
ln -s clang++ %{buildroot}/usr/bin/clang++-22
python3 /home/abuild/bolt-work/bolt-v4-20261015-validation/bolt_helper.py snapshot "%{buildroot}" "/home/abuild/bolt-work/bolt-v4-20261015-validation/smoke/d/work/install-before.json" || exit 1
# Reuse the already qualified pipeline candidate; no CMake/build/rewrite in this smoke.
python3 /home/abuild/bolt-work/bolt-v4-20261015-validation/bolt_helper.py compare-root "%{buildroot}" "/home/abuild/bolt-work/bolt-v4-20261015-validation/smoke/d/work/install-before.json" "/home/abuild/bolt-work/bolt-v4-20261015-validation/smoke/d/work/install-after-pipeline.json" || exit 1
python3 /home/abuild/bolt-work/bolt-v4-20261015-validation/bolt_helper.py install "%{buildroot}" "%{SOURCE0}" "/home/abuild/bolt-work/bolt-v4-20261015-validation/smoke/d/work/install-state.json" "/home/abuild/bolt-work/bolt-v4-20261014-fallback/identity.json" || exit 1
%files
%defattr(-,root,root,-)
/usr/bin/clang-22
/usr/bin/clang
/usr/bin/clang++
/usr/bin/clang++-22
/usr/bin/bolt-control
%global __bolt_original_spec_install_post %{__spec_install_post}
%define __spec_install_post \
    %{__bolt_original_spec_install_post} \
    python3 /home/abuild/bolt-work/bolt-v4-20261015-validation/bolt_helper.py post "%{buildroot}" "/home/abuild/bolt-work/bolt-v4-20261015-validation/smoke/d/work/install-state.json" "/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/bin/clang-22" "/home/abuild/bolt-work/bolt-v4-20261015-validation/smoke/d/work/post-gate" --resource-dir "/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/lib64/clang/22" || exit 1
