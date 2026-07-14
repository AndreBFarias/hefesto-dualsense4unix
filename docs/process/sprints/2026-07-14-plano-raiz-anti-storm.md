# Plano — Cura de raiz do storm do DualSense (kernel) + GUI + install

Workflow raiz-anti-storm-e-materializa (6 agentes, com pesquisa de kernel).

I have all the grounding I need. Returning the executable implementation plan directly as my output (per the guardrail against writing report `.md` files — the orchestrator captures this text).

---

# PLANO DE IMPLEMENTAÇÃO — Cura de raiz do storm do DualSense (kernel) + exposição na GUI

Contexto/prova: `ev_dmesg.txt` L281-350 (`cannot get min/max values for control 2` / `failed to get current value for ch 0 (-22)` → `usbhid …:1.3: can't add hid device: -71` → `USB disconnect` em loop). Módulo alvo confirmado ao vivo em `ev_kernel_root.txt` L23 (`quirk_flags: … (array of quirkp)`), L30/39 (`ignore_ctl_error=N`, `skip_validation=N`), L38 (`quirk_flags=(null)…`). Descritor: If1 = fone 4ch, If2 = mic (`ev_usb_audio_desc.txt`).

---

## 1. A cura de RAIZ escolhida

**Alavanca:** parâmetro por-dispositivo `quirk_flags` do módulo `snd_usb_audio`, via `/etc/modprobe.d`. É a única alavanca de kernel que ataca o amplificador do storm **sem tocar** nas interfaces de áudio (preserva mic + fone). Não é gambiarra: é o mecanismo idiomático que o mainline usa para outros devices UAC bugados (Extigy `041e:3000`, Hercules `06f8`, Schiit Hel `30be:0101`); o DualSense simplesmente ainda **não tem entrada** na `quirk_flags_table` estática (mainline só tem `054c:0b8c`, um Walkman — por isso hoje `chip->quirk_flags=0x0`).

**Arquivo `/etc/modprobe.d/hefesto-dualsense-storm.conf` (conteúdo literal):**

```
# hefesto-dualsense4unix — cura de RAIZ do storm -71 do DualSense (camada snd-usb-audio).
# PRESERVA mic (If2) + fone (If1): NAO desliga o audio. Torna o probe do mixer UAC
# tolerante (ignore_ctl_error) e ESPACA os control-transfers no EP0 (ctl_msg_delay_1m)
# para nao colidir com o usbhid anexando a interface HID — origem do "can't add hid device: -71".
# Por-dispositivo (VID:PID:flags): NAO afeta nenhuma outra placa USB-audio.
# Ortogonal ao usbcore.quirks=...gn (cmdline, dominio Aurora/install_usb_quirk.sh): somam.
# Reversivel: apague este arquivo + replug/reload do modulo.
options snd_usb_audio quirk_flags=054c:0ce6:ignore_ctl_error|ctl_msg_delay_1m,054c:0df2:ignore_ctl_error|ctl_msg_delay_1m
```

**Valor a testar 1º (e por quê):** `ignore_ctl_error|ctl_msg_delay_1m` (equivalente hex `0x4200` = bit14 `0x4000` + bit9 `0x200`). Cobre DualSense (`054c:0ce6`) e DualSense Edge (`054c:0df2`, espelhando o Aurora). **Escalada** se o A/B mostrar colisão residual: trocar `ctl_msg_delay_1m` (usleep ~1-2 ms) por `ctl_msg_delay_5m` (`0x400`, ~5-6 ms). **Não** usar `ctl_msg_delay` puro (bit8 `0x100`, msleep **20 ms**) como 1ª escolha: 20 ms × N feature-units × até 10 retries pode **alongar** a janela frágil de re-enumeração e piorar. Preferir os **nomes** (o kernel resolve o bit em qualquer versão; validado ao vivo que o sysfs desta máquina aceita e ecoa os nomes verbatim); hex só como fallback.

**Por que preserva mic+fone (garantido):** não deautoriza interface, não faz unbind, não troca profile do card, não escreve `node.disabled`. Só torna o *probe do mixer* tolerante e espaça control-msgs. If1 (fone 4ch) e If2 (mic) continuam enumerando normalmente. É a diferença central para a **regra 75** (`assets/75-ps5-controller-disable-usb-audio.rules`), que é tudo-ou-nada e mata os dois áudios — **a regra 75 fica FORA** (opt-in agressivo, inalterada).

