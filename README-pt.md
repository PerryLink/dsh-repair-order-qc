# dsh-repair-order-qc — Registo de ordens de reparação de veículos e verificação da aritmética de liquidação

[![DSH Market](https://raw.githubusercontent.com/2BingLing/dsh-market/master/assets/readme/badge-listed-en.svg)](https://dsh.market/)

`dsh-repair-order-qc` lê um registo de ordens de reparação de veículos —o cabeçalho do veículo mais uma linha por linha de trabalho— e verifica a completude e a aritmética desse próprio registo: se ficam registados a manifestação do cliente e o trabalho realizado, se a coluna do nome do trabalho está preenchida, se a quantidade, o preço unitário e o montante são analisáveis, se o montante é igual à quantidade × o preço unitário, se a soma dos montantes das linhas confere com o valor da liquidação, se o valor da liquidação é igual às peças mais a mão de obra menos o desconto, se a data de receção não é posterior à data de entrega, se o número de ordem é único no registo e se não resta nenhum marcador de modelo na coluna do nome do trabalho.

## Como é a saída

![Terminal demo of dsh-repair-order-qc: real output over its RO-001 fixture](https://raw.githubusercontent.com/PerryLink/dsh-repair-order-qc/main/docs/assets/dsh-repair-order-qc-demo.png)

Saída real deste plugin sobre o seu próprio fixture de teste `RO-001` — não é uma simulação. O pacote de regras não inventa citações, por isso cada achado nomeia a cláusula aplicada e avisa que o seu texto não foi obtido.

## O que ele responde

| Você pergunta | O que ele responde |
|---|---|
| Uma linha diz quantidade 2, preço unitário 180 e um montante de 400 — a verificação nota? | Sim. `RO-002` assinala essa linha, porque 2 × 180 = 360 enquanto a célula do montante diz 400. A regra só corre quando a quantidade, o preço unitário e o montante são todos analisáveis como números, e a sua tolerância é `0.01` para arredondamento. Não julga se o preço unitário é razoável nem se o item devia ter sido cobrado. |
| Os montantes das linhas não conferem com o valor da liquidação escrito no cabeçalho do material. | `RO-003` soma a coluna `amount` e compara esse total com o valor da liquidação `total` declarado no cabeçalho do material, indicando quantas linhas somou e a dimensão da diferença. A tolerância é `0.01`. Faz apenas essa soma; não julga se os encargos individuais são razoáveis. |
| As nossas ordens não trazem total de peças nem total de mão de obra — ainda assim pode dizer-me que o valor da liquidação está errado? | Não, e di-lo. `RO-004` verifica peças mais mão de obra menos desconto contra o valor da liquidação e reporta-se a si mesma em `skipped` quando o material não traz os totais `partsTotal` e `laborTotal`, em vez de presumir uma composição. A sua coluna de desconto significa um montante de redução; um registo que anote uma taxa de desconto deveria desativar a regra ou usar outra verificação. |
| A data de entrega é anterior à data de receção. | `RO-005` assinala essa linha: compara a data de receção com a data de entrega e assinala a linha quando a receção é posterior à entrega. O mesmo dia conta como não posterior, uma data que não consegue analisar é reportada na sua própria linha em vez de ser ignorada, e não julga se a reparação demorou um tempo razoável. |
| O mesmo número de ordem aparece em duas linhas. | `RO-006` reporta o número repetido, porque duplicaria os encargos e quebraria a ligação entre uma ordem e o seu arquivo; ao comparar, os espaços são ignorados. Uma ordem repartida por várias linhas de trabalho é uma forma legítima: distinga essas linhas na coluna do nome do trabalho em vez de repetir o número. A regra verifica apenas a unicidade. |
| A célula do nome do trabalho ainda diz 【】 ou 待填. | `RO-007` reporta o marcador de modelo que resta, porque uma ordem sem um trabalho real não pode ser liquidada. A lista de `terms` que procura é a do seu próprio pacote de regras e pode ser ajustada ao seu modelo. Verifica apenas se essas cadeias literais aparecem, não se a redação é adequada. |

## Normas que segue

| Documento | Número | Regras que o citam |
|---|---|---|
| 《机动车维修管理规定》 | 交通运输部令2021年第18号（2005 年公布，经 2015、2016、2019、2021 年四次修正，自 2005 年 8 月 1 日起施行） | RO-001, RO-002, RO-003, RO-004, RO-005, RO-006, RO-007 |

**Boundary:** this plugin checks a **机动车维修工单** for arithmetic and completeness — that the customer's
report and the work performed are recorded, that a line's amount equals quantity × unit price, that the line
amounts total the settlement figure, that the settlement figure equals parts plus labour less discount, that
delivery does not precede receipt, that work-order numbers are used consistently, and that no placeholder
survives. It does **not** decide whether a repair was necessary, whether a charge is reasonable, whether there
was over-servicing, or whether the work was done properly.

> ### ⚠️ It checks arithmetic, not the repair
>
> A work order with perfectly consistent figures for work that should never have been sold passes this plugin.
> Judging necessity and price needs the vehicle's actual condition, the technical standards and the repair
> contract — this plugin has none of them.
>
> **The labour rate comes from the register or your configuration.** No rate standard is built in. The plugin
> does not check whether a part is genuine either; it reports what the register says.
>
> Two arithmetic rules read the register's composition, and **both say so when they cannot run**:
>
> - `RO-002` verifies `金额 = 数量 × 单价`, and reports itself in `skipped` unless all three cells parse. Its
>   tolerance is `0.01`, for rounding.
> - `RO-004` verifies `配件费合计 + 工时费合计 − 折扣 = 结算总额`. The subtraction is expressed as a **per-term
>   sign** in the rule pack (`signs: [1, 1, -1]`) rather than a negative scale, so the finding reads like the
>   arithmetic a person would write. A register with no parts/labour breakdown leaves the rule unrun instead of
>   assuming a composition.
>
> **Every `excerpt` in the rule pack says, in so many words, that the clause text was not obtained.** The regime
> lives in 《机动车维修管理规定》 and GB/T 16739. The verification pass could not retrieve verbatim clause
> text, so the pack states the gap in the `excerpt` field itself and keeps every rule at `warn` or `info`.
> **When the texts are in hand, replace each `excerpt` with the real clause and raise `kind` to `direct`.**

## Compatibility

| Superfície | Estado |
|---|---|
| Harness | Faixa de peers `>=0.1.2-rc.1 <0.2.0 \|\| >=0.2.0-0 <0.3.0` — verificada para aceitar tanto `0.2.0-rc.2` quanto `0.2.1-alpha.1`. **`engines.dsh` não é declarado**: não tem leitor e não pode recusar nenhum host |
| Node | `^22.19.0 || >=24.0.0` |
| Plataformas | Todas (ESM puro; sem código nativo, sem rede, sem chamada ao modelo) |
| Modo de ferramenta | Funciona em `native`, `ptc` e `both`; para um diretório inteiro use `ptc` |

## What it does

A tabela de regras, os campos e o comportamento detalhado estão em [README.md](README.md#what-it-does) (versão principal em inglês). O plugin apenas lista divergências literais frente às cláusulas citadas e indica em `skipped` cada verificação que não pôde ser executada.

## Install

```sh
dsh plugin --profile <name> add dsh-repair-order-qc
dsh --profile <name> --dump-config | grep 'dsh-repair-order-qc'
```

## Configuration

Todos os parâmetros ajustáveis ficam no esquema Schemastery de `src/config.ts`, portanto mudam pelo `cordis.yml` sem editar código; os limites por regra ficam no pacote de regras sob `rules/`.

| Chave | Tipo | Padrão | Descrição |
|---|---|---|---|
| `rulesFile` | string | `rules/repair-order-qc.yaml` | Caminho do pacote de regras, relativo à raiz do pacote |
| `disabledRules` | string[] | `[]` | Ids de regras a desativar; cada uma aparece em `skipped` |
| `onlyRules` | string[] | `[]` | Executar apenas estas regras; vazio executa todas |
| `skipNotes` | string | `""` | Nota acrescentada a cada motivo de `skipped` |
| `timeoutMs` | number | `120000` | Orçamento de tempo limite cooperativo da ferramenta |

## Material format

Aceita JSON ou YAML. O exemplo completo de campos está em [README.md](README.md#material-format) (versão principal em inglês). Os campos são opcionais na camada de leitura e validados pelo motor, de modo que uma exportação parcial gera achados sobre o que falta em vez de falhar.

## Rule sources

Os dados das regras ficam separados do código: cada regra traz documento, número, cláusula na numeração própria da fonte, trecho literal e URL de origem. O carregador impõe que o trecho seja citação real de pelo menos oito caracteres e que uma verificação baseada apenas em princípio geral (`kind: derived-from-principle`, teto `warn`) ou em política local (`kind: institutional-configuration`, teto `info`) nunca seja declarada `error`.

Os limites verificados e as conclusões deliberadamente **não** afirmadas estão em [README.md](README.md#rule-sources) (versão principal em inglês) e em `rules/evidence/`.

## Troubleshooting

- **O plugin instala mas a ferramenta não aparece**: confirme que `main` resolve para `lib/index.mjs` e que `pnpm run build` o gerou.
- **`dsh plugin add` recusa o pacote**: a faixa de peers cobre `0.1.x` e `0.2.x`; fora dela, conceda isenção explícita com `dsh plugin --profile <name> allow-version <pkg@ver> --dsh-version <runtime> --accept-risk`.
- **Uma regra não executou**: leia o arranjo `skipped`.
- **`check` informa `manifest-peers` como falha**: problema conhecido do `dsh-plugin-dev`; o runtime aplica a compatibilidade na instalação.
- **Os horários parecem deslocados**: toda a aritmética é de hora local sobre as cadeias fornecidas.

## Development

```sh
pnpm install
pnpm run typecheck
pnpm test
pnpm run build
node ../scripts/sync-shared.mjs dsh-repair-order-qc
```

O último comando copia o kit compartilhado de `../_shared` para `src/shared/`; execute-o novamente após cada alteração compartilhada.

## License

[Apache License 2.0](LICENSE) © 2026 dsh-repair-order-qc contributors.
