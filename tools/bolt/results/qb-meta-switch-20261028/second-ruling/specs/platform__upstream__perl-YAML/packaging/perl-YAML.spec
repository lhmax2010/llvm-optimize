Name:           perl-YAML
Version:        1.31
Release:        0
License:        GPL-1.0+ or Artistic-1.0
Summary:        YAML Ain't Markup Language (tm)
Group:          Development/Libraries/Perl
Url:            http://search.cpan.org/dist/YAML/
%define cpan_name YAML
Source:         %{cpan_name}-%{version}.tar.gz
Source1001: 	perl-YAML.manifest

BuildRequires:  perl
BuildRequires:  perl-macros


%description
The YAML.pm module implements a YAML Loader and Dumper based on the YAML
1.0 specification. the http://www.yaml.org/spec/ manpage

YAML is a generic data serialization language that is optimized for human
readability. It can be used to express the data structures of most modern
programming languages. (Including Perl!!!)

For information on the YAML syntax, please refer to the YAML specification.

%prep
%setup -q -n %{cpan_name}-%{version}
cp %{SOURCE1001} .

%build
perl -I. Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
%perl_make_install
%perl_process_packlist
%remove_docs
%perl_gen_filelist

%files -f %{name}.files
%manifest %{name}.manifest
%license LICENSE