**Por que ataca o amplificador:** `ignore_ctl_error` impede o probe do mixer de **falhar e cascatear** em re-enum (o card sobe com defaults em vez de abortar); `ctl_msg_delay_1m` **des-raja** os control-transfers no EP0 para não colidirem com o `usbhid` anexando a If HID — que é exatamente a origem do `can't add hid device: -71`.

**Honestidade (incerteza real, pesquisa dividida):** `ignore_ctl_error` **sozinho** NÃO reduz o tráfego do EP0 — em `mixer.c` o "cannot get min/max" é impresso incondicionalmente e o loop de retry (`timeout=10`) martela o EP0 sem olhar o flag. Quem realmente ataca a colisão é `ctl_msg_delay_*`. Por isso o **payload é a combinação**, e o resultado é **PROVÁVEL, não garantido** (dois ângulos de pesquisa dizem "não cura sozinho", dois dizem "provável" com o combo). → **A Fase 1 A/B a quente é obrigatória** e a mitigação de gatilho (§3-b, vpad) permanece como defense-in-depth.

**Não precisa de reboot nem initramfs:** `snd_usb_audio` é módulo carregado tarde (do root real, quando o áudio do controle é detectado); confirmado ao vivo que **não está no initramfs**. `update-initramfs` é no-op para este caso.

---

## 2. Como vai no INSTALL por default

**Novos artefatos:**
- `assets/modprobe/hefesto-dualsense-storm.conf` — o arquivo literal do §1.
- `scripts/install_snd_quirk.sh` — **espelha** `scripts/install_usb_quirk.sh` (mesma UX: sem-arg = aplica; `--remove`; `--status` read-only sem sudo; `--runtime` escreve no sysfs). Como é modprobe.d (não cmdline), é **mais simples** que o usb_quirk — sem lógica de bootloader.

**`scripts/install_snd_quirk.sh` — comportamento concreto:**
- `apply` (default): `install -o root -g root -m 0644 assets/modprobe/hefesto-dualsense-storm.conf /etc/modprobe.d/hefesto-dualsense-storm.conf`. Idempotente (grep do marcador `054c:0ce6` no destino → no-op se igual).
- `--runtime`: `printf '054c:0ce6:ignore_ctl_error|ctl_msg_delay_1m,054c:0df2:…' > /sys/module/snd_usb_audio/parameters/quirk_flags` (best-effort; vale na próxima re-enumeração/replug). Diferente do usb_quirk, aqui o sysfs é `0644` e aceita a string — validado ao vivo.
- `--status`: lê `/sys/module/snd_usb_audio/parameters/quirk_flags` (ativo na sessão) + presença do `.conf` (agendado p/ próximo load). Sem sudo.
- `--remove`: `rm -f /etc/modprobe.d/hefesto-dualsense-storm.conf` + (best-effort) limpar o sysfs.

**Wiring no `install.sh` (por DEFAULT):** adicionar **step "3c"** logo após o bloco do quirk usbcore (`install.sh:455-470`, step "3b"). Diferença crucial: o 3b é **opt-in** (`--with-usb-quirk`) porque mexe em **cmdline** (sensível); o **3c é default-ON** porque preserva mic+fone e escreve só em `/etc/modprobe.d` (não é boot-crítico). Chamar `bash "${ROOT_DIR}/scripts/install_snd_quirk.sh"`. Adicionar flag `--no-snd-quirk` (simétrica a `--no-udev`) para CI/quem não quer.
- **Paridade de pacote:** copiar o `.conf` também no caminho host do `.deb`/Flatpak — `scripts/install-host-udev.sh` (espelho do `install_udev.sh`) e incluir o asset em `scripts/build_deb.sh`; rodar `scripts/check_packaging_parity.sh` no fim.

**Idempotência:** garantida pelo grep do marcador no `.conf` de destino (nunca duplica) e pelo `install -m` (sobrescreve com a mesma fonte).

**Coexistência com `usbcore.quirks=…gn` (Aurora):** **ortogonal, somam.** Módulo diferente (`usbcore` builtin vs `snd_usb_audio` módulo), parâmetro diferente (`quirks` vs `quirk_flags`), local diferente (cmdline/kernelstub vs `/etc/modprobe.d`). **NÃO** tocar em `/etc/kernelstub/configuration` (domínio Aurora, token único de `usbcore.quirks`). O `gn` espaça a **enumeração** no USB-core; o nosso trata a camada de **áudio** — o `gn` sozinho já provou não bastar.
- **Novo cross-check (não bloqueante):** snd-quirk ativo **e** regra 75 ativa = contraditório (o snd-quirk preserva o áudio que a 75 desliga). Espelhar o padrão de `scripts/doctor.sh:221` (`check_usb_storm_config_conflict`) com um WARN "escolha uma".

