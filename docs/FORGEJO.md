# Forgejo: CI e releases

## O que o workflow faz

`.forgejo/workflows/build.yaml` roda **só** num push de **tag de versão** (`v1.0.0`); push em branch e
pull request não disparam nada. Na imagem `node:22-bookworm-slim` (a action de checkout precisa de
Node.js no container), ele instala as ferramentas, confere (`make tools`), faz lint, roda os testes,
gera o `.deb` e o `.tar.gz` e confere o `.deb` com lintian (`make build`), gera o manual em PDF dos 9
idiomas, confere o comando do tarball e publica a **release** dessa versão com três anexos:

- `hecate-g2000-pro-volume_<versão>_all.deb`
- `hecate-g2000-pro-volume-<versão>.tar.gz`
- `Hecate-G2000-PRO-Volume-<versão>-Manual.pdf`

As notas são a seção da versão no `CHANGELOG.md` mais o SHA-256 de cada anexo. Tag da mesma versão de
novo: a release anterior e os anexos dela são apagados e só o build mais novo fica. Se a tag foi movida
para outro commit enquanto o job rodava, nada é publicado (`BUILD_COMMIT`). Nenhum segredo é necessário:
a etapa usa o token automático do job. A tag precisa ser `v` + a versão de
`src/hecate_volume/__init__.py`; senão, a etapa falha antes de qualquer pedido. O endereço do servidor
precisa ser `https`.

Requisito do runner: label `docker` (troque só o `runs-on` se o seu usa outro).

## Primeiro envio (a partir do ZIP)

O ZIP contém a pasta `hecate-g2000-pro-volume/` com o repositório git (branch `main`, um commit, tag
`v1.0.0`). Crie o repositório vazio no Forgejo (sem README) e:

```sh
cd ~/Downloads
unzip hecate-g2000-pro-volume-1.0.0.zip
cd hecate-g2000-pro-volume
git remote add origin <URL do repositório no Forgejo>
git push -u origin main
git push origin v1.0.0
```

O push da tag dispara o workflow; acompanhe em **Actions**.

## Nova versão, dia a dia

```sh
git commit -am 'Hecate G2000 PRO Volume 1.0.1'
git tag -a v1.0.1 -m 'Hecate G2000 PRO Volume 1.0.1'
git push origin main v1.0.1
```

Refazer o build da mesma versão (substitui a release):

```sh
git tag -fa v1.0.1 -m 'Hecate G2000 PRO Volume 1.0.1'
git push --force origin v1.0.1
```

Com os dois remotos no mesmo clone (`origin` no Forgejo e `github` no GitHub), envie a tag para cada
um: cada forja publica a sua release. Veja [GITHUB.md](GITHUB.md).
