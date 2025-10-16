def generate_spec(spec: dict) -> str:
    """
    Generate a shell script that produces an RPM SPEC file.
    Args:
        spec (dict): A dictionary containing metadata and build parameters
            for the RPM package.
    Returns:
        str: A shell script string that, when executed, writes out the
            corresponding RPM SPEC file.
    """
    package = "cms_" + spec.get("package", "") + "_" + spec.get("version", "") + "_" + spec.get("revision", "") + "_" + spec.get("hash", "")
    summary = spec.get("summary", "CMS external package")
    license_ = spec.get("license", "Proprietary")
    return f"""#!/bin/bash
cat > "$BUILDDIR/{package}.spec" <<SPECEOF
Name: {package}
Version: ${{PKG_VERSION}}
Release: ${{PKGREVISION}}
Summary: {summary}
License: {license_}
Packager: CMS <hn-cms-sw-develtools@cern.ch>
BuildArch: $(uname -m)
Prefix: ${{BITS_WORK_DIR}}/${{ARCHITECTURE}}
BuildRoot: ${{BUILDDIR}}/buildroot
SPECEOF

# Generate Requires dynamically
for pkg in ${{FULL_REQUIRES}}; do
    # Skip if pkg starts with DEFAULTS
    [[ "${{pkg}}" == DEFAULTS* ]] && continue
    pkg_sanitized=$(echo "${{pkg}}" | tr '-' '_')
    upper=$(echo "${{pkg_sanitized}}" | tr '[:lower:]' '[:upper:]')
    version_var="${{upper}}_VERSION"
    revision_var="${{upper}}_REVISION"
    hash_var="${{upper}}_HASH"
    echo "Requires: cms_${{pkg}}_${{!version_var}}_${{!revision_var}}_${{!hash_var}}" >> "$BUILDDIR/{package}.spec"
done

# Add description and file sections
cat >> "$BUILDDIR/{package}.spec" <<SPECEOF
%description
%install
mkdir -p %{{buildroot}}${{BITS_WORK_DIR}}/${{ARCHITECTURE}}/${{PKGNAME}}
cp -a "${{INSTALLROOT}}/"* %{{buildroot}}${{BITS_WORK_DIR}}/${{ARCHITECTURE}}/${{PKGNAME}}/
%files
%defattr(0755,root,root,0755)
${{BITS_WORK_DIR}}/${{ARCHITECTURE}}/${{PKGNAME}}/*
SPECEOF

# Build the RPM
rpmbuild -bb \\
  --define "_topdir ${{BITS_WORK_DIR}}/rpmbuild" \\
  "$BUILDDIR/{package}.spec"
"""
