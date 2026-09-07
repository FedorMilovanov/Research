# Research — stable current authority entrypoint

> Этот файл — стабильная human-readable точка входа. Машинный SSOT находится в [`data/research-authority-registry-v1.json`](data/research-authority-registry-v1.json).

Текущая корневая stage/navigation authority:

- [`00_RESEARCH_CURRENT_AUTHORITY_2026-08-02.md`](00_RESEARCH_CURRENT_AUTHORITY_2026-08-02.md)

Связанные нормативные владельцы:

- control plane: [`00_RESEARCH_CONTROL_PLANE_AUTHORITY_2026-08-02.md`](00_RESEARCH_CONTROL_PLANE_AUTHORITY_2026-08-02.md);
- evidence policy: [`data/repository-evidence-policy-v2.json`](data/repository-evidence-policy-v2.json);
- public projection: [`data/public-projection-current-2026-08-02.json`](data/public-projection-current-2026-08-02.json);
- artifact custody: [`data/artifact-custody-policy-v2.json`](data/artifact-custody-policy-v2.json).

Не меняйте README/AGENT_RULES на следующий датированный authority-файл. При смене root authority обновляется registry и этот stable entrypoint одной транзакцией; CI проверяет их согласованность.
