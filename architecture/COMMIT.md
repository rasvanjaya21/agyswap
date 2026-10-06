# Commit

Ditulis lewat `/agyswap-commit` pada 2026-10-06. Isinya aturan dari user bahwa agent tidak pernah menjalankan `git push` (termasuk tag dan force), `restore`, `reset`, `checkout -- <path>`, `clean`, `revert`, `rebase`, dan sejenisnya. User yang menjalankannya sendiri, dan agent cukup menuliskan perintahnya. Commit dipecah per scope, tanpa trailer co-author atau atribusi, dan **tidak di-push** (push dilakukan user).

## Commit yang dibuat

| Hash | Pesan | File |
| ---- | ----- | ---- |
| `c2ff87c` | `feat(skill): forbid agent push and restore in commit and ship skills` | `skills/agyswap-commit/SKILL.md`, `skills/agyswap-ship/SKILL.md` |
| `6159357` | `docs(agents): add rule against agent push, restore and history rewrites` | `AGENTS.md` |
| (commit ini) | `docs(architecture): update commit record` | `architecture/COMMIT.md` |

## Alasan pengelompokan

- Skill commit dan skill ship digabung dalam satu commit `skill`, karena keduanya mengubah aturan yang sama: push, tag, dan rilis dijalankan oleh user.
- `AGENTS.md` dipisah ke scope `agents`, karena aturan di sana berlaku untuk semua agent dan menang atas teks skill.

## File yang sengaja tidak di-commit

Tidak ada. Working tree bersih setelah commit ini.

## Hook

Tidak ada git hook. Semua commit dibuat tanpa `--no-verify`.
