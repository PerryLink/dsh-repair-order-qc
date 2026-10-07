/**
 * dsh-repair-order-qc — table shape and material contract.
 *
 * The plugin is data-only: this file declares which columns the material may use
 * and how they map onto canonical field names; the shared kit supplies the reader
 * and the check engine, and the rule pack declares every check. Adding a check
 * that fits an existing kind is a rule-pack edit, not a code change.
 */

import { canonicaliseRow, parseTable, type TableSpec } from './shared/table.ts'
import { runTableCheck, type TableCheckOptions, type TableInput } from './shared/rows.ts'
import type { Ruleset } from './shared/rules.ts'

/** Tool id exposed to the model, and the row id in `cordis.patch.yml`. */
export const TOOL_NAME = 'repair_order_qc'

/** The register's column aliases, declared once so both the spec and the guard see them. */
const COLUMNS = {
  orderNo: ['工单号', '结算单号', '维修单号', 'orderNo'],
  receivedAt: ['进厂日期', '接车日期', '受理日期', 'receivedAt'],
  deliveredAt: ['出厂日期', '交车日期', '完工日期', 'deliveredAt'],
  plateNo: ['车牌号', '车牌', '车号', 'plateNo'],
  itemType: ['项目类型', '费用类型', '类别', 'itemType'],
  itemName: ['项目名称', '维修项目', '配件名称', 'itemName'],
  quantity: ['数量', '用量', '工时', 'quantity'],
  unitPrice: ['单价', '工时单价', '配件单价', 'unitPrice'],
  amount: ['金额', '小计', '费用', 'amount'],
  laborRate: ['工时费率', '工时单价标准', 'laborRate'],
  partsTotal: ['配件费合计', '材料费', 'partsTotal'],
  laborTotal: ['工时费合计', '工时费', 'laborTotal'],
  discount: ['折扣', '优惠', 'discount'],
  total: ['结算总额', '合计金额', '总额', 'total'],
  customerConcern: ['客户反映', '故障描述', '报修内容', 'customerConcern'],
  workDone: ['施工内容', '处理措施', '维修内容', 'workDone'],
} as const

/** How the material declares its table. */
export const SPEC: TableSpec = {
  rowKeys: ['rows', 'items', 'orders', '工单'],
  columns: COLUMNS,
  header: {
  customer: ['customer', '客户名称', '送修人'],
  vehicle: ['vehicle', '车辆型号', '车型'],
  mileage: ['mileage', '进厂里程', '里程'],
  insurer: ['insurer', '保险公司', '承修方'],
  claimNo: ['claimNo', '理赔单号', '保险报案号'],
  checkedAt: ['checkedAt', '核对日期'],
  },
}

/** Fields the material must carry somewhere for the reader to accept it. */
export const REQUIRE_ANY_OF = [
  '项目名称',
  'itemName',
  '金额',
  'amount',
  '结算总额',
  'total',
  '客户反映',
  'customerConcern',
]

/**
 * Parse the material and attach its canonical field names.
 * @param source - JSON or YAML text.
 * @param target - description of where the material came from.
 * @returns the normalized table, with each row's aliases resolved to field names.
 */
export function parseMaterial(source: string, target: string): TableInput {
  const table = parseTable(source, target, {
    ...SPEC,
    ...(REQUIRE_ANY_OF === undefined ? {} : { requireAnyOf: REQUIRE_ANY_OF }),
  })
  for (const row of table.rows) canonicaliseRow(row, SPEC)
  return table
}

/**
 * Run the rule pack against the material.
 * @param input - normalized table.
 * @param ruleset - validated rule pack.
 * @param options - plugin identity, clock value, rule selection and overrides.
 * @returns the report.
 */
export function runCheck(input: TableInput, ruleset: Ruleset, options: TableCheckOptions) {
  return runTableCheck(input, ruleset, options)
}

export type { TableCheckOptions, TableInput }
