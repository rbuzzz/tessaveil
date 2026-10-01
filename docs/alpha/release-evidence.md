# Windows v1 candidate evidence — exact-byte fail-closed gate

Unsigned synthetic candidate only. Not RC/stable. No Authenticode, real funds,
final format/KDF freeze, migration promise, tag, GitHub Release, installer, or
update channel. Verdict: **NO-GO для реальных данных**.

Security audit: not yet independently completed

[English](#english) · [Русский](#русский)

## English

### Current candidate contract

The source-controlled decision in
[`reports/windows-v1/release-decision.json`](../../reports/windows-v1/release-decision.json)
has 29 mandatory rows. At the Task 7 review point it recorded 4 engineering
passes and 25 blocked rows. It is a policy template and deliberately contains no
source SHA or artifact hash. Packaging materializes a copy for one clean exact
source SHA and binds that copy to runtime ZIP, compliance ZIP, and the inner EXE.
Missing evidence remains `blocked`; a predecessor build, PR run, local host, VM,
simulator, or Windows Server runner never transfers evidence to another row/SHA.

The exact hosted container name is:

`Tessaveil-unsigned-synthetic-windows-v1-candidate-<source-sha>`

It must contain exactly these externally verified subjects:

| Role | Exact filename suffix | Required binding |
| --- | --- | --- |
| Runtime | `-runtime.zip` | EXE, SBOM, notices, bilingual guidance, internal `SHA256SUMS`, source SHA and runtime observations |
| Compliance | `-compliance.zip` | full Qt source/relink material, application objects, build receipt, license/source inventory, decision template, test protocols and threat/limitations guidance |
| Decision | `-release-decision.json` | exact source SHA plus runtime/compliance/EXE SHA-256 and all 29 gate dispositions |
| External manifest | `-manifest.json` | filenames, byte sizes and SHA-256 for both ZIPs, EXE, decision, SBOM and notices |

`GATE-PASS.json` is local/CI control output, not an uploaded release subject. It
is written only after `verify.py --distribution` validates exact archive bytes,
decision, external manifest, license/source bindings, SBOM, PE imports,
observations, modified-Qt relink proof, and adversarial archive mutations.
A technical PASS leaves `real_data_authorized=false` and the NO-GO verdict.

### Exact-SHA sequence

1. Finish every tracked documentation and packaging-source change.
2. Commit once and require an exact clean `HEAD`; later tracked edits invalidate
   the candidate.
3. Build pinned Rust 1.90.0, LLVM-MinGW 20250709 / Clang 20.1.8, QtBase 6.8.3,
   CMake 3.31.8, Ninja 1.12.1, and Python 3.12.10 inputs.
4. Run Rust formatting/clippy/tests/doctests, all discovered Python tests,
   catalogue/schema/generated/notices/sensitive/history gates, native synthetic
   UI, package audit, actual modified-Qt rebuild/relink, and relinked UI smoke.
5. Materialize the four conspicuously named files, independently verify them,
   then upload only after the same-run receipt matches every name and hash.
6. The separate least-privilege provenance job re-verifies downloaded bytes,
   attests all four subjects, and runs strict `gh attestation verify` with exact
   repository, signer workflow, source digest/ref, JSON output, and self-hosted
   runners denied.

The local development desktop may fail before packaging if the candidate-owned
dialog cannot retain foreground. Task 7 repeatedly observed the Windows system
`LockApp` owning the secure foreground; the gate stopped before staging and no
ZIP/decision/manifest/PASS was claimed. Do not bypass or special-case that
condition. Hosted CI or a later unlocked interactive desktop must satisfy the
same observer.

### Mandatory blockers

The machine-readable decision is authoritative. Principal unresolved work is:

- resolve release-blocking catalogue rows and complete sustained sanitizer fuzz;
- run format/KDF/open/normalization measurements on two physical Android classes,
  two physical iPhone classes, and a provenance-recorded Mac/Xcode host;
- approve exact Figma fonts or the documented substitution;
- run exact unsigned bytes offline/non-admin on clean Windows 10 22H2 and 11;
- test pre-identified removable NTFS/exFAT and separately authorized controlled
  power loss without formatting or mutating an unidentified device;
- capture packet, TEMP, process/file/startup-log, Narrator, keyboard, and real
  display-scaling evidence;
- complete independent security audit and SignPath/Authenticode path;
- materialize/download/re-hash the final exact-SHA package, SBOM/relink proof,
  branch/PR CI, manifest, and strict provenance receipts;
- prove final bilingual documentation/threat/limitations parity on those exact
  bytes.

Each action and pass/fail criterion is specified in
[`reports/windows-v1/test-protocols.md`](../../reports/windows-v1/test-protocols.md).
No physical-device, removable-media, independent-audit, signing, or exact hosted
result is claimed by this source document.

### Historical evidence

Older artifacts and workflow runs are historical diagnostics only. They are
intentionally omitted from the normative candidate ledger because their SHA,
package content, release decision, and manifest do not match the current source.
They may not satisfy any current decision row.

## Русский

### Контракт текущего кандидата

Версионируемое решение
[`reports/windows-v1/release-decision.json`](../../reports/windows-v1/release-decision.json)
содержит 29 обязательных строк. На проверенном этапе Task 7 было 4 инженерных
`pass` и 25 `blocked`. Это шаблон политики без source SHA и хешей артефактов.
Упаковка материализует его для одного чистого точного SHA и связывает с runtime,
compliance и EXE. Отсутствующее доказательство остаётся `blocked`; старый билд,
PR-run, рабочий компьютер, VM, симулятор и Windows Server не передают результат
другой строке или SHA.

Контейнер имеет имя
`Tessaveil-unsigned-synthetic-windows-v1-candidate-<source-sha>` и содержит
четыре проверяемых файла: `-runtime.zip`, `-compliance.zip`,
`-release-decision.json` и `-manifest.json`. Внешний манифест связывает имена,
размеры и SHA-256 обоих ZIP, EXE, решения, SBOM и уведомлений. Compliance включает
полный исходный Qt/relink material, объекты приложения, build receipt, лицензии,
операторские протоколы, модель угроз и ограничения. Технический PASS оставляет
`real_data_authorized=false` и **NO-GO для реальных данных**.

Сначала завершаются все tracked-изменения и создаётся единственный commit. Затем
чистый точный HEAD без новых tracked-правок проходит полный build/test/package,
независимый `verify.py --distribution`, загрузку четырёх файлов, повторную
проверку downloaded bytes и строгий GitHub provenance с точными repository,
workflow, source digest/ref и запретом self-hosted runner.

На рабочем компьютере Task 7 системный `LockApp` удерживал secure foreground.
Gate честно остановился до staging; ZIP, решение, манифест и PASS не заявлялись.
Ослаблять observer или делать исключение для LockApp нельзя.

### Что остаётся закрыть

Авторитетный перечень находится в machine-readable решении. Основные действия:
закрыть блокирующие записи каталога и sanitizer fuzz; выполнить физические
Android/iPhone и Mac/Xcode измерения; решить точные шрифты Figma; проверить чистые
Windows 10/11; испытать заранее указанные съёмные NTFS/exFAT и отдельно
разрешённую потерю питания; собрать network/TEMP/process/file/log/Narrator/scale
evidence; пройти независимый аудит и SignPath/Authenticode; затем проверить
точные hosted SHA, архивы, SBOM/relink, CI, манифест, provenance и двуязычную
документацию. Нельзя форматировать или разрушительно изменять неуказанный носитель.

Команды, receipts и критерии описаны в
[`reports/windows-v1/test-protocols.md`](../../reports/windows-v1/test-protocols.md).
Этот документ не заявляет физические, audit, signing или hosted результаты.
Старые артефакты — только историческая диагностика и не закрывают текущие строки.
