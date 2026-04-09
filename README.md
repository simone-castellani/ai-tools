# AI Skills Collection

Questo repository raccoglie una selezione di agent skill riutilizzabili in altri progetti, compatibili con OpenCode, Claude Code e con il formato standard [Agent Skills](https://agentskills.io).

Ogni skill vive in `skills/<nome-skill>/` e contiene almeno un file `SKILL.md`.

## Skill disponibili

| Skill | Descrizione |
|---|---|
| `c4-architecture` | Genera documentazione architetturale con diagrammi C4 in Mermaid. |
| `code-review` | Esegue code review strutturate e actionable su file modificati o pull request. |
| `commit-work` | Aiuta a preparare commit Git puliti, ben separati e con messaggi Conventional Commits. |
| `difficult-workplace-conversations` | Fornisce un framework per gestire conversazioni difficili sul lavoro. |
| `doc-coauthoring` | Guida la scrittura collaborativa di documentazione, RFC, proposal e technical spec. |
| `docx` | Crea, legge, modifica e converte documenti Word `.docx`. |
| `explain-code` | Spiega codice e codebase in modo chiaro, adattando profondita e linguaggio al lettore. |
| `humanizer` | Riscrive testi per renderli meno artificiali e piu naturali. |
| `msg-to-md` | Converte email Outlook `.msg` in Markdown con metadata e allegati. |
| `pptx` | Crea, legge e modifica presentazioni PowerPoint `.pptx`. |
| `skill-creator` | Aiuta a creare, migliorare e valutare nuove skill. |
| `writing-clearly-and-concisely` | Migliora testi tecnici e non tecnici rendendoli piu chiari e concisi. |

## Installazione con npx

Il metodo consigliato per installare queste skill e usare [`npx skills`](https://www.npmjs.com/package/skills), cosi puoi installarle direttamente dal repository senza clonarlo manualmente.

Per vedere prima l'elenco delle skill disponibili:

```bash
npx skills add simone-castellani/ai-tools --list
```

### Installare tutte le skill

```bash
# Claude Code, livello progetto
npx skills add simone-castellani/ai-tools --skill '*' -a claude-code

# Claude Code, livello utente
npx skills add simone-castellani/ai-tools --skill '*' -a claude-code -g

# OpenCode, livello progetto
npx skills add simone-castellani/ai-tools --skill '*' -a opencode

# OpenCode, livello utente
npx skills add simone-castellani/ai-tools --skill '*' -a opencode -g

# Entrambi gli agent
npx skills add simone-castellani/ai-tools --skill '*' -a claude-code -a opencode
```

Installazione non interattiva:

```bash
npx skills add simone-castellani/ai-tools --skill '*' -a claude-code -a opencode -y
```

### Installare una skill specifica

Per installare una sola skill usa `--skill <nome-skill>`. I nomi validi corrispondono alle directory sotto `skills/`.

```bash
# Una skill specifica per Claude Code
npx skills add simone-castellani/ai-tools --skill code-review -a claude-code

# Una skill specifica per OpenCode
npx skills add simone-castellani/ai-tools --skill docx -a opencode

# Una skill specifica a livello utente
npx skills add simone-castellani/ai-tools --skill humanizer -a claude-code -g

# La stessa skill su piu agent
npx skills add simone-castellani/ai-tools --skill writing-clearly-and-concisely -a claude-code -a opencode
```

## Installazione manuale

Se preferisci mantenere una copia locale del repository e usare link simbolici, puoi installare manualmente una skill puntando alla relativa directory.

### Claude Code

Installazione per utente:

```bash
mkdir -p ~/.claude/skills
ln -s "$(pwd)/skills/<nome-skill>" ~/.claude/skills/<nome-skill>
```

Installazione per progetto:

```bash
mkdir -p .claude/skills
ln -s "$(pwd)/skills/<nome-skill>" .claude/skills/<nome-skill>
```

### OpenCode

Installazione per utente:

```bash
mkdir -p ~/.config/opencode/skills
ln -s "$(pwd)/skills/<nome-skill>" ~/.config/opencode/skills/<nome-skill>
```

Installazione per progetto:

```bash
mkdir -p .agents/skills
ln -s "$(pwd)/skills/<nome-skill>" .agents/skills/<nome-skill>
```

## Aggiornamento

Se usi `npx skills`, puoi controllare e applicare aggiornamenti con:

```bash
npx skills check
npx skills update
```

Se usi link simbolici verso un clone locale del repository, gli aggiornamenti vengono recepiti automaticamente dopo un `git pull`.

## Aggiungere una nuova skill

1. Crea una nuova directory sotto `skills/`.
2. Aggiungi un file `SKILL.md`.
3. Inserisci nel file il frontmatter YAML con almeno `name` e `description`.

Esempio minimo:

```md
---
name: my-skill
description: Quando e perche usare questa skill.
---

Istruzioni della skill.
```

## Struttura del repository

```text
skills/
  <nome-skill>/
    SKILL.md
    README.md
    references/
    scripts/
    assets/
```

## Risorse

- [Agent Skills Specification](https://agentskills.io)
- [skills](https://www.npmjs.com/package/skills)
- [OpenCode Skills Documentation](https://opencode.ai/docs/skills)
- [Claude Code Skills Documentation](https://code.claude.com/docs/en/skills)

## Licenza

MIT
