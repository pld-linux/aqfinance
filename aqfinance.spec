#
# Conditional build:
%bcond_without	static_libs	# static library
#
Summary:	AqFinance - financial application with GUI
Summary(de.UTF-8):	AqFinance - eine graphische Anwendung zur Verwaltung von Finanzen
Summary(pl.UTF-8):	AqFinance - aplikacja finansowa z graficznym interfejsem
Name:		aqfinance
Version:	0.9.108beta
Release:	1
License:	GPL v2+
Group:		X11/Applications
# https://www.aquamaniac.de/sites/download/packages.php?showall=1
Source0:	https://www.aquamaniac.de/sites/download/download.php?package=12&release=49&file=01&dummy=/%{name}-%{version}.tar.gz
# Source0-md5:	4ae8f233d71597802da39cd3aea5a7c9
Patch0:		%{name}-update.patch
Patch1:		%{name}-make.patch
URL:		https://www.aquamaniac.de/sites/aqfinance/
BuildRequires:	aqbanking-backend-aqhbci-devel >= 5
BuildRequires:	aqbanking-devel >= 5
BuildRequires:	aqdatabase-devel
BuildRequires:	aqfoxext-devel
BuildRequires:	autoconf >= 2.60
BuildRequires:	automake
BuildRequires:	cairo-devel
BuildRequires:	fox16-devel >= 1.6
BuildRequires:	gettext-tools
BuildRequires:	gwenhywfar-devel >= 4
BuildRequires:	gwenhywfar-fox-devel >= 4
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:1.5
BuildRequires:	pkgconfig
Requires:	aqbanking >= 5
Requires:	aqbanking-backend-aqhbci >= 5
Requires:	gwenhywfar-fox >= 4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
AqFinance is a financial application with GUI, successor of
QBankManager.

It supports (via AqBanking) HBCI, OFX DirectConnect and EBICS.

%description -l de.UTF-8
AqFinance ist eine grafische Anwendung zur Verwaltung von Finanzen und
der Nachfolger von QBankManager.

Es bietet via AqBanking Unterstützung für HBCI, OFX DirectConnect und
EBICS.

%description -l pl.UTF-8
AqFinance to aplikacja finansowa z graficznym interfejsem, następca
programu QBankManager.

Poprzez AqBanking ma obsługę HBCI, OFX DirectConnect oraz EBICS.

%package devel
Summary:	Header files for AqFinance library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki AqFinance
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	aqbanking-devel >= 5
Requires:	aqdatabase-devel
Requires:	gwenhywfar-devel >= 4

%description devel
Header files for AqFinance library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki AqFinance.

%package static
Summary:	Static AqFinance library
Summary(pl.UTF-8):	Statyczna biblioteka AqFinance
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static AqFinance library.

%description static -l pl.UTF-8
Statyczna biblioteka AqFinance.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

install -d aqfinance/report
ln -s ../src/lib/engine aqfinance
ln -s lib/book aqfinance/engine/book
ln -s lib/modules aqfinance/engine/modules
ln -s ../src/lib/graphics aqfinance
ln -s ../src/lib/graphs aqfinance
ln -s ../src/lib/print aqfinance
ln -s ../src/lib/report2 aqfinance
ln -s ../src/lib/update aqfinance
cd aqfinance/report
ln -s ../../src/lib/engine/lib/modules/report/*.h .
ln -s ../../src/lib/engine/plugins/report/csv/*.h .
ln -s ../../src/lib/engine/plugins/report/htmlbase/*.h .

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_static_libs:--disable-static}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by -config and .m4
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libaqfinance.la

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS README TODO
%attr(755,root,root) %{_bindir}/aqfinance
%attr(755,root,root) %{_bindir}/aqfinance-cli
%attr(755,root,root) %{_libdir}/libaqfinance.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libaqfinance.so.0
%dir %{_datadir}/aqfinance
%dir %{_datadir}/aqfinance/accounts
%{_datadir}/aqfinance/accounts/c
%lang(de_DE) %{_datadir}/aqfinance/accounts/de_DE
%{_datadir}/aqfinance/icons

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/aqfinance-config
%attr(755,root,root) %{_libdir}/libaqfinance.so
%{_includedir}/aqfinance
%{_datadir}/aqfinance/typemaker2
%{_aclocaldir}/aqfinance.m4

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libaqfinance.a
%endif
