# TODO:
#   - enigmail doesn't work
#   - check -alpha-gcc3, -gfx, -blockimage, -gcc-bugs patches
#   - check %files
#
# Conditional builds
%bcond_without	enigmail    # don't build enigmail - GPG/PGP support
%bcond_without	spellcheck  # build without spellcheck function
#
Summary:	Mozilla Thunderbird - email client
Summary(pl):	Mozilla Thunderbird - klient poczty
Name:		mozilla-thunderbird
Version:	1.5
Release:	0.1
License:	MPL/LGPL
Group:		Applications/Networking
Source0:	http://ftp.mozilla.org/pub/mozilla.org/thunderbird/releases/%{version}/source/thunderbird-%{version}-source.tar.bz2
# Source0-md5:	781c1cd1a01583d9b666d8c2fe4288e6
Source1:	http://www.mozilla-enigmail.org/downloads/src/enigmail-0.94.0.tar.gz
# Source1-md5:	d326c302c1d2d68217fffcaa01ca7632
Source2:	%{name}.desktop
Source3:	%{name}.sh
Patch0:		%{name}-alpha-gcc3.patch
Patch1:		%{name}-gfx.patch
Patch2:		%{name}-nss.patch
Patch3:		%{name}-lib_path.patch
Patch4:		%{name}-blockimage.patch
Patch5:		%{name}-gcc-bugs.patch
Patch6:		%{name}-nopangoxft.patch
# official patches
# certain ui operations cause prolonged hang (cpu at 100%)
Patch100:	%{name}-bug305970.patch
# Ctrl-Shift-Home + typing with mozInlineSpellChecker causes NULL nsCOMPtr assertion
Patch101:	%{name}-bug304720.patch
URL:		http://www.mozilla.org/projects/thunderbird/
BuildRequires:	automake
BuildRequires:	freetype-devel >= 1:2.1.8
BuildRequires:	gtk+2-devel >= 1:2.0.0
BuildRequires:	libIDL-devel >= 0.8.0
BuildRequires:	libjpeg-devel >= 6b
BuildRequires:	libpng-devel >= 1.2.0
BuildRequires:	libstdc++-devel
BuildRequires:	nspr-devel >= 1:4.6-0.20041030.1
BuildRequires:	nss-devel >= 3.8
BuildRequires:	pango-devel >= 1:1.1.0
BuildRequires:	sed >= 4.0
%if %{with enigmail}
BuildRequires:	/bin/ex
BuildRequires:	/bin/csh
%endif
Requires:	nspr >= 1:4.6-0.20041030.1
Requires:	nss >= 3.8
%if %{with spellcheck}
Provides:	mozilla-thunderbird-spellcheck
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_thunderbirddir		%{_libdir}/%{name}
# mozilla and thunderbird provide their own versions
%define	_noautoreqdep		libgkgfx.so libgtkembedmoz.so libgtkxtbin.so libjsj.so libmozjs.so libxpcom.so libxpcom_compat.so
%define	_noautoprovfiles	libplc4.so libplds4.so

%description
Mozilla Thunderbird is an open-source,fast and portable email client.

%description -l pl
Mozilla Thunderbird jest open sourcowym, szybkim i przeno�nym klientem
poczty.

%package dictionary-en-US
Summary:	English (US) dictionary for spellchecking
Summary(pl):	Angielski (USA) s�ownik do sprawdzania pisowni
Group:		Applications/Dictionaries
Requires:	mozilla-thunderbird-spellcheck

%description dictionary-en-US
This package contains English (US) myspell-compatible dictionary used
for spellcheck function of mozilla-thunderbird. An alternative for
this can be the OpenOffice's dictionary.

%description dictionary-en-US -l pl
Ten pakiet zawiera angielski (USA) s�ownik kompatybilny z myspellem,
u�ywany przez funkcj� sprawdzania pisowni mozilli-thunderbird.
Alternatyw� dla niego mo�e by� s�ownik OpenOffice'a.

