Name:       libev
VCS:        platform/upstream/libev#4397b3f65f4c10c2e3921681f785bd2f05d265d5
Summary:    High-performance event loop/event model with lots of features
Version:    4.33
Release:    1.1
License:    BSD-2-Clause or GPL-2.0-or-later
Group:      Development/ROS
Source0:    %{name}-%{version}.tar.gz
Source1001: %{name}.manifest

BuildRequires:  cmake

%description
Libev is modeled (very loosely) after libevent and the Event Perl
module, but is faster, scales better and is more correct, and also more
featureful. And also smaller.

%package    devel
Summary:    High-performance event loop/event model with lots of features
Requires:   %{name} = %{version}


%description devel
Libev is modeled (very loosely) after libevent and the Event Perl
module, but is faster, scales better and is more correct, and also more
featureful. And also smaller.


%prep
%setup -q
cp %{SOURCE1001} .

%build
%{configure}
%{__make} %{?_smp_mflags}

%install
%{make_install}

%{remove_docs}

%clean

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%license LICENSE
%{_libdir}/%{name}.so.*

%files devel
%manifest %{name}.manifest
%license LICENSE
%{_libdir}/%{name}.so
%{_includedir}/*.h
