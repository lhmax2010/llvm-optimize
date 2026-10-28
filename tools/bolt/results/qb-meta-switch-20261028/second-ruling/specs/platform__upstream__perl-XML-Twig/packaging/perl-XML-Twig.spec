Name:           perl-XML-Twig
Version:        3.52
Release:        1
License:        GPL-1.0+ or Artistic-1.0
Summary:        Tree interface to XML documents
Group:          Development/Libraries/Perl
Url:            http://search.cpan.org/dist/XML::Twig
# http://search.cpan.org/CPAN/authors/id/M/MI/MIROD/XML-Twig-%{version}.tar.gz
Source:         XML-Twig-%{version}.tar.gz
Source1001: 	perl-XML-Twig.manifest

BuildRequires:  perl-XML-Parser
BuildRequires:  perl-macros

Requires:       perl-XML-Parser

%description
XML::Twig is (yet another!) XML transformation module.

Its strong points: can be used to process huge documents while still
being in tree mode; not bound by DOM or SAX, so it is very perlish and
offers a very comprehensive set of methods; simple to use; DWIMs as
much as possible

What it doesn't offer: full SAX support (it can export SAX, but only
reads XML), full XPath support (unless you use XML::Twig::XPath), nor
DOM support.

Other drawbacks: it is a big module, and with over 500 methods
available it can be a bit overwhelming. A good starting point is the
tutorial at http://xmltwig.com/xmltwig/tutorial/index.html. In fact the
whole XML::Twig page at http://xmltwig.com/xmltwig/ has plenty of
information to get you started with XML::Twig

%prep
%setup -q -n XML-Twig-%{version}
cp %{SOURCE1001} .

%build
perl Makefile.PL
make

# %check
# make test

%install
%perl_make_install
%perl_process_packlist
%remove_docs
%perl_gen_filelist

%files -f %{name}.files
%manifest %{name}.manifest
