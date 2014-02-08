%define	major 1
%define	libname %mklibname %{name} %{major}
%define	develname %mklibname %{name} -d

Summary:	API in "C" for Shapefile handling
Name:		shapelib
Version:	1.2.10
Release:	8
License:	LGPL MIT
Group:		Sciences/Geosciences
URL:		http://shapelib.maptools.org/
Source0:	http://shapelib.maptools.org/dl/%{name}-%{version}.tar.bz2
Patch0:		shapelib-1.2.10-gcc4-fix.patch
Patch1:		shapelib-1.2.10-mdkconf.patch
Requires:	proj >= 4.4.1
BuildRequires:	proj-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
The Shapefile C Library provides the ability to write
simple C programs for reading, writing and updating (to a
limited extent) ESRI Shapefiles, and the associated
attribute file (.dbf).

%package -n	%{libname}
Summary:	API in "C" for Shapefile handling
Group:		System/Libraries

%description -n	%{libname}
The Shapefile C Library provides the ability to write
simple C programs for reading, writing and updating (to a
limited extent) ESRI Shapefiles, and the associated
attribute file (.dbf).

%package -n	%{develname}
Summary:	API in "C" for Shapefile handling
Group:		Development/Other
Requires:	%{libname} = %{version}
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{mklibname %{name} 1 -d}

%description -n	%{develname}
The Shapefile C Library provides the ability to write
simple C programs for reading, writing and updating (to a
limited extent) ESRI Shapefiles, and the associated
attribute file (.dbf).

%prep

%setup -q
%patch0 -p1 -b .gcc4
%patch1 -p1 -b .mdkconf

%build
make CFLAGS="$RPM_OPT_FLAGS"
%ifarch sparc sparcv9 sparc64 ppc
make CFLAGS="$RPM_OPT_FLAGS -DPROJ4 -D_BIG_ENDIAN -I.. -w" -C contrib
%else
make CFLAGS="$RPM_OPT_FLAGS -DPROJ4 -D_LITTLE_ENDIAN -I.. -w" -C contrib
%endif
make lib CFLAGS="$RPM_OPT_FLAGS"

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_bindir}
install -m755 dbfadd dbfcreate dbfdump shpadd shpcreate shpdump shptest %{buildroot}%{_bindir}
install -m755 contrib/{dbfcat,dbfinfo,shpcat,shpcentrd,shpdata,shpdxf,shpfix,shpinfo,shpwkb,shpproj} %{buildroot}%{_bindir}

make lib_install LIB=%{_lib} DESTDIR=$RPM_BUILD_ROOT

#(peroyvind) don't care about these for now..
rm -f %{buildroot}%{_libdir}/lib*.*a

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files -n %{name}
%defattr (-,root,root)
%doc README.tree dbf_api.html shapelib.html shp_api.html
%doc contrib/doc/shpproj.txt
%{_bindir}/*

%files -n %{develname}
%defattr (-,root,root)
%{_includedir}/libshp/shapefil.h
%{_libdir}/*.so

%files -n %{libname}
%defattr (-,root,root)
%{_libdir}/*.so.*


%changelog
* Sun Sep 20 2009 Thierry Vignaud <tvignaud@mandriva.com> 1.2.10-7mdv2010.0
+ Revision: 445104
- rebuild

* Sat Jan 24 2009 Funda Wang <fundawang@mandriva.org> 1.2.10-6mdv2009.1
+ Revision: 333297
- rebuild

* Wed Jul 09 2008 Oden Eriksson <oeriksson@mandriva.com> 1.2.10-5mdv2009.0
+ Revision: 233022
- rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Tue Mar 11 2008 Oden Eriksson <oeriksson@mandriva.com> 1.2.10-4mdv2008.1
+ Revision: 185450
- bump release
- fix build

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tvignaud@mandriva.com>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Sep 09 2007 Oden Eriksson <oeriksson@mandriva.com> 1.2.10-3mdv2008.0
+ Revision: 83611
- new devel naming

* Sun Sep 09 2007 Oden Eriksson <oeriksson@mandriva.com> 1.2.10-2mdv2008.0
+ Revision: 83606
- Import shapelib



* Thu Aug 03 2006 Oden Eriksson <oeriksson@mandriva.com> 1.2.10-2mdv2007.0
- fix deps

* Thu Jun 16 2005 Per Øyvind Karlsen <pkarlsen@mandriva.com> 1.2.10-1mdk
- 1.2.10
- reintroduced this package with lots of fixes as it's required by roadmap (requested on the club)

* Mon Sep 03 2001 Lenny Cartier <lenny@mandrakesoft.com> 1.2.8-3mdk
- rebuild

* Mon Jan 29 2001 Lenny Cartier <lenny@mandrakesoft.com> 1.2.8-2mdk
- rebuild
- apply library policy

* Thu Nov 16 2000 Lenny Cartier <lenny@mandrakesoft.com> 1.2.8-1mdk
- patch makefile to install in buildroot
- used srpm from Franck Martin <franck@sopac.org>
