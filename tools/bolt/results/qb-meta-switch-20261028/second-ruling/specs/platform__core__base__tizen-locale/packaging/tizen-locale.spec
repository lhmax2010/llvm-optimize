Name:   tizen-locale	
Summary: carring locale information for tizen platform
Version:0.1
Release: 2
License: GPL-2.0+ and LGPL-2.1+
Group: 	System/Libraries

Source: %{name}-%{version}.tar.gz
Source10: generate-supported.mk
Source11: tizen-build-locale-archive
Source12: tzdata-update

BuildRequires: tzdata >= 2003a
Requires: toybox
Requires: coreutils
Requires: tzdata
Requires: glibc-locale

%description
carring locale information for tizen platform

%prep
%setup -q 

%build
%{?asan:%gcc_unforce_options}
sed -ie "s#__DATADIR__#%{_datadir}#" $RPM_SOURCE_DIR/tizen-build-locale-archive
sed -ie "s#__PREFIX__#%{_prefix}#" $RPM_SOURCE_DIR/tizen-build-locale-archive
sed -ie "s#__SBINDIR__#%{_sbindir}#" $RPM_SOURCE_DIR/tizen-build-locale-archive
sed -ie "s#__DATADIR__#%{_datadir}#" $RPM_SOURCE_DIR/tzdata-update


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT

mkdir -p %{buildroot}%{_sbindir}

install -m 0700 $RPM_SOURCE_DIR/tizen-build-locale-archive %{buildroot}%{_sbindir}
install -m 0700 $RPM_SOURCE_DIR/tzdata-update %{buildroot}%{_sbindir}

mkdir -p %{buildroot}%{_prefix}/lib/locale


CHARSET=UTF-8
LOCALE_DIR=%{buildroot}%{_prefix}/lib/locale
mkdir -p $LOCALE_DIR

%if "%{?tizen_profile_name}" == "tv"
REGEX="(af_ZA|am_ET|ar_AE|as_IN|az_AZ|bg_BG|bh_IN|bn_BD|bn_IN|bs_BA|ca_ES|ckb_IQ|ckb_IR|cs_CZ|da_DK|de_DE|el_GR|en_AU|en_GB|en_PH|en_US|es_ES|es_MX|et_EE|eu_ES|fa_IR|fi_FI|fr_CA|fr_FR|fil_PH|ga_IE|gl_ES|gu_IN|ha_NG|he_IL|hi_IN|hr_HR|hu_HU|hy_AM|id_ID|ig_NG|is_IS|it_IT|ja_JP|ka_GE|kk_KZ|km_KH|kn_IN|ko_KR|kok_IN|ks_IN|ks_IN@devanagari|ku_TR|lt_LT|lv_LV|mai_IN|mi_NZ|mk_MK|ml_IN|mn_MN|mni_IN|mr_IN|ms_MY|my_MM|nb_NO|ne_NP|nl_NL|nn_NO|or_IN|pa_IN|pa_PK|pl_PL|pt_BR|pt_PT|ro_RO|ru_RU|sa_IN|sat_IN|sd_IN|sd_IN@devanagari|sk_SK|sl_SI|sq_AL|sr_ME|sr_RS|sr_RS@latin|sv_SE|sw_KE|ta_IN|te_IN|th_TH|tl_PH|tr_TR|tu_IN|uk_UA|ur_PK|uz_UZ|uz_UZ@cyrillic|vi_VN|xh_ZA|yo_NG|zh_CN|zh_HK|zh_SG|zh_TW|zu_ZA)"
%else
REGEX="(bhb_IN|tcy_IN|aa_DJ|aa_ER|aa_ET|af_ZA|am_ET|an_ES|ar_AE|ar_BH|ar_DZ|ar_EG|ar_IN|ar_IQ|ar_JO|ar_KW|ar_LB|ar_LY|ar_MA|ar_OM|ar_QA|ar_SA|ar_SD|ar_SY|ar_TN|ar_YE|as_IN|ast_ES|az_AZ|be_BY|ber_DZ|ber_MA|bg_BG|bn_BD|bn_IN|bo_CN|bo_IN|br_FR|bs_BA|byn_ER|ca_AD|ca_ES|ca_FR|ca_IT|crh_UA|csb_PL|cs_CZ|cv_RU|cy_GB|da_DK|de_AT|de_BE|de_CH|de_DE|de_LU|dv_MV|dz_BT|el_CY|el_GR|en_AG|en_AU|en_BW|en_CA|en_DK|en_GB|en_HK|en_IE|en_IN|en_NG|en_NZ|en_PH|en_SG|en_US|en_ZA|en_ZW|es_AR|es_BO|es_CL|es_CO|es_CR|es_DO|es_EC|es_ES|es_GT|es_HN|es_MX|es_NI|es_PA|es_PE|es_PR|es_PY|es_SV|es_US|es_UY|es_VE|et_EE|eu_ES|fa_IR|fi_FI|fil_PH|fo_FO|fr_BE|fr_CA|fr_CH|fr_FR|fr_LU|fur_IT|fy_DE|fy_NL|ga_IE|gd_GB|gez_ER|gez_ET|gl_ES|gu_IN|gv_GB|ha_NG|he_IL|hi_IN|hne_IN|hr_HR|hsb_DE|ht_HT|hu_HU|hy_AM|i18n|id_ID|ig_NG|ik_CA|is_IS|it_CH|it_IT|iu_CA|iw_IL|ja_JP|ka_GE|kk_KZ|kl_GL|km_KH|kn_IN|kok_IN|ko_KR|ks_IN|ku_TR|kw_GB|ky_KG|lg_UG|li_BE|li_NL|lo_LA|lt_LT|lv_LV|mai_IN|mg_MG|mi_NZ|mk_MK|ml_IN|mn_MN|mr_IN|ms_MY|mt_MT|my_MM|nb_NO|nds_DE|nds_NL|ne_NP|nl_AW|nl_BE|nl_NL|nn_NO|nr_ZA|nso_ZA|oc_FR|om_ET|om_KE|or_IN|pa_IN|pap_AN|pa_PK|pl_PL|POSIX|ps_AF|pt_BR|pt_PT|ro_RO|ru_RU|ru_UA|rw_RW|sa_IN|sc_IT|sd_IN|se_NO|shs_CA|sid_ET|si_LK|sk_SK|sl_SI|so_DJ|so_ET|so_KE|so_SO|sq_AL|sq_MK|sr_ME|sr_RS|ss_ZA|st_ZA|sv_FI|sv_SE|ta_IN|te_IN|tg_TJ|th_TH|ti_ER|ti_ET|tig_ER|tk_TM|tl_PH|tn_ZA|tr_CY|tr_TR|ts_ZA|tt_RU|tu_IN|ug_CN|uk_UA|ur_IN|ur_PK|uz_UZ|ve_ZA|vi_VN|wa_BE|wal_ET|wo_SN|xh_ZA|yi_US|yo_NG|zh_CN|zh_HK|zh_SG|zh_TW|zu_ZA|raj_IN|ce_RU|raj_IN|ce_RU|ckb_IQ|ckb_IR)"
%endif


