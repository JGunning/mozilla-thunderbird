# TODO:
# - CHECK all features of enigmail
# - separate spec for enigmail
# - enigmail says it's not compatible with thunderbird 2.0, while home page says it is.
#
# Conditional builds
%bcond_without	enigmail    # don't build enigmail - GPG/PGP support
%bcond_without	ldap	    # disable e-mail address lookups in LDAP directories
#
%define		_enigmail_ver	0.94.3

Summary:	Thunderbird Community Edition - email client
Summary(pl.UTF-8):	Thunderbird Community Edition - klient poczty
Name:		mozilla-thunderbird
Version:	2.0.0.0
Release:	1
License:	MPL/LGPL
Group:		Applications/Networking
Source0:	http://ftp.mozilla.org/pub/mozilla.org/thunderbird/releases/%{version}/source/thunderbird-%{version}-source.tar.bz2
# Source0-md5:	8e672d9f9206e0e1f03790dacb51e1bb
Source1:	http://www.mozilla-enigmail.org/downloads/src/enigmail-%{_enigmail_ver}.tar.gz
# Source1-md5:	08727eea68589eb4c9087ca771229f06
Source2:	%{name}.desktop
Source3:	%{name}.sh
Source4:	%{name}-enigmail.manifest
Source5:	%{name}.png
Patch1:		%{name}-lib_path.patch
Patch3:		%{name}-nopangoxft.patch
Patch4:		%{name}-enigmail-shared.patch
Patch5:		%{name}-gcc.patch
Patch6:		%{name}-fonts.patch
Patch8:		%{name}-install.patch
Patch9:		%{name}-myspell.patch
Patch10:	%{name}-regionNames.patch
URL:		http://www.mozilla.org/projects/thunderbird/
BuildRequires:	automake
BuildRequires:	freetype-devel >= 1:2.1.8
BuildRequires:	gtk+2-devel >= 1:2.0.0
BuildRequires:	libIDL-devel >= 0.8.0
BuildRequires:	libjpeg-devel >= 6b
BuildRequires:	libpng-devel >= 1.2.0
BuildRequires:	libstdc++-devel
BuildRequires:	myspell-devel
BuildRequires:	nspr-devel >= 1:4.6.1
BuildRequires:	nss-devel >= 1:3.11.3
BuildRequires:	pango-devel >= 1:1.1.0
BuildRequires:	sed >= 4.0
Requires:	nspr >= 1:4.6.1
Requires:	nss >= 1:3.11.3
Obsoletes:	mozilla-thunderbird-dictionary-en-US
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# mozilla and thunderbird provide their own versions
%define		_noautoreqdep		libgfxpsshar.so libgkgfx.so libgtkembedmoz.so libgtkxtbin.so libjsj.so libmozjs.so libxpcom_compat.so libxpcom_core.so libxpcom.so libxpistub.so
%define		_noautoprovfiles	%{_libdir}/%{name}/components
# we don't want these to satisfy xulrunner-devel
%define		_noautoprov			libmozjs.so libxpcom.so libxul.so
# and as we don't provide them, don't require either
%define		_noautoreq			libmozjs.so libxpcom.so libxul.so

%description
Thunderbird Community Edition is an open-source,fast and portable
email client.

%description -l pl
Thunderbird Community Edition jest open sourcowym, szybkim i
przeno�nym klientem poczty.

%package addon-enigmail
Summary:	Extension for the authentication and encryption features provided by GnuPG
Summary(pl):	Rozszerzenie do uwierzytelniania i szyfrowania zapewnianego przez GnuPG
Version:	%{_enigmail_ver}
Release:	%{release}
License:	MPL/LGPL
Group:		Applications/Networking
URL:		http://enigmail.mozdev.org/
Requires:	%{name} = %{version}-%{release}

%description addon-enigmail
Enigmail is an extension to the mail client of Mozilla Thunderbird
which allows users to access the authentication and encryption
features provided by GnuPG.

Main Features:
- Encrypt/sign mail when sending, decrypt/authenticate received mail
- Support for inline-PGP (RFC 2440) and PGP/MIME (RFC 3156)
- Per-Account based encryption and signing defaults
- Per-Recipient rules for automated key selection, and
  enabling/disabling encryption and signing
- OpenPGP key management interface

%description addon-enigmail -l pl
Enigmail to rozszerzenie klienta pocztowego Mozilla Thunderbird
pozwalaj�ce u�ytkownikom na dost�p do uwierzytelniania i szyfrowania
zapewnianego przez GnuPG.

G��wne mo�liwo�ci:
- szyfrowanie/podpisywanie poczty przy wysy�aniu,
  odszyfrowywanie/uwierzytelnianie poczty odebranej
