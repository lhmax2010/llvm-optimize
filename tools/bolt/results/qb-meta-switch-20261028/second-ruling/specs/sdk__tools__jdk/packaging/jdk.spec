Name: jdk
Summary: Oracle JDK for Tizen Application Build
Version: 1.8.0.281
Release: 1
Group: Development/Tools
License: Oracle Technology Network License
Source0: %{name}-%{version}.tar.gz
AutoReqProv: no
BuildRequires: elfutils
BuildRequires: patchelf

%description
%{summary}

%prep
%setup -q

%build
%ifarch %{arm} aarch64 riscv64
LD_INTERPRETER=$(patchelf --print-interpreter /emul/usr/bin/gcc)
LD_RPATH="$(patchelf --print-rpath /emul/usr/bin/gcc):/usr/jdk-%{version}/lib/amd64/jli"
patchelf --set-rpath ${LD_RPATH} ./jdk-%{version}/bin/java
patchelf --set-interpreter ${LD_INTERPRETER} ./jdk-%{version}/bin/java
patchelf --set-rpath ${LD_RPATH} ./jdk-%{version}/bin/javac
patchelf --set-interpreter ${LD_INTERPRETER} ./jdk-%{version}/bin/javac
patchelf --set-rpath ${LD_RPATH} ./jdk-%{version}/bin/javah
patchelf --set-interpreter ${LD_INTERPRETER} ./jdk-%{version}/bin/javah
patchelf --set-rpath ${LD_RPATH} ./jdk-%{version}/bin/jar
patchelf --set-interpreter ${LD_INTERPRETER} ./jdk-%{version}/bin/jar
patchelf --set-rpath ${LD_RPATH} ./jdk-%{version}/jre/lib/amd64/server/libjvm.so
%endif

%ifarch x86_64
LD_INTERPRETER=$(patchelf --print-interpreter /usr/bin/gcc)
LD_RPATH="$(patchelf --print-rpath /usr/bin/gcc):/usr/jdk-%{version}/lib/amd64/jli"
patchelf --set-rpath ${LD_RPATH} ./jdk-%{version}/bin/java
patchelf --set-interpreter ${LD_INTERPRETER} ./jdk-%{version}/bin/java
patchelf --set-rpath ${LD_RPATH} ./jdk-%{version}/bin/javac
patchelf --set-interpreter ${LD_INTERPRETER} ./jdk-%{version}/bin/javac
patchelf --set-rpath ${LD_RPATH} ./jdk-%{version}/bin/javah
patchelf --set-interpreter ${LD_INTERPRETER} ./jdk-%{version}/bin/javah
patchelf --set-rpath ${LD_RPATH} ./jdk-%{version}/bin/jar
patchelf --set-interpreter ${LD_INTERPRETER} ./jdk-%{version}/bin/jar
patchelf --set-rpath ${LD_RPATH} ./jdk-%{version}/jre/lib/amd64/server/libjvm.so
%endif


%install
install -d %{buildroot}/%{_bindir}
/bin/cp -rvf jdk-%{version} %{buildroot}/usr/
/bin/ln -sf /usr/jdk-%{version}/bin/java %{buildroot}/%{_bindir}

%clean
rm -rf %{buildroot}

%files
%attr(755,root,root)
/usr/jdk-%{version}
%{_bindir}/java
