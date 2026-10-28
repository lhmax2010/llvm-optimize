Name:           perl-XML-Simple
Version:        2.25
Release:        0
License:        GPL-1.0 or Artistic-1.0
Summary:        Easy API to read/write XML (Perl module)
Group:          Development/Libraries/Perl
Url:            http://cpan.org/modules/by-module/XML/
Source:         XML-Simple-%{version}.tar.gz
Source1001: 	perl-XML-Simple.manifest

BuildRequires:  perl-XML-Parser
BuildRequires:  perl-macros

Requires:       perl-XML-Parser

%description
XML::Simple - Easy API to read/write XML (esp config files)

%prep
%setup -q -n XML-Simple-%{version}
cp %{SOURCE1001} .

%build
perl Makefile.PL
%{__make}

%check
%{__make} test

%install
%perl_make_install
%perl_process_packlist
%remove_docs
%perl_gen_filelist

%files -f %{name}.files
%manifest %{name}.manifest
%license LICENSE