**Reversibilidade (uninstall):** `uninstall.sh` remove o `.conf` **por default** (simétrico ao install — regra da memória `feedback_uninstall_simetrico_default`), porque modprobe.d **não** é sensível como cmdline. Contrasta com o quirk de cmdline, que só sai com `--remove-usb-quirk` explícito (`uninstall.sh:281`). Adicionar ao bloco de remoção de regras (`uninstall.sh:258`): `bash scripts/install_snd_quirk.sh --remove`.

**update-initramfs:** desnecessário (módulo tardio, fora do initramfs). O script pode chamar `update-initramfs -u` só se detectar `snd_usb_audio` no initrd (hoje: não).

---

## 3. TODAS as soluções aplicadas + exposição na GUI

Tudo entra no **cartão anti-storm** já existente (`storm_diag_label`, populado por `daemon_actions.py:75-107` via `storm_doctor.storm_report()`, com o botão `on_storm_fix_safe` em `daemon_actions.py:109`). Aba: **Início** (resumo) e **Emulação** (detalhe). Linguagem pela ação da usuária (padrão `UX-MODE-TERMS-01`, `home_actions.py:39-60`), sem jargão.

| # | Solução | Onde/como aparece na GUI | O que o daemon/doctor faz |
|---|---------|--------------------------|---------------------------|
| **a** | **Cura de raiz (modprobe.d snd quirk)** | Toggle no cartão anti-storm: **"Cura do travamento do controle (recomendado)"**, ligado. Texto: *"Mantém o microfone e o fone do controle. Desliga só o mixer de volume do controle que trava o USB e derruba a conexão."* | Ligar/desligar via **pkexec** → `install_snd_quirk.sh` (apply/`--remove`) + `--runtime` para valer sem reboot; `--status` alimenta a linha do cartão. Já vem ligado pelo install, então o toggle é sobretudo status + re-aplicar/reverter. |
| **b** | **vpad Xbox isolado por perfil** | O comutador de modo já existe (`home_actions.py:41-60`): **"Jogar pelo Hefesto"** (gamepad/xbox) = **default** p/ jogos; **"Jogar direto (Sony)"** = nativo. Acrescentar aviso no nativo: *"pode desconectar em jogos com vibração de áudio (ex.: alguns títulos PS5)"*. Sackboy já migrado p/ gamepad+coop (memória). | `native.mode.set` / `gamepad.emulation.set` via IPC (`home_actions.py:393-423`). Rumble volta pelo FF do vpad ("amassou" validado). |
| **c** | **Launch options do Steam (orientação)** | Painel **"Passos no Steam"** no cartão anti-storm com botão **Copiar**: `SDL_JOYSTICK_HIDAPI=0 %command%`, *"remover PROTON_ENABLE_HIDRAW"*, *"Steam Input: Desligado"*. | Orientação + verificação **apenas** — o Hefesto não injeta env (`steam_launcher.py` só abre/foca a Steam). |
| **d** | **Steam Input OFF** | Botão existente **"Corrigir com segurança"** (`on_storm_fix_safe`, `daemon_actions.py:109`), sem sudo. | `cli --fix-safe` (Steam Input OFF + WirePlumber); `storm_doctor.check_steam_input` marca ON = WARN. |

Observação: **não** expor nada que corte mic/fone. A regra 75 permanece opt-in agressivo, fora do painel amigável (só INFO no doctor via `check_authorized_rule`, `storm_doctor.py:92`).

---

## 4. Doctor / verificação (read-only, `storm_doctor.py`)

Adicionar em `src/hefesto_dualsense4unix/integrations/storm_doctor.py` e incluir em `storm_report()` (L104-118) + `__all__` (L128-135). Consumido automaticamente pela CLI (`cli/cmd_doctor.py:79`) e pela GUI (`daemon_actions.py:81`).

