Summary:	Gecko Media Player - browser plugin
Summary(pl.UTF-8):	Gecko Media Player - wtyczka dla przeglądarek
Name:		gecko-mediaplayer
Version:	1.0.9a
Release:	1
License:	GPL
Group:		X11/Applications/Multimedia
Source0:	http://gecko-mediaplayer.googlecode.com/files/%{name}-%{version}.tar.gz
# Source0-md5:	a27a507dc9b578c85c659fd6bb85d62e
Patch0:		%{name}-runtime.patch
URL:		http://kdekorte.googlepages.com/gecko-mediaplayer
BuildRequires:	GConf2
BuildRequires:	GConf2-devel
BuildRequires:	autoconf >= 2.57
BuildRequires:	automake
BuildRequires:	dbus-devel
BuildRequires:	gettext-tools
BuildRequires:	gmtk-devel >= 1.0.8
BuildRequires:	gtk+2-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.357
BuildRequires:	xulrunner-devel >= 1.8.1.12-1.20080208.3
Requires:	browser-plugins >= 2.0
Requires:	browser-plugins(%{_target_base_arch})
Requires:	gnome-mplayer >= 1.0.8
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Gecko Media Player is a browser plugin that uses GNOME MPlayer to play
media in a browser.

%description -l pl.UTF-8
Gecko Media Player to wtyczka dla przeglądarek wykorzystująca GNOME
MPlayera do otwarzania multimediów w przeglądarce.

%prep
%setup -q
%patch -P0 -p1
%{__sed} -i 's/AM_CONFIG_HEADER/AC_CONFIG_HEADERS/g' configure.in
%{__sed} -i 's/AM_PROG_CC_STDC/AC_PROG_CC/g' configure.in

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	install_libexecdir=%{_browserpluginsdir} \
	xptdir=%{_browserpluginsdir} \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_sysconfdir}/gconf/schemas
cp -p %{name}.schemas $RPM_BUILD_ROOT%{_sysconfdir}/gconf/schemas

%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%gconf_schema_install gecko-mediaplayer.schemas
%update_browser_plugins

%preun
%gconf_schema_uninstall gecko-mediaplayer.schemas

%postun
if [ "$1" = 0 ]; then
	%update_browser_plugins
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc ChangeLog DOCS/tech/javascript.txt
%{_sysconfdir}/gconf/schemas/gecko-mediaplayer.schemas
%attr(755,root,root) %{_browserpluginsdir}/gecko-mediaplayer*.so
