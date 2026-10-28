# "enable foo" will turn into --enable-foo or --disable-foo
# depending "with_foo" macro
%define enable() %{expand:%%{?with_%{1}:--enable-%{1}}%%{!?with_%{1}:--disable-%{1}}}
%define DOTNET_MEMORY_LIB /usr/share/dotnet.tizen/netcoreapp/libdnetmemoryenum.so

Name:           minicoredumper
Version:        2.9.11
Release:        0%{?release_flags}
# For a breakdown of the licensing, see COPYING
License:        BSD-2-Clause, MIT
Url:            https://linutronix.de/minicoredumper/
Group:          System/Monitoring
Source0:        https://linutronix.de/minicoredumper/files/minicoredumper-%{version}.tar.xz
Source1:        minicoredumper.manifest
Summary:        Generate minimal and customized core dump files on Linux
BuildRequires:  pkgconfig(json-c)

%description
minicoredumper is a program that handles the creation of core dump files on
Linux. It can produce much smaller core dump files by making use of sparse
files, compression, and allowing the user to configure what parts of the
process memory image should be dumped.

%prep
%setup -q
cp %{SOURCE1} .

%build
%autogen
%configure --with-dotnet-memory-lib=%{DOTNET_MEMORY_LIB}
make %{?_smp_mflags} CFLAGS="-fPIE" LDFLAGS="-pie -ldl"

%install
%make_install

%post
ln -sf %{_sysconfdir}/minicoredumper/generic-rel.recept.json %{_sysconfdir}/minicoredumper/generic.recept.json

%files
%license COPYING COPYING.BSD LICENSE.MIT
%manifest minicoredumper.manifest
%{_sbindir}/minicoredumper
%{_sysconfdir}/minicoredumper/generic-rel.recept.json
%{_sysconfdir}/minicoredumper/generic-dbg.recept.json
%{_sysconfdir}/minicoredumper/generic-fullcore.recept.json
%{_sysconfdir}/minicoredumper/dotnet.recept.json
%{_sysconfdir}/minicoredumper/minicoredumper.cfg.json
%dir %{_localstatedir}/crash/minicoredumper
%attr(0700,root,root) %{_localstatedir}/crash/minicoredumper

%docs_package
