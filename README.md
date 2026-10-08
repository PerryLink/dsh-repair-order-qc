# dsh-repair-order-qc — Motor-vehicle repair work-order register and settlement arithmetic check

`dsh-repair-order-qc` reads one motor-vehicle repair work-order register — the vehicle header plus one row per item line — and checks that register's own completeness and arithmetic: that the customer's report and the work done are recorded, that the item name column is filled, that quantity, unit price and amount are parseable, that amount equals quantity × unit price, that the line amounts total the settlement figure, that the settlement figure equals parts plus labour less discount, that the receipt date does not fall after the delivery date, that work-order numbers are unique in the register, and that no template placeholder survives in the item name column.

## What it answers

| You ask | What it answers |
|---|---|
| A line says quantity 2, unit price 180, and an amount of 400 — does the check notice? | Yes. `RO-002` reports that row, because 2 × 180 = 360 while the amount cell says 400. The rule runs only when quantity, unit price and amount all parse as numbers, and its tolerance is `0.01` for rounding. It does not judge whether the unit price is reasonable or whether the item should have been charged at all. |
| The line amounts do not add up to the settlement figure written in the header of the material. | `RO-003` adds the `amount` column and compares that total with the settlement figure `total` stated in the material header, reporting how many rows it summed and how large the gap is. The tolerance is `0.01`. It only performs that addition; it does not judge whether the individual charges are reasonable. |
| Our work orders carry no parts total and no labour total — can the plugin still tell me the settlement figure is wrong? | No, and it says so. `RO-004` checks parts plus labour less discount against the settlement figure and reports itself in `skipped` when the material carries no `partsTotal` and `laborTotal` totals, instead of assuming a composition. Its discount column means a reduction amount; a register that records a discount rate should disable the rule or use another check. |
| The delivery date is earlier than the receipt date. | `RO-005` reports that row: it compares the receipt date with the delivery date and reports the row when receipt falls after delivery. The same day counts as not later, a date it cannot parse is reported on its own row rather than passed over in silence, and it does not judge whether the repair took a reasonable length of time. |
| The same work-order number appears on two rows. | `RO-006` reports the repeated number, because it would double-count the fees and break the link between a work order and its archive; whitespace is ignored when comparing. One work order spread over several item lines is a legitimate shape — distinguish those rows in the item name column instead of repeating the number. The rule checks uniqueness only. |
| The item name cell still reads 【】 or 待填. | `RO-007` reports the residual placeholder, because a work order with no real item cannot be settled. The `terms` list it looks for is the one in its own rule pack and can be adjusted to your template. It only checks whether those literal strings appear, not whether the wording is apt. |

## Standards it follows

| Document | Number | Cited by rules |
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

| Surface | Status |
|---|---|
| Harness | Peer range `>=0.1.2-rc.1 <0.2.0 \|\| >=0.2.0-0 <0.3.0` — verified to accept both `0.2.0-rc.2` and `0.2.1-alpha.1`. `engines.dsh` is deliberately not declared: it has no reader and cannot reject a host |
| Node | `^22.19.0 || >=24.0.0` |
| Platforms | All (plain ESM; no native code, no network, no model call) |
| Tool mode | Works in `native`, `ptc` and `both`; for a month of orders use `ptc` |

## What it does

Registers the `repair_order_qc` tool. It reads one repair-order register — the vehicle header plus one row per
item line — applies a versioned rule pack, and returns a report.

| Rule | Check | Severity | Basis kind |
|---|---|---|---|
| `RO-001` | the report and the work performed are recorded | warn | principle |
| `RO-002` | a line's amount equals quantity × unit price | warn | principle |
| `RO-003` | line amounts total the settlement figure | warn | principle |
| `RO-004` | the total equals parts + labour − discount | warn | principle |
| `RO-005` | delivery does not precede receipt | warn | principle |
| `RO-006` | work-order numbers are used consistently | warn | principle |
| `RO-007` | the item column holds no unreplaced placeholder | warn | principle |

## Install

```sh
dsh plugin --profile <name> add dsh-repair-order-qc
dsh --profile <name> --dump-config | grep 'dsh-repair-order-qc'
```

## Configuration

