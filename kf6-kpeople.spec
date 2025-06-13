# Conditional build:
%bcond_with	tests		# build without tests
#
%define		kdeframever	6.15
%define		qtver		5.15.2
%define		kfname		kpeople
Summary:	Provides access to all contacts and the people who hold them
Name:		kf6-%{kfname}
Version:	6.15.0
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	db479f08002ac2ef0a76995053e08fa5
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6Gui-devel >= %{qtver}
BuildRequires:	Qt6Network-devel >= %{qtver}
BuildRequires:	Qt6Test-devel >= %{qtver}
%if %{with tests}
BuildRequires:	Qt6Gui-devel >= %{qtver}
BuildRequires:	Qt6Widgets-devel >= %{qtver}
%endif
BuildRequires:	cmake >= 3.16
BuildRequires:	kf6-extra-cmake-modules >= %{version}
BuildRequires:	kf6-kcontacts-devel >= %{version}
BuildRequires:	kf6-kcoreaddons-devel >= %{version}
BuildRequires:	ninja
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	kf6-dirs
#Obsoletes:	kf5-%{kfname} < %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Provides access to all contacts and the people who hold them.

%package devel
Summary:	Header files for %{kfname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kfname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
#Obsoletes:	kf5-%{kfname}-devel < %{version}

%description devel
Header files for %{kfname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kfname}.

%prep
%setup -q -n %{kfname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON

%ninja_build -C build

%{?with_tests:%ninja_build -C build test}


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kfname}5 --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{kfname}5.lang
%defattr(644,root,root,755)
%doc README.md
%{_datadir}/qlogging-categories6/kpeople.categories
%attr(755,root,root) %{_libdir}/libKF6People.so.*.*.*
%ghost %{_libdir}/libKF6People.so.6
%attr(755,root,root) %{_libdir}/libKF6PeopleBackend.so.*.*.*
%ghost %{_libdir}/libKF6PeopleBackend.so.6
%attr(755,root,root) %{_libdir}/libKF6PeopleWidgets.so.*.*.*
%ghost %{_libdir}/libKF6PeopleWidgets.so.6
%dir %{_libdir}/qt6/plugins/kpeople
%dir %{_libdir}/qt6/plugins/kpeople/datasource
%attr(755,root,root) %{_libdir}/qt6/plugins/kpeople/datasource/KPeopleVCard.so
%dir %{_libdir}/qt6/qml/org/kde/people
%{_libdir}/qt6/qml/org/kde/people/qmldir
%attr(755,root,root) %{_libdir}/qt6/qml/org/kde/people/libKF6PeopleDeclarative.so
%{_datadir}/qlogging-categories6/kpeople.renamecategories
%{_libdir}/qt6/qml/org/kde/people/KF6PeopleDeclarative.qmltypes
%{_libdir}/qt6/qml/org/kde/people/kde-qmlmodule.version

%files devel
%defattr(644,root,root,755)
%{_libdir}/libKF6People.so
%{_libdir}/libKF6PeopleBackend.so
%{_libdir}/libKF6PeopleWidgets.so
%{_includedir}/KF6/KPeople
%{_libdir}/cmake/KF6People
