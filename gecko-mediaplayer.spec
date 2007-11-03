Summary:	Gecko Media Player - browser plugin
Summary(pl.UTF-8):	Gecko Media Player - wtyczka dla przeglądarek
Name:		gecko-mediaplayer
Version:	0.5.2
Release:	1
License:	GPL
Group:		X11/Applications/Multimedia
Source0:	http://dekorte.homeip.net/download/gecko-mediaplayer/%{name}-%{version}.tar.gz
# Source0-md5:	da57304e4adfedbbc440d175650308a8
URL:		http://dekorte.homeip.net/download/gecko-mediaplayer/
BuildRequires:	autoconf >= 2.57
BuildRequires:	automake
BuildRequires:	dbus-devel
BuildRequires:	gettext-devel
BuildRequires:	gtk+2-devel
BuildRequires:	libstdc++-devel
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.357
BuildRequires:	xorg-lib-libXpm-devel
BuildRequires:	xorg-lib-libXt-devel
BuildRequires:	xulrunner-devel
Requires:	gnome-mplayer >= 0.5.2
Requires:	browser-plugins >= 2.0
Requires:	browser-plugins(%{_target_base_arch})
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Gecko Media Player is a browser plugin that uses GNOME MPlayer to play
media in a browser.

%description -l pl.UTF-8
Gecko Media Player to wtyczka dla przeglądarek wykorzystująca GNOME
MPlayera do otwarzania multimediów w przeglądarce.

%prep
%setup -q

%build
%configure
%{__make} \
	GECKO_IDLDIR=%{_includedir}/xulrunner/idl

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
%update_browser_plugins

%postun
if [ "$1" = 0 ]; then
	%update_browser_plugins
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog
%attr(755,root,root) %{_browserpluginsdir}/*.so
%{_browserpluginsdir}/*.xpt
%{_sysconfdir}/gconf/schemas/*.*
