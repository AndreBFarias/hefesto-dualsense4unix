# 25/07/2026 — Leva de causas-raiz: checklist sincero

Registro da sessão em que a mantenedora listou, em texto corrido e ao longo de
várias mensagens, tudo o que a incomodava no uso diário. Este documento existe
para responder **cada** item dela com o que foi medido, o que foi corrigido e o
que ficou pendente — inclusive o que não foi resolvido.

A regra que orientou o trabalho é dela: *"queremos resolver na raiz"* e *"não
queremos solução gambiarra/placeholder genérico falando que o app não
funciona"*. Uma hipótese só vale se explicar **o que já funcionava antes**.

---

## O tema comum

Quase tudo abaixo tem a mesma forma: **uma premissa que vale no cabo escrita
como se valesse sempre**, ou **a interface afirmando sucesso sem verificar**.

---

## Checklist por input

| # | O que ela disse | Estado | Causa-raiz medida |
|---|---|---|---|
| 1 | "os dois controles da nintendo … ambos reconhecidos como player 1" | **Corrigido** (falta validar em hardware) | Duas causas somadas: o clone 8BitDo falha o probe e não existe para o sistema; e havia um alvo fixo em `1` para o primário, com dois espaços de numeração chegando à mesma lâmpada |
| 2 | "a questão do bt e outras pendências" | **Levantado**, parcial | Ver seção "Bluetooth" |
| 3 | "procure por bugs, glitchs" | **Corrigido** | Achado não relatado por ela: laço eterno a ~1 Hz no daemon (~1.600 linhas de journal em 45 min) |
| 4 | "falta microfone" | **Corrigido** no cabo; **em aberto** por BT | O mic voltava mudo: `default-routes` guarda o *mute* e o projeto só conhecia o `default-nodes` |
| 5 | "alinha … aba de status … sem scroll" | **Corrigido** | `status_players_slot` era `GtkBox` vertical; virou `GtkGrid` de 2 colunas |
| 6 | "botão aplicar … fonte do branco para o roxo" | **Corrigido** | Não era só cor: uma regra atingia o label **interno** e anulava a cor dos 4 botões |
| 7 | "controles … alternando de perfis instantaneamente" | **Corrigido** | 3 causas: backend X11 lia `_NET_ACTIVE_WINDOW` rançoso; catch-all com autoridade sobre janela de jogo; sem histerese de saída |
| 8 | "o modo jogo não ativa automaticamente" | **Corrigido** | O cadeado do autoswitch barrava até a regra do próprio jogo; e a allowlist do Steam Input pulava o arming inteiro |
| 9 | "aplicar correções … não fecham a steam automaticamente" | **Corrigido** | A maquinaria existia e era inalcançável pela interface |
| 10 | "aplicar correções deveria ser default sempre" | **Corrigido** | Botão "Deixar tudo pronto" |
| 11 | "falta investir na QoL do user inexperiente … abas precisam se conversar" | **Parcial** | Dois botões novos e rótulo "Avançado"; a reorganização ampla das 9 abas **não** foi feita |
| 12 | "tem jogos que precisam ativar entrada steam, outros … comandos de inicialização … confusão real" | **Corrigido** | A regra existia no código e nada na interface escrevia a allowlist |
| 13 | "os controles se reenumeram e nunca sei o que é o quê" | **Corrigido** | O mapa MAC→slot era descartado quando o `boot_id` mudava |
| 14 | "muito teste travando … vale auditar" | **Auditado**, correção **parcial** | Ver seção "Testes" |
| 15 | "um pro da nintendo e um da 8bitdo … lidos como um controle" | **Código pronto**, **não validado** | Handshake USB transmitido com 2 bytes num endpoint de 64 |

---

## Bluetooth — o que ficou

O crash do `bluetoothd` que come bonds **não foi resolvido nesta leva** e segue
sem correção upstream conhecida. O que existe é mitigação: watchdog, snapshot de
bonds na borda da conexão, drop-in de resiliência. A **captura forense do crash
continua desligada** — precisa ser armada *antes* do próximo episódio, senão não
haverá dump para analisar.

O que esta leva mudou no domínio do rádio foi outra coisa: o daemon parou de
tratar silêncio em BT como link morto.

---

## Microfone — os dois lados

**No cabo (corrigido).** São dois estados em dois arquivos e o projeto só
conhecia um. `default-nodes` guarda *quem* é a fonte padrão — governado pelos
drop-ins e pelo reset. `default-routes` guarda o **mute** e o volume de cada
rota, e sobrevive a tudo. Medido:

```
alsa_card.usb-...DualSense...:input:iec958-stereo-input={"mute":true, ...}
alsa_card.usb-...DualSense...:output:analog-output={"mute":true}
```

Então "ligar o mic" removia os drop-ins, reiniciava o WirePlumber, e ele
restaurava fielmente o mute salvo. Sem nada no log. Era o elo entre "já
funcionou antes" e "não funciona mais" — o estado de 19/07 mostra o DualSense
como fonte padrão.

