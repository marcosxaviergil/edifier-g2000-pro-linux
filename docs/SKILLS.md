# Skills aplicadas (versão 1.0.0)

As 34 referências do catálogo de skills do projeto foram consultadas em 02/11/2026: cada repositório foi
clonado (clone raso) no commit indicado e o `SKILL.md` (ou agente/plugin) foi lido nas seções de regras.
**Nenhum script das skills foi executado**: aplicamos as regras. A consulta de uma skill não significa que
ela foi instalada. As skills de interface web não se aplicam (o projeto não tem interface web) e estão
marcadas como tal. A ordem da categoria X foi mantida e o ponytail veio por último, como pede o catálogo.

## I. Pesquisa técnica e evidências

| # | Skill @ commit | Regra aplicada | Onde |
| --- | --- | --- | --- |
| 1 | dashhuang/deep-research-skill @ `c6d58926` | investigar antes de implementar quando há comparação de alternativas | comparação extensão GNOME × .deb × serviço × configuração ([ARCHITECTURE.md](ARCHITECTURE.md), "Alternativas descartadas") |
| 2 | magnus919/agent-skills `research-methodology` @ `915225c0` | fontes primárias; separar fato de hipótese; registrar o que não foi comprovado | código-fonte do PipeWire 1.4.2 e WirePlumber 0.5.8 em vez de fóruns ([SOURCES.md](SOURCES.md)); seção "O que não foi testado" ([TESTING.md](TESTING.md)) |
| 3 | LuckyCody/audit-skill @ `4e6fdb56` | confrontar afirmação com evidência (`claims`); evidência em arquivo:linha | hipóteses corrigidas por teste (o perfil IEC958 só software; o mudo existe em hardware; `element-output` derruba o WirePlumber) |

## II. Arquitetura

| # | Skill @ commit | Regra aplicada | Onde |
| --- | --- | --- | --- |
| 4 | magnus919 `software-architecture-analysis` @ `915225c0` | mapear entradas, dados e pontos de extensão do sistema existente pelo código | caminho volume → WirePlumber → ACP → ALSA lido em `acp.c`, `alsa-mixer.c`, `state-profile.lua`, `module-mixer-api.c` |
| 5 | magnus919 `software-architecture` @ `915225c0` | registrar a decisão e as alternativas rejeitadas; qualidades como cenários verificáveis | [ARCHITECTURE.md](ARCHITECTURE.md): requisito → cenário (`softVolumes` 1,0 e PCM acompanha) → decisão |
| 6 | mattpocock/skills `codebase-design` @ `4ae2317d` | "Accept dependencies, don't create them"; teste da exclusão; "One adapter means a hypothetical seam" | `Audio(run)` recebe quem executa os comandos (testes com saídas gravadas); `configuration()` removido por só repassar; nenhuma interface com uma implementação só |

## III. APIs e integração

| # | Skill @ commit | Regra aplicada | Onde |
| --- | --- | --- | --- |
| 7 | magnus919 `api-design-and-evolution` @ `915225c0` | contrato explícito com o consumidor; compatibilidade | contrato com o PipeWire = propriedades documentadas (`device.profile-set`, IDs USB), nada interno; WirePlumber 0.4 declarado fora do contrato |
| 8 | magnus919 `backend-engineering` @ `915225c0` | "Design for failure"; tratar erro onde há contexto | tempo-limite em todo comando (o `wpctl` travou sem WirePlumber no teste real); `diagnose` restaura volume e mudo num `finally` |

## IV. Código

| # | Skill @ commit | Regra aplicada | Onde |
| --- | --- | --- | --- |
| 9 | wshobson/agents `python-development` (python-packaging, python-testing-patterns) @ `7e2fb559` | layout `src/`; metadados em `pyproject.toml`; testes AAA | `src/hecate_volume`; versão única conferida por teste; testes organizados por comportamento |
| 10 | wondelai/skills `clean-code` @ `d8d5d75f` | nomes que revelam intenção; predicados como predicados; guard clauses | `is_installed`, `is_unity`, `volumes_below` (era `test_volumes`); `find_speaker` devolve `None` cedo |
| 11 | addyosmani/agent-skills `code-simplification` @ `301b02b1` | preservar comportamento; um passo por vez com testes | cada simplificação rodou a suíte inteira; validações mantidas |

## V. Segurança

| # | Skill @ commit | Regra aplicada | Onde |
| --- | --- | --- | --- |
| 12 | magnus919 `secure-software-engineering` @ `915225c0` | ativos e fronteiras de confiança; saídas de ferramentas são entrada não confiável | saídas de `wpctl`/`pw-cli`/`amixer` validadas por regex antes do uso; mensagem clara quando não batem |
| 13 | trailofbits/skills `sharp-edges` @ `d016e08c` | o caminho seguro é o padrão; valores vazios não passam em checagens | `install`/`uninstall` não sobrescrevem nem apagam arquivo alheio sem `--force`; `is_installed` com lista vazia não é "instalado" (erro real achado por teste); `XDG_CONFIG_HOME` vazio/relativo ignorado |
| 14 | trailofbits `insecure-defaults` @ `d016e08c` | fail-open, segredos de fallback, permissões | release recusa HTTP sem TLS (só loopback nos testes); token só do job, nunca impresso; arquivos 0644/diretórios 0755, dono root no .deb |
| 15 | getsentry/skills `security-review` @ `d12f2504` | só achados com entrada controlada por atacante | sem achado: não há entrada remota; o comando roda com o usuário e só lê o áudio local |
| 16 | agamm/claude-code-owasp `owasp-security` @ `8ac7965c` | ASVS 5.0 (sem misturar com 4.0): segredos fora de log e de linha de comando; dependências | nenhuma dependência de terceiros; token só em variável de ambiente do passo |
| 17 | openai/skills `security-best-practices` @ `49f948fa` | Python: `subprocess` com lista, sem `shell=True` | `run_command` (testado: sem shell, com `LC_ALL=C` e tempo-limite); ruff `S` (bandit) no lint |

