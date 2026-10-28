Name:           python3-libxml2
VCS:            platform/upstream/python3-libxml2#ba5558a34a8f7bcee3c8658497843b73ab48bedb
Version:        2.15.1
Release:        1.1
Summary:        python3 Bindings for libxml2
License:        MIT
Group:          Development/Python
Source:         %{name}-%{version}.tar.gz
Source1001:     %{name}.manifest

BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  libxml2-devel
BuildRequires:  doxygen

Requires:       libxml2
Obsoletes:      libxml2-python3 < %{version}
Provides:       libxml2-python3 = %{version}

%description
The libxml2-python package contains a module that permits applications
written in the Python3 programming language to use the interface
supplied by the libxml2 library to manipulate XML files.

This library allows manipulation of XML files. It includes support for
reading, modifying, and writing XML and HTML files. There is DTD
support that includes parsing and validation even with complex DTDs,
either at parse time or later once the document has been modified.

%prep
%setup -q -n %{name}-%{version}
cp %{SOURCE1001} .

%build
export CFLAGS="%{optflags} -fno-strict-aliasing"
export PYTHON=/usr/bin/python3

%autogen
%configure \
    --with-history \
    --with-sax1 \
    --with-regexps \
    --with-threads \
    --with-reader \
    --with-http \
    --with-python

# Build full project first to generate doc/html.stamp needed for Python bindings
make %{?_smp_mflags}

%install
make -C python install \
    DESTDIR=%{buildroot} \
    pythondir=%{python3_sitelib} \
    PYTHON_SITE_PACKAGES=%{python3_sitelib}

# Unwanted doc stuff
rm -fr %{buildroot}%{_datadir}/doc
rm -f %{buildroot}%{_libdir}/python%{python3_version}/site-packages/*.{la,a}

%files
%manifest %{name}.manifest
%license Copyright
%{python3_sitelib}/*
%{python3_sitearch}/*
