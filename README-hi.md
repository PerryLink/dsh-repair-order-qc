# dsh-repair-order-qc — मोटर वाहन मरम्मत कार्य-आदेश रजिस्टर और निपटान अंकगणित की जाँच

[English](README.md) · [简体中文](README-zh.md) · [Español](README-es.md) · [Português](README-pt.md) · [हिन्दी](README-hi.md)

[![DSH Market](https://raw.githubusercontent.com/2BingLing/dsh-market/master/assets/readme/badge-listed-en.svg)](https://dsh.market/)
[![dshfind](https://dshfind.com/api/badge/PerryLink/dsh-repair-order-qc?metric=downloads)](https://dshfind.com/en/plugins/PerryLink/dsh-repair-order-qc?ref=badge)

`dsh-repair-order-qc` मोटर वाहन मरम्मत कार्य-आदेश का एक रजिस्टर पढ़ता है — वाहन हेडर और प्रत्येक कार्य-पंक्ति की एक पंक्ति — और उसी रजिस्टर की पूर्णता तथा अंकगणित की जाँच करता है: ग्राहक की बताई बात और किया गया कार्य दर्ज हैं या नहीं, कार्य के नाम का कॉलम भरा है या नहीं, मात्रा, इकाई मूल्य और राशि पढ़ी जा सकती हैं या नहीं, राशि मात्रा × इकाई मूल्य के बराबर है या नहीं, पंक्तियों की राशियों का जोड़ निपटान राशि से मेल खाता है या नहीं, निपटान राशि पुर्ज़ों की राशि में से छूट घटाकर मज़दूरी जोड़ने के बराबर है या नहीं, प्राप्ति तिथि वितरण तिथि के बाद नहीं पड़ती, रजिस्टर में कार्य-आदेश क्रमांक अद्वितीय हैं या नहीं, और कार्य के नाम के कॉलम में कोई टेम्पलेट प्लेसहोल्डर शेष नहीं है।

## Install

```sh
dsh plugin --profile <name> add dsh-repair-order-qc
dsh --profile <name> --dump-config | grep 'dsh-repair-order-qc'
```

## आउटपुट कैसा दिखता है

![dsh-repair-order-qc कार्यप्रवाह आरेख: कॉल → प्लगइन → परिणाम।](docs/assets/dsh-repair-order-qc-flow.svg)

*कार्यप्रवाह: कॉल → प्लगइन → परिणाम। नीचे के उदाहरण वास्तविक कमांड सतह का उपयोग करते हैं।*


इस प्लगइन का अपने ही `RO-001` टेस्ट फ़िक्स्चर पर वास्तविक आउटपुट — कोई नकली चित्र नहीं। नियम-पैक उद्धरण नहीं गढ़ता, इसलिए हर निष्कर्ष लागू किए गए खंड का नाम और यह भी बताता है कि उसका मूल पाठ इस बार प्राप्त नहीं हुआ।

## यह किन सवालों का जवाब देता है

### उदाहरण

नीचे दी गई तालिका उदाहरण-समुच्चय है: पहली पंक्ति विस्तृत केस है, बाकी संक्षिप्त केस हैं।

#### विस्तृत आउटपुट

**उपकरण** `repair_order_qc`

**इनपुट**

~~~json
{"customer":"某某客户","vehicle":"某某车型","rows":[{"工单号":"WX-2026-0018","项目名称":"前制动片","客户反映":"","施工内容":""}]}
~~~
 
**आउटपुट**

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

*स्रोत `dsh-repair-order-qc/tests/fixtures/RO-001/RO-001-unsafe.json (cases.json expects 1×RO-001); executed parseMaterial+runCheck, checkedAt=2026-10-06T00:00:00.000Z`*

| आपका सवाल | इसका जवाब |
|---|---|
| एक पंक्ति में मात्रा 2, इकाई मूल्य 180 और राशि 400 लिखी है — क्या जाँच इसे पकड़ती है? | हाँ। `RO-002` उस पंक्ति को दर्ज करता है, क्योंकि 2 × 180 = 360 है जबकि राशि की कोशिका में 400 लिखा है। यह नियम तभी चलता है जब मात्रा, इकाई मूल्य और राशि तीनों संख्या के रूप में पढ़ी जा सकें, और दशमलव पूर्णांकन के लिए इसकी सहनशीलता `0.01` है। यह नहीं आँकता कि इकाई मूल्य उचित है या उस मद का शुल्क लिया ही जाना चाहिए था। |
| पंक्तियों की राशियों का जोड़ सामग्री के हेडर में लिखी निपटान राशि से मेल नहीं खाता। | `RO-003` `amount` कॉलम को जोड़कर उस जोड़ की तुलना सामग्री हेडर में घोषित निपटान राशि `total` से करता है, और बताता है कि कितनी पंक्तियाँ जोड़ी गईं तथा अंतर कितना है। सहनशीलता `0.01` है। यह केवल वह जोड़ करता है; यह नहीं आँकता कि अलग-अलग शुल्क उचित हैं या नहीं। |
| हमारे कार्य-आदेशों में पुर्ज़ों का कुल और मज़दूरी का कुल नहीं है — क्या तब भी यह बता सकता है कि निपटान राशि ग़लत है? | नहीं, और यह यह भी बताता है। `RO-004` पुर्ज़े जमा मज़दूरी घटा छूट की तुलना निपटान राशि से करता है और जब सामग्री में `partsTotal` तथा `laborTotal` के कुल न हों तो स्वयं को `skipped` में दर्ज करता है, किसी संरचना का अनुमान नहीं लगाता। इसका छूट-कॉलम छूट की राशि के अर्थ में है; जो रजिस्टर छूट-दर दर्ज करता है उसे यह नियम बंद करना चाहिए या कोई अन्य जाँच अपनानी चाहिए। |
| वितरण तिथि प्राप्ति तिथि से पहले की है। | `RO-005` उस पंक्ति को दर्ज करता है: यह प्राप्ति तिथि की तुलना वितरण तिथि से करता है और जब प्राप्ति वितरण के बाद पड़ती है तो वह पंक्ति दर्ज करता है। एक ही दिन को «बाद में नहीं» माना जाता है, जो तिथि पढ़ी न जा सके वह चुपचाप छोड़े जाने के बजाय उसी पंक्ति पर दर्ज होती है, और यह नहीं आँकता कि मरम्मत में उचित समय लगा या नहीं। |
| एक ही कार्य-आदेश क्रमांक दो पंक्तियों में आया है। | `RO-006` दोहराया गया क्रमांक दर्ज करता है, क्योंकि इससे शुल्क दो बार जुड़ जाते हैं और कार्य-आदेश तथा उसके अभिलेख का संबंध टूट जाता है; तुलना करते समय रिक्त स्थान अनदेखे किए जाते हैं। एक ही कार्य-आदेश का कई कार्य-पंक्तियों में फैला होना सामान्य है — ऐसी पंक्तियों को क्रमांक दोहराने के बजाय कार्य के नाम के कॉलम में अलग दिखाएँ। यह नियम केवल अद्वितीयता देखता है। |
| कार्य के नाम की कोशिका में अब भी 【】 या 待填 लिखा है। | `RO-007` शेष बचा टेम्पलेट प्लेसहोल्डर दर्ज करता है, क्योंकि बिना वास्तविक कार्य वाले आदेश का निपटान नहीं हो सकता। यह जिन `terms` को खोजता है वे उसके अपने नियम-पैक की सूची हैं और आपके टेम्पलेट के अनुसार बदली जा सकती हैं। यह केवल देखता है कि वे अक्षर-समूह दिखते हैं या नहीं, यह नहीं कि शब्दावली उपयुक्त है या नहीं। |

## यह किन मानकों पर आधारित है

| दस्तावेज़ | संख्यांक | इन्हें उद्धृत करने वाले नियम |
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

| सतह | स्थिति |
|---|---|
| Harness | peer रेंज `>=0.1.2-rc.1 <0.2.0 \|\| >=0.2.0-0 <0.3.0` — `0.2.0-rc.2` और `0.2.1-rc.2` दोनों को स्वीकार करने के लिए सत्यापित। **`engines.dsh` `>=0.2.1-0 <0.3.0` के रूप में घोषित है** और 0.2.1 से होस्ट इसे लागू करता है |
| Node | `^22.19.0 || >=24.0.0` |
| प्लेटफ़ॉर्म | सभी (शुद्ध ESM; कोई नेटिव कोड नहीं, कोई नेटवर्क नहीं, कोई मॉडल कॉल नहीं) |
| टूल मोड | `native` और `ptc` में काम करता है; पूरे फ़ोल्डर के लिए `ptc` चुनें |

## What it does

नियम-सूची, फ़ील्ड और विस्तृत व्यवहार [README.md](README.md#what-it-does) (अंग्रेज़ी मुख्य संस्करण) में हैं। यह प्लगइन केवल उद्धृत धाराओं के सामने शाब्दिक अंतर सूचीबद्ध करता है और हर न चल पाई जाँच को `skipped` में बताता है।

## Configuration

सभी समायोज्य पैरामीटर `src/config.ts` की Schemastery स्कीमा में हैं, इसलिए कोड बदले बिना `cordis.yml` से बदले जा सकते हैं; प्रति-नियम सीमाएँ `rules/` के नियम-पैक में हैं।

| कुंजी | प्रकार | डिफ़ॉल्ट | विवरण |
|---|---|---|---|
| `rulesFile` | string | `rules/repair-order-qc.yaml` | नियम-पैक का पथ, पैकेज रूट के सापेक्ष |
| `disabledRules` | string[] | `[]` | बंद करने वाले नियम id; प्रत्येक `skipped` में दिखता है |
| `onlyRules` | string[] | `[]` | केवल ये नियम चलाएँ; खाली होने पर सभी नियम चलते हैं |
| `skipNotes` | string | `""` | हर `skipped` कारण के आगे जोड़ी जाने वाली टिप्पणी |
| `timeoutMs` | number | `120000` | उपकरण का सहकारी समय-सीमा बजट |

## Material format

JSON या YAML स्वीकार्य है। पूरा फ़ील्ड उदाहरण [README.md](README.md#material-format) (अंग्रेज़ी मुख्य संस्करण) में है। पढ़ने की परत में फ़ील्ड वैकल्पिक हैं और जाँच इंजन उन्हें सत्यापित करता है, इसलिए आंशिक निर्यात पर क्रैश के बजाय "अनुपस्थित" श्रेणी के निष्कर्ष मिलते हैं।

## Rule sources

नियम-डेटा कोड से अलग है: प्रत्येक नियम में दस्तावेज़, संख्या, स्रोत की अपनी क्रमांकन-प्रणाली के अनुसार धारा, शब्दशः उद्धरण और स्रोत URL होता है। लोडर लागू करता है कि उद्धरण कम से कम आठ अक्षरों का वास्तविक उद्धरण हो, और जिस जाँच का आधार केवल सामान्य सिद्धांत (`kind: derived-from-principle`, अधिकतम `warn`) या स्थानीय नीति (`kind: institutional-configuration`, अधिकतम `info`) हो, उसे कभी `error` घोषित न किया जाए।

सत्यापित सीमाएँ और जान-बूझकर **न** कहे गए निष्कर्ष [README.md](README.md#rule-sources) (अंग्रेज़ी मुख्य संस्करण) और `rules/evidence/` में हैं।

## Troubleshooting

- **प्लगइन इंस्टॉल हो गया पर टूल दिखता नहीं**: जाँचें कि `main` `lib/index.mjs` पर जाता है और `pnpm run build` ने उसे बनाया है।
- **`dsh plugin add` असंगत बताकर मना करता है**: peer range `0.1.x` और `0.2.x` दोनों को कवर करती है; बाहर होने पर स्पष्ट छूट दें: `dsh plugin --profile <name> allow-version <pkg@ver> --dsh-version <runtime> --accept-risk`।
- **कोई नियम नहीं चला**: `skipped` सरणी देखें।
- **`check` में `manifest-peers` विफल दिखता है**: यह `dsh-plugin-dev` की ज्ञात अपस्ट्रीम समस्या है; रनटाइम इंस्टॉल के समय अनुकूलता लागू करता है।
- **समय खिसका हुआ लगता है**: सारी गणना दिए गए स्ट्रिंग पर वॉल-क्लॉक है।

## Development

```sh
pnpm install
pnpm run typecheck
pnpm test
pnpm run build
node ../scripts/sync-shared.mjs dsh-repair-order-qc
```

अंतिम कमांड `../_shared` का साझा किट `src/shared/` में कॉपी करता है; हर साझा बदलाव के बाद इसे दोबारा चलाएँ।

## PerryLink DSH Plugin Family

Full family index: [choose a checker by material](https://perrylink.github.io/zh/checkers/choose/) and [all plugins](https://github.com/PerryLink). This repository is one of them.

## License

[Apache License 2.0](LICENSE) © 2026 dsh-repair-order-qc contributors.
