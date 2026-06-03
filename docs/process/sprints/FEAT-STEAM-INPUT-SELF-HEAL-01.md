# FEAT-STEAM-INPUT-SELF-HEAL-01 — Persistência do Steam Input OFF

Status: **DONE** (2026-06-03). Parte do guarda-chuva [FEAT-DSX-DEFINITIVE-FIX-01](FEAT-DSX-DEFINITIVE-FIX-01.md).

## Problema
`disable_steam_input.sh --apply` é one-shot (rodado só no install/dsx). A Steam **reescreve**
`localconfig.vdf` ao sair / após updates, podendo re-ativar `SteamController_PSSupport=2`. Sem
reaplicar, o controle volta a ser interceptado pela Steam.

## Solução
Guard systemd `--user` que reaplica PSSupport=OFF sobrevivendo a updates da Steam:

- `assets/hefesto-steam-input-guard.path` — `PathChanged` nos dirs `userdata` da Steam
  (best-effort; writes profundos via rename podem não disparar).
- `assets/hefesto-steam-input-guard.timer` — `OnBootSec=3min`, `OnUnitActiveSec=30min`
  (**rede de segurança real**).
- `assets/hefesto-steam-input-guard.service` — `Type=oneshot`, roda
  `disable_steam_input.sh --apply-quiet`.

### Por que `--apply-quiet` (novo modo)
O `--apply` **fecha e reabre a Steam** se ela estiver rodando — catastrófico se disparado no meio
de um jogo. O `--apply-quiet` **adia** (loga e sai 0) quando a Steam está viva; só edita quando ela
já saiu — que é justamente quando ela grava o `vdf`. Assim o guard nunca mata a Steam.

## Instalação / remoção
- `install.sh` (passo 11) e `dsx.sh` (`ensure_services`) instalam + habilitam, com `__SCRIPT__`
  substituído pelo caminho absoluto de `disable_steam_input.sh`.
- `uninstall.sh` faz `disable --now` + remove os 3 arquivos (simetria).

## Verificação
```bash
systemctl --user list-timers | grep steam-input
journalctl --user -u hefesto-steam-input-guard.service -n 20
```

## Limitação conhecida
`PathChanged` em diretório não pega modificação de arquivo aninhado profundo (rename atômico do
`localconfig.vdf` dentro de `userdata/<id>/config/`). Por isso o **timer de 30min** é a garantia;
o path unit é só o gatilho rápido oportunista (ex.: re-login na Steam recria a árvore `userdata`).
