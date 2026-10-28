Name:           rfcdiff
Version:        1.49
Release:        1
Summary:        Compare two RFCs or Internet-Drafts and produce a diff in various formats
License:        GPL-2.0-or-later
Group:          Development/Tools
URL:            https://github.com/ietf-tools/rfcdiff
Source0:        %{name}-%{version}.tar.gz
Source1:        %{name}.manifest
Source1000:     rfcdiff-dash-compat.patch
BuildArch:      noarch
Requires:       /bin/sh
Requires:       gawk
Requires:       diffutils
Requires:       coreutils

%description
rfcdiff takes two RFCs or Internet-Drafts in text form as input, and produces
output which indicates the differences found in one of various forms:
side-by-side HTML diff, paged wdiff output in a text terminal, a text file
with changebars in the left margin, or a simple unified diff output.
In all cases, internet-draft page headers and footers are stripped before
generating the diff, to produce a cleaner diff.

%prep
%setup -q -n %{name}-%{version}
%{__patch} -p1 < %{SOURCE1000}
cp %{SOURCE1} .

%install
install -D -m 0755 rfcdiff %{buildroot}%{_bindir}/rfcdiff

%files
%manifest %{name}.manifest
%license LICENSE
%{_bindir}/rfcdiff
