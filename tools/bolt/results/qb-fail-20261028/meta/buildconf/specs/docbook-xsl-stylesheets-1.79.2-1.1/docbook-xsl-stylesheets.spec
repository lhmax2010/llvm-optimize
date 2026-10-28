%define regcat /usr/bin/sgml-register-catalog

Name:           docbook-xsl-stylesheets
VCS:            platform/upstream/docbook-xsl-stylesheets#b39544e3bc20f18d386dd483d53a4027e234e561
Version:        1.79.2
Release:        1.1
License:        MIT
Summary:        XSL Stylesheets for DocBook 4
Url:            http://sourceforge.net/projects/docbook/
Group:          Base/Utilities
Source0:        http://switch.dl.sourceforge.net/sourceforge/docbook/docbook-xsl-%{version}.tar.bz2
Source1001:     docbook-xsl-stylesheets.manifest
BuildRequires:  fdupes
BuildRequires:  sgml-skel
BuildRequires:  unzip
Requires(pre):  %{regcat}
Requires(pre):  /usr/bin/xmlcatalog
Requires(pre):  sgml-skel
Requires:       docbook_4
Requires:       xmlcharent
BuildArch:      noarch

%description
These are the XSL stylesheets for DocBook XML and "Simplified" DocBook
DTDs. Use these stylesheets for documents based on DocBook 4 and
earlier; they are not aware of the namespace feature.

The stylesheets transform DocBook documents into HTML, XHTML, Manpages,
XSL-FO (for PDF), and a few other formats.

XSL is a standard W3C stylesheet language for both print and online
rendering. For more information about XSL, see the XSL page at the W3C:
http://www.w3.org/Style/XSL/

%define INSTALL install -m755 -s
%define INSTALL_DIR install -d -m755
%define INSTALL_DATA install -m644
%define INSTALL_SCRIPT install -m755
%define sgml_dir %{_datadir}/sgml
%define sgml_var_dir /var/lib/sgml
%define sgml_mod_dir %{sgml_dir}/docbook
%define sgml_mod_dtd_dir %{sgml_mod_dir}/dtd
%define sgml_mod_custom_dir %{sgml_mod_dir}/custom
%define sgml_mod_style_dir %{sgml_mod_dir}/stylesheet
%define xml_dir %{_datadir}/xml
%define xml_mod_dir %{xml_dir}/docbook
%define xml_mod_dtd_dir %{xml_mod_dir}/dtd
%define xml_mod_custom_dir %{xml_mod_dir}/custom
%define xml_mod_style_dir %{xml_mod_dir}/stylesheet
%define xml_mod_style_prod_dir %{xml_mod_style_dir}/nwalsh
%define sgml_config_dir /var/lib/sgml
%define sgml_sysconf_dir %{_sysconfdir}/sgml
%define xml_config_dir /var/lib/xml
%define xml_sysconf_dir %{_sysconfdir}/xml

%prep
%setup -q -n docbook-xsl-%{version}
cp %{SOURCE1001} .

# mv epub/bin/dbtoepub epub/bin/dbtoepub.tmp
sed -i 's=@@EPUBDIR@@=%{xml_mod_style_prod_dir}/current//epub/bin='  epub/bin/dbtoepub

# We don't need these scripts:
rm -rf install.sh tools/bin/docbook-xsl-update