- **`check_snd_quirk(quirk_flags_text=None, conf_path=None)`** — a cura de raiz está ativa? Lê `/sys/module/snd_usb_audio/parameters/quirk_flags` (ativo na sessão) e `/etc/modprobe.d/hefesto-dualsense-storm.conf` (agendado). `054c:0ce6` no sysfs → **OK** "cura ativa (mic+fone preservados)"; só no `.conf` → **INFO** "agendada p/ próximo replug/boot"; ausente → **WARN** "cura de raiz ausente — storm pode reincidir". Regex `054c:0ce6` (reusar padrão `_QUIRK_RE`, L20).
- **`check_snd_audio_healthy()`** — áudio saudável? Presença do card ALSA "Controller" via `/proc/asound/cards` (read-only, sem root). Presente → **OK** "mic+fone do controle ativos"; ausente com controle plugado → **WARN**. (Prova que a cura não quebrou o áudio.)
- **`check_hidraw_owner(daemon_pid=None)`** — via `/proc/*/fd` (ou `fuser`), alertar se um processo que **não é o daemon** segura o hidraw do DualSense enquanto um perfil storm-prone está ativo → **WARN** "vazamento de isolação (jogo no hidraw físico)".
- **`check_profile_native_stormprone(env=None)`** — perfil em `native` **e** `PROTON_ENABLE_HIDRAW` presente no ambiente → **WARN** "troque para 'Jogar pelo Hefesto' neste jogo".
- **Cross-check** (novo, espelha `doctor.sh:221`): snd-quirk ativo **e** regra 75 ativa → **WARN** "config contraditória (a cura preserva o áudio que a regra 75 desliga)".

Atualizar `tests/unit/test_storm_doctor.py` com fixtures (sysfs texto com/sem `054c:0ce6`; `.conf` presente/ausente; `/proc/asound/cards` com/sem "Controller").

---

## 5. Plano de teste — Fase 1 reversível (A/B a quente, sem reboot) e critérios de aceite

O sysfs `quirk_flags` é `0644` e aceita a string a quente (validado ao vivo) — o A/B custa segundos e é 100% reversível.

**Setup:** `sudo dmesg -w | grep -Ei 'min/max|current value|can.t add hid|-71|disconnect'` num terminal.

1. **Run A (baseline / controle):** limpar → `echo '' | sudo tee /sys/module/snd_usb_audio/parameters/quirk_flags`; re-enumerar o controle (desplugar/replugar USB, **ou** `echo 0|sudo tee /sys/bus/usb/devices/<DS>/authorized; sleep1; echo 1|…`); rodar Sackboy com `PROTON_ENABLE_HIDRAW=1`. **Esperado:** reproduz o storm (`min/max` → `-71` → `disconnect`) como em `ev_dmesg.txt` L281-350.
2. **Run B (cura de raiz):**
   ```
   echo '054c:0ce6:ignore_ctl_error|ctl_msg_delay_1m,054c:0df2:ignore_ctl_error|ctl_msg_delay_1m' \
     | sudo tee /sys/module/snd_usb_audio/parameters/quirk_flags
   ```
   re-enumerar (com o quirk já no sysfs) e rodar Sackboy no **mesmo** cenário (inclusive `PROTON_ENABLE_HIDRAW=1`, para estressar o mesmo gatilho) por **>10 min**.
3. **Áudio durante a Run B:** `wpctl status` mostra Source (mic) + Sink (fone) do card "Controller"; `arecord -D plughw:CARD=Controller -d3 t.wav && aplay t.wav` (ouvir no fone).

**Critérios de aceite (Fase 1):**
-  **0** `can't add hid device: -71`, **0** loop de `USB disconnect` por >10 min de carga.
-  mic + fone funcionando (grava e ouve).
-  As linhas `cannot get min/max` **podem** persistir (ignore_ctl_error tolera, não silencia todas) — **o critério é o loop de disconnect NÃO começar**, não o log sumir.

**Ramificação:**
- Se B fica limpa **e** áudio OK → promover a default (já é o payload do install).
- Se houver `-71` residual → escalar `ctl_msg_delay_1m` → `ctl_msg_delay_5m` e repetir B.
- Se **ainda** stormar com o combo → root-alone não basta: manter a cura como **piso/higiene** e apoiar a mitigação de gatilho (vpad §3-b) como principal (defense-in-depth). Nada permanente foi instalado no A/B → custo zero para descobrir.

