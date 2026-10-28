Name:           perl-HTML-Parser
VCS:            platform/upstream/perl-HTML-Parser#5428707eb5dc1afad83feea13fb26bb03fe78269
Version:        3.83
Release:        1.1
License:        GPL-1.0 or Artistic-1.0
Summary:        Perl module for parsing HTML
Url:            http://search.cpan.org/dist/HTML-Parser/
Group:          Development/Libraries
Source0:        HTML-Parser-%{version}.tar.gz
Source1001: 	perl-HTML-Parser.manifest

BuildRequires:  perl(HTML::Tagset) >= 3.03
Requires:       perl(HTML::Tagset) >= 3.03

%description
The HTML-Parser module for perl to parse and extract information from
HTML documents, including the HTML::Entities, HTML::HeadParser,
HTML::LinkExtor, HTML::PullParser, and HTML::TokeParser modules.

%prep
%setup -q -n HTML-Parser-%{version}
cp %{SOURCE1001} .

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
%perl_make_install
%perl_process_packlist
%remove_docs
%perl_gen_filelist

%files -f %{name}.files
%manifest %{name}.manifest
%license README
