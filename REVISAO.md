Nota: 9/10

# Revisão independente — FTH 3 · Corpo inteiro (PT) — 19/10/2026

Revisor independente (não o autor). Li `conteudo/pt/curso.json`, as 8 aulas, `PLANO.md`, `ATUALIZACAO.md`, o kit (`kit/*.py`, `kit/blocos/*.sh`, `kit/saidas/*.txt`) e conferi contra as fontes:
- `PESQUISA-ESTADO-DA-ARTE.md` (FTH), `PESQUISA-MODELOS.md` e `PESQUISA-ECOSSISTEMA.md` (VLA);
- READMEs e código clonados em `scratchpad/formacao-fth-corpo-inteiro-v72/src/`: GMR `bb1bbe4` (02/04/2026), GR00T-WholeBodyControl `45c03fa` (13/10/2026), mjlab `8bb2bc9` (18/10/2026), whole_body_tracking `9db9158` (15/10/2026);
- o Menagerie `62ab00f` da bancada do autor (só leitura; medi limites, kp e torques com o MuJoCo 3.16.0 do venv).

Rodei 6 "pronto quando" que não tinham captura numa bancada isolada (`FTH` apontando para pasta minha; nada do repo nem da bancada do autor foi alterado).

**Resumo:** curso muito bem verificado. Fatos com fonte, `[2ª]` sempre como "relatado", nenhum termo proibido, nenhum dado de terceiros no repo, todo "pronto quando" sustentado por captura ou pelo código (6 que não tinham captura eu rodei e bateram). **Um problema grave de conceito** (taxonomia S0/S1/S2 da aula 1 contradiz o Helix 02, a pesquisa, o CURRICULO e a própria aula 7). Com ele corrigido, a nota sobe para ~9/10.

---

## 1. Quinze fatos sorteados

| # | Fato | Onde | Fonte | Resultado |
|---|---|---|---|---|
| 1 | Helix original: S2 a 7–9 Hz | 01-wbc, diagrama S2 | PESQUISA-MODELOS l.68 [FATO] | ok |
| 2 | Helix 02: S0 aprendido a 1 kHz, 10M parâmetros, 1.000+ h, substitui 109.504 linhas de C++, 27/01/2026; S1 a 200 Hz | 01-wbc passos; 07-com-vla passos | PESQUISA-MODELOS l.69 [FATO] | ok (mas ver Grave G1 sobre o mapeamento) |
| 3 | SONIC: 42M parâmetros, 100M+ quadros (~700 h) | 02 diagrama; 04 passos | PESQUISA-ESTADO-DA-ARTE §3.2 [FATO] | ok |
| 4 | SONIC controlador a 50 Hz, tokens de 64 dim, 3 checkpoints (original, baixa latência, v1.1), C++/TensorRT | 01 diagrama S1; 04 passos | Pesquisa marca 50 Hz como [2ª], **mas** o README do GR00T-WBC `45c03fa` l.97 diz "run the controller at 50 Hz" (fonte primária) | ok (o texto da aula 1 já atribui ao README) |
| 5 | Baixa latência: 4 quadros a 20 ms ≈ 80 ms; padrão 10 quadros ≈ 200 ms; "não é latência ponta a ponta" | 05 passos e quiz; 04 diagrama | README GR00T-WBC l.93–99; pesquisa §3.2 [FATO] | ok |
| 6 | Datas do GR00T-WBC: baixa latência e CloudXR `isaacteleop[cloudxr]` 16/06/2026; v1.1 23/07/2026 (aumento de pose de punho); IsaacTeleop 1.4 + AGX Orin 14/09/2026; fluxo VLA N1.7 + SONIC 07/05/2026 | 05 e 07 passos | README GR00T-WBC l.34–39 | ok |
| 7 | BONES-SEED 16/03/2026, 142 mil+ movimentos, ~288 h, trajetórias do G1 em MuJoCo (rotulado "Relatado", licença não conferida) | 02 passos | README GR00T-WBC l.44 | ok |
| 8 | WBC desacoplado (RL nas pernas, IK nos braços) usado sob N1.5/N1.6 | 01, 07 | README GR00T-WBC l.28; pesquisa [FATO] | ok |
| 9 | whole_body_tracking fixa Isaac Lab 2.1.0 e está aposentado; rastreio do BeyondMimic segue no mjlab | 04 passos e quiz | README wbt l.4, l.15–17 (commit 15/10/2026) | ok |
| 10 | Comando `uv run train Mjlab-Tracking-Flat-Unitree-G1 --registry-name … --env.scene.num-envs 4096` / `play … --wandb-run-path` | 04 código "mostrado" | README mjlab `8bb2bc9` l.71–72 | ok (marcado como não rodado e não pré-requisito) |
| 11 | GMR `bb1bbe4`: setup.py pede proxqp, smplx, redis; solver padrão daqp; o pacote importa torch; escala 0,9 pernas / 0,75 braços em `bvh_xsens_to_g1.json`; pickle de exemplo grava x,y,z,w | 03 diagrama e passos | `setup.py` l.20–28; `motion_retarget.py` l.18; `kinematics_model.py`/`rot_utils.py` (import torch); `ik_configs/bvh_xsens_to_g1.json`; `scripts/bvh_to_robot.py` l.166–167 | ok |
| 12 | GMR: 17 robôs, ICRA 2026, tempo real na CPU, exporta CSV para o BeyondMimic | 02, 03, 04 | Pesquisa §3.3 [FATO]; README GMR l.36, l.45 | ok |
| 13 | Limites do `g1_mocap_29dof.xml` (GMR) mais apertados em 15 das 29 juntas do Menagerie, mesma ordem | 03 passos e quiz | Medido por mim: 29 = 29, mesma ordem, 15 mais apertadas, 0 mais largas | ok |
| 14 | G1 Menagerie: atuador de posição kp=500; cintura ±150°; mãos 1,4 / 2,45 N·m (polegar 0); `scene_with_hands` nu=43 | 01, 04, 06, 07 | `g1.xml` l.10; medido no MJCF | ok |
| 15 | Dex3-1: 7 GDL (polegar 3, indicador 2, médio 2), tátil opcional, no G1 EDU; Shadow 24 juntas / 20 atuadores por acoplamento (tendão) | 06 | Pesquisa §2.2 [FATO]; `shadow_hand/right_hand.xml` tem 4 `<fixed>` (FFJ0, MFJ0, RFJ0, LFJ0) | ok |