- obs�uga inline-PGP (RFC 2440) i PGP/MIME (RFC 3156)
- ustawienia domy�lne szyfrowania i podpisywania dla ka�dego konta
- regu�y automatycznego wyboru kluczy i w��czenia szyfrowania oraz
  podpisywania dla ka�dego adresata
- interfejs do zarz�dzania kluczami OpenPGP

%prep
%setup -q -c
cd mozilla
%{?with_enigmail:tar xvfz %{SOURCE1} -C mailnews/extensions}
%patch1 -p1
%patch3 -p1
%{?with_enigmail:%patch4 -p1}
%patch5 -p1
%patch6 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1

:> config/gcc_hidden.h

%build
cd mozilla
export CFLAGS="%{rpmcflags} `%{_bindir}/pkg-config mozilla-nspr --cflags-only-I`"
export CXXFLAGS="%{rpmcflags} `%{_bindir}/pkg-config mozilla-nspr --cflags-only-I`"

cp -f %{_datadir}/automake/config.* build/autoconf
cp -f %{_datadir}/automake/config.* nsprpub/build/autoconf
cp -f %{_datadir}/automake/config.* directory/c-sdk/config/autoconf

cat << 'EOF' > .mozconfig
. $topsrcdir/mail/config/mozconfig

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

%if %{with ldap}
ac_add_options --enable-ldap
%else
ac_add_options --disable-ldap
%endif
ac_add_options --disable-installer
ac_add_options --disable-jsd
ac_add_options --disable-xprint
ac_add_options --enable-canvas
ac_add_options --enable-crypto
ac_add_options --enable-default-toolkit="gtk2"
ac_add_options --enable-extensions="pref,cookie,wallet,spellcheck"
ac_add_options --enable-mathml
ac_add_options --enable-optimize="%{rpmcflags}"
ac_add_options --enable-pango
ac_add_options --enable-reorder
ac_add_options --disable-strip
ac_add_options --disable-strip-libs
ac_add_options --enable-system-cairo
ac_add_options --enable-system-myspell
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

%{__make} -j1 -f client.mk build_all \
	CC="%{__cc}" \
	CXX="%{__cxx}"

%if %{with enigmail}
	cd mailnews/extensions/enigmail
	./makemake -r
	%{__make}
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir},%{_pixmapsdir},%{_desktopdir}} \
	$RPM_BUILD_ROOT%{_datadir}/%{name}

cd mozilla
%{__make} -C xpinstall/packager stage-package \
	DESTDIR=$RPM_BUILD_ROOT \
	MOZ_PKG_APPDIR=%{_libdir}/%{name} \
	PKG_SKIP_STRIP=1

# move arch independant ones to datadir
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/chrome $RPM_BUILD_ROOT%{_datadir}/%{name}/chrome
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/defaults $RPM_BUILD_ROOT%{_datadir}/%{name}/defaults
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/greprefs $RPM_BUILD_ROOT%{_datadir}/%{name}/greprefs
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/icons $RPM_BUILD_ROOT%{_datadir}/%{name}/icons
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/init.d $RPM_BUILD_ROOT%{_datadir}/%{name}/init.d
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/isp $RPM_BUILD_ROOT%{_datadir}/%{name}/isp
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/res $RPM_BUILD_ROOT%{_datadir}/%{name}/res
ln -s ../../share/%{name}/chrome $RPM_BUILD_ROOT%{_libdir}/%{name}/chrome
ln -s ../../share/%{name}/defaults $RPM_BUILD_ROOT%{_libdir}/%{name}/defaults
ln -s ../../share/%{name}/greprefs $RPM_BUILD_ROOT%{_libdir}/%{name}/greprefs
ln -s ../../share/%{name}/icons $RPM_BUILD_ROOT%{_libdir}/%{name}/icons
ln -s ../../share/%{name}/init.d $RPM_BUILD_ROOT%{_libdir}/%{name}/init.d
ln -s ../../share/%{name}/isp $RPM_BUILD_ROOT%{_libdir}/%{name}/isp
ln -s ../../share/%{name}/res $RPM_BUILD_ROOT%{_libdir}/%{name}/res

rm -rf $RPM_BUILD_ROOT%{_libdir}/%{name}/dictionaries
ln -s %{_datadir}/myspell $RPM_BUILD_ROOT%{_libdir}/%{name}/dictionaries

%{__sed} -e 's,@LIBDIR@,%{_libdir},' %{SOURCE3} > $RPM_BUILD_ROOT%{_bindir}/mozilla-thunderbird
ln -s %{name} $RPM_BUILD_ROOT%{_bindir}/thunderbird