%prep
%setup -q -n mozilla
%{?with_enigmail:tar xvfz %{SOURCE1} -C mailnews/extensions}

##%patch0 -p1
##%patch1 -p1
%patch2 -p1
%patch3 -p1
##%patch4 -p1
##%patch5 -p1
%patch6 -p1

# official patches
%patch100 -p1
%patch101 -p1

%build
export CFLAGS="%{rpmcflags} `%{_bindir}/pkg-config mozilla-nspr --cflags-only-I`"
export CXXFLAGS="%{rpmcflags} `%{_bindir}/pkg-config mozilla-nspr --cflags-only-I`"

cp -f %{_datadir}/automake/config.* build/autoconf
cp -f %{_datadir}/automake/config.* nsprpub/build/autoconf
cp -f %{_datadir}/automake/config.* directory/c-sdk/config/autoconf

cat << EOF > .mozconfig
. \$topsrcdir/mail/config/mozconfig

export BUILD_OFFICIAL=1
export MOZILLA_OFFICIAL=1
#export MOZ_THUNDERBID=1

mk_add_options BUILD_OFFICIAL=1
mk_add_options MOZILLA_OFFICIAL=1

ac_add_options --prefix=%{_prefix}
ac_add_options --exec-prefix=%{_exec_prefix}
ac_add_options --bindir=%{_bindir}
ac_add_options --sbindir=%{_sbindir}
ac_add_options --sysconfdir=%{_sysconfdir}
ac_add_options --datadir=%{_datadir}
ac_add_options --includedir=%{_includedir}
ac_add_options --libdir=%{_libdir}
ac_add_options --libexecdir=%{_libexecdir}
ac_add_options --localstatedir=%{_localstatedir}
ac_add_options --sharedstatedir=%{_sharedstatedir}
ac_add_options --mandir=%{_mandir}
ac_add_options --infodir=%{_infodir}
%if %{?debug:1}0
ac_add_options --enable-debug
ac_add_options --enable-debug-modules
%else
ac_add_options --disable-debug
ac_add_options --disable-debug-modules
%endif
%if %{with tests}
ac_add_options --enable-tests
%else
ac_add_options --disable-tests
%endif

ac_add_options --disable-ldap
ac_add_options --disable-installer
ac_add_options --disable-jsd
ac_add_options --disable-xprint
ac_add_options --enable-canvas
ac_add_options --enable-crypto
ac_add_options --enable-default-toolkit="gtk2"
ac_add_options --enable-extensions="pref,cookie,wallet%{?with_spellcheck:,spellcheck}"
ac_add_options --enable-mathml
ac_add_options --enable-optimize="%{rpmcflags}"
ac_add_options --enable-pango
ac_add_options --enable-reorder
ac_add_options --enable-strip
ac_add_options --enable-strip-libs
ac_add_options --enable-system-cairo
ac_add_options --enable-svg
ac_add_options --enable-xft
ac_add_options --enable-xinerama
ac_add_options --with-system-jpeg
ac_add_options --with-system-nspr
ac_add_options --with-system-nss
ac_add_options --with-system-png
ac_add_options --with-system-zlib
ac_add_options --with-pthreads
ac_add_options --enable-single-profile
ac_add_options --disable-profilesharing

EOF


%{__make} -f client.mk build_all \
	CC="%{__cc}" \
	CXX="%{__cxx}"

%if %{with enigmail}
   cd mailnews/extensions/enigmail
   ./makemake -r
   %{__make}
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir},%{_pixmapsdir},%{_desktopdir}}

%{__make} -C xpinstall/packager \
	MOZ_PKG_APPNAME="mozilla-thunderbird" \
	MOZILLA_BIN="\$(DIST)/bin/thunderbird-bin" \
	EXCLUDE_NSPR_LIBS=1

