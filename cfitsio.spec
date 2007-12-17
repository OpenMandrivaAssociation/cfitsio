%define sversion 3040

%define libname %mklibname %name
%define develname %mklibname %name -d

Name: cfitsio
Version: 3.040
Release: %mkrel 1
URL:	http://heasarc.gsfc.nasa.gov/docs/software/fitsio/
Source:	ftp://heasarc.gsfc.nasa.gov/software/fitsio/c/%{name}%{sversion}.tar.gz
License:	BSD-like
Summary:	Library for accessing files in FITS format for C and Fortran
Group:		System/Libraries
BuildRequires:	gcc-gfortran
BuildRequires: pkgconfig
Obsoletes: %libname

%description
CFITSIO is a library of C and Fortran subroutines for reading and 
writing data files in FITS (Flexible Image Transport System) data format. 
CFITSIO simplifies the task of writing software that deals with FITS 
files by providing an easy to use set of high-level routines that insulate 
the programmer from the internal complexities of the FITS file format. 
At the same time, CFITSIO provides many advanced features that have made 
it the most widely used FITS file programming interface in the astronomical 
community.

%package -n %{develname}
License:	BSD-like
Summary:	Library for accessing files in FITS format for C and Fortran
Group:		System/Libraries
Provides:	fitsio-devel = %{version} 
Provides:   cfitsio-devel = %{version}
Requires:   pkgconfig

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

%prep
%setup -q -n %{name}

%build
%configure

%make

%install
rm -Rf %{buildroot}
install -d %{buildroot}/{%{_libdir},%{_includedir}}
%makeinstall_std CFITSIO_LIB=%{buildroot}/%{_libdir} CFITSIO_INCLUDE=%{buildroot}/%{_includedir}

%clean
rm -Rf %{buildroot}


%files -n %{develname}
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.a
%{_libdir}/pkgconfig/*