find -type f -print0 | xargs -0 chmod -x
chmod -R a+rX,g-w,o-w .
find images -type f \( -name "*.svg" -o -name "*.png" -o -name "*.gif" -o -name "*.tif" \) -exec chmod -x {} + 2>/dev/null || true
find images/callouts -type f \( -name "*.svg" -o -name "*.png" -o -name "*.gif" \) -exec chmod -x {} + 2>/dev/null || true
[ -f extensions/docbook.py ] && chmod -x extensions/docbook.py
# Start cleanup (to avoid warnings for rpmlint
[ -f ./extensions/saxon65/dist/saxon65.jar ] && rm -rf ./extensions/saxon65/dist/saxon65.jar
[ -f ./extensions/xalan27/dist/xalan27.jar ] && rm -rf ./extensions/xalan27/dist/xalan27.jar
find . -name '.gitignore' | xargs rm -fr
#x=$(find {lib,html,fo,lib,website,slides/fo,slides/html,roundtrip,manpages}/.[a-zA-Z0-9]* -maxdepth 1 -type f )
#if [ "$x" != '' ]; then
## rm $x;
#  for i in $x; do
#     if [ -f $i ]; then
#        rm $i
#     fi
#  done
#fi

%build
xmlcatbin=/usr/bin/xmlcatalog
CATALOG=%{name}.xml
# file:///usr/share/sgml/docbook/ = %%{sgml_mod_dir} map it to
# %%{xml_mod_style_prod_dir}/%%{version}
$xmlcatbin --noout --create $CATALOG
/usr/bin/xmlcatalog --noout --add "rewriteSystem" \
 "http://docbook.sourceforge.net/release/xsl/%{version}" \
 "file://%{xml_mod_style_prod_dir}/%{version}" $CATALOG
/usr/bin/xmlcatalog --noout --add "rewriteURI" \
 "http://docbook.sourceforge.net/release/xsl/%{version}" \
 "file://%{xml_mod_style_prod_dir}/%{version}" $CATALOG
/usr/bin/xmlcatalog --noout --add "rewriteSystem" \
 "http://docbook.sourceforge.net/release/xsl/current" \
 "file://%{xml_mod_style_prod_dir}/%{version}" $CATALOG
/usr/bin/xmlcatalog --noout --add "rewriteURI" \
 "http://docbook.sourceforge.net/release/xsl/current" \
 "file://%{xml_mod_style_prod_dir}/%{version}" $CATALOG
%define FOR_ROOT_CAT for-catalog-%{name}-%{version}.xml
CATALOG=etc/xml/$CATALOG
rm -f %{FOR_ROOT_CAT}.tmp
$xmlcatbin --noout --create %{FOR_ROOT_CAT}.tmp
$xmlcatbin --noout --add "delegateSystem" \
  "http://docbook.sourceforge.net/release/xsl/" \
  "file:///$CATALOG" %{FOR_ROOT_CAT}.tmp
# $xmlcatbin --noout --add "delegatePublic" \
#   "-//OASIS//xxx" \
#   "file:///$CATALOG" %%{FOR_ROOT_CAT}.tmp
# Create tag
sed '/<catalog/a\
  <group id="%{name}-%{version}">
/<\/catalog/i\
  </group>' \
  %{FOR_ROOT_CAT}.tmp > %{FOR_ROOT_CAT}

%install
# FIXME: Danger!?
# export NO_BRP_CHECK_BYTECODE_VERSION=true

# Install scripts
%{INSTALL_DIR} %{buildroot}%{_bindir}
%{INSTALL_SCRIPT} fo/pdf2index       %{buildroot}%{_bindir}
%{INSTALL_SCRIPT} epub/bin/dbtoepub  %{buildroot}%{_bindir}
rm fo/pdf2index

doc_dir=%{buildroot}%{_defaultdocdir}/%{name}
%{INSTALL_DIR} %{buildroot}%{xml_mod_style_prod_dir}/%{version}
cp -a [[:lower:]]* %{buildroot}%{xml_mod_style_prod_dir}/%{version}
cp -a VERSION.xsl %{buildroot}%{xml_mod_style_prod_dir}/%{version}
find %{buildroot}%{xml_mod_style_prod_dir} -type f -name '*.orig' -print0 |xargs -0 rm -f
rm -f %{buildroot}%{xml_mod_style_prod_dir}/%{version}/for-catalog*
: >%{name}_list
(
  cd %{buildroot}%{xml_mod_style_prod_dir}
# do not create the current link for snapshots
#  if ! echo %%{SOURCE0} | grep -q snapshot; then
    ln -sf %{version} current
    echo %{xml_mod_style_prod_dir}/current
#  fi
) >%{name}_list
%{INSTALL_DIR} $doc_dir
# documentation
for f in README BUGS TODO WhatsNew RELEASE-NOTES.html; do
  # On snapshots, WhatsNew is missing
  [ -f $f ] && %{INSTALL_DATA} $f $doc_dir/$f
