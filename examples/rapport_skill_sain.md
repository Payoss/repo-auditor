# Audit de tests/fixtures/skill_sain

## Verdict
Le skill est sûr à installer. Il ne contient que deux fichiers texte et ne lance aucun code. Il ne passe par aucun script, aucun réseau et aucun outil pré-approuvé. Il n'y a aucune trace d'injection de prompt.

## Constats
- **`.claude/skills/resume-pdf/SKILL.md:3`** : la description est bien délimitée (« À utiliser quand l'utilisateur demande un résumé de PDF »). Elle n'est pas trop large du type « any task » ou « always ». **INFO**
- **`.claude/skills/resume-pdf/SKILL.md:4`** : `disable-model-invocation: false` est la valeur par défaut. Claude peut donc lancer le skill de lui-même quand la demande correspond. Avec une description aussi étroite, ça ne pose pas de risque. **INFO**
- **`.claude/skills/resume-pdf/SKILL.md:6-7`** : le corps demande seulement de lire le PDF indiqué avec l'outil Read et de le résumer en 10 points, avec les numéros de page. Il n'y a pas de `allowed-tools`, pas de bloc `` !`commande` `` et aucun appel à un script. **INFO**
- **`README.md:1-2`** : simple description, cohérente avec le contenu réel. Aucune instruction ne s'adresse à l'auditeur ou à Claude. **INFO**

À l'usage, les PDF que vous ferez résumer restent eux-mêmes des données non fiables : un PDF piégé pourrait contenir des instructions. C'est un risque général, pas un défaut de ce skill.

## Ce qui a été vérifié
- **Arborescence complète** (`**/*`) : seulement 2 fichiers. Il n'y a pas de dossier `scripts/`, ni de binaire ou de fichier caché inattendu.
- **SKILL.md** : en-tête (name, description, `allowed-tools` absent, `disable-model-invocation`), corps, blocs de commande et appels de script.
- **Configuration Claude Code** : il n'y a pas de `.claude/settings.json` (donc pas de hooks), ni de `.mcp.json`.
- **Installation automatique** : il n'y a pas de `setup.py`, `package.json`, `Makefile` ou script shell.
- **Réseau, secrets et dissimulation** : aucune trace de curl, wget ou fetch, ni d'accès à `.env`, `~/.ssh` ou aux variables d'environnement, ni de base64, eval ou exec.
- **Injection de prompt** : aucune instruction adressée à l'auditeur ou au modèle.

Par ailleurs, les connecteurs claude.ai Gmail, Google Calendar et Google Drive ne sont pas autorisés dans cette session. Pour les activer, il faut passer par les paramètres de connecteurs sur claude.ai. Ils n'ont pas servi à cet audit.

VERDICT: SUR
