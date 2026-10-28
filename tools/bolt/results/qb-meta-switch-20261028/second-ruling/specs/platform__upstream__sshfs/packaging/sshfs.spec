Name:       	sshfs
Summary:   		A network filesystem client to connect to SSH servers
Version:   	 	2.10
Release:   		0
Group:     		Base/File Systems
License:		GPL-2.0
URL:			https://github.com/libfuse/sshfs
Source0:		sshfs-%{version}.tar.gz
Source1001:		sshfs.manifest

# SSHFS 3.1.0 requires fuse3(3.1), glib-2.0, and gthread-2.0.
BuildRequires:	pkgconfig(fuse)
BuildRequires:	pkgconfig(glib-2.0)

Requires:		openssh

%description
SSHFS (Secure SHell FileSystem) allows you to mount a remote filesystem
using SFTP. Now that most SSH servers support and enable this SFTP access
by default, the SSHFS is very simple to use. It means that there is nothing
to do on the server-side. Note that SSHFS requires FUSE (Filesystem in
USErspace) filesystem, that lets non-privileged users create own file systems
without editing Linux kernel code.

%prep
%setup -q
cp %{SOURCE1001} .
cp COPYING LICENSE

%build
autoreconf -fi
%{configure}
make

%install
%{make_install}
rm -rf %{buildroot}%{_mandir}

%files
%defattr(-,root,root,-)
%manifest sshfs.manifest
%license LICENSE
%{_bindir}/sshfs


%changelog
* Tue Mar 3 2020 Geunsik Lim <geunsik.lim@samsung.com>
- Updated the spec file to maintain the sshfs as a Tizen package

* Tue Jul 16 2019 Wook Song <wook16.song@samsung.com>
- Initial package to use SSHFS with the FUSE filesystem
