%global __os_install_post %{nil}
%define debug_package %{nil}

Name:       dotnet-build-tools
Summary:    Tools for building C# API projects
Version:    10.0.402
Release:    1
Group:      Development/Libraries
License:    MIT and Apache-2.0
URL:        https://www.tizen.org
Source0:    %{name}-%{version}.tar.gz
Source1:    macros.dotnet-build-tools
Source21:   dotnet-sdk-%{version}-linux-x64.tar.gz
Source22:   deps.tar.gz
Source23:   crossgen2-mic.tar.gz

AutoReqProv: no

BuildRequires: patchelf
#BuildRequires: crossgen2-mic

Requires: mscorlib
Requires: corefx-managed
Requires: csapi-tizenfx-full
Requires: corefx-managed-ref
Requires: libicu
Requires: openssl3
Requires: make
Recommends: dotnet-launcher-gbs-support

%description
Provides dotnet-sdk for GBS environment

%define TOOLS_PATH /usr/share/dotnet-build-tools
%define SDK_PATH %{TOOLS_PATH}/sdk

%prep
%setup -q

mkdir -p dotnet/deps
mkdir -p dotnet/crossgen2/ref
tar xvfz %{SOURCE21} -C dotnet
tar xvfz %{SOURCE22} -C dotnet/deps
tar xvfz %{SOURCE23} -C dotnet/crossgen2
#cp -rf /opt/usr/dotnet/mic/* dotnet/crossgen2

%build
# Prepare dotnet-sdk
%ifnarch x86_64
# Every dynamically linked executable the SDK runs itself must use the bundled loader and
# libraries: the dotnet muxer, and since .NET 9 also the compilers (Roslyn/bincore/csc, vbc,
# VBCSCompiler), MSBuild and createdump, which ship as native apphosts instead of being
# started through `dotnet <tool>.dll`. An unpatched apphost fails inside a non-x86_64 build
# root with "No such file or directory" because /lib64/ld-linux-x86-64.so.2 does not exist.
# The apphost templates (AppHostTemplate/apphost, packs/**/apphost, singlefilehost) are
# copied into applications that are built, so they keep the system interpreter.
for file in $( find ./dotnet -type f ! -name "*.so" ! -name "*.so.*" ! -name "*.dll" ! -name "apphost" ! -name "singlefilehost" ! -name "*.dbg" -size +8k )
do
    patchelf --print-interpreter ${file} >/dev/null 2>&1 || continue
    chmod 0755 ${file}
    patchelf --set-interpreter %{SDK_PATH}/deps/ld-linux-x86-64.so.2 ${file}
    patchelf --set-rpath %{SDK_PATH}/deps/ ${file}
done
for file in $( find ./dotnet -type f \( -name "*.so" -or -name "*.so.*" \) -not -name "*.dbg" -not -name "ld-*.so*" )
do
    chmod 0755 ${file}
    patchelf --set-rpath %{SDK_PATH}/deps/ ${file}
done

# Prepare crossgen2
tar xvfz dotnet/crossgen2/crossgen2.tar.gz -C dotnet/crossgen2
chmod 0755 ./dotnet/crossgen2/* -R
patchelf --set-interpreter %{SDK_PATH}/crossgen2/ld-linux-x86-64.so.2 ./dotnet/crossgen2/crossgen2
patchelf --set-rpath %{SDK_PATH}/crossgen2/ ./dotnet/crossgen2/crossgen2
for file in $( find ./dotnet/crossgen2 -type f \( -name "*.so" -or -name "*.so.*" \) -not -name "*.dbg" -not -name "ld-*.so*" )
do
    patchelf --set-rpath %{SDK_PATH}/crossgen2/ ${file}
done

cd dotnet/crossgen2
tar -zcvf crossgen2.tar.gz crossgen2
rm crossgen2
cd -
%endif

# Normalize CRLF -> LF for all shell scripts (defensive against Windows checkouts)
sed -i 's/\r$//' tools/*.sh build/*.sh 2>/dev/null || true

# overrides
cp -f overrides/Microsoft.Build.Tasks.Core.dll dotnet/sdk/*/Microsoft.Build.Tasks.Core.dll

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{SDK_PATH}

# RPM Macros
install -D -p -m 0644 %{S:1} %{buildroot}%{_sysconfdir}/rpm/macros.dotnet-build-tools

# .NETCore SDK
cp -fr ./dotnet/* %{buildroot}%{SDK_PATH}

# .NETCore Additional Packs
cp -fr ./packs/* %{buildroot}%{SDK_PATH}/packs

# Tizen Workload
cp -rf ./sdk-manifests %{buildroot}%{SDK_PATH}
cp -rf ./template-packs %{buildroot}%{SDK_PATH}
cp -rf ./metadata %{buildroot}%{SDK_PATH}

# BuildTools
cp -fr ./tools/* %{buildroot}%{TOOLS_PATH}
ln -s %{TOOLS_PATH}/dotnet-build.sh %{buildroot}%{_bindir}/dotnet-build
ln -s %{TOOLS_PATH}/dotnet-wrapper.sh %{buildroot}%{_bindir}/dotnet
ln -s %{TOOLS_PATH}/dotnet-validate-struct.sh %{buildroot}%{_bindir}/dotnet-validate-struct
ln -s %{SDK_PATH}/crossgen2/crossgen2 %{buildroot}%{_bindir}/crossgen2

# Tizen.Pre.Compiled.BuildTasks
install -p -m 644 ./targets/Tizen.Pre.Compiled.targets %{buildroot}%{SDK_PATH}/sdk/*/Current/Microsoft.Common.targets/ImportAfter
install -p -m 644 ./targets/Tizen.Pre.Compiled.Reference.targets %{buildroot}%{SDK_PATH}/sdk/*/Current/Microsoft.Common.targets/ImportAfter

%files
%config(noreplace) %{_sysconfdir}/rpm/macros.dotnet-build-tools
%{_bindir}/*
%{TOOLS_PATH}/*

%post
dotnet --version
dotnet workload list

cd %{SDK_PATH}/crossgen2
tar -zxvf crossgen2.tar.gz
rm -f crossgen2.tar.gz
cd -
