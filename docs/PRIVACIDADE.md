# Privacidade

Este documento descreve o que o software faz com dados. Não é parecer jurídico.

## O que o software trata

| Dado | Onde | Para quê |
| --- | --- | --- |
| Estado do áudio (dispositivos, volume, perfil, controles ALSA) | lido na hora com `wpctl`, `pw-cli` e `amixer`; não é gravado | mostrar no `status` e testar no `diagnose` |
| Dois arquivos de configuração | `~/.config/...` (instalação por usuário) ou `/usr/share/...` (pacote) | fazer o PipeWire usar o controle de volume da caixa |

O número de série da caixa aparece na saída do `status` (no nome da saída do PipeWire), só na tela de
quem roda o comando.

## O que o software não faz

- Não coleta, não grava e não envia dados pessoais.
- Não acessa a rede.
- Não tem telemetria, conta, login nem cookies.

## Papéis (LGPD)

Os autores não recebem nenhum dado de quem usa o software, então não são controladores nem operadores
(LGPD, art. 5º, VI e VII). Quem usa o software no próprio computador decide sobre os próprios dados.

## Contato

Dúvidas: abra uma issue no repositório do projeto.