Extras conferidos fora da amostra: G1 1,32 m [FATO]; GR00T N1.7 com S2 VLM de raciocínio (Cosmos-Reason2-2B) e S1 DiT [FATO]; MuJoCo 3.16.0 [FATO]; AMASS exige cadastro / termos [incerto] (o curso diz "não confirmados", correto).

**`[2ª]` como "relatado" — todos certos:** TWIST2 (PICO 4U, pescoço ~US$ 250, 100 demos/15 min), HOVER (~1,5M, ICRA 2025), GMT, Inspire RH56H1, Sharpa Wave, mão do Optimus "sem dado verificado". MPC × RL "sem comparação independente" (pesquisa [incerto]) está como ressalva. Nenhum `[2ª]` dito como fato.

---

## 2. Todos os "pronto quando" (24)

Legenda: **cap** = bate com `kit/saidas/`; **rodei** = sem captura, rodei numa bancada isolada em 19/10/2026; **código** = sem captura, sustentado pelo código; **aluno** = depende de arquivo do aluno.

| Aula · ex. | Comando → esperado | Situação |
|---|---|---|
| 1 · E1 | `git log -1 --format=%h` → `62ab00f` | cap (a1a) |
| 1 · E2 | `hierarquia.py` → `3 camadas`, `saída: 0`, `1000 passos` | cap (a1b) |
| 1 · E3 | `--s1-hz 100 \| grep S1` → `200 chamadas (100 Hz)` | rodei: ok |
| 2 · E1 | `ler_clipe.py … \| tail -1` → `4249/4249` | cap (a2a) |
| 2 · E2 | `bvh_minimo.py --quadros 90` → `quadros: 90 · fps: 30 · duração: 3.0 s` | rodei: ok |
| 2 · E3 | `grep -c` em `licenca.md` → `3` | aluno (comando correto) |
| 3 · E1 | import do GMR no `.venv-gmr` → `saída: 0` | cap indireta (a3a) |
| 3 · E2 | `retarget.py [clipe do GMR] --fim 1200` → `violações … 0`, `saída: 0` | cap (a3b); ver Menor m3 |
| 3 · E3 | `boxe_trecho2.npz` existe + `saída: 0` | cap indireta (a8c roda o mesmo retarget) |
| 4 · E1 | `reproduzir.py … \| tail -2` → `0.3°` e `queda: não` | cap (a4a) |
| 4 · E2 | `--modo livre \| tail -1` → `queda: sim, em t = 1.68 s` | cap (a4b) |
| 4 · E3 | `boxe_trecho2.npz \| grep erro` → `1.5°` | cap (a8c) |
| 5 · E1 | `teleop_sim.py … \| tail -1` → `5/6` | cap (a5a) |
| 5 · E2 | roteiro com dx < 0,3 → `6/6` | rodei com dx 0,29 e 0,25: `6/6` |
| 5 · E3 | `--latencia-ms 550` → `0/6` | cap (a5b) |
| 6 · E1 | `mao.py \| tail -1` → `dedos tocando o objeto: 3/3 …` | cap (a6a) |
| 6 · E2 | `--so-contar \| grep -c "7 GDL"` → `2` | rodei: `2` |
| 6 · E3 | `wonik_allegro/right_hand.xml` → `mão avulsa: [N] GDL · [N] atuadores` | código: o ramo "avulsa" conta juntas hinge e `nu` de qualquer modelo sem base livre; não rodei (não alterei o sparse-checkout do autor) |
| 7 · E1 | `comando_wbc.py` → `executado: sim`, `saída: 0` | cap (a7a) |
| 7 · E2 | `comandos-ruins.json \| tail -1` → `executado: não · 3 comando(s) recusado(s)` | cap (a7b) |
| 7 · E3 | `meus-comandos.json` → `executado: sim` | aluno |
| 8 · E1 | `conferir_pipeline.py` → `4 etapas ok`, `saída: 0` | cap (a8b). Rodei também numa bancada vazia: lista as 4 etapas faltando, `0 de 4 etapas ok`, `saída: 1` (o critério falha antes do trabalho, como o texto promete) |
| 8 · E2 | `--teto-graus-s 150 \| tail -1` → `segurança: 3/4 regras` | rodei: `3/4` |
| 8 · E3 | `conferir_pipeline.py \| tail -2` → `boxe_trecho2.npz` e `3 de 4 etapas ok` | cap (a8c) |

