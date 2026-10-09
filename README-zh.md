# dsh-repair-order-qc — 机动车维修工单登记与结算算术核对

[![DSH Market](https://raw.githubusercontent.com/2BingLing/dsh-market/master/assets/readme/badge-listed-en.svg)](https://dsh.market/)

`dsh-repair-order-qc` 读取一份机动车维修工单——车辆表头加每个项目一行——核对这份工单自身的齐备与算术：客户反映与施工内容是否记录、项目名称栏是否填写、数量、单价与金额是否可解析、金额是否等于数量乘单价、明细金额合计是否等于结算总额、结算总额是否等于配件费加工时费减折扣、进厂日期是否不晚于出厂日期、工单号在工单内是否唯一、项目名称栏是否残留模板占位符。

## 实际输出长什么样

![Terminal demo of dsh-repair-order-qc: real output over its RO-001 fixture](https://raw.githubusercontent.com/PerryLink/dsh-repair-order-qc/main/docs/assets/dsh-repair-order-qc-demo.png)

本插件对自己 `RO-001` 测试夹具的**真实输出**，不是示意图。规则库不伪造引文，因此每条发现都会同时写明所引条款，以及该条款原文本次未取得。

## 它回答什么问题

| 你会问 | 它怎么答 |
|---|---|
| 一行写着数量 2、单价 180，金额却填了 400，能查出来吗？ | 能。`RO-002` 会报出该行：2 × 180 = 360，而金额栏写的是 400。本条只在数量、单价、金额三栏都可解析为数值时执行，容差 `0.01`，用于容纳小数进位。它不判断单价是否合理、该项目是否应当收费。 |
| 各行金额加起来，与材料表头写的结算总额对不上。 | `RO-003` 会把 `amount` 一栏相加，与材料表头的结算总额 `total` 比较，并报出参与相加的行数与差额。容差 `0.01`。它只做这个加法核对，不判断各项收费是否合理。 |
| 我们的工单没有配件费合计与工时费合计两栏，还能查出结算总额不对吗？ | 不能，而且它会说明这一点。`RO-004` 核对配件费加工时费减折扣是否等于结算总额；材料没有 `partsTotal` 与 `laborTotal` 两栏合计时，本条在 `skipped` 中报告自己，不假定任何构成。它的折扣栏口径是减免金额；若台账登记的是折扣率，应停用本条或改用其它检查。 |
| 出厂日期早于进厂日期。 | `RO-005` 会报出该行：它比较进厂日期与出厂日期，进厂日期晚于出厂日期时报出该行。同一天视为不晚于；无法解析的日期单独报在该行上，不会静默放过；它不判断维修工期是否合理。 |
| 同一个工单号出现在两行上。 | `RO-006` 会报出重复的工单号，因为重复会让费用被重复计算，也会让工单与档案无法对应；比较时忽略空白字符。同一张工单分多行登记不同项目属正常情形——请在项目名称栏区分这些行，而不是重复工单号。本条只核对唯一性。 |
| 项目名称栏还是【】、待填这样的字样。 | `RO-007` 会报出残留的占位符，因为没有真实项目的工单不能结算。它查找的字样就是它自己规则库里那份 `terms` 清单，可按本机构模板调整。它只核对是否出现这些字面字样，不判断表述是否恰当。 |

## 依据的标准

| 文件 | 文号 | 引用它的规则 |
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

| 项目 | 状态 |
|---|---|
| Harness | 对等版本范围 `>=0.1.2-rc.1 <0.2.0 \|\| >=0.2.0-0 <0.3.0` —— 已实测同时接受 `0.2.0-rc.2` 与 `0.2.1-alpha.1`。**刻意不声明 `engines.dsh`**：它没有任何读取者，也无法拒装任何宿主 |
| Node | `^22.19.0 || >=24.0.0` |
| 平台 | 全平台（纯 ESM；无原生代码、无联网、不调用模型） |
| 工具模式 | `native` / `ptc` / `both` 均可；批量校验整个目录时建议 `ptc`，schema 成本只付一次 |

## What it does

规则表、字段说明与行为细节见 [README.md](README.md#what-it-does)（英文主版本）。本插件只列出材料与所引条款之间的字面差异，并对无法执行的检查在 `skipped` 中逐项说明。

## Install

```sh
dsh plugin --profile <name> add dsh-repair-order-qc
dsh --profile <name> --dump-config | grep 'dsh-repair-order-qc'
```

## Configuration

全部可调参数都在 `src/config.ts` 的 Schemastery schema 中，只改 `cordis.yml` 即可生效，无需改代码；逐条阈值在 `rules/` 下的规则库文件里。

| 键 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `rulesFile` | string | `rules/repair-order-qc.yaml` | 规则库文件路径，相对插件包根目录 |
| `disabledRules` | string[] | `[]` | 要停用的规则 id 列表；每条都会出现在 `skipped` 中 |
| `onlyRules` | string[] | `[]` | 只执行这些规则 id；留空表示执行全部规则 |
| `skipNotes` | string | `""` | 附加到每条 `skipped` 说明后的备注 |
| `timeoutMs` | number | `120000` | 工具协作式超时预算（毫秒） |

## Material format

支持 JSON 与 YAML。完整字段示例见 [README.md](README.md#material-format)（英文主版本）。字段在读取层是可选的，由检查引擎校验，因此部分导出的材料会产生"缺项"类差异，而不是让程序崩溃。

## Rule sources

规则数据与代码分离，每条规则都带文件名、文号、按原文自身编号体系的条款号、逐字摘录与来源地址。加载期强制：摘录必须是真实引文且不少于八个字符；依据仅为原则性条款（`kind: derived-from-principle`，严重级上限 `warn`）或本机构配置（`kind: institutional-configuration`，上限 `info`）的检查不得标为 `error`。夸大依据的规则库会在加载期失败，而不会产出一份看起来很有底气的报告。

核验中确认的边界与"刻意没有作出的结论"见 [README.md](README.md#rule-sources)（英文主版本）与随包的 `rules/evidence/` 目录。

## Troubleshooting

- **插件装上了但工具不出现**：确认 `main` 指向 `lib/index.mjs` 且 `pnpm run build` 已生成该文件；`main` 写错会让加载器静默跳过该条目。
- **`dsh plugin add` 报版本不兼容**：peer 范围覆盖 `0.1.x` 与 `0.2.x`；若运行时在其之外，可显式豁免：`dsh plugin --profile <name> allow-version <包名@版本> --dsh-version <runtime> --accept-risk`
- **某条规则没有执行**：查看 `skipped` 数组，其中写明了规则 id 与原因。
- **`check` 报 `manifest-peers` 失败**：静态检查器比对的是一份早于 0.2 世代的硬编码 peer 范围；安装期的 peer 校验以运行时为准。这是 `dsh-plugin-dev` 的已知上游问题。
- **时间看起来偏移**：全部计算都是对输入字符串做墙上时钟运算，不做时区换算。

## Development

```sh
pnpm install
pnpm run typecheck
pnpm test
pnpm run build
node ../scripts/sync-shared.mjs dsh-repair-order-qc
```

第 4 项把 `../_shared` 的共享件同步进 `src/shared/`；每次改动共享件后都要重跑。

## License

[Apache License 2.0](LICENSE) © 2026 dsh-repair-order-qc contributors.
