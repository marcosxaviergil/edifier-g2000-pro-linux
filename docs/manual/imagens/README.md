# Imagens do manual

O manual (`scripts/build_manual.py`) procura cada imagem pelo nome, nesta ordem:

1. `docs/manual/imagens/<idioma>/<nome>` (captura de tela de um idioma, por exemplo `ja/configuracoes_som_saida.jpg`);
2. `docs/manual/imagens/<nome>` (a mesma imagem para todos os idiomas).

Se não achar, o PDF mostra uma caixa com `<nome>` no lugar, e o build lista no log as imagens que faltam.
Para substituir, coloque o arquivo com o mesmo nome aqui e gere o manual de novo (ou publique uma nova versão).

Imagens usadas hoje:

| Nome | O que mostrar |
| --- | --- |
| `configuracoes_som_saida.jpg` | Configurações → Som → Saída, com a HECATE G2000 PRO escolhida |
| `controle_volume_gnome.jpg` | Barra de volume do sistema (Configurações rápidas do GNOME) com a HECATE G2000 PRO |
| `terminal_status.jpg` | Terminal com `hecate-g2000-pro-volume status` terminando em `Result: OK` |
| `terminal_diagnose.jpg` | Terminal com `hecate-g2000-pro-volume diagnose` e as três linhas `PASS` |

Formatos aceitos: `.jpg`, `.jpeg` e `.png`; o nome só pode ter letras, números, `_`, `.` e `-`.
