Name:           python3-Cheetah
Version:        3.4.0.post5
Release:        0
Url:            http://www.cheetahtemplate.org/
Summary:        Cheetah is a template engine and code generation tool
License:        MIT
Group:          Development/Languages/Python3
Source:         Cheetah-%{version}.tar.gz
Source1001: 	python3-Cheetah.manifest
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  fdupes
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
Provides:       python3-cheetah = %{version}
Obsoletes:      python3-cheetah < %{version}

%description
Cheetah is an open source template engine and code generation tool.

It can be used standalone or combined with other tools and frameworks. Web
development is its principle use, but Cheetah is very flexible and is also being
used to generate C++ game code, Java, sql, form emails and even Python3 code.

%prep
%setup -q -n Cheetah-%{version}
cp %{SOURCE1001} .

%build
CFLAGS="%{optflags}" %{_bindir}/python3 setup.py build

%install
%{_bindir}/python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
%fdupes %{buildroot}

%files
%manifest %{name}.manifest
%license LICENSE
%{_bindir}/cheetah*
%{python3_sitearch}/*

%changelog
