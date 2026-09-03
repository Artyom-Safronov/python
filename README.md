# Template-engine demo suite

Шесть небольших рабочих приложений — по одному на движок шаблонизации, каждое со
своим каталогом товаров (Keyboard / Mouse / Monitor), общей навигацией и страницей
About. Задача — дать плагину [python-frameworks-for-openide](https://gitflic.ru/project/sazonovfm/python-frameworks-for-openide)
реальный материал для live-verify новых фич поддержки шаблонизаторов (spec 006 и
последующие), помимо уже существующих `rw-django` / `rw-flask` / `rw-fastapi`.

Все приложения независимы, у каждого свой `.venv` (не в git) и `requirements.txt`.

## Как запустить любое приложение

```bash
cd <папка-приложения>
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python app.py        # для Flask-приложений — открыть http://127.0.0.1:5000
# для Django-приложений вместо этого:
.venv/bin/python manage.py migrate
.venv/bin/python manage.py runserver
```

## Приложения

### `jinja2-flask-demo/` — Jinja2 (Flask)
Канонический случай: Flask + `render_template()`. `base.html` + `{% extends %}` +
`{% include %}` партиалы (`_nav.html`, `_footer.html`), Jinja-макрос
(`_macros.html`), фильтры (`|upper`, `|format`), контекст через `**kwargs`
(`render_template("index.html", **{...})`) и через keyword-аргументы
(`render_template(..., product=product, related=related)`).
**Уже целевой движок плагина** — `RENDER_CALLEES` в `RenderCallResolver` включает
`render_template`.

### `dtl-django-demo/` — Django Template Language
Полноценный Django-проект (`config` + приложение `catalog`, модели
`Category`/`Product`, sqlite). `templates/base.html` (project-level, `DIRS`) +
`catalog/templates/catalog/*.html` (app-level, `APP_DIRS`) — покрывает оба пути
резолва из `TemplatePaths`. Кастомный тег/фильтр в
`catalog/templatetags/catalog_extras.py` (`{% load catalog_extras %}`,
`|usd`, `{% stock_badge %}`), `{% url %}` реверс, контекст через `render(request,
name, {...})`. **Уже целевой движок плагина.**

### `mako-demo/` — Mako
Flask-приложение, где Mako используется напрямую через `mako.lookup.TemplateLookup`
(не через загрузчик Flask/Jinja). `<%inherit file="base.mako"/>` вместо
`{% extends %}`, `<%include file="..."/>`, `<%def>`-локальные функции (аналог
Jinja-макросов), `${ expr }`-интерполяция, `%for`/`%if` управляющие блоки.
**Не в текущем скоупе плагина** — синтаксис `<% %>`/`${ }` целиком отличается от
DTL/Jinja2, добавление потребовало бы отдельного `TemplateCatalog`-набора и
отдельной эвристики в `TemplateLanguageSelector`.

### `htpy-demo/` — htpy (HTML-in-Python)
Flask-приложение без единого файла шаблона: `components.py`/`pages.py` строят
дерево `Element` обычными функциями (`base_layout(title, content)`,
`price_tag(product)`, `product_detail_page(...)`), рендер — `str(element)`.
Показывает противоположный полюс: здесь **нечего парсить** — навигация,
автодополнение, рефакторинг уже работают из коробки через обычный Python PSI
(`PyFunction`, `PyCallExpression`), без единой строчки нового кода в плагине.

### `django-cotton-demo/` — django-cotton (компоненты поверх DTL)
Django-проект, идентичный `dtl-django-demo` по моделям/urls, но UI собран из
компонентов в `templates/cotton/*.html`: `<c-vars>` (`button.html`,
`price_tag.html`, `product_card.html`), именованные слоты (`<c-slot
name="actions">` → `{{ actions }}`), `:attr`-синтаксис для передачи переменных
(`:price="product.price"`), `{{ attrs }}`/проксирование атрибутов. Компилируется в
нативные DTL-теги, так что существующая DTL-логика продолжает работать, но
появляется новая поверхность: маппинг `<c-product-card>` ↔
`cotton/product_card.html`, автодополнение `<c-vars>`/слотов/`:attr` внутри
компонентных шаблонов. Растущий тренд компонентного Django (~2024–2026).

### `python-liquid-demo/` — python-liquid (Shopify Liquid)
Flask-приложение поверх `liquid.Environment` + `FileSystemLoader`. Показывает
принципиально другую модель композиции: в Liquid **нет** `{% extends %}`/`{%
block %}` — только `{% render 'partials/nav.liquid' %}` (изолированный scope,
только явные параметры). Каждая страница (`index.liquid`,
`product_detail.liquid`, `about.liquid`) собирается через `{% render %}` из
`partials/nav.liquid` и `partials/price_tag.liquid`. Другой набор
тегов/фильтров, чем у DTL/Jinja2 (`upcase`, `date`, `size` вместо `length` и т.д.).
**Не в текущем скоупе плагина** — ни Django, ni Flask, ни FastAPI не используют
Liquid «из коробки»; включён для полноты картины и на случай будущего запроса.

## Соответствие приоритетам из предложения по фиче

| Приложение | Движок | В скоупе плагина сейчас | Зачем демо |
|---|---|---|---|
| `jinja2-flask-demo` | Jinja2 | ✅ (spec 006, RenderCallResolver) | live-verify навигации/лайн-маркеров/инспекций «Волны 1» |
| `dtl-django-demo` | DTL | ✅ (spec 006) | то же + кастомные `{% load %}`-теги для «Волны 2» |
| `django-cotton-demo` | DTL + компоненты | 🔜 отдельная спека, средний приоритет | материал для будущей `<c-...>`-поддержки |
| `mako-demo` | Mako | ❌ низкий приоритет | контрольный пример «другого» синтаксиса шаблонов |
| `python-liquid-demo` | Liquid | ❌ низкий приоритет | то же, другой набор тегов/фильтров |
| `htpy-demo` | htpy (без шаблонов) | ➖ не требуется | контрольный пример «PSI и так работает» |