install %{SOURCE2} $RPM_BUILD_ROOT%{_desktopdir}/%{name}.desktop

%if %{with enigmail}
_enig_dir=$RPM_BUILD_ROOT%{_libdir}/%{name}/extensions/\{847b3a00-7ab1-11d4-8f02-006008948af5\}
install -d $_enig_dir/chrome
install -d $_enig_dir/components
install -d $_enig_dir/defaults/preferences
mv -f $RPM_BUILD_ROOT%{_libdir}/%{name}/chrome/enigmail.jar $_enig_dir/chrome
mv -f $RPM_BUILD_ROOT%{_libdir}/%{name}/chrome/enigmail-skin-tbird.jar $_enig_dir/chrome
mv -f $RPM_BUILD_ROOT%{_libdir}/%{name}/components/enig* $_enig_dir/components
mv -f $RPM_BUILD_ROOT%{_libdir}/%{name}/components/libenigmime.so $_enig_dir/components
mv -f $RPM_BUILD_ROOT%{_libdir}/%{name}/components/ipc.xpt $_enig_dir/components
mv -f $RPM_BUILD_ROOT%{_libdir}/%{name}/defaults/preferences/enigmail.js $_enig_dir/defaults/preferences
cp -f mailnews/extensions/enigmail/package/install.rdf $_enig_dir
rm -rf $RPM_BUILD_ROOT%{_libdir}/%{name}/defaults/preferences
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/chrome/enigmail-en-US.jar
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/chrome/enigmail-skin.jar
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/chrome/enigmime.jar
rm -rf $RPM_BUILD_ROOT%{_libdir}/%{name}/components/enig*
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/components/libenigmime.so
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/components/ipc.xpt
cp -f %{SOURCE4} $_enig_dir/chrome.manifest
cp -f %{SOURCE5} $RPM_BUILD_ROOT%{_pixmapsdir}/mozilla-thunderbird.png
%endif

# win32 stuff
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/dirver

%clean
rm -rf $RPM_BUILD_ROOT

%pretrans
if [ -d %{_libdir}/%{name}/dictionaries ] && [ ! -L %{_libdir}/%{name}/dictionaries ]; then
	mv -v %{_libdir}/%{name}/dictionaries{,.rpmsave}
fi
for d in chrome defaults greprefs icons init.d isp res; do
	if [ -d %{_libdir}/%{name}/$d ] && [ ! -L %{_libdir}/%{name}/$d ]; then
		install -d %{_datadir}/%{name}
		mv %{_libdir}/%{name}/$d %{_datadir}/%{name}/$d
	fi
done
exit 0

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mozilla-thunderbird
%attr(755,root,root) %{_bindir}/thunderbird
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/components
%attr(755,root,root) %{_libdir}/%{name}/components/*.so
%{_libdir}/%{name}/components/*.js
%{_libdir}/%{name}/components/*.xpt
%attr(755,root,root) %{_libdir}/%{name}/*.so
%attr(755,root,root) %{_libdir}/%{name}/*.sh
%attr(755,root,root) %{_libdir}/%{name}/*-bin
%attr(755,root,root) %{_libdir}/%{name}/mozilla-xremote-client
%attr(755,root,root) %{_libdir}/%{name}/reg*
%attr(755,root,root) %{_libdir}/%{name}/thunderbird
%{_libdir}/%{name}/*.txt
%attr(755,root,root) %{_libdir}/%{name}/x*

# symlinks
%{_libdir}/%{name}/chrome
%{_libdir}/%{name}/defaults
%{_libdir}/%{name}/dictionaries
%{_libdir}/%{name}/greprefs
%{_libdir}/%{name}/icons
%{_libdir}/%{name}/init.d
%{_libdir}/%{name}/isp
%{_libdir}/%{name}/res

%{_libdir}/%{name}/dependentlibs.list
%{_libdir}/%{name}/updater
%{_libdir}/%{name}/updater.ini
%{_pixmapsdir}/*.png
%{_desktopdir}/*.desktop

%dir %{_datadir}/%{name}
%{_datadir}/%{name}/chrome
%{_datadir}/%{name}/defaults
%{_datadir}/%{name}/greprefs
%{_datadir}/%{name}/icons
%{_datadir}/%{name}/init.d
%{_datadir}/%{name}/isp
%{_datadir}/%{name}/res

%dir %{_libdir}/%{name}/extensions
%{_libdir}/%{name}/extensions/{972ce4c6-7e08-4474-a285-3208198ce6fd}

%if %{with enigmail}
%files addon-enigmail
%defattr(644,root,root,755)
%{_libdir}/%{name}/extensions/{847b3a00-7ab1-11d4-8f02-006008948af5}
%endif
