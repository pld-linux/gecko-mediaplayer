Summary:	Gecko Media Player - browser plugin
Summary(pl.UTF-8):	Gecko Media Player - wtyczka dla przeglądarek
Name:		gecko-mediaplayer
Version:	0.9.9
Release:	1
License:	GPL
Group:		X11/Applications/Multimedia
Source0:	http://gecko-mediaplayer.googlecode.com/files/%{name}-%{version}.tar.gz
# Source0-md5:	1833c83ee2bb226914aa078165d04ddd
Patch0:		%{name}-runtime.patch
Patch1:		%{name}-configure_in.patch
URL:		http://kdekorte.googlepages.com/gecko-mediaplayer
BuildRequires:	GConf2
BuildRequires:	GConf2-devel
BuildRequires:	autoconf >= 2.57
BuildRequires:	automake
BuildRequires:	dbus-devel
BuildRequires:	gettext-devel
BuildRequires:	gtk+2-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.357
BuildRequires:	xulrunner-devel >= 1.8.1.12-1.20080208.3
Requires(post,preun):	GConf2
Requires:	browser-plugins >= 2.0
Requires:	browser-plugins(%{_target_base_arch})
Requires:	gnome-mplayer >= 0.9.5
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Gecko Media Player is a browser plugin that uses GNOME MPlayer to play
media in a browser.

%description -l pl.UTF-8
Gecko Media Player to wtyczka dla przeglądarek wykorzystująca GNOME
MPlayera do otwarzania multimediów w przeglądarce.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

# remove with new upstream version (should have this fixed)
sed -i -e 's#utf8characters#UTF8Characters#g' src/plugin.cpp

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
%attr(755,root,root) %{_browserpluginsdir}/gecko-mediaplayer*.so
%{_sysconfdir}/gconf/schemas/gecko-mediaplayer.schemas
