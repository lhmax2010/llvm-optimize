Name:		dejagnu
VCS:   platform/upstream/dejagnu#7129ba345434e97093f391228acc759b1832c304
Summary:	Framework for testing other programs.
Version:	1.6.2
Release:	1.1
Group:		Development/Testing
License:	GNU GPL
Source0:	%{name}-%{version}.tar.gz
Source1001:	%{name}.manifest
Requires:	tcl
Requires:	expect
BuildRequires:	expect
BuildRequires:  makeinfo

%description
DejaGnu is a framework for testing other programs. Its purpose is to provide a single front end for all tests. Think of it as a custom library of Tcl procedures crafted to support writing a test harness. A test harness is the testing infrastructure that is created to support a specific program or tool. Each program can have multiple testsuites, all supported by a single test harness.

%package	devel
Summary:	Development package for dejagnu

%description	devel
Development package for dejagnu

%prep
%setup -q
cp %{SOURCE1001} .

%build
%reconfigure
%__make %{?_smp_mflags}

sed -e '26aDEJAGNULIBS="%{_datadir}/dejagnu"' -i runtest

%install
rm -rf %{buildroot}
%make_install

%remove_docs

%post
echo -e "Setting up DEJAGNULIBS\n"
echo 'export DEJAGNULIBS="%{_datadir}/dejagnu"' >> /etc/profile
echo 'export DEJAGNULIBS="%{_datadir}/dejagnu"' >> /etc/bashrc

%files
%defattr(-,root,root)
%manifest %{name}.manifest
%{_datadir}/dejagnu/*
%{_bindir}/runtest

%files devel
%defattr(-,root,root)
%manifest %{name}.manifest
%{_includedir}/dejagnu.h