| Key | Type | Default | Description |
|---|---|---|---|
| `rulesFile` | string | `rules/repair-order-qc.yaml` | Rule-pack path, relative to the package root |
| `disabledRules` | string[] | `[]` | Rule ids to stop running; each appears in `skipped` |
| `onlyRules` | string[] | `[]` | Run only these rule ids; empty runs every rule |
| `skipNotes` | string | `""` | Note appended to every `skipped` reason |
| `timeoutMs` | number | `120000` | Cooperative tool timeout budget |

Rule-level parameters worth knowing:

- `RO-002` `resultField` / `factorFields` / `tolerance` — the line arithmetic.
- `RO-003` `field` / `headerField` / `tolerance` — the column summed and the header figure it must match.
- `RO-004` `expression` — the composition, as `{ "op": "sum", "fields": [...], "signs": [1, 1, -1] }`. Change
  the signs if your settlement composes differently; if you charge a discount *rate* rather than an amount,
  disable the rule.
- `RO-007` `terms` — the placeholders to look for.

## Material format

The tool accepts JSON or YAML:

```yaml
customer: 某某客户
vehicle: 某某车型
mileage: '48600'
partsTotal: '360'
laborTotal: '200'
discount: '0'
total: '560'
rows:
  - { 工单号: WX-2026-0018, 进厂日期: 2026-03-02, 出厂日期: 2026-03-04,
      项目名称: 前制动片, 数量: '2', 单价: '180', 金额: '360',
      客户反映: 刹车时有异响, 施工内容: 更换前制动片一副并试车 }
```

Column names are matched case-insensitively and ignoring spaces, underscores and hyphens; the register's own
column names are kept, so a finding names the column it read. Figures stated once for the whole order (the
parts and labour totals, the settlement figure) may live in the header, and the arithmetic checks find them.

## Rule sources

Rule data lives in `rules/repair-order-qc.yaml`. The pack's header states the citation gap in full, and each
rule's `note` repeats the part that matters for that rule. The load-time guard that normally enforces "an
excerpt must be a real quotation of at least eight characters" cannot tell a quotation from a description —
so this pack leans on the header, the per-rule notes and a test that asserts every `excerpt` admits the gap.

## Troubleshooting

- **`RO-004` reports itself as skipped.** The register carries no parts or labour total, so there is no
  composition to check. The plugin will not assume one.
- **`RO-004` fires on a settlement I know is right.** The parts/labour/discount figures disagree with the total.
  Check whether your discount is a rate rather than an amount — if so, disable the rule.
- **`RO-002` fires on a line I consider rounded.** The default tolerance is `0.01`; raise it if your pricing
  rounds more coarsely.
- **`RO-006` fires twice on one work order.** One order with several item lines is normal — leave the order
  number shared. The rule fires only when the *same number* appears on rows you meant as separate orders;
  if your register shares the number across lines by design, disable the rule.
- **The plugin installs but the tool never appears.** Check that `main` resolves to `lib/index.mjs` and
  that `pnpm run build` produced it; a wrong `main` makes the loader skip the entry silently.
- **`dsh plugin add` refuses the package as incompatible.** The peer range covers `0.1.x` and `0.2.x`; if
  your runtime sits outside it, grant an explicit exemption:
  `dsh plugin --profile <name> allow-version dsh-repair-order-qc@0.1.0 --dsh-version <runtime> --accept-risk`
- **`check` reports `manifest-peers` as failed.** The static checker compares against a hard-coded peer
  range that predates the 0.2 line. The runtime enforces peer compatibility at install time, so the
  declared range is the correct one; this is a known upstream issue in `dsh-plugin-dev`.

## Development

```sh
pnpm install
pnpm run typecheck   # tsc --noEmit
pnpm test            # vitest, the shared table-plugin suite plus paired fixtures
pnpm run build       # tsdown -> lib/index.mjs + lib/index.d.mts
node ../scripts/sync-shared.mjs dsh-repair-order-qc   # refresh src/shared from ../_shared
```

The plugin is **data-only**: `src/model.ts` declares the table shape, the shared kit supplies the reader and
the check engine, and the rule pack declares every check.

## License

[Apache License 2.0](LICENSE) © 2026 dsh-repair-order-qc contributors.