REGEX=`echo $REGEX | sed "s#\<en\>#en_GB#" | sed "s#\<[a-z]\+\>#&_.*#g"`

pids=
count=1
for LOCALE in `grep -E "^\<$REGEX\>.*/$CHARSET" localedata/SUPPORTED | cut -d '/' -f 1`
do
	I18NPATH=localedata GCONV_PATH=iconvdata localedef --quiet -c -f $CHARSET -i ${LOCALE%%.*} $LOCALE_DIR/$LOCALE &
	pids="$pids $!"
	count=`expr $count + 1`
	if [ $count = 5 ]; then
		for pid in $pids; do
			wait $pid
		done
		pids=
		count=1
	fi
done

if [ ! -z "$pids" ]; then
	for pid in $pids; do
		wait $pid
	done
fi

mkdir -p %{buildroot}%{_datadir}/i18n/
make -f %{SOURCE10} IN=localedata/SUPPORTED OUT=%{buildroot}%{_datadir}/i18n/SUPPORTED

%post -p %{_sbindir}/tizen-build-locale-archive

%triggerin -- tzdata
%{_sbindir}/tzdata-update

%postun

%posttrans
find %{_prefix}/lib/locale/ -name "*_*" -not -name "en_US.utf8" -not -name "en_US.UTF-8" -delete
find %{_prefix}/lib/locale/ -name "C.UTF-8" -delete
find %{_datadir}/locale/ -not -path "*/en_GB/*" -name "libc.mo" -delete

%clean
rm -rf "$RPM_BUILD_ROOT"

%files
%defattr(-,root,root)
%license COPYING COPYING.LIB
%exclude %{_prefix}/lib/locale/en_US.utf8
%exclude %{_prefix}/lib/locale/en_US.UTF-8
%{_prefix}/lib/locale/*
%attr(0644,root,root) %config %{_datadir}/i18n/SUPPORTED
%{_sbindir}/tizen-build-locale-archive
%{_sbindir}/tzdata-update
%manifest tizen-locale.manifest
