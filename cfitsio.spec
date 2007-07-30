%define name	cfitsio
%define version 2.490
%define release %mkrel 2
%define sversion %(echo %version|sed -e 's/\\.//g')

%define libname	%mklibname %name

Name:		cfitsio
Version:	%version
Release:	%release
URL:	http://heasarc.gsfc.nasa.gov/docs/software/fitsio/
Source:	ftp://heasarc.gsfc.nasa.gov/software/fitsio/c/%{name}%{sversion}.tar.bz2
License:	BSD-like
Summary:	Library for accessing files in FITS format for C and Fortran
Group:		System/Libraries
BuildRequires:	gcc-gfortran
BuildRoot:	%{_tmppath}/%{name}-%{version}-root

%description
CFITSIO is a library of C and Fortran subroutines for reading and 
writing data files in FITS (Flexible Image Transport System) data format. 
CFITSIO simplifies the task of writing software that deals with FITS 
files by providing an easy to use set of high-level routines that insulate 
the programmer from the internal complexities of the FITS file format. 
At the same time, CFITSIO provides many advanced features that have made 
it the most widely used FITS file programming interface in the astronomical 
community.

%package -n %libname
License:	BSD-like
Summary:	Library for accessing files in FITS format for C and Fortran
Group:		System/Libraries

%description -n %{libname}
CFITSIO is a library of C and Fortran subroutines for reading and 
writing data files in FITS (Flexible Image Transport System) data format. 
CFITSIO simplifies the task of writing software that deals with FITS 
files by providing an easy to use set of high-level routines that insulate 
the programmer from the internal complexities of the FITS file format. 
At the same time, CFITSIO provides many advanced features that have made 
it the most widely used FITS file programming interface in the astronomical 
community.

This package contains the shared library required by prgrams that use the
cfits library.

%package -n %{libname}-devel
License:	BSD-like
Summary:	Library for accessing files in FITS format for C and Fortran
Group:		System/Libraries
Provides:	fitsio-devel = %{version} cfitsio-devel = %{version}

%description -n %{libname}-devel
CFITSIO is a library of C and Fortran subroutines for reading and 
writing data files in FITS (Flexible Image Transport System) data format. 
CFITSIO simplifies the task of writing software that deals with FITS 
files by providing an easy to use set of high-level routines that insulate 
the programmer from the internal complexities of the FITS file format. 
At the same time, CFITSIO provides many advanced features that have made 
it the most widely used FITS file programming interface in the astronomical 
community.

This package contains the headers required for compiling software that uses
the cfits library.

%prep
%setup -q -n %{name}

%build
%configure
%make shared

%install
rm -Rf %{buildroot}
install -d %{buildroot}/{%{_libdir},%{_includedir}}
%makeinstall_std CFITSIO_LIB=%{buildroot}/%{_libdir} CFITSIO_INCLUDE=%{buildroot}/%{_includedir}

%clean
rm -Rf %{buildroot}

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so

%files -n %{libname}-devel
%defattr(-,root,root)
%{_includedir}/drvrsmem.h
%{_includedir}/fitsio.h
%{_includedir}/fitsio2.h
%{_includedir}/longnam.h
%{_libdir}/libcfitsio.a

