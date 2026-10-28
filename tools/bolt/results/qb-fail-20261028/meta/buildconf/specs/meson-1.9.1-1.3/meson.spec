%define _name   mesonbuild
Name:           meson
VCS:            platform/upstream/meson#3450073f64fd8528133d8cbb5d81fccdfe596511
Version:        1.9.1
Release:        1.3
Summary:        Python-based build system
License:        Apache-2.0
Group:          Development/Tools/Building
Url:            http://mesonbuild.com/
Source:         https://github.com/%{_name}/meson/releases/download/%{version}/meson-%{version}.tar.gz
SOURCE1001:     meson.manifest
SOURCE1002:     macros.meson
SOURCE1003:     meson-1.9.1-py3-none-any.whl

BuildRequires:  python3 >= 3.4
BuildRequires:  python3-setuptools

BuildRequires:  python3-build
BuildRequires:  python3-wheel
BuildRequires:  python3-pip
BuildRequires:  ninja 

Requires:       ninja
Requires:       python3-xml
Requires:       python3-setuptools

BuildArch:      noarch

Provides:       meson-gui = %{version}
Obsoletes:      meson-gui < %{version}

%description
Meson is a build system designed to optimise programmer productivity.
It aims to do this by providing support for software development
tools and practices, such as unit tests, coverage reports, Valgrind,
CCache and the like. Supported languages include C, C++, Fortran,
Java, Rust. Build definitions are written in a non-turing complete
Domain Specific Language.

%package vim
%{!?vim_data_dir:%global vim_data_dir %{_datadir}/vim}
Summary:        Vim support for meson.build files
Group:          Productivity/Text/Editors
Requires:       vim
Supplements:    packageand(vim:%{name})
BuildArch:      noarch

%description vim
Meson is a build system designed to optimise programmer productivity.
It aims to do this by providing support for software development
tools and practices, such as unit tests, coverage reports, Valgrind,
CCache and the like. Supported languages include C, C++, Fortran,
Java, Rust. Build definitions are written in a non-turing complete
Domain Specific Language.

This package provides support for meson.build files in Vim.

%prep
%setup -q -n meson-%{version}
cp %{SOURCE1001} .
cp -f %{SOURCE1002} ./data

%build

%install
%{_bindir}/python3 -m pip install --root %{buildroot} %{SOURCE1003}

install -Dpm 0644 data/macros.meson \
  %{buildroot}%{_rpmconfigdir}/macros.d/macros.meson

mkdir -p %{buildroot}%{vim_data_dir}/site/ftdetect
install -Dpm 0644 data/syntax-highlighting/vim/ftdetect/meson.vim \
  -t %{buildroot}%{vim_data_dir}/site/ftdetect

mkdir -p %{buildroot}%{vim_data_dir}/site/indent
install -Dpm 0644 data/syntax-highlighting/vim/indent/meson.vim \
  -t %{buildroot}%{vim_data_dir}/site/indent

mkdir -p %{buildroot}%{vim_data_dir}/site/syntax
install -Dpm 0644 data/syntax-highlighting/vim/syntax/meson.vim \
  -t %{buildroot}%{vim_data_dir}/site/syntax

%remove_docs

%files
%manifest %{name}.manifest
%license COPYING
%{_bindir}/meson
%{python3_sitelib}/%{_name}/
%{python3_sitelib}/meson-*
%{_rpmconfigdir}/macros.d/macros.meson
%{_datadir}/polkit-1/actions/com.mesonbuild.install.policy

%files vim
%manifest %{name}.manifest
%dir %{vim_data_dir}
%dir %{vim_data_dir}/site
%dir %{vim_data_dir}/site/ftdetect
%dir %{vim_data_dir}/site/indent
%dir %{vim_data_dir}/site/syntax
%{vim_data_dir}/site/ftdetect/meson.vim
%{vim_data_dir}/site/indent/meson.vim
%{vim_data_dir}/site/syntax/meson.vim

%changelog
