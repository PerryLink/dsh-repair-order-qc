# dsh-repair-order-qc — Registro de órdenes de reparación de vehículos y verificación de la aritmética de liquidación

`dsh-repair-order-qc` lee un registro de órdenes de reparación de vehículos —la cabecera del vehículo más una fila por línea de trabajo— y comprueba la completitud y la aritmética de ese propio registro: que se registren la manifestación del cliente y el trabajo realizado, que la columna del nombre del trabajo esté rellenada, que la cantidad, el precio unitario y el importe se puedan analizar, que el importe sea igual a la cantidad × el precio unitario, que la suma de los importes de las líneas cuadre con la cifra de liquidación, que la cifra de liquidación sea igual a las piezas más la mano de obra menos el descuento, que la fecha de recepción no sea posterior a la fecha de entrega, que el número de orden sea único dentro del registro y que no quede ninguna marca de plantilla en la columna del nombre del trabajo.

## Qué responde

| Usted pregunta | Qué responde |
|---|---|
| Una línea dice cantidad 2, precio unitario 180 y un importe de 400, ¿lo nota la comprobación? | Sí. `RO-002` señala esa fila, porque 2 × 180 = 360 mientras que la celda del importe dice 400. La regla solo se ejecuta cuando la cantidad, el precio unitario y el importe se pueden analizar como números, y su tolerancia es `0.01` para el redondeo. No juzga si el precio unitario es razonable ni si el concepto debía cobrarse. |
| Los importes de las líneas no cuadran con la cifra de liquidación escrita en la cabecera del material. | `RO-003` suma la columna `amount` y compara ese total con la cifra de liquidación `total` que declara la cabecera del material, e informa de cuántas filas sumó y de la magnitud de la diferencia. La tolerancia es `0.01`. Solo hace esa suma; no juzga si los cargos individuales son razonables. |
| Nuestras órdenes no traen total de piezas ni total de mano de obra, ¿aun así puede decirme que la cifra de liquidación está mal? | No, y lo dice. `RO-004` comprueba piezas más mano de obra menos descuento contra la cifra de liquidación y se informa a sí misma en `skipped` cuando el material no trae los totales `partsTotal` y `laborTotal`, en lugar de suponer una composición. Su columna de descuento significa un importe de reducción; un registro que anote una tasa de descuento debería desactivar la regla o usar otra comprobación. |
| La fecha de entrega es anterior a la fecha de recepción. | `RO-005` señala esa fila: compara la fecha de recepción con la fecha de entrega y señala la fila cuando la recepción es posterior a la entrega. El mismo día cuenta como no posterior, una fecha que no puede analizar se informa en su propia fila en lugar de pasarse por alto, y no juzga si la reparación duró un tiempo razonable. |
| El mismo número de orden aparece en dos filas. | `RO-006` señala el número repetido, porque duplicaría las tarifas y rompería el vínculo entre una orden y su archivo; al comparar se ignoran los espacios. Una orden repartida en varias líneas de trabajo es una forma legítima: distinga esas filas en la columna del nombre del trabajo en lugar de repetir el número. La regla solo comprueba la unicidad. |
| La celda del nombre del trabajo aún dice 【】 o 待填. | `RO-007` señala la marca de plantilla que queda, porque una orden sin un trabajo real no se puede liquidar. La lista de `terms` que busca es la de su propio paquete de reglas y puede ajustarse a su plantilla. Solo comprueba si esas cadenas literales aparecen, no si la redacción es adecuada. |

## Normas que sigue

| Documento | Número | Reglas que lo citan |
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

| Superficie | Estado |
|---|---|
| Harness | Rango de peers `>=0.1.2-rc.1 <0.2.0 \|\| >=0.2.0-0 <0.3.0` — verificado para aceptar tanto `0.2.0-rc.2` como `0.2.1-alpha.1`. **No se declara `engines.dsh`**: no tiene lector y no puede rechazar ningún host |
| Node | `^22.19.0 || >=24.0.0` |
| Plataformas | Todas (ESM puro; sin código nativo, sin red, sin llamada al modelo) |
| Modo de herramienta | Funciona en `native`, `ptc` y `both`; para un directorio completo use `ptc` |

## What it does

La tabla de reglas, los campos y el comportamiento detallado están en [README.md](README.md#what-it-does) (versión principal en inglés). El plugin sólo enumera divergencias literales frente a las cláusulas citadas e indica en `skipped` cada comprobación que no pudo ejecutarse.

## Install

```sh
dsh plugin --profile <name> add dsh-repair-order-qc
dsh --profile <name> --dump-config | grep 'dsh-repair-order-qc'
```

## Configuration

Todos los parámetros ajustables viven en el esquema Schemastery de `src/config.ts`, por lo que se cambian desde `cordis.yml` sin tocar el código; los umbrales por regla están en el paquete de reglas bajo `rules/`.

| Clave | Tipo | Predeterminado | Descripción |
|---|---|---|---|
| `rulesFile` | string | `rules/repair-order-qc.yaml` | Ruta del paquete de reglas, relativa a la raíz del paquete |
| `disabledRules` | string[] | `[]` | Ids de reglas que se dejan de ejecutar; cada una aparece en `skipped` |
| `onlyRules` | string[] | `[]` | Ejecutar solo estas reglas; vacío ejecuta todas |
| `skipNotes` | string | `""` | Nota añadida a cada motivo de `skipped` |
| `timeoutMs` | number | `120000` | Presupuesto de tiempo de espera cooperativo de la herramienta |

## Material format

Acepta JSON o YAML. El ejemplo completo de campos está en [README.md](README.md#material-format) (versión principal en inglés). Los campos son opcionales en la capa de lectura y los valida el motor, de modo que una exportación parcial produce hallazgos sobre lo que falta en lugar de un fallo.

## Rule sources

Los datos de las reglas están separados del código: cada regla lleva documento, número, cláusula en la numeración propia de la fuente, extracto literal y URL de origen. El cargador impone que el extracto sea una cita real de al menos ocho caracteres y que una comprobación basada sólo en un principio general (`kind: derived-from-principle`, tope `warn`) o en una política local (`kind: institutional-configuration`, tope `info`) nunca se declare `error`.

Los límites verificados y las conclusiones deliberadamente **no** afirmadas están en [README.md](README.md#rule-sources) (versión principal en inglés) y en `rules/evidence/`.

## Troubleshooting

- **El plugin se instala pero la herramienta no aparece**: compruebe que `main` resuelve a `lib/index.mjs` y que `pnpm run build` lo generó.
- **`dsh plugin add` rechaza el paquete**: la faixa de peers cubre `0.1.x` y `0.2.x`; fuera de ella, conceda una exención explícita con `dsh plugin --profile <name> allow-version <pkg@ver> --dsh-version <runtime> --accept-risk`.
- **Una regla no se ejecutó**: lea el arreglo `skipped`.
- **`check` informa `manifest-peers` como fallo**: es un problema conocido de `dsh-plugin-dev`; el runtime aplica la compatibilidad al instalar.
- **Los horarios parecen desplazados**: toda la aritmética es de hora local sobre las cadenas entregadas.

## Development

```sh
pnpm install
pnpm run typecheck
pnpm test
pnpm run build
node ../scripts/sync-shared.mjs dsh-repair-order-qc
```

El último comando copia el kit compartido de `../_shared` a `src/shared/`; vuelva a ejecutarlo tras cada cambio compartido.

## License

[Apache License 2.0](LICENSE) © 2026 dsh-repair-order-qc contributors.
