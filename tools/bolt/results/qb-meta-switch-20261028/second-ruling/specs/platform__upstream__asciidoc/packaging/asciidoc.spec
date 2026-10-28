Name:           asciidoc
Summary:        Text-Based Document Generation
Version:        8.6.6
Release:        1
License:        GPL-2.0+
Group:          Development/Tools/Doc Generators
Requires:       python >= 2.3 python-xml
Requires:       docbook-xsl-stylesheets
# a2x needs /usr/bin/xsltproc
Recommends:     libxslt
Url:            http://www.methods.co.nz/asciidoc/
Source0:        %{name}-%{version}.tar.gz
Source1001: 	asciidoc.manifest
BuildArch:      noarch

%description
AsciiDoc is a text document format for writing short documents,
articles, books, and UNIX man pages. AsciiDoc files can be translated
to HTML and DocBook markups using the asciidoc command.

%package examples
Summary:        Examples and Documents for asciidoc
Group:          Development/Tools/Doc Generators
License:        GPL-2.0+

%description examples
This package contains examples and documetns of asciidoc.

%prep
%setup -q
cp %{SOURCE1001} .

%build

%install
mkdir -p $RPM_BUILD_ROOT/etc/asciidoc/filters
mkdir -p $RPM_BUILD_ROOT%{_datadir}/asciidoc
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
install -m 0644 *.conf $RPM_BUILD_ROOT/etc/asciidoc
install -m 0644 filters/*/*.conf $RPM_BUILD_ROOT/etc/asciidoc/filters/
install -m 0755 filters/*/*.py $RPM_BUILD_ROOT/etc/asciidoc/filters/
install -m 0755 -D asciidoc.py $RPM_BUILD_ROOT%{_bindir}/asciidoc
install -m 0755 -D a2x.py $RPM_BUILD_ROOT%{_bindir}/a2x
install -m 0644 doc/*.1  $RPM_BUILD_ROOT%{_mandir}/man1/
for i in images stylesheets javascripts docbook-xsl dblatex; do
  cp -av $i $RPM_BUILD_ROOT%{_datadir}/asciidoc/
  ln -s ../../%{_datadir}/asciidoc/$i $RPM_BUILD_ROOT/etc/asciidoc
done
# install vim files
mkdir -p $RPM_BUILD_ROOT%{_datadir}/vim/site/{syntax,ftdetect}
install -m 0644 vim/syntax/* $RPM_BUILD_ROOT%{_datadir}/vim/site/syntax
install -m 0644 vim/ftdetect/* $RPM_BUILD_ROOT%{_datadir}/vim/site/ftdetect

%files
%manifest %{name}.manifest
%defattr(-,root,root)
%license COPYRIGHT
%config /etc/asciidoc
%{_datadir}/asciidoc
%{_bindir}/*
%{_datadir}/vim
%doc %{_mandir}/man1/*

%changelog
