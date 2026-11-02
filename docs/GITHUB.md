# GitHub: CI e releases

## O que o workflow faz

`.github/workflows/build.yaml` é o mesmo pipeline de `.forgejo/workflows/build.yaml` (veja
[FORGEJO.md](FORGEJO.md)): roda **só** num push de **tag de versão**, na mesma imagem, com os mesmos
passos. Só mudam dois:

- **Checkout:** `actions/checkout` do GitHub, fixado por SHA (v6.1.0), sem credencial persistida.
- **Release:** `scripts/github_release.py`. Apaga a release (ou o rascunho deixado por uma execução que
  falhou) da mesma tag, cria um **rascunho** com as notas do `CHANGELOG.md` e o SHA-256 dos anexos,
  anexa o `.deb`, o `.tar.gz` e o manual em PDF e só então **publica**. A tag git fica. Se a tag foi
  movida para outro commit enquanto o job rodava, não publica nada (`BUILD_COMMIT`).

`tests/test_ci.py` falha se os passos dos dois workflows deixarem de ser iguais (exceto checkout e
release) ou se uma action não estiver fixada por SHA.

Os dois workflows convivem no mesmo repositório: o Forgejo só lê `.github/workflows` quando **não
existe** `.forgejo/workflows`, e o GitHub só lê `.github/workflows`. Cada forja roda o seu.

## Permissões e segredos

- Nenhum segredo para criar. A etapa da release usa o `GITHUB_TOKEN` do job, entregue só a ela, com
  `permissions: contents: write`; o resto do workflow fica com `permissions: {}`.
- Execuções da mesma tag esperam umas pelas outras (`concurrency`), sem cancelar.

## Releases imutáveis

Com **immutable releases** ligado, o GitHub não aceita anexos depois de publicar: por isso os arquivos
entram no rascunho e a publicação é o último passo. Depois de publicada, refazer a mesma versão falha:
suba a versão.

## Enviar ao GitHub por HTTPS

O push leva `.github/workflows/build.yaml`, e o GitHub recusa um token pessoal sem permissão de
workflow. Token clássico: escopos `repo` (ou `public_repo`) e `workflow`. Token fine-grained: neste
repositório, **Contents** e **Workflows** em *Read and write*.

## Primeiro envio (no mesmo clone do Forgejo)

Crie o repositório vazio no GitHub (sem README) e:

```sh
cd ~/Downloads/hecate-g2000-pro-volume
git remote add github <URL do repositório no GitHub>
git push -u github main
git push github v1.0.0
```

## Nova versão

```sh
git push origin main v1.0.1
git push github main v1.0.1
```