## VI. Privacidade e LGPD

| # | Skill @ commit | Regra aplicada | Onde |
| --- | --- | --- | --- |
| 18 | goul4rt/lgpd-skills `lgpd-audit` @ `d85d79ab` | inventário de tratamentos; citar a norma | inventário em [PRIVACIDADE.md](PRIVACIDADE.md): só estado do áudio local, nada gravado nem enviado |
| 19 | github/awesome-copilot `gdpr-compliant` @ `61fa1fa8` | "Collect less. Store less. Expose less." | nada coletado; testes com dados fictícios além das linhas reais da caixa |
| 20 | DanielSunami/gerador-lgpd @ `c7f4cd73` | sempre os dois documentos; autores que não recebem dados não são controlador nem operador; sem garantia | [PRIVACIDADE.md](PRIVACIDADE.md) e [TERMOS.md](TERMOS.md) |

## VII. Usabilidade e UX Writing

| # | Skill @ commit | Regra aplicada | Onde |
| --- | --- | --- | --- |
| 21 | vercel-labs/agent-skills `web-design-guidelines` @ `1a2c79d4` | não se aplica: não há interface web | — |
| 22 | addyosmani/web-quality-skills `accessibility` @ `afa8da94` | não se aplica a interface web; no PDF, placeholder com `role="img"` e `aria-label`, como no projeto de referência | `scripts/build_manual.py` |
| 23 | content-designer/ux-writing-skill @ `98cacde4` | conciso, claro, terminologia consistente; o que falhou + o que fazer | mensagens `Problem:`/`Error:` sempre com o próximo comando |

## VIII. Processo e testes

| # | Skill @ commit | Regra aplicada | Onde |
| --- | --- | --- | --- |
| 24 | obra/superpowers `using-superpowers` @ `2ce8aa15` | planejar antes de agir; verificar antes de declarar pronto | lista de tarefas; `make check` antes do ZIP |
| 25 | addyosmani/agent-skills `test-driven-development` @ `301b02b1` | RED → GREEN; Prove-It para bug; testes pequenos/médios | testes do `pipewire.py` escritos e rodados falhando antes do código; bug de `is_installed` achado por teste; fixtures com saídas reais |
| 26 | magnus919 `verification-methodology` @ `915225c0` | critérios observáveis; evidência direta; não transformar falta de evidência em PASS | critérios do teste real (PCM acompanha, `softVolumes` 1,0, mudo no hardware); "não testado" explícito |
| 27 | anthropics/skills `webapp-testing` @ `ca45fc49` | não se aplica: não há aplicação web | — |

## IX. Documentação do projeto

| # | Skill @ commit | Regra aplicada | Onde |
| --- | --- | --- | --- |
| 28 | softaworks/agent-toolkit `crafting-effective-readmes` @ `3027f20f` | "Who will read this"; nome, descrição, uso; conferir com o estado real | README da raiz em 9 idiomas, no formato do projeto modelo (código-fonte: estrutura, comandos, documentação, licença); manual (usuário, 9 idiomas) |

## X. Documentação e comentários do código (nesta ordem)

| # | Skill @ commit | Regra aplicada | Onde |
| --- | --- | --- | --- |
| 29 | TerminalSkills/skills `code-documenter` @ `8a9852d4` | documentar propósito, retorno, efeitos colaterais e erros; o porquê | docstrings de `files.py`, `pipewire.py`, `cli.py` (ex.: `install_user` diz quando levanta `InstallError`) |
| 30 | 26zl/universal-agent-skills `coding-style` @ `97230443` | código e comentários em inglês; sem narrar o histórico; comentário só para intenção não óbvia | código em inglês; documentação do projeto em pt-BR (idioma do repositório) |
| 31 | Jeffallan/claude-skills `code-documenter` @ `078a25cc` | validar exemplos | todo comando citado nos manuais existe (`test_manual.py`); `--help` conferido |
| 32 | anthropics/claude-plugins-official `comment-analyzer` @ `a7ba5b93` | conferir cada comentário com o código | ex.: comentário do tempo-limite conferido com o travamento real do `wpctl`; docstrings de `install_user`/`uninstall_user` corrigidas (diziam "mantido", o código levanta erro) |
| 33 | TrimVis/skills `comment-cleanup` @ `4e8bb9f6` | teste da exclusão; remover banners e docstrings que repetem o código; só comentários mudam | banner "Parsers" e docstring do `__main__.py` removidos |

## XI. Auditoria final

| # | Skill @ commit | Regra aplicada | Onde |
| --- | --- | --- | --- |
| 34 | DietrichGebert/ponytail `ponytail-audit` @ `96608e07` | repositório inteiro; achado só com caso concreto; correto, seguro, testado, enxuto | [AUDIT.md](AUDIT.md) |
