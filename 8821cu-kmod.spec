%global buildforkernels akmod
%global debug_package %{nil}

%global gitref a0c18978d1c9ab89f96083354f2c55cf15d483f7

%global modname 8821cu

Name: %{modname}-kmod
Summary: Kernel module (kmod) for %{modname}
Version: 20230122.a0c1897
Release: 5%{?dist}
License: GPLv2+

URL: https://github.com/morrownr/8821cu-20210118
Source0: %{URL}/archive/%{gitref}.tar.gz

BuildRequires: %{_bindir}/kmodtool
%{!?kernels:BuildRequires: gcc, elfutils-libelf-devel, buildsys-build-rpmfusion-kerneldevpkgs-%{?buildforkernels:%{buildforkernels}}%{!?buildforkernels:current}-%{_target_cpu} }

# kmodtool does its magic here
%{expand:%(kmodtool --target %{_target_cpu} --repo rpmfusion --kmodname %{modname} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%description
Realtek RTL8811CU/RTL8821CU USB wifi adapter driver.

This package contains the kmod module for %{modname}.

%prep
# error out if there was something wrong with kmodtool
%{?kmodtool_check}

# print kmodtool output for debugging purposes:
kmodtool  --target %{_target_cpu} --repo rpmfusion --kmodname %{modname} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null


#%setup -q -n %{modname}-20210118-%{gitref}
%setup -q -c
for kernel_version in %{?kernel_versions} ; do
  cp -a %{modname}-20210118-%{gitref} _kmod_build_${kernel_version%%___*}
done


%build
for kernel_version  in %{?kernel_versions} ; do
  pushd _kmod_build_${kernel_version%%___*}
	CONFIG_RTL8821CU=m make -C ${kernel_version##*___} M=${PWD} modules
	popd
done


%install
rm -fr ${RPM_BUILD_ROOT}
for kernel_version in %{?kernel_versions}; do
	pushd _kmod_build_${kernel_version%%___*}
  mkdir -p %{buildroot}%{kmodinstdir_prefix}${kernel_version%%___*}%{kmodinstdir_postfix}
  install -D -m 755 %{modname}.ko %{buildroot}%{kmodinstdir_prefix}${kernel_version%%___*}%{kmodinstdir_postfix}
	chmod a+x %{buildroot}%{kmodinstdir_prefix}${kernel_version%%___*}%{kmodinstdir_postfix}%{modname}.ko
done
%{?akmod_install}


%changelog
* Sun Jan 22 2023 First Akmod release of 8821CU drivers - 20230122.a0c1897-1
- Built the first version of this kmod to enable rtl8821CU for silverblue
