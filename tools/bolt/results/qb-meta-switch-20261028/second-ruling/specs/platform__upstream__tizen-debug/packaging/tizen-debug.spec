#%define debug_package %{nil}
#%define __strip /bin/true
%if 0%{?asan}
%define _build_id_links none
%endif

Name:		tizen-debug
Summary:	libc debug information with .debug_frame section only and ld debug information
Version:	2.40
Release:	1
License:	LGPL-2.1+ and LGPL-2.1+-with-GCC-exception and GPL-2.0+
Group:		Development/Libraries
Source0:	%{name}-%{version}.tar.gz

BuildRequires:	glibc-debuginfo
BuildRequires:	binutils
BuildRequires:	elfutils >= 0.165

%{lua: rpm.define("debugpath " .. rpm.expand("%{__debuginfo_path}"):gsub("%^", ""))}

%description
The package contains the libc.so debug library with .debug_frame section only
which can be helpful during signal frame backtrace.
Also, the ld.so debug information is included for the debugging convenience.

%prep
%setup -q

%install
LD_SO=$(basename $(readlink -f `readelf --program-headers /usr/bin/cp | sed -ne '/program interpreter/s|.*: \(.*\)\]|\1|p'`))
LIBC_SO=libc.so.6

mkdir -p %{buildroot}/%{debugpath}/%{_lib}
eu-elfcompress %{debugpath}/%{_lib}/${LIBC_SO}.debug -o %{buildroot}%{debugpath}/%{_lib}/${LIBC_SO}.debug
eu-elfcompress %{debugpath}/%{_lib}/${LD_SO}.debug   -o %{buildroot}%{debugpath}/%{_lib}/${LD_SO}.debug

chmod 444 %{buildroot}%{debugpath}/%{_lib}/*.so.*.debug
%if 0%{?asan} != 1
for file in %{buildroot}%{debugpath}/%{_lib}/${LD_SO}.debug %{buildroot}%{debugpath}/%{_lib}/${LIBC_SO}.debug; do
	BuildID=$(readelf -n $file | grep 'Build ID' | awk '{print $3}')
	Dir=$(echo $BuildID | cut -b-2)
	File=$(echo $BuildID | cut -b3-)
	mkdir -p %{buildroot}%{debugpath}/.build-id/$Dir
	cp -d %{debugpath}/.build-id/$Dir/$File.debug  %{buildroot}%{debugpath}/.build-id/$Dir
done
%else
mv %{buildroot}/%{debugpath}/%{_lib} %{buildroot}/%{debugpath}/%{_lib}.tizen-debug
%endif

%files
%defattr(-,root,root)
%license COPYING COPYING.LIB
%if 0%{?asan} != 1
%{debugpath}/%{_lib}/*.so.*.debug
%{debugpath}/.build-id/*
%else
%{debugpath}/%{_lib}.tizen-debug/*.so.*.debug
%endif
%manifest %{name}.manifest