Coerência texto × captura: todas as saídas citadas no texto batem com `kit/saidas/` (5/6, 4/6 a 450 ms, 0.3°/1.9°, 1.68 s, 18.6/53.0/81.4 N, 313°/s, 635°/s, 1.4 cm = 1,9 cm abaixo de 3.3 cm etc.). Um único desencontro: Menor m1. O "pior junta (2.7°)" do boxe_curto contra 1.9° do boxe_g1 parece estranho, mas está certo: `reproduzir.py` mostra o erro **médio** da pior junta, não o máximo.

---

## 3. Varreduras

- **Termos proibidos do BRIEF** (Webots/NAO, Isaac Gym/legged_gym, Humble, Figure 01/02, Jetson Thor, K-Scale, "US$ 16 mil", OpenVLA/Octo, MindOn, PREMIUM, Discord, "compre"): **nenhuma ocorrência**.
- **Dados de terceiros no repo:** nenhum `.bvh/.npz/.pkl/.csv/.fbx` versionado; `.git` tem 2,4 MB. "AMASS/LAFAN" aparece só em texto e num caminho de import do GMR (`lafan_vendor`) em `kit/retarget.py`. O trecho de 12 linhas do cabeçalho BVH do clipe de teste do GMR (aula 2) é citação mínima de arquivo que o próprio GMR publica: aceitável.
- **Placeholders `<…>` fora de bloco de código:** nenhum. Em `<code>` de "pronto quando" há `[clipe do GMR]` e `[N]` (ver m3).
- **Técnica (MuJoCo, IK, retargeting, teleop):** correta. Juntas que não dividem 500 Hz recusadas; replay × rastreio bem explicado (pórtico = base recolocada); quatérnio w,x,y,z × x,y,z,w; limites conferidos no modelo que executa; latência × horizonte de referência; GDL ≠ atuadores; força simulada dita como estimativa do modelo. O único erro conceitual é o G1.

---

## 4. Problemas

### Graves (impedem publicar)