**Persistência (pós-Fase 2):** após reboot, `cat /sys/module/snd_usb_audio/parameters/quirk_flags` mostra o valor **sem** passo manual (prova que o modprobe.d aplicou no load tardio) e o boot sobe normal.

---

## 6. Ordem de implementação e riscos/incertezas honestos

**Ordem (a raiz primeiro, como pedido):**
1. **Fase 1 A/B a quente (0 código, gate):** roda o §5 para fixar o payload empírico (`1m` vs `5m`) **antes** de escrever qualquer código. É a porta de entrada — barata e reversível.
2. **Cura de raiz no install:** `assets/modprobe/hefesto-dualsense-storm.conf` + `scripts/install_snd_quirk.sh` (espelhando `install_usb_quirk.sh`) + step "3c" **default-ON** em `install.sh` (após L470) + `--no-snd-quirk` + remoção **default** no `uninstall.sh` (L258) + paridade `.deb`/host (`install-host-udev.sh`, `build_deb.sh`, `check_packaging_parity.sh`).
3. **Doctor:** 4 checks novos + cross-check em `storm_doctor.py` + testes.
4. **GUI:** toggle da cura + painel "Passos no Steam" + aviso de storm no modo nativo (itens a/c/b do §3) — reusando o cartão anti-storm e o padrão pkexec.
5. **Validação Fase 3 (ao vivo):** Sackboy >10 min no vpad-isolado + cura ativa → 0 `-71`; mic+fone OK durante o jogo; rumble dispara ("amassou").

**Riscos/incertezas honestos:**
- **Eficácia (não a entrega):** `ignore_ctl_error` **não** reduz o tráfego do EP0 (só tolera; confirmado em `mixer.c`); quem des-raja é `ctl_msg_delay_*`. Logo a cura é **mitigação forte de raiz, PROVÁVEL não garantida** contra uma corrida de timing de HW. Por isso: A/B como gate + defense-in-depth (vpad) mantida.
- **`ctl_msg_delay` pode piorar:** o `ctl_msg_delay` puro (20 ms) pode **alongar** a janela frágil (delays × retries). Por isso o 1º payload é `ctl_msg_delay_1m` (~1-2 ms), escalando p/ `5m` só se preciso — nunca o 20 ms como default.
- **Recarga do módulo:** o `.conf` só pega no próximo load de `snd_usb_audio`; a quente use o **sysfs + replug** (o replug é a própria janela frágil — faça **uma vez**, com o quirk já no sysfs). Não usar `modprobe -r/modprobe` com o card em uso (derruba áudio).
- **Portabilidade de versão:** usar os **nomes** das flags (o kernel resolve o bit); hex (`0x4200`) só como fallback. Validado ao vivo que este kernel (7.0.11) aceita os nomes.
- **cmdline vs Aurora:** **NÃO** pôr `snd_usb_audio.quirk_flags` no cmdline/kernelstub — pisaria no token único de `usbcore.quirks` (domínio Aurora) e é desnecessário (módulo tardio → modprobe.d).
- **Storm espontâneo (sem jogo):** re-enum por energia/cabo/suspend ainda é teoricamente possível se a cura só amortecer parcialmente — endereçado pela camada-gatilho (vpad) e, como trilha separada de HW, mover o controle para o controlador USB mais robusto (chipset `02:00.0`), reversível e sem custo de áudio.
- **Regra 75 permanece FORA** (mata mic+fone) — só INFO no doctor; a cura de raiz é a **alternativa que preserva os dois áudios**.

**Arquivos-âncora (referência para a implementação):** `install.sh:455-470` (padrão do step 3b/quirk), `scripts/install_usb_quirk.sh` (espelho para o novo script), `scripts/install_udev.sh:61-69` (padrão opt-in a evitar — o snd-quirk é default), `uninstall.sh:258,281` (simetria), `src/hefesto_dualsense4unix/integrations/storm_doctor.py:104-135` (checks + report), `src/hefesto_dualsense4unix/cli/cmd_doctor.py:74-123` (consumo CLI), `src/hefesto_dualsense4unix/app/actions/daemon_actions.py:75-107` (cartão anti-storm na GUI), `src/hefesto_dualsense4unix/app/actions/home_actions.py:41-60` (comutador de modo), `src/hefesto_dualsense4unix/app/actions/emulation_actions.py:233-299` (padrão de aviso de quirk), `src/hefesto_dualsense4unix/profiles/schema.py:227-252` (modo por perfil — sem schema novo obrigatório).
