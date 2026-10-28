Name:           nasm
Version:        2.11.05
Release:        0
License:        BSD-2-Clause
Summary:        Netwide Assembler (An x86 Assembler)
Url:            http://nasm.sourceforge.net/
#X-Vc-Url:      git://repo.or.cz/nasm.git
Group:          Development/Languages
Source:         %{name}-%{version}.tar.xz
Source1001:     nasm.manifest
Source1002:     nasm.changes
BuildRequires:  asciidoc
BuildRequires:  docbook
BuildRequires:  makeinfo
BuildRequires:  xmlto

%description
NASM is a prototype general-purpose x86 assembler. It can currently
output several binary formats, including ELF, a.out, Win32, and OS/2.

Read the licence agreement in /usr/share/doc/packages/nasm/Licence.

%prep
%setup -q
cp %{SOURCE1001} .

%package doc
License:        LGPL-2.1+
Summary:        Documentation for Nasm
Group:          Development/Languages

%description doc
This package contains the documentation for Nasm.

%build
touch -r ./ver.c ./ver.c.stamp
TS=$(LC_ALL=C date -u -r %{_sourcedir}/%{name}.changes '+%%b %%e %%Y')
sed -i "s/__DATE__/\"$TS\"/g" ver.c
touch -r ./ver.c.stamp ./ver.c
%autogen
%reconfigure
%__make all

%__make -C doc html info nasmdoc.ps nasmdoc.txt

%install
install -d -m 755 %{buildroot}/usr/bin
install -d -m 755 %{buildroot}/%{_mandir}/man1
install -d -m 755 %{buildroot}/%{_docdir}/nasm
install -d -m 755 %{buildroot}/%{_docdir}/nasm/rdoff
install -d -m 755 %{buildroot}/%{_docdir}/nasm/html
install -d -m 755 %{buildroot}/%{_infodir}
make INSTALLROOT=%{buildroot} install
make INSTALLROOT=%{buildroot} rdf_install
install -m 644 AUTHORS CHANGES ChangeLog LICENSE TODO README doc/*.txt \
	%{buildroot}/%{_docdir}/nasm
install -m 644 rdoff/README rdoff/doc/* \
	%{buildroot}/%{_docdir}/nasm/rdoff
install -m 644 doc/html/* %{buildroot}%{_docdir}/nasm/html
install -m 644 ndisasm.1 nasm.1 rdoff/*.1 %{buildroot}%{_mandir}/man1
install -m 644 doc/info/* %{buildroot}%{_infodir}

%files
%manifest %{name}.manifest
%defattr(-,root,root)
%license LICENSE
/usr/bin/*
%doc %{_mandir}/man1/*.1.gz

%files doc
%manifest %{name}.manifest
%defattr(-,root,root)
%doc %{_docdir}/nasm
%doc %{_infodir}/nasm*

