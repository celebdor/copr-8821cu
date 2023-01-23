%global debug_package %{nil}

Name: 8821cu
Version: 20230122.a0c1897
Release: 2%{?dist}
Summary: Common files for 8821CU driver

%global gitref a0c18978d1c9ab89f96083354f2c55cf15d483f7

%global modname 8821cu

License: GPLv2+
URL: https://github.com/morrownr/8821cu-20210118
Source0: %{URL}/archive/%{gitref}.tar.gz

BuildArch: noarch
Provides: %{modname}-kmod-common = %{?epoch}:%{version}
Requires: %{modname}-kmod

%description
Provides module options files for usb wireless cards based on 8821CU.


%prep
%setup -q -n %{modname}-20210118-%{gitref}


%build
echo "Nothing to build"


%install
install -m 0755 -d %{buildroot}%{_modprobedir}
install -p -m 0644 %{modname}.conf %{_sysconfdir}/modprobe.d/
install -m 0755 -d %{buildroot}%{_docdir}/%{name}
install -m 0755 -d %{buildroot}%{_licensedir}/%{name}


%files
%license LICENSE
%doc README.md
%config(noreplace) %{_sysconfdir}/modprobe.d/%{modname}.conf

%changelog
* Sun Jan 22 2023 First release of 8821CU drivers - 20230122.a0c1897-1
- Built the first version of this common files to enable rtl8821CU for silverblue

