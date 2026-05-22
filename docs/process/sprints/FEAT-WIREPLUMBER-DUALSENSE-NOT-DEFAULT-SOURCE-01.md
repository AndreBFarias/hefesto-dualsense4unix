# FEAT-WIREPLUMBER-DUALSENSE-NOT-DEFAULT-SOURCE-01 — DualSense não sequestra o microfone padrão

**Tipo:** feat (áudio/integração WirePlumber).
**Wave:** V3.7 — Recuperação de instalação + áudio COSMIC.
**Estimativa:** S — asset de drop-in + script de reset + flag no install.
**Dependências:** nenhuma.
**Status:** DONE (implementado; validação empírica na recuperação).

---

## Contexto

Relato central da mantenedora: "o controle do ps5 fica diminuindo o som do
microfone". Continua a observação de [[BUG-DAEMON-CONNECT-GHOST-INPUT-01]], que
já previa abrir uma sprint dedicada de áudio "se confirmado". Confirmado.

## Diagnóstico (causa-raiz)

NÃO é o daemon (que nem estava rodando). `~/.local/state/wireplumber/default-nodes`
tinha `default.configured.audio.source =
alsa_input.usb-Sony_Interactive_Entertainment_DualSense_Wireless_Controller-00.iec958-stereo`.
O WirePlumber (0.5.12) fixou o microfone do DualSense como fonte de entrada
padrão; ao conectar o controle, o sistema troca para o mic (ruim) do controle.

## Decisão / Entrega

Escolha da mantenedora: **rebaixar** (manter usável), não desabilitar.

1. **Drop-in** `assets/wireplumber/51-hefesto-dualsense-no-default-source.conf`
   (SPA-JSON, WP 0.5): `monitor.alsa.rules` casando
   `node.name = ~alsa_input.*DualSense.*` / `device.name = ~alsa_card.*DualSense.*`
   com `update-props` rebaixando `priority.session`/`priority.driver` e
   `node.dont-reconnect=true`. Variante `node.disabled=true` comentada (desligar
   de vez). Instalado em `~/.config/wireplumber/wireplumber.conf.d/`.
2. **Reset one-shot** `scripts/fix_wireplumber_default_source.sh`
   (`--install`/`--reset-only`/`--status`): reelege uma fonte não-DualSense como
   padrão (`wpctl set-default`, parse robusto do `wpctl status`), sobrescrevendo a
   chave persistida, e reinicia o WirePlumber.
3. **`install.sh`:** flag `--with-wireplumber-fix` (etapa 10/10) chama o script.
4. **Todas as formas:** entrega uniforme via `scripts/doctor.sh --fix` (postinst
   de .deb/Arch roda como root e não deve escrever no `~/.config` do usuário).

## Critérios de aceite

- [ ] Após o fix, `wpctl status` mostra `Audio/Source` != DualSense.
- [ ] Reconectar o DualSense **não** troca o microfone do sistema para o controle.
- [ ] `scripts/doctor.sh` mostra `[ OK ] WirePlumber não fixa o DualSense como fonte padrão`.

## Arquivos tocados

- `assets/wireplumber/51-hefesto-dualsense-no-default-source.conf` (novo)
- `scripts/fix_wireplumber_default_source.sh` (novo)
- `install.sh` (flag + etapa 10/10)

## Notas para o executor

- Validação **empírica**: após `systemctl --user restart wireplumber`, confirmar
  com `wpctl status`. Se o WP 0.5.12 ainda promover o DualSense, ajustar os
  `update-props` (o reset da chave persistida é o efeito imediato garantido).
- O drop-in é removido pelo `uninstall.sh` (só o arquivo, nunca o dir).

## Proof-of-work runtime

```bash
bash scripts/fix_wireplumber_default_source.sh --install
wpctl status | sed -n '/Default Configured/,$p'
grep audio.source ~/.local/state/wireplumber/default-nodes
```

## Fora de escopo

- Política de *sink* (saída) do DualSense — escopo é a *source* (microfone).
