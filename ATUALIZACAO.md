# ATUALIZACAO — FTH 3 · Corpo inteiro: imitar, teleoperar e obedecer (19/10/2026)

Conferência "atualizar, não copiar": cada afirmação das fontes antigas usadas neste curso foi comparada com as pesquisas da formação (`~/projetos/wifi/longrun/2026-10-19-formacao-fth-v72/PESQUISA-ESTADO-DA-ARTE.md` = **PE**, `../2026-10-19-vla-v72/PESQUISA-MODELOS.md` = **VM**, `PESQUISA-ECOSSISTEMA.md` = **VE**), com os repositórios oficiais lidos nesta máquina em 19/10/2026 (= **REPO**, commit indicado) e com o que o kit mede no MuJoCo 3.16.0 + Menagerie `62ab00f` (= **MEDIDO**).
Fontes antigas (intocadas): HG1 `5ee0596` (`docs/tier3.1/locomocao-customizada.mdx`, `docs/tier2.1/controle-remoto.mdx`, `docs/tier1/05-atuadores.mdx`, conteúdo de 22–25/11/2025) e FTH `26fe21c` (`niveis/nivel-3/modulo-3.md`, 29/10/2025).
Legenda da coluna "curso diz agora": **fato** (fonte primária), **relatado** (fonte secundária, dito como tal no texto), **fora** (não entra por falta de fonte).

## Controle do corpo (aulas 1 e 4)

| fonte antiga | o que dizia | o que o curso diz agora | fonte (URL/data) |
|---|---|---|---|
| HG1 tier3.1/locomocao-customizada | Controlador de marcha feito à mão: planejador → passos → perna no ar → perna de apoio → "Balance Controller (ZMP)" → juntas, laço a 100 Hz; "para produção, use IK (Pinocchio, IKFast) e balanço (ZMP, MPC)" | ZMP e MPC ficam como conceito (curso 0 aula 6). O paradigma de 2025–26 é **rastrear movimento humano** com uma política aprendida: GMR → BeyondMimic/GMT → SONIC; a hierarquia S2/S1/S0 com S0 aprendido a 1 kHz (Helix 02) e o WBC desacoplado (RL nas pernas + IK nos braços) do GR00T. **fato** | PE §3.1–3.2 · VM §4 (Helix 02, 27/01/2026) · https://github.com/NVlabs/GR00T-WholeBodyControl (REPO `45c03fa`, 13/10/2026) |
| HG1 tier3.1/locomocao-customizada | `from unitree_sdk2_python import G1Robot, MotionCommand`, `cmd.gait_type = "walk"`, `robot.send_motion_command(cmd)` | **fora**: essa API não existe no SDK oficial. No clone `unitree_sdk2_python` `814556d` (21/09/2026) o pacote é `unitree_sdk2py` e a locomoção de alto nível é `unitree_sdk2py.g1.loco.g1_loco_client.LocoClient` (`SetVelocity`, `Damp`…). SDK e DDS são do curso 4 da FTH, por link | REPO unitree_sdk2_python `814556d` (clone do piloto, 19/10/2026) |
| HG1 tier3.1/locomocao-customizada | Três "gaits de firmware" do G1 (walk 0–1,5 m/s, duty factor 60 %, ciclo ~1,2 s…) | **fora**: números sem fonte na pesquisa; locomoção é do curso 1 da FTH | — |
| — (ausente) | — | **MPC × RL**: "não achei comparação quantitativa independente em 2026" (dito assim, sem escolher vencedor) | PE §3.1 |
| — (ausente) | — | Medido no kit: as três camadas contadas num laço de 2 s (S2 5 Hz, S1 50 Hz, S0 500 Hz = passo de 2 ms do G1 do Menagerie) | MEDIDO `kit/hierarquia.py` |

## Movimento humano e retargeting (aulas 2 e 3)

