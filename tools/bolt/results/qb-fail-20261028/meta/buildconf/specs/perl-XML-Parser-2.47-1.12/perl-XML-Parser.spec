Name:           perl-XML-Parser
VCS:            platform/upstream/perl-XML-Parser#cf0d34f2b88782c41f6a4066fba9d9f6a92db246
Summary:        A perl module for parsing XML documents
Version:        2.47
Release:        1.12
License:        GPL-1.0+ or Artistic-1.0
Group:          Development/Libraries/Perl
Url:            http://www.cpan.org/modules/by-module/XML/
%define cpan_name XML-Parser
Source:         %{cpan_name}-%{version}.tar.gz
Source1001: 	perl-XML-Parser.manifest
Source1002: 	LICENSE

BuildRequires:  perl
BuildRequires:  libexpat-devel

%description
This module provides ways to parse XML documents. It is built on top of
 XML::Parser::Expat, which is a lower level interface to James Clark's expat
 library. Each call to one of the parsing methods creates a new instance of
 XML::Parser::Expat which is then used to parse the document. Expat options may
 be provided when the XML::Parser object is created. These options are then
 passed on to the Expat object on each parse call. They can also be given as
 extra arguments to the parse methods, in which case they override options
 given at XML::Parser creation time.

The behavior of the parser is controlled either by "Style" and/or "Handlers"
 options, or by "setHandlers" method. These all provide mechanisms for
 XML::Parser to set the handlers needed by XML::Parser::Expat. If neither
 Style nor Handlers are specified, then parsing just checks the document
 for being well-formed.

When underlying handlers get called, they receive as their first parameter
 the Expat object, not the Parser object.

You will find examples in
/usr/share/doc/packages/perl-XML-Parser/samples.  For documentation
read the XML::Parser and XML::Parser::Expat man pages.


%prep
%setup -n XML-Parser-%{version} -q
cp %{SOURCE1001} .
cp %{SOURCE1002} .

%build
CFLAGS="$RPM_OPT_FLAGS" perl Makefile.PL
%{__make}

%check
# %{__make} test

%install
%perl_make_install
%perl_process_packlist
%perl_gen_filelist

%files -f %{name}.files
%manifest %{name}.manifest
%license LICENSE
