# 2026-07-23 — Diagnóstico: controle "Conectado sem input" = registro SDP ausente

Sessão da noite de 23/07, com os 4 controles ligados. A mantenedora abriu com o
relato: *"o dsx roxo tá conectado como azul"* — e a página de Bluetooth do COSMIC
mostrava **4 dispositivos "Conectado"**. O kernel mostrava **3**.

Este documento registra a cadeia causal completa, **incluindo três hipóteses
minhas que foram refutadas no meio do caminho** — elas estão aqui de propósito,
porque cada uma custou uma rodada e nenhuma deve ser repetida.

## 1. A assinatura do zumbi

| | roxo (quebrado) | branco | Pro Nintendo | 8BitDo |
|---|---|---|---|---|
| `Connected` (D-Bus) | `true` | `true` | `true` | `true` |
| `Paired`/`Bonded`/`Trusted` | todos `true` | todos `true` | todos `true` | todos `true` |
| ACL (`hcitool con`) | vivo, `AUTH ENCRYPT` | idem | idem | idem |
| **`hidraw` / `uhid`** | **nenhum** | hidraw5 | hidraw4 | hidraw6 |
| `Input1.ReconnectMode` | **`none`** | `device` | `device` | `device` |
| **`cache/<MAC>`** | **46 bytes** | 1433 bytes | 1360 bytes | 1124 bytes |
| seções do cache | só `[General]` | `[General]` + **`[ServiceRecords]`** | idem | idem |

Log do `bluetoothd`, em loop:

```
profiles/input/device.c:hidp_add_connection() Could not parse HID SDP record: No such file or directory (2)
src/device.c:read_device_records() Unable to load key file from /var/lib/bluetooth/<adaptador>/cache/<MAC>
```

O registro SDP do perfil HID mora em
`/var/lib/bluetooth/<adaptador>/cache/<MAC>`, seção `[ServiceRecords]`. É dele
que o BlueZ tira o descritor HID em `extract_hid_record()`. Sem a seção,
`idev->rec == NULL` → `-ENOENT` → o perfil HID **nunca sobe**, e o controle fica
"conectado" sem existir para o sistema de input.

## 2. Três hipóteses REFUTADAS — não repetir

### 2.1  "`ServicesResolved` distingue o quebrado do são"

Foi o primeiro discriminador que usei. **Errado**: `ServicesResolved` é `false`
**também** nos três controles que funcionam — é propriedade de GATT/LE, não de
BR/EDR. Discriminadores que de fato servem: `Input1.ReconnectMode` (`none` ×
`device`), ausência de `[ServiceRecords]` no cache, e ausência de `uhid`.

### 2.2  "É auto-sustentável: `info` lista `Services=…1124…`, então o BlueZ nunca refaz o browse"

Afirmei isso **antes** de ler o fonte. O fonte do 5.86 que o projeto empacota
(`~/.cache/hefesto-dualsense4unix/bluez-src-586/bluez-5.86`) diz o **contrário**
— `src/device.c:4415`:

```c
/* Check if ServiceRecords cached group exists */
if (stat(filename, &st) < 0) {
        DBG("Missing cache file for ServiceRecords");
        device->bredr_state.svc_resolved = false;
} else if (!g_key_file_has_group(key_file, "ServiceRecords")) {
        DBG("Missing ServiceRecords from cache file");
        device->bredr_state.svc_resolved = false;
} else {
        device->bredr_state.svc_resolved = true;   /* só aqui */
}
```

E `device_connect_profiles()` (`src/device.c:2762`) faz
`if (!state->svc_resolved) goto resolve_services;` → `device_browse_sdp()`.

**Do lado do host, o BlueZ sabe se recuperar.** O cache podre não é um estado
auto-sustentável. Ler o fonte ANTES de afirmar mecanismo.

### 2.3  "Apagar o cache e reconectar cura"

Duas falhas distintas nesta:

1. **`rm` num laço de retry destrói a cura.** O browse bem-sucedido **reescreve**
   `cache/<MAC>`. Meu laço apagava o arquivo antes de *cada* tentativa — o
   `Connect()` retornou OK nas tentativas 3 e 12, e eu apaguei o registro logo
   depois de obtê-lo. Sintoma enganoso: "o Connect funciona mas nada acontece".
2. **Desconectar para "forçar reconexão" é contraproducente.** O DualSense
   **dorme** ao perder o link; só o botão PS o acorda. `Connect()` volta
   `Host is down (112)`. Converte uma cura automática em intervenção manual.

## 3. As DUAS causas reais da mesma assinatura

### (a) Direção da conexão — **curável por software**

Controle de videogame reconecta sempre **ENTRANTE** (botão PS/SYNC). No caminho
entrante o perfil `input` só consulta o registro em cache; **nada ali dispara
browse**. O browse só acontece quando o **HOST** inicia a conexão.

Cura: com o ACL de pé, `org.bluez.Device1.Connect()`. Como `svc_resolved` já é
`false`, o BlueZ é obrigado a fazer o browse, grava o `[ServiceRecords]` e
reprova os perfis — o HID sobe e o `hidraw` nasce. **A LinkKey nunca é tocada:
não há re-pareamento.**

