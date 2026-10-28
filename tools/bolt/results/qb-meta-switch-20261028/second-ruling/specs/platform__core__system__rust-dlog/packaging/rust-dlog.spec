%define _rpm_strip_option --keep-section=.rustc

%global rustc_edition 2021

Name:       rust-dlog
Summary:    rust-dlog
Version:    0.1
Release:    1
Group:      System/Management
License:    MIT
Source0:    %{name}-%{version}.tar.gz
Source1:    %{name}.manifest
BuildRequires: rust
BuildRequires: rust-libc
BuildRequires: rust-log
BuildRequires: libdlog-devel

%description
dlog rust bindings

%package -n rust-libdlog
Summary:    Logging service dlog API
%description -n rust-libdlog

%package -n rust-libdlogutil
Summary:    Logging service dlog API
%description -n rust-libdlogutil

%package    tests
Summary:    Rust-dlog tests
Requires: rust-devel
%description tests

%package    doc
Summary:    Rust-dlog documentation
%description doc

%prep
%setup -q
cp %{SOURCE1} .

%build
build_library () {
	%{rustc_std_build} \
		--crate-type=dylib \
		-Clink-arg="-Wl,-ldlog,-ldlogutil,-ldlog_redirect_stdout" \
		$@
	clippy-driver \
		-C prefer-dynamic \
		--extern std=${__rust_std} \
		-L%{_rust_libdir} \
		-L%{_rust_dylibdir} \
		--crate-type=dylib \
		--out-dir=/tmp \
		-Dclippy::undocumented_unsafe_blocks \
		$@
	rustdoc \
		-C prefer-dynamic \
		--extern std=${__rust_std} \
		-L%{_rust_libdir} \
		-L%{_rust_dylibdir} \
		--crate-type=dylib \
		-o rustdoc_output \
		$@
}

build_library \
	--crate-name=dlog_sys \
	--edition=%{rustc_edition} \
	--cfg='feature="std"' \
	./dlog-sys/src/lib.rs

build_library \
	--crate-name=dlog \
	--edition=%{rustc_edition} \
	--cfg='feature="std"' \
	%rust_dylib_extern log \
	--extern dlog_sys=libdlog_sys.so \
	./dlog/src/lib.rs

build_library \
	--crate-name=dlogutil_sys \
	--edition=%{rustc_edition} \
	--cfg='feature="std"' \
	%rust_dylib_extern libc \
	--extern dlog_sys=libdlog_sys.so \
	./dlogutil-sys/src/lib.rs

build_library \
	--crate-name=dlogutil \
	--edition=%{rustc_edition} \
	--cfg='feature="std"' \
	-L. \
	%rust_dylib_extern libc \
	--extern dlog_sys=libdlog_sys.so \
	--extern dlog=libdlog.so \
	--extern dlogutil_sys=libdlogutil_sys.so \
	./dlogutil/src/lib.rs

build_library \
	--crate-name=dlog_redirect_stdout_sys \
	--edition=%{rustc_edition} \
	--cfg='feature="std"' \
	./dlog-redirect-stdout-sys/src/lib.rs

build_library \
	--crate-name=dlog_redirect_stdout \
	--edition=%{rustc_edition} \
	--cfg='feature="std"' \
	-L. \
	--extern dlog=libdlog.so \
	--extern dlog_redirect_stdout_sys=libdlog_redirect_stdout_sys.so \
	./dlog-redirect-stdout/src/lib.rs

TESTFLAGS="--edition=%{rustc_edition} \
	--cfg feature=\"std\" \
	-L. \
	%rust_dylib_extern libc \
	%rust_dylib_extern log \
	--extern dlog=libdlog.so \
	--extern dlogutil=libdlogutil.so \
	--extern dlog_redirect_stdout=libdlog_redirect_stdout.so \
	-Clink-arg=%{_libdir}/libdlog.so \
	-Clink-arg=%{_libdir}/libdlogutil.so \
	-Clink-arg=%{_libdir}/libdlog_redirect_stdout.so \
	"

build_test () {
	%{rustc_std_build} \
		--crate-type=bin \
		$TESTFLAGS \
		$@
	clippy-driver \
		-C prefer-dynamic \
		--extern std=${__rust_std} \
		-L%{_rust_libdir} \
		-L%{_rust_dylibdir} \
		--crate-type=bin \
		--out-dir=/tmp \
		-Dclippy::undocumented_unsafe_blocks \
		$TESTFLAGS \
		$@
}

%{rustc_std_build} --crate-type=bin \
	--crate-name=dlogsend_rust \
	$TESTFLAGS \
	./tests/src/dlogsend.rs

build_test \
	--crate-name=test_dlog_print \
	./tests/src/test_dlog_print.rs

build_test \
	--crate-name=test_dlog_critical_print \
	./tests/src/test_dlog_critical_print.rs

build_test \
	--crate-name=test_dlog_custom_tag \
	./tests/src/test_dlog_custom_tag.rs

build_test \
	--crate-name=test_dlog_redirect \
	./tests/src/test_dlog_redirect.rs

%install
mkdir -p %{buildroot}%{_bindir}

install -d -m 0755 %{buildroot}%{_rust_dylibdir}
install -m 0644 libdlog_sys.so %{buildroot}%{_rust_dylibdir}/libdlog_sys.so
install -m 0644 libdlog.so %{buildroot}%{_rust_dylibdir}/libdlog.so
install -m 0644 libdlogutil_sys.so %{buildroot}%{_rust_dylibdir}/libdlogutil_sys.so
install -m 0644 libdlogutil.so %{buildroot}%{_rust_dylibdir}/libdlogutil.so
install -m 0644 libdlog_redirect_stdout_sys.so %{buildroot}%{_rust_dylibdir}/libdlog_redirect_stdout_sys.so
install -m 0644 libdlog_redirect_stdout.so %{buildroot}%{_rust_dylibdir}/libdlog_redirect_stdout.so
install -m 0755 dlogsend_rust %{buildroot}%{_bindir}/dlogsend_rust

for file in test_*; do
	install -m 0755 "$file" %{buildroot}%{_bindir}/"$file"
done

mkdir -p %{buildroot}/usr/share/doc/rust-dlog
cp -r rustdoc_output/* %{buildroot}/usr/share/doc/rust-dlog

%files
%manifest %{name}.manifest

%files -n rust-libdlog
%manifest %{name}.manifest
%{_rust_dylibdir}/libdlog_sys.so
%{_rust_dylibdir}/libdlog.so
%{_rust_dylibdir}/libdlog_redirect_stdout_sys.so
%{_rust_dylibdir}/libdlog_redirect_stdout.so

%files -n rust-libdlogutil
%manifest %{name}.manifest
%{_rust_dylibdir}/libdlogutil_sys.so
%{_rust_dylibdir}/libdlogutil.so

%files tests
%manifest %{name}.manifest
%attr(750,log,log) %{_bindir}/dlogsend_rust
%attr(750,log,log) %{_bindir}/test_*

%post tests
echo "This package contains binaries: dlogsend_rust, which should be treated as an example,"
echo "and integration tests that are run in dlog_test with other dlog tests."

%files doc
%manifest %{name}.manifest
/usr/share/doc/rust-dlog
