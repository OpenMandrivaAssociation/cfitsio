%define sversion %(echo %version |sed -e 's#\\.##')
%define major 3
%define libname %mklibname %{name} %{major}
%define develname %mklibname %name -d
%define develnamestatic %mklibname %name -d -s

Name: cfitsio
Version: 3.210
Release: %mkrel 1
URL:	http://heasarc.gsfc.nasa.gov/docs/software/fitsio/
Source:	ftp://heasarc.gsfc.nasa.gov/software/fitsio/c/%{name}%{sversion}.tar.gz
Patch0: cfitsio-3.210-autotools.patch
License:	BSD-like
Summary:	Library for accessing files in FITS format for C and Fortran
Group:		System/Libraries
BuildRequires:	gcc-gfortran
BuildRequires: pkgconfig
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

%package -n %{libname}
License: BSD-like
Summary: Library for accessing files in FITS format for C and Fortran
Group:	 	 System/Libraries
Obsoletes:	%{_lib}%{name} < 3.090

%description -n %{libname}

CFITSIO is a library of C and Fortran subroutines for reading and
writing data files in FITS (Flexible Image Transport System) data
format.  CFITSIO simplifies the task of writing software that deals
with FITS files by providing an easy to use set of high-level routines
that insulate the programmer from the internal complexities of the
FITS file format.  At the same time, CFITSIO provides many advanced
features that have made it the most widely used FITS file programming
interface in the astronomical community.  This package contains the
shared library required by prgrams that use the cfits library.

%package -n %{develname}
License:	BSD-like
Summary:	Library for accessing files in FITS format for C and Fortran
Group:		System/Libraries
Provides:	fitsio-devel = %{version} 
Provides:   cfitsio-devel = %{version}
Requires:   pkgconfig
Requires:   %libname = %version
Conflicts:	%{_lib}%{name} < 3.090

%description -n %{develname}
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

%package -n %{develnamestatic}
License:	BSD-like
Summary:	Library for accessing files in FITS format for C and Fortran
Group:		System/Libraries
Requires:   %{develname}
Requires:   %libname = %version

%description -n %{develnamestatic}
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
%patch0 -p0

%build
autoreconf -fi
%configure2_5x --enable-static --enable-shared
%make

%install
rm -Rf %{buildroot}
install -d %{buildroot}/{%{_libdir},%{_includedir}}
%makeinstall_std CFITSIO_LIB=%{buildroot}/%{_libdir} CFITSIO_INCLUDE=%{buildroot}/%{_includedir}

%clean
rm -Rf %{buildroot}

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%files
%defattr(-,root,root)
%{_bindir}/*

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/*.la
%{_includedir}/*
%{_libdir}/pkgconfig/*

%files -n %{develnamestatic}
%defattr(-,root,root)
%{_libdir}/*.a