install %{SOURCE3} $RPM_BUILD_ROOT%{_bindir}/mozilla-thunderbird
%{__sed} -i 's@%{_prefix}/lib/@%{_libdir}/@g' $RPM_BUILD_ROOT%{_bindir}/mozilla-thunderbird

tar -xvz -C $RPM_BUILD_ROOT%{_libdir} -f dist/mozilla-thunderbird-*.tar.gz

install mail/app/default.xpm $RPM_BUILD_ROOT%{_pixmapsdir}/mozilla-thunderbird.xpm
install %{SOURCE2} $RPM_BUILD_ROOT%{_desktopdir}/mozilla-thunderbird.desktop

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mozilla-thunderbird
%dir %{_thunderbirddir}
%{_thunderbirddir}/res
%dir %{_thunderbirddir}/components
%attr(755,root,root) %{_thunderbirddir}/components/*.so
%{_thunderbirddir}/components/*.js
%{_thunderbirddir}/components/*.xpt
%if %{with spellcheck}
%dir %{_thunderbirddir}/components/myspell
%endif
%{_thunderbirddir}/defaults
%{_thunderbirddir}/greprefs
%{_thunderbirddir}/icons
#%{_thunderbirddir}/plugins
%attr(755,root,root) %{_thunderbirddir}/*.so
%attr(755,root,root) %{_thunderbirddir}/*.sh
%attr(755,root,root) %{_thunderbirddir}/*-bin
%attr(755,root,root) %{_thunderbirddir}/mozilla-xremote-client
%attr(755,root,root) %{_thunderbirddir}/reg*
%attr(755,root,root) %{_thunderbirddir}/thunderbird
%attr(755,root,root) %{_thunderbirddir}/thunderbird-config
#%attr(755,root,root) %{_thunderbirddir}/TestGtkEmbed
#%ifarch %{ix86}
#%attr(755,root,root) %{_thunderbirddir}/elf-dynstr-gc
#%endif
%{_thunderbirddir}/*.txt
%{_thunderbirddir}/x*
%dir %{_thunderbirddir}/chrome
%{_thunderbirddir}/chrome/US.jar
%{_thunderbirddir}/chrome/classic.jar
%{_thunderbirddir}/chrome/comm.jar
%{_thunderbirddir}/chrome/en-US.jar
#%{_thunderbirddir}/chrome/help.jar
%{_thunderbirddir}/chrome/icons
%{_thunderbirddir}/chrome/messenger.jar
#%{_thunderbirddir}/chrome/modern.jar
%{_thunderbirddir}/chrome/newsblog.jar
%{_thunderbirddir}/chrome/offline.jar
#%{_thunderbirddir}/chrome/pipnss.jar
%{_thunderbirddir}/chrome/pippki.jar
%{_thunderbirddir}/chrome/toolkit.jar
%{_thunderbirddir}/chrome/*.txt
#%{_thunderbirddir}/chrome/embed-sample.jar
# TODO: check if we really need these
%{_thunderbirddir}/chrome/*.manifest
%if %{with enigmail}
%{_thunderbirddir}/chrome/enigmail-en-US.jar
%{_thunderbirddir}/chrome/enigmail-skin-tbird.jar
%{_thunderbirddir}/chrome/enigmail-skin.jar
%{_thunderbirddir}/chrome/enigmail.jar
%{_thunderbirddir}/chrome/enigmime.jar
%endif
%dir %{_thunderbirddir}/init.d
%{_thunderbirddir}/init.d/README
%{_thunderbirddir}/dependentlibs.list
%{_thunderbirddir}/extensions
%{_thunderbirddir}/updater
%{_thunderbirddir}/updater.ini
%{_pixmapsdir}/*
%{_desktopdir}/*

%if %{with spellcheck}
%files dictionary-en-US
%defattr(644,root,root,755)
%{_thunderbirddir}/components/myspell/en-US.dic
%{_thunderbirddir}/components/myspell/en-US.aff
%endif