`br-connection-busy` é esperado enquanto a conexão entrante ainda está em curso
— insistir é o certo.

### (b) Controle travado — **sem cura por software**

O controle aceita ACL, autentica, criptografa — e **não responde mais nada acima
disso**. Aqui o cache truncado é **CONSEQUÊNCIA**, não causa: o BlueZ obtém o
nome (via remote name request) e grava o arquivo, mas o browse não devolve
serviço nenhum, então sobra só o `[General]`.

Nem `Connect()` nem re-pareamento resolvem. Cura: **reset de hardware do
controle** (furinho atrás do DualSense, ~5 s com um clipe — procedimento do
fabricante).

### 3.1 O discriminador decisivo

```
sudo sdptool browse <MAC>
```

| | resultado medido |
|---|---|
| controle são (branco) | `exit 0`, responde em **< 1 s** |
| controle travado (roxo) | `exit 124` — **estourou 35 s, zero linhas** |

Foi o roxo o caso (b). Confirmação independente: `Connect()` retornou OK três
vezes e nenhum browse aconteceu; `control_connect_cb()` deu
`Connection refused (111)` no PSM de controle HID. O `info` dele **já lista**
`Services=…1124…`, prova de que num passado o browse funcionou — ou seja, o
controle **degradou**, não nasceu assim.

## 4. O bug nosso — real e independente das duas causas

`scripts/bt_bonds_snapshot.sh` excluía `cache/` **de propósito**, com a premissa
escrita no próprio cabeçalho:

> `- 'cache/' fica de fora (é só cache de SDP/nome, grande e não-crítico).`

A premissa é falsa. Restaurar um bond **sem** o cache SDP devolve exatamente o
zumbi da §1 — e, por causa de (a), ninguém nunca dispara o browse que
consertaria, porque o controle reconecta entrante.

O `doctor.sh` piorava: o `check_bt_connected_sem_hidraw` detectava o sintoma e
prescrevia `bluetoothctl remove` + re-parear — **destruição de bond à toa**,
justamente a dor que o projeto promete curar.

## 5. Entregue (SDP-CACHE-01)

| Arquivo | Mudança |
|---|---|
| `scripts/bt_bonds_snapshot.sh` | inclui `cache/` **dos devices com bond**; o cache de MACs só vistos em scan (dezenas) segue fora — esse sim era grande e descartável |
| `scripts/bt_bonds_restore.sh` | recusa entrada de cache **sem** `[ServiceRecords]`; nunca sobrescreve um registro bom com um podre |
| `scripts/bt_health_watchdog.sh` | nova `vigia_sdp_cache()`: tenta (a) via `Connect()` e, ao falhar, **distingue (b) com `sdptool browse`** e prescreve o reset de hardware em vez de mandar re-parear |
| `scripts/doctor.sh` | novo `check_bt_sdp_cache_envenenado` explicando as duas causas; o check do sintoma parou de mandar desparear de cara |
| `tests/unit/test_bt_sdp_cache.py` | 7 testes; travam inclusive **os erros que cometi** (não apagar cache, não desconectar) |

Seams de teste (idioma do projeto — "raiz parametrizada p/ teste"):
`HEFESTO_BT_SRC`, `HEFESTO_BT_SNAP_ROOT`, `HEFESTO_HIDRAW_ROOT`,
`HEFESTO_BT_STAMP_DIR`, e a flag `--sdp-cache-only` do watchdog.

Suíte completa: **4505 testes verdes**.

## 6. Pendências / gates

1.  **A vigia 3 nunca foi validada ao vivo no caminho (a)** — o único caso
   disponível na sessão era (b), que ela corretamente identifica mas não cura.
   Gate humano: reproduzir um controle com cache truncado que **responda** ao
   `sdptool browse` e confirmar que o `Connect()` do watchdog levanta o HID.
2. **Roxo**: reset de hardware pendente (decisão da mantenedora).
3. **8BitDo**: caiu sozinho durante a sessão, **sem uma linha de log do
   bluetoothd**, e com o cache **íntegro** (1124 bytes) — doença **diferente**,
   a mesma assinatura nova catalogada em
   `2026-07-23-arqueologia-8bitdo-bt.md`. Não confundir com SDP.
4. Achado colateral: `test_docs_mac_anonimato` estava **vermelho no HEAD limpo**
   (6123d2e) — o doc de 22/07 vazou dois MACs reais sem máscara, incluindo um
   BSSID. Mascarados na convenção `OUI:00:00:NN`.

## 7. Achado colateral fora do BT

O perfil **FPS** (ativo) tem `window_title_regex` com `|Control)` e `|Metro)`
**sem âncora**. Teste feito contra títulos reais:

| título | casa? |
|---|---|
| `Pro Controller` |  (grupo `Control`) |
| `Painel de Controle` |  |
| `Controle de Volume` |  |
| `Steam - Controller Settings` |  |
| `Metrônomo` / `Metrologia` |  (grupo `Metro`) |
| `Sackboy: A Big Adventure` |  |
| `Mullet Mad Jack` |  |

Em pt-BR isso é uma mina: qualquer janela com "Controle" no título ativa o
perfil de FPS. Tratado na auditoria da GUI
(`2026-07-23-auditoria-gui-perfis-4-controles.md`).
