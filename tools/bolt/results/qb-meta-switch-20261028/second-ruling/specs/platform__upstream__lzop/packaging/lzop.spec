Name:           lzop
Version:        1.04.01
Release:        0
License:        GPLv2+
Summary:        lzop
URL:            http://www.lzop.org
Group:          Applications/Text
Source:         %{name}-%{version}.tar.gz
Source1001: lzop.manifest 
BuildRequires:  lzo
BuildRequires:  lzo-devel


%description
lzop is a file compressor which is very similar to gzip. lzop uses
the LZO data compression library for compression services, and its
main advantages over gzip are much higher compression and
decompression speed (at the cost of some compression ratio).

lzop is copyrighted OpenSource software distributed under the terms
of the GNU General Public License (GPL).

%prep
%setup -q

%build
cp %{SOURCE1001} .
%configure --disable-nls
make PR_PROGRAM=%{_bindir}/pr

%install
%make_install
%remove_docs

%clean
rm -rf %{buildroot}


%files 
%manifest %{name}.manifest
%defattr(-,root,root,-)
%license COPYING
%{_bindir}/*
