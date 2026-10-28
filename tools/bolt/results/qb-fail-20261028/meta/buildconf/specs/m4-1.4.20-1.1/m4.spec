Name:           m4
VCS:            platform/upstream/m4#8b8ae1241fc09cb34a7361c77f98a1ca5f1418e9
Version:        1.4.20
Release:        1.1
License:        GPL-3.0-or-later
Summary:        GNU m4 macro processor
URL:            http://www.gnu.org/software/m4/
Source0:        %{name}-%{version}.tar.bz2
Source1001:     %{name}.manifest

%description
GNU m4 is an implementation of the traditional Unix macro processor.

%prep
%setup -q
cp %{SOURCE1001} .

%build
export CFLAGS="$CFLAGS -fPIC "
export CXXFLAGS="$CXXFLAGS -fPIC "
export LDFLAGS="$LDFLAGS -pie "

%configure \
    --without-included-regex \
    gl_cv_func_isnanl_works=yes \
    gl_cv_func_printf_directive_n=yes \
    ac_cv_sys_stack_overflow_works=yes \
    ac_cv_sys_xsi_stack_overflow_heuristic=yes

make %{?_smp_mflags}

%check
make %{?_smp_mflags} check || true

%install
%make_install

%remove_docs

%files
%manifest %{name}.manifest
%license COPYING
%{_bindir}/m4
%{_datadir}/locale/*

