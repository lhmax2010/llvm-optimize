Name:           perl-JSON-PP
Version:        4.16
Release:        1
License:        Artistic-1.0 OR GPL-1.0-or-later
Summary:        JSON::PP - JSON::XS compatible pure-Perl module.
Url:            https://metacpan.org/pod/JSON::PP
Group:          Development/Libraries
Source0:        %{name}-%{version}.tar.gz
Source1001: 	perl-JSON-PP.manifest
BuildRequires:  perl
BuildRequires:  perl(MIME::Base64)

%description
JSON::PP is a pure perl JSON decoder/encoder, and (almost) compatible 
to much faster JSON::XS written by Marc Lehmann in C. 
JSON::PP works as a fallback module when you use JSON module 
without having installed JSON::XS.

Because of this fallback feature of JSON.pm, 
JSON::PP tries not to be more JavaScript-friendly than JSON::XS 
(i.e. not to escape extra characters such as U+2028 and U+2029, etc), 
in order for you not to lose such JavaScript-friendliness silently 
when you use JSON.pm and install JSON::XS for speed or by accident. 
If you need JavaScript-friendly RFC7159-compliant pure perl module,
try JSON::Tiny, which is derived from Mojolicious web framework and
is also smaller and faster than JSON::PP.

JSON::PP has been in the Perl core since Perl 5.14, mainly 
for CPAN toolchain modules to parse META.json.

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
%license README
