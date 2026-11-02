# Auditoria do repositório (ponytail-audit, versão 1.0.0)

Feita por último, no repositório inteiro, segundo `DietrichGebert/ponytail` `skills/ponytail-audit` @
`96608e07`. Os achados de "Must fix" e "Should fix" foram corrigidos e testados antes da entrega.

**O que o repositório faz:** instala dois arquivos de configuração que fazem o PipeWire e o WirePlumber
usarem o controle de volume em hardware da Edifier Hecate G2000 PRO, e oferece um comando para conferir
e testar isso. Carga assumida: uma pessoa, no próprio computador, rodando comandos à mão.

## Must fix (corrigidos)

1. **O `diagnose` tocava mais alto do que antes** (`src/hecate_volume/cli.py`, `volumes_below`)
   - **O que é:** o teste escolhe três volumes abaixo do atual.
   - **Problema:** com o volume em 0, ele usava 0,03, 0,02 e 0,01: acima do atual, contra o que o manual
     promete.
   - **Correção:** abaixo de 4% o teste não roda e pede para aumentar o volume; nada é alterado.
     Teste: `test_too_low_volume_is_not_tested_and_nothing_changes`.
   - **Se ficasse:** um teste com o volume no zero faria som de repente.

2. **"Instalado" sem nenhum arquivo** (`cli.py`, `is_installed`)
   - **O que é:** decide se a configuração está instalada em algum escopo.
   - **Problema:** com só os arquivos do sistema na lista, o escopo "user" ficava vazio e `all([])` é
     verdadeiro: o `install` dizia "já instalado pelo pacote" sem pacote nenhum.
   - **Correção:** lista vazia não conta. Achado pelos testes do `install`.

## Should fix (corrigidos)

3. **Leitura duplicada do `pyproject.toml`** (`scripts/build.py`): duas funções liam a mesma tabela;
   agora uma só (`debian_fields`).
4. **Função que só repassava** (`cli.py`, `configuration`): removida.
5. **Docstrings que contradiziam o código** (`files.py`, `install_user`/`uninstall_user`): diziam que o
   arquivo alheio "é mantido"; o código levanta `InstallError` antes de mexer em qualquer arquivo.
   Corrigidas.

## Conferido e mantido de propósito

- Os arquivos de configuração existem duas vezes no .deb (no código do comando e nas pastas do sistema):
  o comando compara o que está instalado com a sua própria cópia. São 1,7 kB.
- `wpctl inspect` em cada dispositivo e saída para achar a caixa: poucos objetos; evita depender de nome
  ou número de placa, que mudam entre máquinas.
- Tempo-limite de 10 s por comando e espera de até 3 s por volume: o `wpctl` trava sem WirePlumber
  (visto no teste real).

**Verdict:** saudável depois das correções; 61 testes passando em Python 3.11, 3.12 e 3.13; lintian sem
achados.

**Lean:** uma função de repasse e uma leitura duplicada removidas; nenhuma dependência de terceiros para cortar.

**Not checked:** comportamento com versões do PipeWire/WirePlumber diferentes de 1.4.2/0.5.8; instalação
do .deb na máquina real (só o conteúdo e o lintian foram conferidos aqui); os workflows não rodaram num
runner real (conferidos por `tests/test_ci.py` e pelos mesmos comandos rodados localmente).