**G1 — Taxonomia S0/S1/S2 da aula 1 contradiz o Helix 02, a pesquisa, o CURRICULO e a aula 7.**
- `01-wbc.json` secoes[0]: S1 = "Transforma o 'o quê' em ângulos para todas as juntas ao mesmo tempo, **mantendo o equilíbrio**. Em 2026 isso é uma política aprendida que rastreia movimento (o SONIC roda a 50 Hz…)"; S0 = "PD de junta + física"; legenda: "**Nomes S0/S1/S2 como no Helix 02 da Figure (27/01/2026)**".
- No Helix 02 (PESQUISA-MODELOS l.69 e l.125), o **S0** é o controlador de corpo inteiro aprendido (1 kHz) que equilibra e coordena; o S1 é a política visuomotora do VLA (alvos de junta a 200 Hz).
- PESQUISA-ESTADO-DA-ARTE §3.1: a política de rastreio "serve de **'sistema 0'** para teleop e VLA". CURRICULO l.70: "aqui é o **controle de corpo inteiro (S0)** que executa".
- `07-com-vla.json` secoes[0].nos[0]: "VLA · **S2 + S1**", com o WBC embaixo, ou seja WBC = S0. A aula 1 põe o mesmo WBC/SONIC no S1 e o VLA só no S2.

É o objetivo da aula 1 ("contar as três camadas … S2, S1, S0"), então o aluno sai com o mapa errado e a aula 7 contradiz a aula 1. **Correção pequena, à escolha:**
(a) alinhar ao Helix 02: S2 + S1 = VLA (o "o quê", poucos Hz a 200 Hz), S0 = controle de corpo inteiro (SONIC, BeyondMimic; no kit, IK + pernas paradas), e embaixo o PD de junta/SDK como laço do motor, sem nome S. Isso exige ajustar o `hierarquia.py` (rótulos impressos), a captura `a1b`/`e1`, o quiz 1 da aula 1 e o resumo; ou
(b) manter os rótulos do kit, mas **tirar "como no Helix 02"** da legenda e escrever explicitamente: "o kit usa S2/S1/S0 para tarefa/corpo/junta; no Helix 02 o controle de corpo inteiro aprendido se chama S0 e o S1 já é parte do VLA". Ajustar também `07-com-vla` nos[0] para não dizer "S2 + S1" sem essa ressalva, e o detalhe do S0 da aula 1 ("No Helix 02 da Figure, o S0 virou um controlador aprendido a 1 kHz"), que hoje sugere que o Helix aprendeu o **PD**, quando o que ele aprendeu foi o controle de corpo inteiro.

### Menores (corrigir, não bloqueiam)

- **m1 — Texto × código, aula 1.** `01-wbc.json` secoes[3].sub: "A cada **100 ms** (S2) troca o alvo da mão direita". O `hierarquia.py` usa `--s2-hz 5` (200 ms), e a saída logo abaixo mostra `10 chamadas (5 Hz)` em 2 s. Trocar por "A cada 200 ms".
- **m2 — "29 motores".** `03-retargeting.json` lead: "o G1 tem 1,32 m e **29 motores** com limites". A pesquisa dá 23 GDL no G1 base e 23–43 no EDU; 29 é o modelo do Menagerie. Sugestão: "o G1 do Menagerie tem 29 juntas com limites".
- **m3 — Placeholder num comando copiável.** `03-retargeting.json` E2 pronto: `python3 kit/retarget.py [clipe do GMR] --fim 1200 --nome boxe_g1`. Todos os outros "pronto quando" dão o caminho completo; use `~/fth/GMR/assets/xsens_bvh_test/251021_04_boxing_120Hz_cm_3DsMax.bvh`. Em `06-maos.json` E3, `mão avulsa: [N] GDL · [N] atuadores` é aceitável, mas sem captura: vale capturar a wonik_allegro e pôr o número.
- **m4 — Medições do autor sem data/ressalva (BRIEF regra 5).** `02-movimento-humano.json` secoes[2].sub: "1,2 GB por causa das malhas de 17 robôs" e "cerca de 3 MB"; `03-retargeting.json` secoes[2].sub: "algumas centenas de MB". O PLANO registra "83 MB em vez de 1,2 GB", mas o texto não diz "medido em 19/10/2026". Acrescentar "(medido em 19/10/2026, commit bb1bbe4)".
- **m5 — Lista do setup.py incompleta.** `03-retargeting.json` passos[1]: "o setup.py pede proxqp, smplx e redis". Ele também pede opencv-python, natsort, psutil e protobuf, que o curso também não instala. Sugestão: "pede, entre outros, proxqp, smplx e redis".
- **m6 — Sem captura (sustentados, mas o BRIEF pede saída testada):** 1·E3, 2·E2, 5·E2, 6·E2, 6·E3, 8·E2. Rodei todos menos o 6·E3 e bateram. Vale gravar as capturas em `kit/saidas/` para o `--conferir` cobri-los.
- **m7 — Rótulo da regra de pé.** Saída `pés acima do chão: site do pé desce até 1.4 cm (de pé: 3.3 cm)`: o nome sugere "acima do chão", mas o critério é descer abaixo da altura de pé, e o simfila diz "pé abaixo do chão". Coerente com o código; só a redação pode confundir (ex.: "pé não afunda: site desce até 1.4 cm, de pé 3.3 cm").

