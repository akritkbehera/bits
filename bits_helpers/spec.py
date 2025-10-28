def rpm_name(spec_or_name) -> str:
  """
  Generate a CMS-style RPM name.
  If `spec_or_name` is a string -> return template with shell vars.
  If `spec_or_name` is a dict  -> return expanded version using its fields.
  """
  if isinstance(spec_or_name, str):
    s = spec_or_name
    upper = s.upper().replace('-', '_')
    return f"cms_{s}_${{{upper}_VERSION}}_${{{upper}_REVISION}}_${{{upper}_HASH}}"
  elif isinstance(spec_or_name, dict):
    s = spec_or_name.get("package")
    version = spec_or_name.get("version")
    revision = spec_or_name.get("revision")
    hash = spec_or_name.get("hash")
    return f"cms_{s}_{version}_{revision}_{hash}"
  else:
    raise TypeError("rpm_name() expects a string or a dict")
def generate_spec(spec: dict):
  if spec.get("package")=="system-base-import":
    return generate_system_base_spec(spec)
  content = [
    '%define __os_install_post %{nil}\n',
    '%define __spec_install_post %{nil}\n',
    # '%define __spec_install_pre %{___build_pre}\n',
    '%define _empty_manifest_terminate_build 0\n',
    '%define _use_internal_dependency_generator 0\n',
    '%define _source_payload w9.gzdio\n',
    '%define _binary_payload w9.gzdio\n',
    '\n',
    f'Name: {rpm_name(spec)}\n',  # Pass without the initial $
    'Version: $PKG_VERSION\n',
    'Release: $PKGREVISION\n',
    'Summary: $PKG_NAME built as a part of CMS\n',
    'License: MIT\n',
    'BuildArch: $(uname -m)\n',
  ]

  full_requires = spec.get("full_runtime_requires", set())
  if full_requires:
    for dep in sorted(full_requires):
      dep_clean = dep.lower().replace('-', '_')
      content.append(f"Requires: {rpm_name(dep_clean)}\n")

  content.append('\n%description\n')
  content.append('CMS package for $PKG_NAME\n')
  content.append('Built on: $(hostname)\n')
  content.append('Build date: $(date)\n')

  content.append('\n%install\n')
  content.append('cp -a $INSTALLROOT/* %{buildroot}/\n')
  content.append('find %{buildroot} -type f -exec chmod u+w {} \\;\n')
  content.append('find %{buildroot} -type d -exec chmod u+w {} \\;\n')
  content.append('\n%files\n')
  content.append('/*\n')
  return ''.join(content)

def generate_system_base_spec(spec: dict):
  content = [
    f"Name: $PKG_NAME\n",
    f"Version: $PKG_VERSION\n",
    f"Release: $PKGREVISION\n",
    f"Summary: Base system capabilities import for CMS environment\n",
    f"License:        Public Domain\n",
    f"BuildArch:      noarch\n",
    f"Vendor: CMS, CERN\n"
  ]

  provides = spec.get("provides", set())
  for provide in provides:
    print(f"Provide: {provide}\n")
    content.append(f"Provides: {provide}\n")

  content.append('\n%description\n')
  content.append('Virtual meta-package used by CMS environments to declare the base '
                 'system capabilities assumed to be available on hosts. '
                 'Contains no files and installs no payload.\n')
  content.append('\n%prep\n')
  content.append('%build\n')
  content.append('\n%install\n')
  content.append('%files\n')

  return ''.join(content)