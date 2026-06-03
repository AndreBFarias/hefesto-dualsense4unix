# FEAT-WIREPLUMBER-DISABLE-SOURCE-MODE-01 — modo opt-in para desabilitar o microfone do DualSense

**Tipo:** feat (áudio/integração WirePlumber).
**Wave:** V3.9 — recuperação de áudio + diagnóstico USB.
**Estimativa:** S — flag no script + flag no install + 1 asset variante.
**Dependências:** decisão [[019-wireplumber-default-active-not-configured]]; complementa [[BUG-WIREPLUMBER-FIX-FALSE-SUCCESS-01]].
**Status:** PENDING.

---

## Contexto

O fix atual [[FEAT-WIREPLUMBER-DUALSENSE-NOT-DEFAULT-SOURCE-01]] **rebaixa** a
prioridade do mic do DualSense (mantém usável para seleção manual). O estudo de
campo 2026-05-28 mostrou o limite dessa abordagem: quando o DualSense é a **única
fonte de captura available** (webcam desconectada, jack onboard vazio), rebaixar
não impede que ele seja o microfone do sistema — é a única fonte que existe.

Para usuários que **não** têm um mic alternativo sempre plugado e querem paz
garantida (o controle nunca vira microfone, ponto), falta um modo que
**desabilite** a fonte do DualSense em vez de só rebaixá-la. O drop-in já
documenta a variante `node.disabled = true`, comentada — falta expô-la.

## Decisão / Entrega

Adicionar um modo opt-in que aplica `node.disabled = true` à fonte do DualSense,
preservando o modo rebaixar como **default**.

1. **Variante de drop-in.** Em vez de manter `node.disabled` comentado no mesmo
   arquivo, gerar/instalar uma variante explícita
   (`assets/wireplumber/52-hefesto-dualsense-disable-source.conf`, ou reescrever
   o `update-props` do 51 conforme o modo) que casa a *source* do DualSense
   (`node.name = ~alsa_input.*DualSense.*`) e seta `node.disabled = true`.
   **Escopo cirúrgico: apenas a source (mic)** — não desabilitar o card inteiro,
   para não derrubar nada além da captura.
2. **`fix_wireplumber_default_source.sh --disable-source`.** Novo modo (ao lado
   de `--install`/`--reset-only`/`--status`): instala a variante disable, remove
   a chave `configured` do DualSense do state e reinicia o WirePlumber. Idempotente.
   `--install` (rebaixar) continua sendo o default sem flag.
3. **`install.sh --with-wireplumber-disable-mic`.** Flag opt-in que chama o modo
   disable na etapa de áudio, mutuamente exclusiva com `--with-wireplumber-fix`
   (se ambas, disable vence + aviso).
4. **`uninstall.sh`** remove a variante disable junto com o drop-in de rebaixar
   (só os arquivos, nunca o diretório — simetria com a FEAT original).
5. **Documentação:** README/CHECKLIST registram o trade-off — desabilitar a
   source remove a captura do headset-jack do controle; reversível removendo o
   drop-in. Verificação alinhada a [[BUG-WIREPLUMBER-FIX-FALSE-SUCCESS-01]] (olha
   o ativo).

## Critérios de aceite

- [ ] Com `--disable-source`, a fonte do DualSense **some** das sources (`wpctl status` não lista o mic do DualSense) e `pactl get-default-source` != DualSense mesmo sem outra fonte plugada.
- [ ] O modo default (`--install`, sem flag) continua **rebaixando** (DualSense permanece available, `priority 50`).
- [ ] `install.sh --with-wireplumber-disable-mic` aplica o modo disable; conflito com `--with-wireplumber-fix` resolvido com aviso.
- [ ] `uninstall.sh` remove a variante disable; diretório `~/.config/wireplumber/wireplumber.conf.d/` preservado.
- [ ] Reverter (remover o drop-in + restart) traz o mic do DualSense de volta.
- [ ] `./scripts/check_anonymity.sh` vazio; acentuação PT-BR verde; saída do DualSense (sink) intacta.

## Arquivos tocados

- `assets/wireplumber/52-hefesto-dualsense-disable-source.conf` (novo) — ou lógica de variante no 51.
- `scripts/fix_wireplumber_default_source.sh` (modo `--disable-source`).
- `install.sh` (flag `--with-wireplumber-disable-mic`).
- `uninstall.sh` (remoção da variante).
- `README.md` / `docs/process/CHECKLIST_HARDWARE_V2.md` (trade-off + verificação).

## Proof-of-work runtime

```bash
bash scripts/fix_wireplumber_default_source.sh --disable-source
wpctl status | sed -n '/Sources:/,/Filters:/p'   # mic do DualSense ausente
pactl get-default-source                          # != DualSense, mesmo sem webcam
# reverter:
rm ~/.config/wireplumber/wireplumber.conf.d/52-hefesto-dualsense-disable-source.conf
systemctl --user restart wireplumber
wpctl status | sed -n '/Sources:/,/Filters:/p'   # mic do DualSense de volta
```

## Fora de escopo

- Desabilitar o *sink* (saída) do DualSense — escopo é só a *source* (mic).
- Auto-detecção "tem webcam? então rebaixa, senão desabilita" — explícito por
  flag é mais previsível; heurística fica para fase 2 se houver demanda.
- Toggle pela GUI/applet — pode virar sprint própria depois.
