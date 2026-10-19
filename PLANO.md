# PLANO — FTH 3 · Corpo inteiro: imitar, teleoperar e obedecer (formacao-fth-corpo-inteiro-v72)

Curso 3 de 5 da **FTH — Formação Tecnológica em Humanoides** (v7.2, PT/EN/ES). Público: quem programa em Python, já viu ROS 2 e quer trabalhar com humanoides sem ter um. Fronteira: o VLA em si é do [`vla-v72`](https://inematds.github.io/vla-v72/) (aulas 2 e 7); aqui é o **controle de corpo inteiro (S0)** que executa. Toda prática roda em CPU, em segundos, com saída determinística.

## Versões testadas nesta máquina (19/10/2026, aarch64 / NVIDIA GB10, Ubuntu, Python 3.12.3)
| item | versão | como |
|---|---|---|
| MuJoCo | **3.16.0** | `.venv` do curso 0 (`pip install -q mujoco==3.16.0 numpy`) |
| numpy | 2.5.4 | idem |
| MuJoCo Menagerie | commit **62ab00f** (15/10/2026) | sparse-checkout do curso 0 + `sparse-checkout add unitree_g1` (aula 1) e `add leap_hand shadow_hand` (aula 6) |
| GMR | commit **bb1bbe4** (02/04/2026) | `git clone --filter=blob:none --sparse` + `sparse-checkout set assets/xsens_bvh_test` (aula 2) e `add general_motion_retargeting scripts assets/unitree_g1` (aula 3) — 83 MB em vez de 1,2 GB |
| ambiente do GMR (`.venv-gmr`) | torch **2.14.1+cpu** (índice CPU do PyTorch), mink **1.3.0**, qpsolvers **4.13.0**, daqp **0.10.3**, scipy **1.18.1**, mujoco 3.16.0, numpy 2.5.4; GMR com `pip install --no-deps -e` | um ambiente por ferramenta: o pacote do GMR importa `torch` no `__init__` |
| Modelos medidos | G1 `nq=36 nu=29`; G1 com mãos `nu=43` (7 GDL por mão); LEAP 16 GDL; Shadow 24 juntas / 20 atuadores | `kit/mao.py` |

Determinismo: `kit/capturar.sh` rodado em duas bancadas novas (`ensaio2`, `ensaio3`) → `diff -r` das saídas sem diferença (19/10/2026). Retargeting com o leitor do kit (sem PyQt6) = leitor do GMR: diferença máxima 0,0 em 600 quadros.
**Não testado aqui (só mostrado):** mjlab `Mjlab-Tracking-Flat-Unitree-G1` (GPU NVIDIA + conta WandB), BeyondMimic/`whole_body_tracking` (aposentado; Isaac Lab 2.1.0), SONIC (C++/TensorRT, PICO/CloudXR), TWIST2. O visualizador do MuJoCo precisa de tela: opcional.

## Pasta do aluno
`~/fth/` (a mesma do curso 0; `FTH` muda o lugar) com `.venv/`, `mujoco_menagerie/`, `corpo-inteiro/` (clone deste repo), `GMR/`, `.venv-gmr/` e `movimentos/` (o que o kit grava, com `movimentos/etapas/*.json` para a aula 8). Os blocos começam com `F=${FTH:-$HOME/fth}`; a captura roda o mesmo texto com `FTH=<scratchpad>` e troca o caminho por `~/fth` na saída.

## Dados de movimento
Nenhum dado é redistribuído neste repositório. Clipe usado: `assets/xsens_bvh_test/251021_04_boxing_120Hz_cm_3DsMax.bvh`, que o aluno baixa do repositório do GMR (MIT). Clipe próprio: `kit/bvh_minimo.py` gera `aceno.bvh` sintético. AMASS/LAFAN1: termos de licença não confirmados em 19/10/2026 → não usados.

## Aulas (objetivo · diagrama · prática "pronto quando", já testada)
| # | slug | objetivo (≤ 160) | diagrama | pronto quando (comando → saída) |
|---|---|---|---|---|
| 1 | wbc | montar a bancada e contar as três camadas de um humanoide de corpo inteiro (S2, S1, S0) com a frequência de cada uma | S2 o quê (5 Hz) → S1 corpo inteiro (50 Hz) → S0 PD + física (500 Hz–1 kHz) | `python3 kit/hierarquia.py; echo "saída: $?"` → `S0 PD de junta + física  : 1000 passos   (500 Hz)` + `3 camadas` + `saída: 0` |
| 2 | movimento-humano | ler um clipe de captura de movimento (BVH) e dizer quadros, fps e juntas, sabendo de onde o dado vem e sob que licença | fontes (mocap, vídeo, VR) → BVH/SMPL-X → licença → clipe | `python3 kit/ler_clipe.py $F/GMR/assets/xsens_bvh_test/…bvh` → `quadros: 4249 · fps: 120 · duração: 35.4 s` + `linhas de movimento conferidas: 4249/4249` |
| 3 | retargeting | levar um clipe humano para o G1 com o GMR num ambiente próprio e conferir que nenhum quadro passa do limite das juntas | humano → escala → IK por quadro (mink) → qpos do G1 → limites | `python3 kit/retarget.py … --fim 1200 --nome boxe_g1` → `violações de limite (Menagerie, folga 0.5°): 0` + `saída: 0` |
| 4 | tracking | reproduzir o movimento no MuJoCo com e sem pórtico e explicar por que é preciso uma política de rastreio | referência → política de rastreio → PD → física; pórtico × livre | `python3 kit/reproduzir.py ~/fth/movimentos/boxe_g1.npz` → `erro médio de junta: 0.3°` + `queda: não` (livre: `queda: sim, em t = 1.68 s`) |
| 5 | teleop | teleoperar os dois braços do G1 por um roteiro de alvos com latência e medir quantos alvos a mão atinge | operador (VR) → rede (latência) → WBC 50 Hz → PD 500 Hz | `python3 kit/teleop_sim.py --roteiro kit/passos.json` → `alvos atingidos: 5/6` (e `0/6` a 550 ms) |
| 6 | maos | contar os graus de liberdade da mão do G1, comparar com outras mãos e medir um aperto simulado no modelo | mão: GDL → atuador/torque → contato → tato | `python3 kit/mao.py` → `mão right: 7 GDL (polegar 3, indicador 2, médio 2)` + `dedos tocando o objeto: 3/3` |
| 7 | com-vla | mandar comandos de alto nível a um controle de corpo inteiro simulado e ver quais ele executa e quais recusa | VLA (S2/S1, lento) → interface de comando → WBC desacoplado (pernas RL / braços IK) → PD | `python3 kit/comando_wbc.py; echo "saída: $?"` → `executado: sim` + `saída: 0`; ruins → `3 comando(s) recusado(s)` |
| 8 | coreografia | rodar a cadeia mocap → retargeting → rastreio → segurança num só movimento e provar que as quatro etapas passam | mapa (4 degraus) + gerador | `python3 kit/conferir_pipeline.py; echo "saída: $?"` → `4 etapas ok` + `saída: 0` (antes do trabalho: `FALHA · …: não rodou`) |

Saídas de erro comum capturadas: `e1-frequencia` (aula 1, S1 que não divide 500 Hz), `e2-clipe-cortado` (2, BVH truncado: `4000/4249`), `e3-ambiente-errado` (3, GMR rodado no `.venv`), `a4b-livre` (4, sem pórtico cai), `e5-roteiro` (5, "esquerdo"), `e6-sem-maos` (6, `scene.xml` sem mãos), `a7b-recusados` (7), `e8-cadeia` (8, re-retarget sem re-checar).

## Simulação de ciclo
`simfila` na aula 8: a cadeia de quatro etapas com falha na checagem de segurança na 1ª execução (ajusta e roda de novo). Sem `simconversa`.

## Links fixos
- Curso seguinte (aula 8, `links`): https://inematds.github.io/formacao-fth-operar-v72/ (ainda não publicado em 19/10/2026 — 404 esperado no `validar --links`).
- Donos externos: vla-v72 (VLA, aulas 2 e 7), cursos 0, 1 e 2 da FTH (corpo, PD/recompensa, sim2sim), robot (ROS 2).
