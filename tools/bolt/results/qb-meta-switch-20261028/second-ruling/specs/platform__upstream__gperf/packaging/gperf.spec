Name:           gperf
Version:        3.0.4
Release:        1
License:        GPL-2.0+
Summary:        A perfect hash function generator
Url:            http://www.gnu.org/software/gperf/
Group:          Development/Tools
Source0:        ftp://ftp.gnu.org/pub/gnu/%{name}/%{name}-%{version}.tar.gz
Source1001: 	gperf.manifest
BuildRequires:  gcc-c++

%description
GNU gperf is a perfect hash function generator. For a given list of strings, it
produces a hash function and hash table, in form of C or C++ code, for looking
up a value depending on the input string. The hash function is perfect, which
means that the hash table has no collisions, and the hash table lookup needs
a single string comparison only.

%prep
%setup -q
cp %{SOURCE1001} .


%build

%configure --disable-static
make %{?_smp_mflags}

%install
%make_install

rm -f %{buildroot}%{_datadir}/doc/gperf.html






%files
%manifest %{name}.manifest
%license COPYING
%defattr(-,root,root,-)
%doc NEWS README doc/gperf.html
%doc %{_mandir}/man1/gperf.1*
%doc %{_infodir}/gperf.info*
%{_bindir}/%{name}