| fonte antiga | o que dizia | o que o curso diz agora | fonte (URL/data) |
|---|---|---|---|
| — (HG1/FTH não tinham) | — | **GMR** (ICRA 2026): retargeting em tempo real na CPU, entradas SMPL-X, BVH (LAFAN1, Nokov, Xsens desde 21/01/2026), FBX, PICO; 17 humanoides. **fato**. No commit `bb1bbe4` (02/04/2026) o `setup.py` lista `proxqp`, `smplx` e `redis`, mas o retargeting de BVH só precisa de `mink` + `daqp` (o código usa `daqp` por padrão): o curso instala com `--no-deps` e fixa as versões | https://github.com/YanjieZe/GMR · arXiv 2510.02252 · REPO `bb1bbe4` |
| — | — | **AMASS** exige cadastro; termos de licença de **AMASS e LAFAN1** para curso aberto **não confirmados** (19/10/2026) → o curso **não redistribui nenhum dado**: usa o clipe de teste que o próprio GMR distribui (`assets/xsens_bvh_test/…boxing…bvh`, baixado pelo aluno do repositório do GMR, licença MIT do repositório) e um BVH sintético gerado pelo kit | PE §3.3 · REPO GMR `bb1bbe4` |
| — | — | Limites de junta dependem do arquivo: o modelo do GMR (`g1_mocap_29dof.xml`) tem limites **mais apertados** que o G1 do Menagerie em 15 das 29 juntas (mesma ordem de juntas). O retargeting respeita os do GMR, logo cabe nos do Menagerie | MEDIDO (comparação de `jnt_range`, 19/10/2026) |
| — | — | BONES-SEED (142 mil+ movimentos, ~288 h, com trajetórias do G1 em MuJoCo, 16/03/2026): citado **só como relatado no README**, licença não conferida, não usado | REPO GR00T-WholeBodyControl `45c03fa` |

## Rastreio de movimento (aula 4)

| fonte antiga | o que dizia | o que o curso diz agora | fonte (URL/data) |
|---|---|---|---|
| CURRICULO / PE §3.2 | BeyondMimic: repositório `whole_body_tracking`, fixa Isaac Lab 2.1.0 | Continua fixando Isaac Lab 2.1.0, mas o README agora diz que o repositório foi **aposentado** e o rastreio do BeyondMimic **vive no mjlab** (tarefa `Mjlab-Tracking-Flat-Unitree-G1`, `uv run train … --registry-name … --env.scene.num-envs 4096`, GPU NVIDIA + registro WandB). **fato**, mostrado (não rodado: exige conta WandB e GPU) | REPO whole_body_tracking `9db9158` (15/10/2026) · REPO mjlab `8bb2bc9` (18/10/2026) |
| PE §3.2 | SONIC: 42M parâmetros, 100M+ quadros, pesos abertos para o G1 | Mantido; acrescentado do README: **três checkpoints** do G1 (original, baixa latência, v1.1), tokens de 64 dimensões, controlador **a 50 Hz** (antes [2ª], agora lido no README), implantação em C++/TensorRT, pesos sob NVIDIA Open Model License | https://huggingface.co/nvidia/GEAR-SONIC · REPO GR00T-WholeBodyControl `45c03fa` |
| CURRICULO aula 5 ("SONIC baixa latência ~80 ms") | latência de ~80 ms | **Corrigido**: os 80 ms são o **horizonte de referência** (4 quadros futuros a 20 ms), não a latência ponta a ponta; o próprio README avisa que a latência total inclui sensores, rede, pré-processamento e inferência | REPO GR00T-WholeBodyControl `45c03fa`, seção Model Card |
| — | — | Medido no kit: seguir só os ângulos com o PD do G1 dá erro médio de 0,3° com a pelve no pórtico e **queda em 1,68 s** sem o pórtico — por isso existe a política de rastreio | MEDIDO `kit/reproduzir.py` |

## Teleoperação (aula 5)

