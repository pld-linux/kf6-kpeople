# Conditional build:
%bcond_with	tests		# build without tests
#
%define		kdeframever	6.23
%define		qtver		6.7.0
%define		kfname		kpeople
Summary:	Provides access to all contacts and the people who hold them
Name:		kf6-%{kfname}
Version:	6.23.0
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	627545d2bb64280cb6e726ca15e3b6a3
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6DBus-devel >= %{qtver}
BuildRequires:	Qt6Gui-devel >= %{qtver}
BuildRequires:	Qt6Sql-devel >= %{qtver}
BuildRequires:	Qt6Qml-devel >= %{qtver}
BuildRequires:	Qt6Quick-devel >= %{qtver}
%{?with_tests:BuildRequires:	Qt6Test-devel >= %{qtver}}
BuildRequires:	Qt6Widgets-devel >= %{qtver}
BuildRequires:	cmake >= 3.16
BuildRequires:	kf6-extra-cmake-modules >= %{version}
BuildRequires:	kf6-kcontacts-devel >= %{kdeframever}
BuildRequires:	kf6-kcoreaddons-devel >= %{kdeframever}
BuildRequires:	kf6-ki18n-devel >= %{kdeframever}
BuildRequires:	kf6-kitemviews-devel >= %{kdeframever}
BuildRequires:	kf6-kwidgetsaddons-devel >= %{kdeframever}
BuildRequires:	ninja
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	kf6-dirs
#Obsoletes:	kf5-%{kfname} < %{version}
%requires_eq_to Qt6Core Qt6Core-devel
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
%{_libdir}/libKF6People.so.*.*.*
%ghost %{_libdir}/libKF6People.so.6
%{_libdir}/libKF6PeopleBackend.so.*.*.*
%ghost %{_libdir}/libKF6PeopleBackend.so.6
%{_libdir}/libKF6PeopleWidgets.so.*.*.*
%ghost %{_libdir}/libKF6PeopleWidgets.so.6
%dir %{_libdir}/qt6/plugins/kpeople
%dir %{_libdir}/qt6/plugins/kpeople/datasource
%{_libdir}/qt6/plugins/kpeople/datasource/KPeopleVCard.so
%dir %{_libdir}/qt6/qml/org/kde/people
%{_libdir}/qt6/qml/org/kde/people/qmldir
%{_libdir}/qt6/qml/org/kde/people/libKF6PeopleDeclarative.so
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