done
# cp -p README.SuSE $doc_dir/README.SuSE
#
find %{buildroot}%{xml_mod_style_prod_dir} -name "documentation.list" -delete
{
  LANG=C \
    find %{buildroot}%{xml_mod_style_prod_dir}/%{version} \
    -type d \
    -not -path "*/%{version}/latex*" \
    | sed 's|%{buildroot}|%dir |'
  LANG=C \
    find %{buildroot}%{xml_mod_style_prod_dir}/%{version} \
    -type f \
    -not -path "*/%{version}/latex*" \
    | sed 's|%{buildroot}||'
} >> %{_builddir}/%{buildsubdir}/%{name}_list
# pushd %%{buildroot}%%{xml_mod_style_prod_dir}
#   rm -f docbook-xsl
#   ln -sf docbook-xsl-stylesheets-%%{version} docbook-xsl
#   rm -f xsl-stylesheets
#   ln -sf docbook-xsl-stylesheets-%%{version} xsl-stylesheets
#   rm -f %%{name}
#   ln -sf docbook-xsl-stylesheets-%%{version} %%{name}
# popd
cat_dir=%{buildroot}%{_sysconfdir}/xml
%{INSTALL_DIR} $cat_dir
%{INSTALL_DATA} %{FOR_ROOT_CAT} %{name}.xml $cat_dir
# cleanup
rm -f %{buildroot}%{xml_mod_style_prod_dir}/%{version}/%{name}.xml
cp $cat_dir/%{FOR_ROOT_CAT} \
  %{buildroot}%{xml_mod_style_prod_dir}/%{version}/%{name}.xml
chmod +x \
%{buildroot}%{xml_mod_style_prod_dir}/%{version}/extensions/docbook.py \
%{buildroot}%{xml_mod_style_prod_dir}/%{version}/extensions/xslt.py
# %%{buildroot}%%{xml_mod_style_prod_dir}/%%{version}/epub/bin/lib/docbook.rb
# %%{buildroot}%%{xml_mod_style_prod_dir}/%%{version}/epub/bin/spec/spec_helper.rb

%fdupes -s %{buildroot}


%post
# remove empty dir if present (from ghost)
# also remove dangling symlink
D=usr/share/sgml
rmdir $D/docbkxsl >/dev/null 2>&1 || :
test -L $D/docbkxsl -a ! -e $D/docbkxsl && rm -f $D/docbkxsl
if [ -x /usr/bin/edit-xml-catalog ]; then
  edit-xml-catalog --group --catalog /etc/xml/suse-catalog.xml \
    --add /etc/xml/%{FOR_ROOT_CAT}
fi

%postun
# remove entries only on removal of file
if [ ! -f %{xml_sysconf_dir}/%{FOR_ROOT_CAT} -a -x /usr/bin/edit-xml-catalog ] ; then
  edit-xml-catalog --group --catalog /etc/xml/suse-catalog.xml \
    --del %{name}-%{version}
fi

%files -f %{name}_list
%manifest %{name}.manifest
%license COPYING
%config %{_sysconfdir}/xml/%{name}.xml
%config %{_sysconfdir}/xml/%{FOR_ROOT_CAT}
%{_defaultdocdir}/%{name}
%dir %{xml_mod_style_dir}
%dir %{xml_mod_style_prod_dir}
%exclude %{xml_mod_style_prod_dir}/documentation.list
# it is now in the list:
# %%{xml_mod_style_prod_dir}/current
%{_bindir}/*