| fonte antiga | o que dizia | o que o curso diz agora | fonte (URL/data) |
|---|---|---|---|
| HG1 tier2.1/controle-remoto | Controle RC do G1: velocidades por posição do joystick (25 % = 0,3 m/s … 100 % = 1,8 m/s), poses por combinação de botões, parada de emergência L2+R2 | **fora** (sem fonte na pesquisa; operação do robô real e parada de emergência são do curso 4). Fica só o conceito: joystick comanda velocidade; teleop de corpo inteiro comanda a pose | — |
| — (ausente) | — | **TWIST2** (PICO 4U + pescoço de 2 GDL de ~US$ 250; 100 demonstrações em 15 min): **relatado** (arXiv, nov/2025) | PE §3.2 (arXiv 2511.02832) |
| — | — | **HOVER** (vários modos de comando numa política de ~1,5M parâmetros, ICRA 2025): **relatado** | PE §3.2 (arXiv 2410.21229) |
| — | — | GR00T-WBC: teleop por VR (PICO), CloudXR em processo via `isaacteleop[cloudxr]` (16/06/2026), IsaacTeleop 1.4 + Jetson AGX Orin (14/09/2026). **fato** | REPO GR00T-WholeBodyControl `45c03fa` |
| — | — | Medido no kit: com janela de 0,6 s, 5 de 6 alvos com latência de 0 a 300 ms, 4/6 a 450 ms e 0/6 a 550 ms (o 6º alvo está fora do alcance de propósito) | MEDIDO `kit/teleop_sim.py` |

## Mãos (aula 6)

| fonte antiga | o que dizia | o que o curso diz agora | fonte (URL/data) |
|---|---|---|---|
| HG1 tier1/05 | Dedos: torque de 1–5 N·m, "micro servo"; mãos com 4× Dynamixel AX-12 a US$ 45 | Dex3-1 do G1 EDU: **7 GDL** (polegar 3, indicador 2, médio 2), tátil opcional (**fato**, unitree.com/g1). No MJCF do Menagerie: 7 juntas por mão, torque declarado de 1,40 a 2,45 N·m (MEDIDO). Preço de servo antigo: **fora** | https://www.unitree.com/g1 (19/10/2026) · MEDIDO `kit/mao.py` |
| — | — | Força de aperto: só **estimativa do modelo** (cilindro fixo, PD kp=500), dita como não medida; a Unitree não publica força de preensão na página lida | MEDIDO, com ressalva |
| — | — | Inspire RH56 (6 ativos/11–12 juntas) e Sharpa Wave (22 GDL): **relatado**; LEAP (16 GDL) e Shadow (24 juntas, 20 atuadores) medidos nos modelos do Menagerie | PE §2.2 · MEDIDO |

## VLA sobre o corpo inteiro (aula 7)

| fonte antiga | o que dizia | o que o curso diz agora | fonte (URL/data) |
|---|---|---|---|
| FTH 3.3 | "Large Behavior Models": RT-1, RT-2, OpenVLA, Octo como estado da arte; `pip install openvla` + `from openvla import OpenVLA` | **fora** como conteúdo: o VLA em si é do `vla-v72` (link). O curso só ensina a **interface** VLA → controle de corpo inteiro. OpenVLA/Octo não aparecem | https://inematds.github.io/vla-v72/ |
| — (ausente) | — | Hierarquia S0/S1/S2 do Helix 02 (S0 a 1 kHz, S1 a 200 Hz); GR00T N1.5/N1.6 sobre o WBC desacoplado; fluxo VLA ponta a ponta no G1 com GR00T N1.7 + SONIC (07/05/2026); espaço de tokens único do SONIC para VR, vídeo humano e VLA. **fato** | VM §4 · PE §3.2 · REPO GR00T-WholeBodyControl `45c03fa` |

## O que ficou de fora por falta de fonte
- Velocidades, poses e botões do controle RC do G1 (HG1 tier2.1) e os "gaits de firmware" (HG1 tier3.1).
- Velocidade máxima por junta do G1: a pesquisa não traz; o teto de velocidade da checagem de segurança (aula 8) é **regra do laboratório do aluno**, dito assim.
- Termos de licença de AMASS/LAFAN1 e de BONES-SEED; horas de GPU do SONIC; latência ponta a ponta medida de qualquer sistema de teleop.
- Comparação MPC × RL independente em 2026.
