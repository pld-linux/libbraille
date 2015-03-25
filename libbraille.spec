#
# Conditional build:
%bcond_without	apidocs	# do not build and package API docs
%bcond_with	java	# Java binding
%bcond_without	python	# Python binding

Summary:	Library to easily access Braille displays and terminals
Summary(pl.UTF-8):	Biblioteka łatwego dostępu do wyświetlaczy i terminali Braille'a
Name:		libbraille
Version:	0.19.0
Release:	4
License:	LGPL v2.1
Group:		Libraries
Source0:	http://downloads.sourceforge.net/libbraille/%{name}-%{version}.tar.gz
# Source0-md5:	80198ae147d726f6b743f5a984fa7bd1
Patch0:		%{name}-link.patch
Patch1:		%{name}-java.patch
URL:		http://libbraille.org/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
%{?with_java:BuildRequires:	jdk}
%{?with_apidocs:BuildRequires:	latex2html}
BuildRequires:	libltdl-devel
BuildRequires:	libtool
BuildRequires:	libusb-compat-devel >= 0.1
BuildRequires:	rpmbuild(macros) >= 1.294
BuildRequires:	sed >= 4.0
%if %{with java} || %{with python}
BuildRequires:	swig
%endif
%if %{with python}
BuildRequires:	python-devel
BuildRequires:	swig-python
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Libbraille is a library to easily access Braille displays and
terminals.

%description -l pl.UTF-8
Libbraille to biblioteka łatwego dostępu do wyświetlaczy i terminali
Braille'a.

%package devel
Summary:	Header files for libbraille library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libbraille
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libltdl-devel

%description devel
Header files for libbraille library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libbraille.

%package static
Summary:	Static libbraille library
Summary(pl.UTF-8):	Statyczna biblioteka libbraille
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libbraille library.

%description static -l pl.UTF-8
Statyczna biblioteka libbraille.

%package apidocs
Summary:	libbraille API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki libbraille
Group:		Documentation
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif


%description apidocs
API and internal documentation for libbraille library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libbraille.

%package -n java-libbraille
Summary:	Java binding for libbraille library
Summary(pl.UTF-8):	Wiązania Javy do biblioteki libbraille
Group:		Libraries/Java
Requires:	%{name} = %{version}-%{release}
Requires:	jpackage-utils

%description -n java-libbraille
Java binding for libbraille library.

%description -n java-libbraille -l pl.UTF-8
Wiązania Javy do biblioteki libbraille.

%package -n python-libbraille
Summary:	Python binding for libbraille library
Summary(pl.UTF-8):	Wiązania Pythona do biblioteki libbraille
Group:		Development/Languages/Python
Requires:	%{name} = %{version}-%{release}

%description -n python-libbraille
Python binding for libbraille library.

%description -n python-libbraille -l pl.UTF-8
Wiązania Pythona do biblioteki libbraille.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

# shared library should use shared libltdl
%{__sed} -i -e 's/^AC_LIBLTDL_CONVENIENCE/AC_LIBLTDL_INSTALLABLE/' configure.ac

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-ltdl-install \
	%{?with_apidocs:--enable-doc} \
	%{?with_java:--enable-java --with-javainc=%{_jvmdir}/java/include --with-javaincnative=%{_jvmdir}/java/include} \
	%{?with_python:--enable-python}

# parallel build fails on docs
%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# remove static modules; keep *.la (lt_dlopen is used), .so symlinks are not needed
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libbraille/*.{a,so}

%if %{with java}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libjbraille.{la,a}
install -D java/jbraille.jar $RPM_BUILD_ROOT%{_javadir}/jbraille.jar
%endif

%if %{with python}
%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/_braille.{a,la}
%py_postclean
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README TODO
%attr(755,root,root) %{_bindir}/test_libbraille
%attr(755,root,root) %{_libdir}/libbraille-0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libbraille-0.so.14
%dir %{_libdir}/libbraille
%attr(755,root,root) %{_libdir}/libbraille/alva-0.so.*
%{_libdir}/libbraille/alva.la
%attr(755,root,root) %{_libdir}/libbraille/alvausb-0.so.*
%{_libdir}/libbraille/alvausb.la
%attr(755,root,root) %{_libdir}/libbraille/baum-0.so.*
%{_libdir}/libbraille/baum.la
%attr(755,root,root) %{_libdir}/libbraille/braillelite-0.so.*
%{_libdir}/libbraille/braillelite.la
%attr(755,root,root) %{_libdir}/libbraille/braillenote-0.so.*
%{_libdir}/libbraille/braillenote.la
%attr(755,root,root) %{_libdir}/libbraille/eurobraille-0.so.*
%{_libdir}/libbraille/eurobraille.la
%attr(755,root,root) %{_libdir}/libbraille/handytech-0.so.*
%{_libdir}/libbraille/handytech.la
%attr(755,root,root) %{_libdir}/libbraille/none-0.so.*
%{_libdir}/libbraille/none.la
%attr(755,root,root) %{_libdir}/libbraille/once-0.so.*
%{_libdir}/libbraille/once.la
%attr(755,root,root) %{_libdir}/libbraille/papenmeierusb-0.so.*
%{_libdir}/libbraille/papenmeierusb.la
%attr(755,root,root) %{_libdir}/libbraille/technibraille-0.so.*
%{_libdir}/libbraille/technibraille.la
%attr(755,root,root) %{_libdir}/libbraille/text-0.so.*
%{_libdir}/libbraille/text.la
%attr(755,root,root) %{_libdir}/libbraille/voyager-0.so.*
%{_libdir}/libbraille/voyager.la
%{_datadir}/libbraille
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/libbraille.conf

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libbraille.so
%{_libdir}/libbraille.la
%{_includedir}/braille.h
%{_includedir}/brl_keycode.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libbraille.a

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc doc/*.{css,html}
%endif

%if %{with java}
%files -n java-libbraille
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libjbraille.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libjbraille.so.14
%attr(755,root,root) %{_libdir}/libjbraille.so
%{_javadir}/jbraille.jar
%endif

%if %{with python}
%files -n python-libbraille
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/_braille.so
%{py_sitescriptdir}/braille.py[co]
%endif
