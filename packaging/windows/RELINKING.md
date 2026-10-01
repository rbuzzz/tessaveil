# Static Qt relinking material — unsigned synthetic candidate

Unsigned Windows v1 candidate, synthetic data only. Not RC/stable. No
Authenticode, no real funds, no final format/KDF/migration promise. Windows
real-data use and freeze remain NO-GO. This material is not legal assurance.

Original Tessaveil application code remains Apache-2.0. QtBase 6.8.3 is used
under the LGPL-3.0-only route. The source archive is the exact unmodified archive
used for the primary build. Its GPLv3/LGPLv3 texts and all source notices remain
inside it; convenient copies of Qt license texts accompany the objects.

You may modify Qt and reverse-engineer the combined work to debug modifications
to Qt. No Tessaveil term restricts those rights. The application object material
includes its entrypoint, native UI archive, and Rust controller/core archive with
embedded application assets. Qt resources and plugin initializers are regenerated
from the bundled complete Qt source. No test object or vault is needed to relink.

Supply an external ASCII toolchain root containing the exact tools described in
toolchains.json (or suitable compatible tools) and a NEW external ASCII work
directory. From PowerShell in this extracted compliance directory:

```powershell
./relink.ps1 -Bundle $PWD -ToolchainRoot $ToolchainRoot -WorkRoot $NewWorkRoot
```

The script checks the source archive hash, extracts it, builds static Qt with
qt-options.json, and links the unchanged application objects against that Qt.
Generated configuration and path-free feature decisions from the original build
are under qt-generated; the complete build cache is intentionally excluded.
The new EXE is in app/ under
the supplied work directory. For arbitrary Qt edits, extract the source and use
the same documented CMake options and relink CMakeLists.txt directly.

The separate -MarkerExercise mode changes only qVersion() in a fresh extracted
source copy to return a harmless diagnostic version marker, referenced by a
diagnostic in Qt's QApplication initialization to prevent dead stripping. It rebuilds Qt and
relinks the SAME application objects, then runs a marker probe. The release gate
additionally requires a changed EXE digest, marker presence in it, and a real
synthetic application smoke. The primary EXE never uses this modified source.

Replacement/installation: close every running copy and launch your relinked EXE
from an ordinary writable local directory. There is no installer, updater,
signature enforcement, remote activation or Tessaveil key needed to execute a
modified build. Keep the original and modified builds visibly distinct. Local
Windows execution policy/SmartScreen/antivirus may independently intervene; no
bypass of machine policy is supplied or claimed. Use synthetic files only.

The full upstream Qt source necessarily retains upstream tests/examples and
their original licenses; these are corresponding library source, not Tessaveil
test fixtures. No Tessaveil vault, test credential or application test binary is
part of this bundle. Source/object/archive hashes are in SHA256SUMS.

Distribution remains blocked until the conditional engineering review and the
real same-SHA relink/audit evidence close every listed condition. An inventory
generated from upstream metadata alone is not a completed license assessment.
