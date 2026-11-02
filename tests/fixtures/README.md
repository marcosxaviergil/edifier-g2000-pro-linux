# Saídas de comando usadas nos testes

Copiadas dos testes na máquina de referência (Debian 13, PipeWire 1.4.2, WirePlumber 0.5.8,
02/11/2026; veja o relatório no projeto). As linhas da Edifier Hecate G2000 PRO são as reais.

- `wpctl_inspect_node.txt`, `wpctl_inspect_device.txt`, `pw_cli_profile.txt`, `amixer_volume.txt`:
  saída real, sem mudanças.
- `pw_cli_props.txt`: saída real (fase A2 do teste completo), com vírgula decimal (`LANG=pt_BR`).
- `wpctl_status.txt`: estrutura e linhas da G2000 PRO como na saída real de `wpctl status`;
  os outros dispositivos têm nomes fictícios e o nome de usuário foi trocado por `user@host`.
