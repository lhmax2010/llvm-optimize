Name:           perl-Params-ValidationCompiler
Version:        0.31
Release:        1
License:        Artistic-2.0
Summary:        Build an optimized subroutine parameter validator once, use it forever
Url:            https://metacpan.org/pod/Params::ValidationCompiler
Group:          Development/Libraries
Source0:        %{name}-%{version}.tar.gz
Source1001: 	perl-Params-ValidationCompiler.manifest
BuildRequires:  perl
BuildRequires:  perl(MIME::Base64)

%description
This module creates a customized, highly efficient 
parameter checking subroutine. It can handle named 
or positional parameters, and can return the 
parameters as key/value pairs or a list of values.

In addition to type checks, it also supports 
parameter defaults, optional parameters, and 
extra "slurpy" parameters.

%prep
%setup -q -n %{name}-%{version}
cp %{SOURCE1001} .

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
%perl_make_install
%perl_process_packlist
%perl_gen_filelist

%files -f %{name}.files
%license LICENSE
