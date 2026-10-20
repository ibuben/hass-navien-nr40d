# Navien NR-40D для Home Assistant

[![hacs](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)
[![release](https://img.shields.io/github/v/release/ibuben/hass-navien-nr40d?include_prereleases)](https://github.com/ibuben/hass-navien-nr40d/releases)

Локальная интеграция комнатного пульта **Navien NR-40D** (котлы Deluxe ONE и совместимые). Home Assistant сам принимает подключение пульта и управляет котлом без облака Smart TOK / Sphere.

После установки в Lovelace появляется карточка `custom:navien-nr40d-card`: температура, уставка, нагрев, «Вне дома», режим отопления, теплоноситель и ГВС на одном экране.

## Карточка

Добавьте вручную или через «Добавить карточку → Navien NR-40D»:

```yaml
type: custom:navien-nr40d-card
entity: climate.navien_nr40d
```

Интеграция сама регистрирует JS-модуль. Связанные сущности (теплоноситель, ГВС, режим, связь, ошибка) карточка находит по устройству. При желании их можно задать явно:

```yaml
type: custom:navien-nr40d-card
entity: climate.navien_nr40d
name: Котёл
water_entity: number.navien_nr40d_water_temp
dhw_entity: number.navien_nr40d_dhw_temp
mode_entity: select.navien_nr40d_heating_mode
away_entity: switch.navien_nr40d_away
```

## Что появляется в Home Assistant

| Сущность | Назначение |
|---|---|
| `climate` | Вкл/выкл, комнатная температура и уставка, пресет «Вне дома» |
| `select` «Режим отопления» | По комнате / по теплоносителю |
| `number` «Температура теплоносителя» | 40–80 °C |
| `number` «Температура ГВС» | 30–60 °C |
| `switch` «Вне дома» | Тот же away-режим, удобно для автоматизаций |
| `sensor` температура, режим, ошибка | Графики и расшифровка кода из инструкции |
| `binary_sensor` связь с пультом | Пульт подключён к интеграции |

Уставки принимаются только целыми градусами — так устроен пульт.

## Требования

- Home Assistant 2024.2 или новее
- Пульт NR-40D в локальной сети
- Перенаправление облачных адресов пульта на хост Home Assistant:
  - `rust2.naviensmartcontrol.com`
  - `rust.naviensmartcontrol.com`
  - TCP-порты `7000`, `21001`, `21003`

На MikroTik это обычно `dst-nat` этих портов на IP Home Assistant. Пока трафик идёт на другой хост, интеграция просто ждёт пульт.

## Установка

### HACS

1. HACS → Интеграции → Пользовательские репозитории
2. Добавьте `https://github.com/ibuben/hass-navien-nr40d`, тип **Integration**
3. Установите **Navien NR-40D** и перезапустите Home Assistant
4. **Настройки → Устройства и службы → Добавить интеграцию → Navien NR-40D**

### Вручную

1. Скопируйте `custom_components/navien_nr40d` в `/config/custom_components/navien_nr40d`
2. Перезапустите Home Assistant
3. Добавьте интеграцию через UI

Адрес прослушивания по умолчанию — `0.0.0.0`, порты `7000,21001,21003`.

### Docker / HAOS

Контейнер Home Assistant должен принимать эти TCP-порты с хоста (режим `host` или проброс `7000`, `21001`, `21003`).

## Ограничения этой связки котла и пульта

Пульт сам сообщает, что функции нет, и команды игнорируются:

- летний режим «только ГВС»
- быстрый нагрев ГВС
- уставки с половиной градуса (25,5 °C)

Сервисное меню котла (`S.THE`, DIP, датчик улицы `G.oN`) через пульт недоступно — только с панели котла. Недельное расписание в этой версии не пишется: его удобнее держать автоматизациями Home Assistant.

## Отладка

Логи: **Настройки → Система → Журналы**, фильтр `navien_nr40d`.  
Диагностика: страница устройства → «Скачать диагностику».