### Pontos fortes
Kit determinístico e conferido (duas bancadas novas); números do texto batem com as capturas; cada aula tem erro comum capturado; ressalvas de licença (AMASS/LAFAN1/BONES-SEED) e de força simulada exemplares; "mostrado" (mjlab) separado de "pronto quando"; datas e commits em todo comportamento de ferramenta.

---

## Revisão das correções (19/10/2026)

Nota da primeira rodada: 7.5/10. **Nota atual: 9/10, sem grave pendente.**

Conferi o `git diff` de `conteudo/pt/`, `kit/hierarquia.py`, `kit/checar_seguranca.py` e `kit/blocos/`, as 28 saídas em `kit/saidas/`, e rodei de novo o kit alterado numa bancada isolada (`FTH` próprio, MuJoCo 3.16.0, Menagerie 62ab00f).

| Item | Correção | Conferência |
|---|---|---|
| G1 taxonomia | Opção (a). Aula 1: nó "VLA · S2+S1", nó "S0 · corpo" (Helix 02 a 1 kHz; SONIC a 50 Hz; kit IK a 50 Hz), "PD do motor" embaixo; legenda alinhada ao Helix 02; quiz, resumo e E3 (`--wbc-hz 100`) ajustados. Aula 7: "S0 · WBC" e o PD "embaixo do S0". `hierarquia.py` com `--tarefa-hz`/`--wbc-hz` e rótulos novos | ok. Coerente com PESQUISA-MODELOS l.69/125 (S0 1 kHz, S1 200 Hz), com a pesquisa §3.1 ("sistema 0") e com o CURRICULO l.70. Aula 1 e aula 7 agora concordam. Rodei: a saída padrão é idêntica a `a1b`; `--wbc-hz 100` dá `200 chamadas (100 Hz)` (= `a1c`); `--wbc-hz 30` dá o erro de `e1` com `saída: 1` |
| m1 | "A cada 200 ms (tarefa)" | ok, bate com 5 Hz e `10 chamadas` |
| m2 | "no modelo do Menagerie, 29 juntas" | ok |
| m3 | Caminho completo do BVH no E2 da aula 3 | ok |
| m4 | 2,9 MB e 1,2 GB "medidos em 19/10/2026, commit bb1bbe4"; venv 1,2 GB numa bancada nova | ok (o texto agora diz "1,2 GB na pasta assets", mais preciso que antes) |
| m5 | "entre outros, proxqp, smplx e redis" | ok, bate com o `setup.py` |
| m6 | Capturas novas `a1c`, `a2c`, `a5c` (dx 0,25 → 6/6), `a6c` (Allegro: 16 GDL · 16 atuadores), `a8d` (teto 150 → 3/4), com abas na página | ok; os números batem com o que rodei na 1ª rodada |
| m7 | Regra renomeada "pé não afunda no chão" no script, nas capturas `a8a`/`a8c` e no texto | ok; rodei `checar_seguranca.py`: o rótulo novo sai igual à captura |

**O que as correções poderiam ter quebrado:** nada encontrado.
- Nenhum resto de `--s1-hz`/`--s2-hz`, "S1 corpo", "S2 comando" ou "pés acima" em `conteudo/pt` nem em `kit/`.
- EN/ES (`conteudo/en`, `conteudo/es`) já trazem a taxonomia nova e o "200 ms".
- O quiz 4 da aula 1 ("o controle de corpo inteiro (S0) em C++ por um controlador aprendido a 1 kHz") segue a fonte (109.504 linhas de C++).

**Menores restantes (não bloqueiam):**
- `PLANO.md` linha 27 ainda descreve a aula 1 com a taxonomia antiga ("S2 o quê → S1 corpo inteiro → S0 PD", saída `S0 PD de junta + física`). É documento interno, mas convém alinhar.
- Na aula 1 o nó "S0 · corpo" tem sub "50 Hz–1 kHz", e a pergunta 1 do quiz diz que quem roda mais rápido é o PD (500 Hz–1 kHz). Os dois estão certos (o S0 do Helix é 1 kHz), mas a sobreposição pode confundir. Opcional: uma frase dizendo que no Helix o S0 aprendido chega à frequência do PD.
