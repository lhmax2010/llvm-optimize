Name:           xmlcharent
VCS:            platform/upstream/xmlcharent#3125da531ccc32065306af38066589e628bf85a0
Version:        0.3
Release:        405.1
License:        BSD-3-Clause
Summary:        XML Character Entities
Url:            http://www.oasis-open.org/committees/docbook/xmlcharent/
Group:          Productivity/Publishing/XML
Source0:        http://www.oasis-open.org/committees/docbook/%{name}/%{version}/%{name}-%{version}.tar.bz2
Source1:        catalog.xml
Source2:        CATALOG.xmlcharent
Source1001: 	xmlcharent.manifest
BuildRequires:  sgml-skel
BuildRequires:  unzip
%define regcat /usr/bin/sgml-register-catalog
Requires(pre):  %{regcat}
Requires(pre):  /usr/bin/edit-xml-catalog
Requires(pre):  /usr/bin/xmlcatalog
Requires(pre):  gawk
Requires(pre):  grep
Requires(pre):  sed
Requires:       libxml2
Requires:       sgml-skel
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch

%description
XML encodings for the 19 standard character entity sets defined in
non-normative Annex D of [ISO 8879:1986].

%define INSTALL install -m755 -s
%define INSTALL_DIR install -d -m755
%define INSTALL_DATA install -m644
%define INSTALL_SCRIPT install -m755 -o root -g root
%define sgml_dir %{_datadir}/sgml
%define sgml_var_dir /var/lib/sgml
%define sgml_mod_dir %{sgml_dir}/xmlcharent
%define xml_dir %{_datadir}/xml
%define xml_mod_dir %{xml_dir}/entities/%{name}/%{version}
%define sgml_config_dir /var/lib/sgml
%define sgml_sysconf_dir %{_sysconfdir}/sgml
%define xml_config_dir /var/lib/xml
%define xml_sysconf_dir %{_sysconfdir}/xml

%prep
%setup -q
cp %{SOURCE1001} .
sed 's|@VERSION@|%{version}|
s|@DIR@|%{xml_mod_dir}|' %{SOURCE1} >catalog.xml
sed 's|@VERSION@|%{version}|
s|@DIR@|%{xml_mod_dir}|' %{SOURCE2} >CATALOG.%{name}
#%setup -q -n %{name}

%build
# # lynx -width=300 -dump  entities-2002-03-19.html \
# #   | grep '\(Public\|System\) identifier' \
# #   | awk -F 'entifier: ' '
# # / System i/ {printf "\"%s\"\n", gensub(/.*\//,"%{sgml_dir_iso}/", g, $2)}
# # / Public i/ {printf "PUBLIC \"-//%s\" ", $2}' > CATALOG.xmlcharent
# {
#   for f in iso-*.ent; do
#     {
#       grep ' *ISO 8879:1986' $f | sed 's:^ \+::' \
#         | awk '{printf "PUBLIC \"-//%s\"", $0}';
#       echo " \"%{sgml_dir_iso}/$f\"";
#     }
#   done
# } > CATALOG.xmlcharent
# sed 's:%{xml_mod_dir}/::' CATALOG.xmlcharent > sgml.catalog
# Prep XML catalog fragment
%define FOR_ROOT_CAT for-catalog-%{name}-%{version}.xml
xmlcatbin=/usr/bin/xmlcatalog
# build root catalog fragment
rm -f %{FOR_ROOT_CAT}.tmp
$xmlcatbin --noout --create %{FOR_ROOT_CAT}.tmp
CATALOG=%{xml_mod_dir}/catalog.xml
$xmlcatbin --noout --add "delegatePublic" "ISO 8879:1986//ENTITIES" \
    "file://$CATALOG" %{FOR_ROOT_CAT}.tmp
# Create tag
sed '/<catalog/a\
  <group id="%{name}-%{version}">
/<\/catalog/i\
  </group>' \
  %{FOR_ROOT_CAT}.tmp > %{FOR_ROOT_CAT}

%install
%{INSTALL_DIR} %{buildroot}%{xml_mod_dir}
%{INSTALL_DIR} %{buildroot}%{sgml_dir}
%{INSTALL_DIR} %{buildroot}%{sgml_var_dir}
%{INSTALL_DATA} catalog.xml *.ent %{buildroot}%{xml_mod_dir}
%{INSTALL_DATA} CATALOG.xmlcharent %{buildroot}%{sgml_var_dir}
(cd %{buildroot}%{sgml_dir} &&
ln -sf ../../../var/lib/sgml/CATALOG.* .
 )
(cd %{buildroot}%{xml_mod_dir} &&
for f in *.ent; do
  ln -sf "$f" "$(echo "$f" | sed 's/-//')"
done
 )
# parse-sgml-catalog.sh CATALOG.xmlcharent > CATALOG.norm
# sgml2xmlcat.sh -i CATALOG.norm \
#   -l -s '%{buildroot}/usr/share/sgml' -p xmlcharent
#
mkdir -p %{buildroot}%{_sysconfdir}/xml
install -m644 %{FOR_ROOT_CAT} %{buildroot}%{_sysconfdir}/xml
#
%define all_cat xmlcharent

%post
if [ -x %{regcat} ]; then
  for c in  %{all_cat}; do
    grep -q -e "%{sgml_dir}/CATALOG.$c\\>" /etc/sgml/catalog \
      || %{regcat} -a %{sgml_dir}/CATALOG.$c >/dev/null 2>&1 || :
  done
fi
xmlcatbin=usr/bin/xmlcatalog
if [ -x /usr/bin/edit-xml-catalog ]; then
/usr/bin/edit-xml-catalog --group --catalog /etc/xml/suse-catalog.xml \
  --add /etc/xml/%{FOR_ROOT_CAT}
fi

%postun
if [  "$1" = "0" -a -x %{regcat} ]; then
  for c in  %{all_cat}; do
    %{regcat} -r %{sgml_dir}/CATALOG.$c >/dev/null 2>&1 || :
  done
fi
xmlcatbin=/usr/bin/xmlcatalog
# remove entries only on removal of file
if [ ! -f %{xml_sysconf_dir}/%{FOR_ROOT_CAT} -a -x /usr/bin/edit-xml-catalog ] ; then
  /usr/bin/edit-xml-catalog --group --catalog /etc/xml/suse-catalog.xml \
    --del %{name}-%{version}
fi

%files
%manifest %{name}.manifest
%defattr(-, root, root)
# %doc entities-*.html
%{xml_mod_dir}
%config %{_sysconfdir}/xml/%{FOR_ROOT_CAT}
%config %{sgml_var_dir}/CATALOG.*
# %{sgml_dir}/ISO*
%{sgml_dir}/CATALOG.*
%dir %{xml_dir}/entities
%dir %{xml_dir}/entities/xmlcharent

%changelog
* Fri Dec  7 2012 Anas Nashif <anas.nashif@intel.com> upstream/0.3@c7efd4b
- fixed %%setup
- Imported Upstream version 0.3