O drop-in `51-hefesto-dualsense-no-default-source.conf` **não** era o culpado:
ele só rebaixa prioridade (`node.disabled` está comentado).

**Por Bluetooth (em aberto, mas mapeado).** O DualSense **não** implementa
A2DP/HFP/HSP — o SDP anunciando só HID (`1124`) e PnP (`1200`) é o comportamento
correto, confirmado pelo mantenedor do BlueZ em `bluez/bluez#892`. Forçar perfil
de áudio no BlueZ é fantasia: `RegisterProfile` registra SDP **local**.

O áudio existe, mas como **Opus tunelado em HID reports**:

- mic: input report `0x31`; se `data[2] & 0x02`, há frame Opus em `data+4` —
  71 bytes, mono, 48 kHz, 10 ms;
- destravar o mic: output `0x32` com `pkt[2]=0x11|(1<<7)`, `pkt[3]=1`, `pkt[4]=0b011`;
- fone: `0x32`, `pkt[141]=200`, dois frames Opus em +142 e +342.

Não existe daemon nativo Linux para isso (as implementações conhecidas são
firmware de microcontrolador). É alcançável por `hidraw` sem patch de kernel — o
`hid-playstation` apenas loga "Unhandled reportID". Risco de integração: disputa
do contador de sequência do `0x32` com o driver.

---

## Testes — a suspeita dela se confirmou

O peso **não é tempo**: 4.866 testes em ~112 s é excelente. São três formas:

1. **~240 asserts em ~70 arquivos travam o TEXTO do código**, não o
   comportamento — `inspect.getsource`, grep literal em `install.sh` (`"-eq 3"`
   quebra ao virar `[[ $rc == 3 ]]`; `"Proton <= 9"` quebra no Proton 10),
   contagem de `GLib.timeout_add` que proíbe extrair helper.
2. **Testes-muralha que proibiam a correção.** O pior: um assert congelava que a
   interface **nunca** poderia fechar a Steam, enquanto a função existia e era
   inalcançável. Foi **reescrito**, não removido.
3. **Premissas de hardware fixadas.** `conftest` força o transporte USB em todo
   teste e **nenhum** teste seta o transporte BT — a classe inteira de bugs de
   rádio é invisível por construção.

**CI era teatro em três pontos** (todos corrigidos nesta leva): filtrava por
markers que nunca existiram, ignorava um diretório inexistente, e engolia a
falha com `|| echo "::warning::"` — um gate que não reprova não é gate, e era
ele que carimbava os releases. Além disso, os testes de interface **pulavam
calados** por falta de PyGObject, e `tests/core` não era executado por job
nenhum.

**O que NÃO foi feito:** a migração em massa dos ~240 asserts de texto para
testes de comportamento. É trabalho grande e independente; ficou registrado.

---

## Gates: o que estava vermelho antes desta leva

Dois gates do repositório **já reprovavam** antes de qualquer mudança daqui, e
foram corrigidos na raiz:

- **Acentuação** (`validar-acentuacao.py`): cobrava acento de **nomes de
  variável** Python (`producao`, `modulo`, `sessao`, `padrao`). Em Python
  identificador não leva acento, então eram dezenas de apontamentos que ninguém
  podia atender — e um gate que sempre reprova deixa de ser lido. A regra passou
  a ser a que sempre foi a intenção: acentuação é sobre **texto**, e num arquivo
  `.py` o texto mora em comentário, docstring e literal. Quem responde isso com
  exatidão é o `tokenize` do próprio Python.
- **Anonimato** (`check_anonymity.sh`): proibia a palavra `opus`. Opus é o codec
  de áudio da IETF (RFC 6716) — o que o DualSense usa por Bluetooth. O termo é
  vocabulário técnico obrigatório aqui; o gate passou a barrar o nome composto
  do modelo, que é o uso que ele existe para pegar. O teste que documentava o
  falso positivo como dívida ("se um dia houver contexto legítimo…") foi
  atualizado: o dia chegou.

**Não corrigido, e declarado:** `scripts/check_test_data.sh` reprova por MACs de
fixture (`aa:bb:cc:…`) que já estavam no repositório. Ele **não é executado por
nenhum workflow**, então não bloqueia release; fica registrado como dívida.

## Pendências declaradas

- **DKMS do 8BitDo**: código pronto, build limpo, paridade de patch validada nos
  dois sentidos — mas **não validado em hardware**. Exige `install.sh`, reboot e
  replug. Só depois disso se sabe se o clone aceita o report de 64 bytes.
- **Áudio do DualSense por Bluetooth**: protocolo mapeado, implementação em
  curso.
- **Crash do `bluetoothd`**: sem cura; captura forense a armar.
- **Reorganização ampla da navegação** (as 9 abas): não feita.
- **Migração dos testes de texto**: não feita.
- **Validação visual da interface**: as mudanças de layout foram validadas por
  teste, não por inspeção da janela aberta.
