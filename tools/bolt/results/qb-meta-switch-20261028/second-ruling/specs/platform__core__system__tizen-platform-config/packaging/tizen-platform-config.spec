%define libname libtzplatform-config
%define keepstatic 1

%if "%{tizen_profile_name}" == "tv"
%define WITH_VD 1
%else
%define WITH_VD 0
%endif

%if "%{mv_prj}" == "1"
%define WITH_VD_MV 1
%else
%define WITH_VD_MV 0
%endif

Name:           tizen-platform-config
Version:        5.0
Release:        1
Summary:        Tizen Platform Configuration
License:        MIT and LGPL-2.0+
Url:            http://www.tizen.org
Group:          System/Configuration
Source0:        %{name}-%{version}.tar.gz
Source1:        %{name}-rpmlintrc
Source1001:     %{name}.manifest
BuildRequires:  tizen-platform-config-meta
BuildRequires:  gperf
# for sha256sum
BuildRequires:  coreutils
Requires(post): smack
Requires(post): coreutils

# the main package only contains a config file but other dependent packages
# will contain binary. So, we can't build a noarch package and have to avoid
# a rpmlint warning using a filter in xxx-rpmlintrc

%description
Tizen Platform Configuration - variables definitions

%package -n %{libname}
Summary:        Tizen Platform Configuration - helper library
Group:          System/Libraries
License:        LGPL-2.0+
Requires:       %{name} = %{version}
%description -n %{libname}
Tizen Platform Configuration - helper library to lookup Tizen variables easily

%package -n %{libname}-devel
Summary:        Tizen Platform Configuration - helper libray headers, RPM macros
Group:          Development/Libraries
License:        LGPL-2.0+
Requires:       %{libname} = %{version}
%description -n %{libname}-devel
Tizen Platform Configuration - helper library headers to include in source code,
RPM macros to call in spec files

%package -n %{name}-tools
Summary:        Tizen Platform Configuration - tools
Group:          System/Utilities
License:        LGPL-2.0+
%description -n %{name}-tools
Tizen Platform Configuration - helper programs to lookup and generate Tizen variables

%prep
%setup -q
cp %{SOURCE1001} .

%build
%reconfigure --enable-static
%__make %{?_smp_mflags}

%check
%__make check

%install
%make_install
rm %{buildroot}%{_libdir}/*.a

%post
##############################################
# BEGIN - setting of predefined directories (also /etc/skel)
##############################################
saveHOME="$HOME"
HOME="/opt/etc/skel"
. "%{_sysconfdir}/tizen-platform.conf"
cat << ENDOFCAT |
MODE 755
SMACK System::Shared true
$TZ_SYS_STORAGE
$TZ_SYS_MEDIA

MODE 700
SMACK _ true
$TZ_USER_HOME

SMACK User::Home true
$TZ_USER_APPROOT
$TZ_USER_DB
$TZ_USER_PACKAGES
$TZ_USER_ICONS
$TZ_USER_APP

MODE 775
SMACK User::Home false
$TZ_SYS_DB
$TZ_SYS_RO_APP
$TZ_SYS_RO_PRODUCT_APP


MODE 775
SMACK User::Home true
$TZ_SYS_RW_ICONS
$TZ_SYS_RW_ICONS/default
$TZ_SYS_RW_ICONS/default/small
%if "%{WITH_VD}" == "1" || "%{WITH_VD_MV}" == "1"
$TZ_SYS_RW_APP
%endif

SMACK User::App::Shared true
$TZ_USER_CONTENT
$TZ_USER_CAMERA
$TZ_USER_DOCUMENTS
$TZ_USER_DOWNLOADS
$TZ_USER_GAMES
$TZ_USER_IMAGES
$TZ_USER_OTHERS
$TZ_USER_SOUNDS
$TZ_USER_MUSIC
$TZ_USER_VIDEOS
$TZ_USER_SHARE
$TZ_USER_CACHE
$TZ_USER_CONFIG
$TZ_USER_DATA
$TZ_USER_HOME/.pki/nssdb
$TZ_USER_APP/xwalk-service
$TZ_USER_MEDIA_APP

SMACK System::Shared true
$TZ_USER_DESKTOP

SMACK System::Shared false
$TZ_SYS_ETC

SMACK System true
$TZ_SYS_RO_PACKAGES
%if "%{WITH_VD}" != "1" && "%{WITH_VD_MV}" != "1"
$TZ_SYS_RO_PRODUCT_PACKAGES
%endif
$TZ_SYS_RW_PACKAGES

%if "%{WITH_VD}" == "1" || "%{WITH_VD_MV}" == "1"
MODE 2770
SMACK User::App::Shared true
$TZ_SYS_MEDIASHARED
%endif

ENDOFCAT
while read s1 s2 s3; do
  case "$s1" in
    MODE) m="$s2";;
    SMACK) c="$s2"; t="$s3";;
    "") ;;
    *) echo "$s1 ${m:-700} ${c:-_} ${t:-false}";;
  esac
done |
LANG=C sort |
while read dirname mode context transmute; do
        if [ -e "$dirname" ]; then
                chmod "$mode" "$dirname"
        else
                mkdir -p -m "$mode" "$dirname"
        fi
        if [ "$transmute" = true ]; then
                chsmack -a "$context" -t "$dirname"
        else
                chsmack -a "$context" "$dirname"
        fi >&2
done
ln -s $TZ_SYS_MEDIASHARED $TZ_USER_MEDIASHARED
HOME="$saveHOME"
##############################################
# END - setting of predefined directories (also /etc/skel)
##############################################

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%license LICENSE.MIT LICENSE.LGPL-2.0+
%config %{_sysconfdir}/tizen-platform.conf

%files -n %{libname}
%manifest %{name}.manifest
%license LICENSE.LGPL-2.0+
%{_libdir}/*.so.*

%files -n %{libname}-devel
%manifest %{name}.manifest
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*.h
%config %{_sysconfdir}/rpm/macros.tizen-platform

%files -n %{name}-tools
%manifest %{name}.manifest
%license LICENSE.LGPL-2.0+
%{_bindir}/tzplatform-get
%{_bindir}/tzplatform-tool
