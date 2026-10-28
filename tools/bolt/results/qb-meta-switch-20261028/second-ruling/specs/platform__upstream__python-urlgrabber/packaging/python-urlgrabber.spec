Name:           python-urlgrabber
Summary:        A high-level cross-protocol url-grabber
Version:        3.9.1
Release:        0
Group:          Development/Libraries
License:        LGPL-2.1+
BuildArch:      noarch
URL:            http://urlgrabber.baseurl.org/
Source0:        urlgrabber-%{version}.tar.gz
Source1001:     python-urlgrabber.manifest
BuildRequires:  python-devel
BuildRequires:  python-pycurl
Requires:       python-pycurl
Provides:       urlgrabber = %{version}-%{release}

%description
A high-level cross-protocol url-grabber for python supporting HTTP, FTP
and file locations.  Features include keepalive, byte ranges, throttling,
authentication, proxies and more.

%prep
%setup -q -n urlgrabber-%{version}

%build
cp %{SOURCE1001} .
%{__python} setup.py build

%install
%{__python} setup.py install --root=%{buildroot} -O1 --prefix=%{_prefix}


%remove_docs

%files
%manifest %{name}.manifest
%{_bindir}/urlgrabber
%{python_sitelib}/urlgrabber*
