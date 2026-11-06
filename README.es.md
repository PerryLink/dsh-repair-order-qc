<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/dsh-repair-order-qc-hero-en-dark.webp">
  <img src="docs/assets/dsh-repair-order-qc-hero-en-light.webp" width="100%" alt="Banner de dsh-repair-order-qc: la columna izquierda lleva el nombre del plugin y dos líneas de valor; a la derecha, una hoja de liquidación de reparación cuyas cuatro celdas de cabecera dan 360 + 200 − 0 = 560 y cuya línea de detalle da 2 × 180 = 360, mientras RO-001 señala las celdas vacías de manifestación del cliente y trabajo realizado y RO-003 señala el total de detalle 360 frente al total de liquidación 560; la lectura del informe es 2 incidencias, skipped 0, error 0 · warn 2 · info 0">
</picture>

# dsh-repair-order-qc

**Compruebe una orden de reparación de vehículos y reciba una lista fila por fila: qué fila, qué columna y qué difiere.**

Un verificador de DeepSeek Harness para recepción de taller y liquidación: el paquete de reglas es dato, cada una de sus siete reglas lleva su cita, y solo enumera diferencias — nunca dictamina.

[Instalar](#instalación-en-tres-pasos) · [Configuración](#configuración) · [FAQ](#faq) · [简体中文](README.md) · [English](README.en.md) · [Español](README.es.md) · [Português](README.pt.md) · [हिन्दी](README.hi.md)

[![License](https://img.shields.io/badge/license-Apache--2.0-3366CC?style=flat-square&labelColor=2B3245)](LICENSE)
[![DSH](https://img.shields.io/badge/DSH-%E2%89%A50.2.1%20%3C0.3.0-4B67B4?style=flat-square&labelColor=2B3245)](#compatibilidad)
[![npm](https://img.shields.io/npm/v/dsh-repair-order-qc?style=flat-square&labelColor=2B3245&color=CB3837)](https://www.npmjs.com/package/dsh-repair-order-qc)
[![CI](https://img.shields.io/github/actions/workflow/status/PerryLink/dsh-repair-order-qc/ci.yml?branch=main&label=CI&style=flat-square&labelColor=2B3245)](https://github.com/PerryLink/dsh-repair-order-qc/actions/workflows/ci.yml)
[![Node](https://img.shields.io/badge/node-%5E22.19%20%7C%7C%20%3E%3D24-339933?style=flat-square&labelColor=2B3245)](#compatibilidad)

[![Stars](https://img.shields.io/github/stars/PerryLink/dsh-repair-order-qc?style=flat-square&labelColor=2B3245)](https://github.com/PerryLink/dsh-repair-order-qc/stargazers)
[![npm downloads](https://img.shields.io/npm/dm/dsh-repair-order-qc?style=flat-square&labelColor=2B3245&color=CB3837)](https://www.npmjs.com/package/dsh-repair-order-qc)
[![dshfind](https://dshfind.com/api/badge/PerryLink/dsh-repair-order-qc?metric=downloads)](https://dshfind.com/plugins/PerryLink/dsh-repair-order-qc?ref=badge)
[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/PerryLink/dsh-repair-order-qc/badge)](https://securityscorecards.dev/viewer/?uri=github.com/PerryLink/dsh-repair-order-qc)
[![DSH Market](https://img.shields.io/badge/DSH_Market-listed-4B67B4?style=flat-square&labelColor=2B3245)](https://dsh.market/)
[![Gitee](https://img.shields.io/badge/Gitee-mirror-C71D23?style=flat-square&labelColor=2B3245&logo=gitee)](https://gitee.com/perrylink/dsh-repair-order-qc)

```sh
dsh plugin --profile <name> add dsh-repair-order-qc
```

</div>

<sub>Plugin de la comunidad, no afiliado a DeepSeek. Repositorio canónico: <https://github.com/PerryLink/dsh-repair-order-qc> (Gitee es un espejo).</sub>

## Qué es

`dsh-repair-order-qc` lee una orden de reparación de vehículos —la cabecera del vehículo más una fila por línea de trabajo— y comprueba la completitud y la aritmética de esa propia orden: que se registren la manifestación del cliente y el trabajo realizado, que la columna del nombre del trabajo esté rellenada, que la cantidad, el precio unitario y el importe se puedan analizar, que el importe sea igual a la cantidad × el precio unitario, que la suma de los importes de las líneas cuadre con la cifra de liquidación, que la cifra de liquidación sea igual a las piezas más la mano de obra menos el descuento, que la fecha de recepción no sea posterior a la fecha de entrega, que el número de orden sea único dentro de la orden y que no quede ninguna marca de plantilla en la columna del nombre del trabajo.

Lee un archivo y devuelve una lista: sin red, sin llamada a modelos, sin escritura en disco, así que el mismo material se puede comprobar una y otra vez; cambie el paquete de reglas y cambia el conjunto de reglas.

Si la reparación era necesaria, si el cargo es razonable, si la pieza es original — no juzga nada de eso: requiere el estado real del vehículo, las normas técnicas y el contrato de reparación.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/dsh-repair-order-qc-flow-v5-dark.svg">
  <img src="docs/assets/dsh-repair-order-qc-flow-v5-light.svg" width="100%" alt="Estructura de dsh-repair-order-qc: parseMaterial() normaliza el material en campos canónicos; el paquete de reglas exige al cargar extractos de al menos 8 caracteres y limita la gravedad por tipo de fundamento (direct puede llegar a error, derived-from-principle se limita a warn, institutional-configuration a info), mientras una puerta de citas vuelve a rastrear cada extracto de forma literal, y las siete reglas se publican como warn; la prueba de liquidación revisa las cuatro celdas de cabecera y la única línea de detalle, RO-001 y RO-003 se activan y las otras cinco se ejecutan sin diferencias, y issues[] (2) con skipped[] (0) se proyectan con buildView() en markdown / reportJson; la conclusión queda en manos de quien revisa">
</picture>

## Instalación en tres pasos

1. **Instalar** (publicado en npm):

   ```sh
   # canal npm (versiones publicadas)
   dsh plugin --profile web add dsh-repair-order-qc
   # canal tarball: tras pnpm pack en este repositorio
   dsh plugin --profile web add ./dsh-repair-order-qc-<version>.tgz
   ```

   Ejecutar desde un checkout del código exige antes `pnpm install && pnpm run build`: `main` apunta al artefacto compilado `lib/index.mjs`, nunca al código fuente.

2. **Configuración mínima** (los valores por defecto sirven; el parche de bundle inserta una fila y no necesita nada más):

   ```yaml
   - insert:
       - id: dsh-repair-order-qc
         name: dsh-repair-order-qc
   ```

3. **Verificar que se ha montado**:

   ```sh
   dsh --profile web --dump-config | grep -A2 'id: dsh-repair-order-qc'
   ```

   Después ejecute el ejemplo incluido; la salida real es (copiada de `docs/assets/quickstart.log`):

   ```sh
   pnpm run build && node samples/quickstart/run.mjs
   ```

   ```text
   $ node samples/quickstart/run.mjs
   repair_order_qc: 2 issue(s) — error 0, warn 2, info 0
   skipped: 0
   ```

   El material está en `samples/quickstart/input/RO-001-unsafe.json`, el resumen esperado en `samples/quickstart/expected/result.json` y la captura en [docs/assets/quickstart.png](docs/assets/quickstart.png).

**Desinstalar**: `dsh plugin --profile web remove dsh-repair-order-qc` (o borre esa fila del parche del perfil).

<details>
<summary>Instalar desde el mercado de DSH Desktop</summary>

Todos los plugins de PerryLink figuran en el mercado integrado de DSH Desktop: **Mercado → Fuentes → Añadir fuente → pegar** `https://perrylink-dsh-catalog.perrylink.workers.dev/catalog-source.json` **→ seleccionar**. La instalación sigue exigiendo la verificación de identidad npm del mercado y su confirmación.

</details>

## Capacidades clave

- **Un comando comprueba toda la orden** — registra la herramienta `repair_order_qc`, acepta `file` o `material` (JSON / YAML) y ejecuta las siete reglas de una vez.
- **El paquete de reglas es dato, no código** — las siete reglas viven en `rules/repair-order-qc.yaml` (versión del paquete `2026.1`); sustituir ese archivo cambia el conjunto de reglas sin tocar TypeScript.
- **Cada diferencia es trazable** — cada hallazgo lleva `document` / `number` / `clause` / `excerpt` / `source`: qué documento, qué cláusula, qué dice el texto y de dónde se leyó.
- **La gravedad sigue a la evidencia** — solo una comprobación cuyo texto de cláusula se leyó literalmente puede ser `error`; una base solo de principio queda limitada a `warn` y un umbral de política local a `info`. El cargador del paquete de reglas lo impone en vez de confiar en el autor.
- **Una lista vacía no es un certificado** — toda comprobación que no puede ejecutarse se informa en `skipped` con su motivo (columna ausente, desactivada por configuración…); nada pasa en silencio.
- **Solo diferencias, sin dictámenes** — sin conclusión de cumplimiento, sin atribución de responsabilidad, sin sustituir al revisor; cada informe lleva su aviso y un guardián de redacción bloquea las formulaciones taxativas.
- **Solo local** — sin red, sin llamadas a modelos, sin escritura en disco; el material y el informe se quedan en su máquina y en el registro de sesión del propio host.

### Cómo se ve la salida

| Campo | Significado |
|---|---|
| `summary` | recuentos de los niveles `error` / `warn` / `info` |
| `issueCount` / `skippedCount` | número de diferencias / número de comprobaciones no ejecutadas |
| `markdown` | la lista legible (esto es lo que renderiza la herramienta) |
| `reportJson` | el mismo informe como cadena JSON, para procesos posteriores |
| `rulesetVersion` | la versión del paquete de reglas, condición previa de un informe reproducible |

### Ejemplos

**Recorrido detallado** — herramienta `repair_order_qc`.

**Entrada**

~~~json
{"customer":"某某客户","vehicle":"某某车型","rows":[{"工单号":"WX-2026-0018","项目名称":"前制动片","客户反映":"","施工内容":""}]}
~~~

**Salida**

~~~json
{
  "id": "dsh-repair-order-qc.RO-001.de09b5a6",
  "ruleId": "RO-001",
  "severity": "warn",
  "locator": {
    "row": 1,
    "field": "customerConcern"
  },
  "found": "第 1 行 customerConcern、workDone 都为空",
  "expected": "customerConcern、workDone 至少应填写一项",
  "fix": "补填客户反映与施工内容；本条只核对是否记录，不判断维修是否必要"
}
~~~

*Observed from `dsh-repair-order-qc/tests/fixtures/RO-001/RO-001-unsafe.json (cases.json expects 1×RO-001); executed parseMaterial+runCheck, checkedAt=2026-10-06T00:00:00.000Z`*

El paquete de reglas no inventa citas, así que cada hallazgo nombra la cláusula en que se apoya y si esa base es texto literal o un principio.

| Usted pregunta | Qué responde |
|---|---|
| Una línea dice cantidad 2, precio unitario 180 y un importe de 400, ¿lo nota la comprobación? | Sí. `RO-002` señala esa fila, porque 2 × 180 = 360 mientras que la celda del importe dice 400. La regla solo se ejecuta cuando la cantidad, el precio unitario y el importe se pueden analizar como números, y su tolerancia es `0.01` para el redondeo. No juzga si el precio unitario es razonable ni si el concepto debía cobrarse. |
| Los importes de las líneas no cuadran con la cifra de liquidación escrita en la cabecera del material. | `RO-003` suma la columna `amount` y compara ese total con la cifra de liquidación `total` que declara la cabecera del material, e informa de cuántas filas sumó y de la magnitud de la diferencia. La tolerancia es `0.01`. Solo hace esa suma; no juzga si los cargos individuales son razonables. |
| Nuestras órdenes no traen total de piezas ni total de mano de obra, ¿aun así puede decirme que la cifra de liquidación está mal? | No, y lo dice. `RO-004` comprueba piezas más mano de obra menos descuento contra la cifra de liquidación y se informa a sí misma en `skipped` cuando el material no trae los totales `partsTotal` y `laborTotal`, en lugar de suponer una composición. Su columna de descuento significa un importe de reducción; un registro que anote una tasa de descuento debería desactivar la regla o usar otra comprobación. |
| La fecha de entrega es anterior a la fecha de recepción. | `RO-005` señala esa fila: compara la fecha de recepción con la fecha de entrega y señala la fila cuando la recepción es posterior a la entrega. El mismo día cuenta como no posterior, una fecha que no puede analizar se informa en su propia fila en lugar de pasarse por alto, y no juzga si la reparación duró un tiempo razonable. |
| El mismo número de orden aparece en dos filas. | `RO-006` señala el número repetido, porque duplicaría las tarifas y rompería el vínculo entre una orden y su archivo; al comparar se ignoran los espacios. Una orden repartida en varias líneas de trabajo es una forma legítima: distinga esas filas en la columna del nombre del trabajo en lugar de repetir el número. La regla solo comprueba la unicidad. |
| La celda del nombre del trabajo aún dice un marcador de plantilla (corchetes de ancho completo o «a rellenar»). | `RO-007` señala la marca de plantilla que queda, porque una orden sin un trabajo real no se puede liquidar. La lista de `terms` que busca es la de su propio paquete de reglas y puede ajustarse a su plantilla. Solo comprueba si esas cadenas literales aparecen, no si la redacción es adecuada. |

### Formato del material

Se aceptan JSON y YAML; el material es «cabecera del vehículo + una fila por línea de trabajo»:

~~~yaml
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
~~~

Los nombres de columna se comparan sin distinguir mayúsculas y minúsculas y ignorando espacios, guiones bajos y guiones; se conservan los nombres propios del registro, de modo que un hallazgo nombra la columna que realmente leyó. Las cifras que se declaran una vez para toda la orden (totales de piezas y mano de obra, cifra de liquidación) pueden estar en la cabecera, y las comprobaciones aritméticas las encuentran allí. Los campos son opcionales en el lector y los valida el motor de comprobación, así que un material exportado a medias produce diferencias de «valor ausente» en lugar de romperse. Un registro en Excel se puede convertir antes a JSON o YAML (también en el chat, si la plataforma lo permite); la herramienta solo lee el material y nunca modifica el original.

## Reglas y fuentes

### Las siete reglas

| Regla | Comprobación | Gravedad | Tipo de base |
|---|---|---|---|
| `RO-001` | se registran al menos una vez la manifestación del cliente y el trabajo realizado | warn | direct |
| `RO-002` | el importe es igual a cantidad × precio unitario | warn | direct |
| `RO-003` | la suma de los importes de las líneas cuadra con la cifra de liquidación | warn | direct |
| `RO-004` | el total es igual a piezas + mano de obra − descuento | warn | direct |
| `RO-005` | la fecha de entrega no es anterior a la de recepción | warn | derived-from-principle |
| `RO-006` | el número de orden es único dentro de la orden | warn | derived-from-principle |
| `RO-007` | la columna del nombre del trabajo no conserva marcadores de plantilla | warn | derived-from-principle |

### Las normas en que se apoya

| Documento | Número | Reglas que lo citan |
|---|---|---|
| Disposiciones sobre la administración del mantenimiento de vehículos de motor | Orden del Ministerio de Transportes n.º 18/2021 (promulgada en 2005; modificada cuatro veces en 2015, 2016, 2019 y 2021; en vigor desde el 1 de agosto de 2005) | RO-001, RO-002, RO-003, RO-004, RO-005, RO-006, RO-007 |

**Límite:** este plugin comprueba una **orden de reparación de vehículos de motor** en su aritmética y su completitud — que se registren la manifestación del cliente y el trabajo realizado, que el importe de una línea sea igual a cantidad × precio unitario, que la suma de las líneas cuadre con la cifra de liquidación, que la cifra de liquidación sea igual a piezas más mano de obra menos descuento, que la entrega no preceda a la recepción, que el número de orden se use de forma coherente y que no quede ningún marcador. **No** decide si una reparación era necesaria, si un cargo es razonable, si hubo sobreventa de servicios ni si el trabajo se hizo bien.

> ### ⚠️ Comprueba la aritmética, no la reparación
>
> Una orden con cifras perfectamente coherentes para un trabajo que nunca debió venderse pasa este plugin. Juzgar la necesidad y el precio exige el estado real del vehículo, las normas técnicas y el contrato de reparación: este plugin no tiene nada de eso.
>
> **La tarifa de mano de obra viene del registro o de su configuración.** No hay ninguna tarifa estándar incorporada. Tampoco comprueba si una pieza es original; informa de lo que dice el registro.
>
> Dos reglas aritméticas leen la composición del registro y **ambas lo dicen cuando no pueden ejecutarse**:
>
> - `RO-002` verifica `importe = cantidad × precio unitario` e informa de sí misma en `skipped` a menos que las tres celdas se analicen. Su tolerancia es `0.01`, para el redondeo.
> - `RO-004` verifica `total de piezas + total de mano de obra − descuento = cifra de liquidación`. La resta se expresa como un **signo por término** en el paquete de reglas (`signs: [1, 1, -1]`) y no como una escala negativa, de modo que el hallazgo se lee como la aritmética que escribiría una persona. Un registro sin desglose de piezas/mano de obra deja la regla sin ejecutar en lugar de suponer una composición.
>
> **El paquete de reglas no inventa citas.** El `excerpt` de `RO-001`–`RO-004` es texto literal obtenido el 2026-10-07 (artículos 26 y 33; los registros de verificación están en `rules/evidence/`); `RO-005`–`RO-007` no tienen una cláusula que se pueda citar literalmente, así que su `kind` sigue siendo `derived-from-principle` y su gravedad queda limitada a `warn`. `check:citations` rastrea cada segmento de los extractos hasta esos registros, y la puerta de citas se ejecuta en CI.

### Origen y verificación de las reglas

Los datos de las reglas están en `rules/repair-order-qc.yaml`. Cada regla lleva un documento, un número, una cláusula en la numeración propia de la fuente, un extracto literal y la URL de donde se leyó. El cargador impone que un extracto sea una cita real de al menos ocho caracteres, y que una comprobación cuya base sea solo un principio general (`kind: derived-from-principle`, limitada a `warn`) o una política local (`kind: institutional-configuration`, limitada a `info`) no pueda declararse nunca `error`. Un paquete que exagera su base falla al cargar en lugar de producir un informe con tono seguro.

Los números de cláusula se cotejaron con el texto completo vigente de las Disposiciones (siete capítulos, 55 artículos, con la modificación de 2021). Tres conclusiones dieron forma al paquete y se registran aquí para que un revisor vea lo que deliberadamente **no** se afirma:

1. **`RO-005` no tiene cláusula explícita.** Las Disposiciones no contienen ningún requisito de que la fecha de entrega no sea anterior a la de recepción; el artículo 32 trata de **la entrega solo tras superar la inspección de terminación**, que nada dice del orden de dos fechas. La regla es por tanto la coherencia temporal del propio registro, su campo `clause` lo dice y su `kind` sigue en `derived-from-principle` (limitada a `warn`).
2. **La modificación de 2021 cambió exactamente una cosa, y fuera de los artículos citados.** La cuarta modificación suprimió una frase del artículo 53; los artículos 26, 32 y 33 se leen igual en el texto de 2019 y en el de 2021. Cítese la «Orden del Ministerio de Transportes n.º 18/2021, modificada», no la Orden n.º 20 de 2019.
3. **«Solo aritmética» es una decisión de alcance que el texto respalda.** El artículo 26 exige que la lista de liquidación exprese **por separado** mano de obra y materiales e incluya un **desglose de costes**: regula la partida, el detalle y la trazabilidad, no el nivel de los precios. El «cobro razonable» del artículo 25 es cualitativo y no fija importe; por eso «¿es razonable el precio unitario?» no se puede decidir desde un registro. El artículo 30 prohíbe **piezas falsificadas o de mala calidad** y exige trazabilidad, y admite expresamente piezas de calidad equivalente, así que «¿es original esta pieza?» tampoco es un criterio de esta norma.

Artículos **registrados pero no activados**: artículo 30 (trazabilidad de piezas), artículo 31 (los tres regímenes de inspección), los requisitos de archivo más allá de los artículos 32 y 33, y el artículo 36 (plazos de garantía de calidad de la reparación: 20.000 km o 100 días para vehículo completo o conjunto, 5.000 km o 30 días para mantenimiento de segundo nivel, 2.000 km o 10 días para mantenimiento de primer nivel, reparación menor o trabajo especial — lo que ocurra primero). ⚠️ **El plazo de garantía de la reparación (artículo 36) no es el plazo de garantía de las «tres garantías» del automóvil**; ambos se apoyan en documentos distintos y no deben mezclarse. La verificación completa y los artículos registrados sin usar están en [`rules/evidence/clause-verification-repair-regulation.md`](rules/evidence/clause-verification-repair-regulation.md) y [`rules/evidence/clause-verification-jdcwxgd.md`](rules/evidence/clause-verification-jdcwxgd.md).

## Configuración

Todos los parámetros están en el esquema Schemastery de `src/config.ts`; basta cambiar `cordis.yml` para que surtan efecto, sin tocar código. Los umbrales de cada comprobación están en el paquete de reglas `rules/repair-order-qc.yaml`.

| Clave | Tipo | Valor por defecto | Descripción |
|---|---|---|---|
| `rulesFile` | string | `rules/repair-order-qc.yaml` | Ruta del paquete de reglas, relativa a la raíz del paquete; sustituir el archivo cambia la versión del conjunto de reglas |
| `disabledRules` | string[] | `[]` | Ids de reglas a desactivar; cada una aparece en `skipped` |
| `onlyRules` | string[] | `[]` | Ejecutar solo estos ids; vacío ejecuta todas las reglas |
| `skipNotes` | string | `""` | Nota añadida a cada motivo de `skipped`, p. ej. para citar su política local |
| `timeoutMs` | number | `120000` | Presupuesto de tiempo de espera cooperativo de la herramienta, en milisegundos |

Parámetros por regla que conviene conocer:

- `RO-002` `resultField` / `factorFields` / `tolerance` — la multiplicación de la línea; `tolerance` vale `0.01` por defecto.
- `RO-003` `field` / `headerField` / `tolerance` — la columna sumada y la cifra de cabecera con la que debe cuadrar.
- `RO-004` `expression` — la composición, como `{ "op": "sum", "fields": [...], "signs": [1, 1, -1] }`. Cambie los signos si su liquidación se compone de otro modo; un registro que anote una **tasa** de descuento en lugar de un importe debería desactivar la regla.
- `RO-007` `terms` — las cadenas de marcador que se buscan.

Ejemplo de sobrescritura en el parche del perfil:

~~~yaml
- insert:
    - id: dsh-repair-order-qc
      name: dsh-repair-order-qc
      config:
        disabledRules: [RO-004]
        onlyRules: []
        skipNotes: política local 2026
        timeoutMs: 120000
~~~

## FAQ

<details>
<summary>¿Se sube o se envía a algún sitio el material? ¿Dónde se guardan los datos?</summary>

No. Solo lee el contenido del documento que usted pasa a sus herramientas: sin red, sin telemetría, sin escritura en disco, sin subida. Aparte del resultado de la herramienta y del almacenamiento de sesión/registros del propio host DSH, este paquete no guarda nada; ese almacenamiento lo controla el host y su retención la decide el host — este paquete nunca añade una segunda copia. Véase [PRIVACY.md](PRIVACY.md).

</details>

<details>
<summary>El resultado es «0 diferencias», ¿significa que no hay nada mal? ¿Y si una regla no se ejecutó?</summary>

«0 diferencias» solo significa que **las comprobaciones ejecutadas no hallaron diferencias literales**; no significa que la orden cumpla. Toda comprobación que no puede ejecutarse se informa en `skipped` con su motivo (columna ausente, desactivada por `disabledRules`…), así que un resultado vacío no puede leerse como «no hay nada mal». Si la herramienta no aparece, confirme primero que existe el `lib/index.mjs` al que apunta `main`: un checkout del código exige `pnpm run build` y el tarball publicado ya trae el artefacto.

</details>

<details>
<summary>¿Me dará un dictamen de cumplimiento o bloqueará una liquidación?</summary>

No. No emite conclusión de cumplimiento, no atribuye responsabilidad y no juzga si una reparación era necesaria o un cargo razonable; nunca bloquea ningún proceso. Cada informe lleva su aviso y un guardián de redacción bloquea las formulaciones taxativas. Lo que recibe es una lista de diferencias para revisión humana: qué fila, qué columna, qué difiere y qué cláusula lo respalda.

</details>

<details>
<summary>`RO-004` se omitió, `RO-002` señaló una línea que considero redondeada, `RO-006` informó dos veces de la misma orden — ¿qué hago?</summary>

Las tres son cuestiones de alcance de la regla, no fallos. `RO-004` solo se ejecuta si la cabecera trae `partsTotal` y `laborTotal`; sin ellos se informa en `skipped` en lugar de suponer una composición. Su columna de descuento es un importe de reducción, así que un registro que anote una tasa debería desactivarla. `RO-002` tolera `0.01` por defecto: suba `tolerance` si su tarificación redondea más grueso. `RO-006` solo comprueba unicidad: una orden repartida en varias líneas de trabajo es normal, y si su registro comparte el número entre líneas por diseño, desactive la regla.

</details>

<details>
<summary>¿Y si la instalación informa de un conflicto de versiones, o `check` informa de `manifest-peers` como fallido?</summary>

El rango de peers cubre las líneas `0.1.x` y `0.2.x`. Si su runtime queda fuera, conceda una exención explícita: `dsh plugin --profile <name> allow-version dsh-repair-order-qc@0.2.11 --dsh-version <runtime> --accept-risk`. El fallo de `manifest-peers` es un problema conocido de `dsh-plugin-dev`: el verificador estático compara con un rango de peers codificado que es anterior a la línea 0.2, mientras que la instalación la valida el runtime. Más diagnóstico en [TROUBLESHOOTING.md](TROUBLESHOOTING.md).

</details>

## Límites de seguridad

- **Solo local, sin superficie de salida.** Sin peticiones de red, sin llamadas a modelos, sin telemetría; `package.json#dsh.demo` también declara `network: false`, `writes: []` y `external: []`.
- **Una regla con base insuficiente no puede ser `error`.** El cargador del paquete exige que `excerpt` sea una cita literal de al menos ocho caracteres y limita la gravedad según `kind`: `derived-from-principle` como máximo `warn`, `institutional-configuration` como máximo `info`. La puerta de citas comprueba además que cada extracto se pueda rastrear a un registro de verificación en `rules/evidence/`.
- **Solo diferencias, sin dictamen.** Los informes no afirman cumplimiento, infracción, responsabilidad ni corrección; el guardián de redacción lo impone en la capa de renderizado.
- **Un resultado vacío no es una absolución.** Una comprobación no ejecutada debe figurar en `skipped` con su motivo; una regla cuyos campos requeridos faltan se informa como no ejecutada en lugar de pasar por defecto.
- **El registro es un efecto.** La herramienta se registra con `ctx.tools.register`, que devuelve el disposer; desactivar el plugin o recargarlo en caliente la retira sin dejar registros colgados.
- **Sin escritura en disco.** Aparte del resultado de la herramienta y del almacenamiento de sesión del host, este paquete no crea ni modifica ningún archivo.

## Permisos y datos

- **Permisos**: solo lee el material que pasa quien llama (una ruta `file` o un `material` en línea); no ofrece ninguna clave de servicio y no registra slots de cliente ni rutas HTTP. `inject` es exactamente `tools`.
- **Datos**: el material participa en la comparación solo dentro de este proceso; el plugin no conserva copia, ni caché, ni archivo. Cómo registre el host los resultados de la herramienta es asunto del host; este paquete no añade una segunda copia.
- **Dependencias**: cero dependencias en tiempo de ejecución (no hay campo `dependencies`); los peers son Cordis, `dsh-tools` y Schemastery, todos ya cargados por el host.

## Limitaciones conocidas

- **Solo diferencias literales.** No decide qué valor es el verdadero, ni si una reparación era necesaria o un cargo razonable, ni decide por el revisor; cuando dos campos chocan, enumera el choque en sí.
- **`RO-005`–`RO-007` no tienen cláusula literal.** Su base es un principio, `kind` es `derived-from-principle` y la gravedad queda limitada a `warn`; el «la entrega no es anterior a la recepción» de `RO-005` no está literalmente en la norma.
- **La forma del material es fija.** Lee una tabla «cabecera del vehículo + una fila por línea de trabajo»; una orden con otra forma no produce conclusión, y un valor ausente aparece como diferencia de valor ausente en lugar de una suposición.
- **La columna de descuento significa un importe de reducción.** Un registro que anote una tasa de descuento, o cuya liquidación no sea «piezas + mano de obra − descuento», debería desactivar `RO-004` o usar otra comprobación.
- **`RO-006` informa de una repetición cuando una orden abarca varias líneas.** Es el comportamiento previsto de una regla de unicidad; si su registro comparte el número entre líneas por diseño, desactívela.
- **La forma de desarrollo exige compilar.** En un checkout del código `main` apunta a `lib/index.mjs`, así que antes debe ejecutarse `pnpm run build`; el tarball publicado de npm trae `lib/` y funciona tal cual.
- **El tiempo es de reloj de pared.** Todo cálculo de fechas es aritmética de reloj de pared sobre las cadenas de entrada, sin conversión de zona horaria; los desfases de la entrada nunca participan en una comparación.
- **Un falso positivo conocido del verificador estático upstream.** El `manifest-peers` de `check` compara con un rango de peers codificado anterior a la línea 0.2, que no concuerda con la validación del runtime en la instalación.

## Interoperabilidad con otros plugins DSH

Este plugin **no interfiere** con otros plugins del mismo perfil:

- **Añade exactamente una herramienta.** Solo se registra `repair_order_qc`, vía `ctx.tools.register`, que devuelve el disposer; no ocupa ningún nombre desnudo de una herramienta integrada y desaparece al desinstalar.
- **Sin claves de servicio.** `inject` es solo `tools`; no se registra ninguna clave de servicio de Cordis, así que no hay conflicto de claves.
- **Sin slots ni rutas.** El paquete no tiene mitad de navegador (no hay `client/`), no registra claves de slot de cliente ni prefijos `webServer`.
- **La capa de parche inserta solo su fila.** `cordis.patch.yml` añade únicamente la fila `id: dsh-repair-order-qc` y nunca sobrescribe el `config` de una fila integrada o ajena.
- **Sin reescrituras globales.** Sin parcheo de prototipos, sin escrituras en `process.env`, sin reemplazo del fetch global.
- **División de trabajo, no competencia, con verificadores hermanos.** El mismo material puede ir a otros verificadores: este plugin comprueba la aritmética y la completitud de la propia orden; las «tres garantías» del automóvil son competencia de `dsh-warranty-calc` (**un plazo de garantía de reparación no es un plazo de tres garantías** — bases distintas); la trazabilidad de piezas queda fuera de este plugin (registrada en el paquete de reglas pero no activada). Cada plugin lee su archivo y produce su informe, sin modificar nada ni compartir estado.

## Compatibilidad

| Dimensión | Estado |
|---|---|
| Harness | Rango de peers `>=0.1.2-rc.1 <0.2.0 \|\| >=0.2.0-0 <0.3.0`, medido para aceptar tanto `0.2.0-rc.2` como `0.2.1-rc.2`; `engines.dsh` declara `>=0.2.1-0 <0.3.0`, impuesto por el host desde 0.2.1 |
| Node | `^22.19.0 \|\| >=24.0.0` |
| Plataformas | Todas (ESM puro; sin código nativo, sin red, sin llamadas a modelos) |
| Modo de herramienta | Sirve `native` y `ptc`; para un mes de órdenes use `ptc` |
| Material | JSON / YAML; cabecera del vehículo + una lista `rows` |

## Ecosistema y calidad

- [Espejo en Gitee](https://gitee.com/perrylink/dsh-repair-order-qc) (espejo sincronizado; GitHub es la referencia)
- [Página del plugin en dshfind](https://dshfind.com/plugins/PerryLink/dsh-repair-order-qc) (instalaciones y ranking)
- [Informe OpenSSF Scorecard](https://securityscorecards.dev/viewer/?uri=github.com/PerryLink/dsh-repair-order-qc) (impulsado por [.github/workflows/scorecard.yml](.github/workflows/scorecard.yml))
- [DSH Market](https://dsh.market/) (publicado)

## Desarrollo

```sh
pnpm install
pnpm run typecheck          # tsc --noEmit
pnpm test                   # vitest: la suite compartida de plugins de tabla más un par de fixtures conforme/infractor por regla
pnpm run build              # tsdown -> lib/index.mjs + lib/index.d.mts
pnpm run verify:self-contained
pnpm run check:lockfile
pnpm run check:readmes      # coherencia de los README: la edición inglesa frente a la fuente china
pnpm run check:citations    # cada extracto es rastreable a rules/evidence/
pnpm pack                   # el tarball publicado
node samples/quickstart/run.mjs   # requiere compilar antes
```

`node ../scripts/sync-shared.mjs dsh-repair-order-qc` copia el kit compartido de `../_shared` a `src/shared/`; vuelva a ejecutarlo tras cada cambio del kit. El plugin es **guiado por datos**: `src/model.ts` declara la forma de la tabla, el kit compartido aporta el lector y el motor de comprobación, y el paquete de reglas declara cada comprobación.

Estructura de directorios:

| Ruta | Función |
|---|---|
| `src/index.ts` | entrada de plugin-función: `name` / `inject` / `Config` / `apply`, registra `repair_order_qc` y resuelve el paquete de reglas |
| `src/config.ts` | esquema Schemastery; aquí vive cada parámetro |
| `src/model.ts` | forma de la tabla y contrato del material: alias de columnas, la clave `rows`, campos de cabecera; `parseMaterial` / `runCheck` vienen del kit compartido |
| `src/view.ts` | la proyección del informe orientada al modelo; `output.schema` la refleja |
| `src/shared/` | el kit compartido (cargador del paquete de reglas, forma del informe, subconjunto de YAML, aritmética de calendario, guardián de redacción, utilidades de tabla), copiado en lugar de importado |
| `rules/repair-order-qc.yaml` | el paquete de reglas, 7 reglas; `rules/evidence/` guarda el registro de verificación de cada cita |
| `tests/` | vitest; un par de fixtures conforme/infractor por regla |

Topics: `deepseek-harness`, `dsh`, `dsh-plugin`, `cordis`, `repair`, `order`

Las imágenes del README las genera por programa [`scripts/gen-readme-assets.py`](scripts/gen-readme-assets.py) —el banner hero con Pillow y el diagrama de estructura como SVG escrito a mano— y se pueden regenerar en cualquier momento; los antiguos `dsh-repair-order-qc-flow*.svg`, la captura de terminal y el GIF de demostración se conservan en `docs/assets/` para los enlaces existentes, mientras que los README solo referencian el nuevo hero (cuatro archivos, zh/en × claro/oscuro) y el diagrama flow-v5 (claro y oscuro).

## Familia y agradecimientos

Este proyecto es miembro de la familia de plugins de DeepSeek Harness mantenida por [PerryLink](https://github.com/PerryLink) (todos Apache-2.0). Si este plugin le ha servido, **dele una estrella**: no desbloquea nada, pero hace que la siguiente persona lo encuentre antes.

- [@PerryLink](https://github.com/PerryLink) — creador y mantenedor: el paquete de reglas y el núcleo de comprobación, la puerta de citas y los registros de verificación, la herramienta `repair_order_qc` y la documentación en cinco idiomas.

Elija un verificador por material (índice completo de la familia): <https://perrylink.github.io/zh/checkers/choose/> · [todos los plugins](https://github.com/PerryLink)

## Licencia

[LICENSE](LICENSE) (Apache License 2.0) © 2026 dsh-repair-order-qc contributors

<p align="center"><sub>Apache-2.0 · Plugin de la comunidad, no afiliado a DeepSeek.</sub></p>
