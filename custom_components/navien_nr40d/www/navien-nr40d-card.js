const CARD_VERSION = "0.3.0";
const CARD_TYPE = "navien-nr40d-card";

const STRINGS = {
  en: {
    title: "Navien",
    room: "Room",
    outdoor: "Outside",
    target: "Target",
    heat: "Heat",
    off: "Off",
    away: "Away",
    mode: "Heating mode",
    mode_room: "Room",
    mode_water: "Water",
    water: "Heating water",
    dhw: "DHW",
    heating: "Heating",
    idle: "Idle",
    offline: "Controller is offline",
    pick: "Select the Navien NR-40D device",
    missing: "Boiler entities were not found",
    no_error: "No errors",
    connected: "Online",
    disconnected: "Offline",
  },
  ru: {
    title: "Navien",
    room: "Комната",
    outdoor: "На улице",
    target: "Уставка",
    heat: "Нагрев",
    off: "Выкл",
    away: "Вне дома",
    mode: "Режим отопления",
    mode_room: "По комнате",
    mode_water: "По теплоносителю",
    water: "Теплоноситель",
    dhw: "ГВС",
    heating: "Нагрев",
    idle: "Ожидание",
    offline: "Пульт не на связи",
    pick: "Выберите устройство Navien NR-40D",
    missing: "Сущности котла не найдены",
    no_error: "Ошибок нет",
    connected: "На связи",
    disconnected: "Нет связи",
  },
};

const STYLE = `
:host {
  display: block;
}
ha-card {
  overflow: hidden;
  padding: 0;
  background:
    radial-gradient(1200px 280px at 10% -20%, color-mix(in srgb, var(--navien-accent, #f97316) 18%, transparent), transparent 55%),
    var(--ha-card-background, var(--card-background-color, #fff));
}
.wrap {
  padding: 16px 18px 14px;
  display: flex;
  flex-direction: column;
  gap: 14px;
}
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}
.brand {
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 0;
}
.logo {
  width: 36px;
  height: 36px;
  border-radius: 12px;
  display: grid;
  place-items: center;
  background: color-mix(in srgb, var(--navien-accent, #f97316) 16%, var(--secondary-background-color, #eee));
  color: var(--navien-accent, #f97316);
  flex: 0 0 auto;
}
.logo.heating {
  animation: pulse 1.6s ease-in-out infinite;
}
.title {
  font-weight: 650;
  font-size: 1.05rem;
  letter-spacing: -0.01em;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.subtitle {
  color: var(--secondary-text-color);
  font-size: 0.78rem;
}
.pill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  border-radius: 999px;
  padding: 5px 10px;
  font-size: 0.75rem;
  font-weight: 600;
  background: var(--secondary-background-color, rgba(127,127,127,.12));
}
.dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--error-color, #ef4444);
}
.dot.on { background: var(--success-color, #22c55e); }
.dot.heat { background: var(--navien-accent, #f97316); }
.hero {
  display: grid;
  grid-template-columns: 1fr auto;
  align-items: end;
  gap: 8px;
}
.temp {
  font-size: 3.2rem;
  line-height: 0.95;
  font-weight: 720;
  letter-spacing: -0.04em;
}
.temp small {
  font-size: 1.3rem;
  margin-left: 2px;
  color: var(--secondary-text-color);
}
.temp-meta {
  color: var(--secondary-text-color);
  font-size: 0.85rem;
  margin-top: 4px;
}
.setpoint {
  display: flex;
  align-items: center;
  gap: 8px;
}
.btn {
  appearance: none;
  border: 0;
  background: var(--secondary-background-color, rgba(127,127,127,.12));
  color: var(--primary-text-color);
  width: 36px;
  height: 36px;
  border-radius: 12px;
  font-size: 1.25rem;
  cursor: pointer;
  display: grid;
  place-items: center;
}
.btn:hover { filter: brightness(1.08); }
.btn:disabled { opacity: .4; cursor: default; }
.target-value {
  min-width: 3.2rem;
  text-align: center;
  font-weight: 700;
  font-size: 1.15rem;
}
.row {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}
.seg {
  display: flex;
  background: var(--secondary-background-color, rgba(127,127,127,.12));
  border-radius: 14px;
  padding: 3px;
  flex: 1;
  min-width: 160px;
}
.seg button {
  flex: 1;
  border: 0;
  background: transparent;
  color: var(--secondary-text-color);
  border-radius: 12px;
  padding: 8px 10px;
  font-weight: 650;
  cursor: pointer;
}
.seg button.active {
  background: var(--card-background-color, #fff);
  color: var(--primary-text-color);
  box-shadow: 0 1px 2px rgba(0,0,0,.08);
}
.chip {
  border: 0;
  border-radius: 14px;
  padding: 8px 12px;
  font-weight: 650;
  cursor: pointer;
  background: var(--secondary-background-color, rgba(127,127,127,.12));
  color: var(--primary-text-color);
}
.chip.active {
  background: color-mix(in srgb, var(--navien-accent, #f97316) 18%, var(--secondary-background-color, #eee));
  color: var(--navien-accent, #f97316);
}
.sliders {
  display: grid;
  gap: 10px;
}
.slider-row {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 4px 12px;
  align-items: center;
}
.slider-row label {
  font-size: 0.82rem;
  color: var(--secondary-text-color);
}
.slider-row .value {
  font-weight: 700;
  font-variant-numeric: tabular-nums;
}
input[type=range] {
  grid-column: 1 / -1;
  width: 100%;
  accent-color: var(--navien-accent, #f97316);
}
.banner {
  border-radius: 12px;
  padding: 8px 10px;
  font-size: 0.82rem;
  background: color-mix(in srgb, var(--error-color, #ef4444) 12%, transparent);
  color: var(--error-color, #ef4444);
}
.ok {
  color: var(--secondary-text-color);
  background: var(--secondary-background-color, rgba(127,127,127,.08));
}
.warning {
  opacity: .85;
  text-align: center;
  padding: 18px 8px;
  color: var(--secondary-text-color);
}
@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.06); }
}
`;

function lang(hass) {
  const code = (hass && (hass.locale?.language || hass.language) || "en").toLowerCase();
  return code.startsWith("ru") ? "ru" : "en";
}

function t(hass, key) {
  return STRINGS[lang(hass)][key] || STRINGS.en[key] || key;
}

function num(value) {
  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : null;
}

const ROOM_OPTIONS = ["room", "По комнате"];
const WATER_OPTIONS = ["water", "По теплоносителю"];
const OK_ERRORS = ["ok", "none", "нет", "unavailable", "unknown", "0", ""];

function isRoom(state) {
  return ROOM_OPTIONS.includes(state);
}

function isWater(state) {
  return WATER_OPTIONS.includes(state);
}

function optionFor(state, wanted) {
  const options = state?.attributes?.options || [];
  return wanted.find((item) => options.includes(item)) || wanted[0];
}

function normalizeDeviceId(value) {
  if (!value) return "";
  if (typeof value === "string") return value.trim();
  if (Array.isArray(value)) return normalizeDeviceId(value[0]);
  if (typeof value === "object") {
    return normalizeDeviceId(value.id || value.device_id || value.device || value.value);
  }
  return "";
}

function registryList(hass) {
  const raw = hass?.entities;
  if (!raw) return [];
  return (Array.isArray(raw) ? raw : Object.values(raw)).filter(Boolean);
}

function entryEntityId(entry, fallback) {
  return entry?.entity_id || entry?.entityId || fallback || "";
}

function entryDeviceId(entry) {
  return entry?.device_id || entry?.deviceId || "";
}

function isNavienId(hass, entityId) {
  if (!entityId) return false;
  const entry = hass?.entities?.[entityId];
  return entry?.platform === "navien_nr40d" || String(entityId).includes("navien");
}

function matchHint(entityId, entry, hints) {
  const uniqueId = String(entry?.unique_id || "").toLowerCase();
  const key = String(entry?.translation_key || "").toLowerCase();
  const name = String(entry?.name || entry?.original_name || "").toLowerCase();
  const id = String(entityId || "").toLowerCase();
  return hints.some((hint) => {
    const needle = String(hint).toLowerCase();
    return id.includes(needle) || uniqueId.includes(needle) || key === needle || name.includes(needle);
  });
}

function idsOnDevice(hass, deviceId) {
  const id = normalizeDeviceId(deviceId);
  const found = [];
  const seen = new Set();
  const add = (entityId) => {
    if (!entityId || seen.has(entityId)) return;
    seen.add(entityId);
    found.push(entityId);
  };

  if (id) {
    for (const entry of registryList(hass)) {
      if (entryDeviceId(entry) === id) add(entryEntityId(entry));
    }
    const configEntries = hass?.devices?.[id]?.config_entries || [];
    for (const entry of registryList(hass)) {
      if (configEntries.includes(entry.config_entry_id)) add(entryEntityId(entry));
    }
  }

  for (const entityId of Object.keys(hass?.states || {})) {
    const entry = hass?.entities?.[entityId];
    if (id && entryDeviceId(entry) === id) add(entityId);
    else if (isNavienId(hass, entityId)) add(entityId);
  }
  return found;
}

function pickDomain(ids, hass, domain, hints) {
  let candidates = (ids || []).filter((entityId) => entityId.startsWith(`${domain}.`));
  if (!candidates.length) {
    candidates = Object.keys(hass?.states || {}).filter(
      (entityId) => entityId.startsWith(`${domain}.`) && isNavienId(hass, entityId)
    );
  }
  const native = candidates.filter((entityId) => hass?.entities?.[entityId]?.platform === "navien_nr40d");
  if (native.length) candidates = native;
  for (const hint of hints || []) {
    const hit = candidates.find((entityId) => matchHint(entityId, hass?.entities?.[entityId], [hint]));
    if (hit) return hit;
  }
  if (hints && hints.length) return candidates.length === 1 ? candidates[0] : null;
  return candidates[0] || null;
}

function pickClimate(ids, hass) {
  return (
    pickDomain(ids, hass, "climate", ["boiler", "kotel", "climate", "navien"]) ||
    Object.keys(hass?.states || {}).find((entityId) => {
      if (!entityId.startsWith("climate.")) return false;
      const name = String(hass.states[entityId].attributes?.friendly_name || "").toLowerCase();
      return entityId.includes("navien") || name.includes("navien") || name.includes("котёл") || name.includes("котел");
    }) ||
    null
  );
}

class NavienNr40dCard extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: "open" });
    this._hass = null;
    this._config = {};
  }

  static getConfigForm() {
    return {
      schema: [
        {
          name: "device",
          selector: { device: { filter: { integration: "navien_nr40d" } } },
        },
        { name: "name", selector: { text: {} } },
      ],
    };
  }

  static getStubConfig(hass) {
    try {
      const ids = idsOnDevice(hass, "");
      const climate = pickClimate(ids, hass);
      const any = climate || ids[0];
      const fromRegistry = registryList(hass).find((entry) => entryEntityId(entry) === any);
      return { device: entryDeviceId(hass?.entities?.[any]) || entryDeviceId(fromRegistry) || "" };
    } catch (error) {
      return { device: "" };
    }
  }

  setConfig(config) {
    this._config = config || {};
    this._safeRender();
  }

  set hass(hass) {
    this._hass = hass;
    this._safeRender();
  }

  _safeRender() {
    try {
      this._render();
    } catch (error) {
      console.error("navien-nr40d-card", error);
    }
  }

  getCardSize() {
    return 5;
  }

  _entities() {
    const hass = this._hass;
    const deviceId = normalizeDeviceId(this._config.device)
      || entryDeviceId(hass?.entities?.[this._config.entity]);
    const ids = idsOnDevice(hass, deviceId);
    const configured = this._config.entity && hass?.states?.[this._config.entity] ? this._config.entity : null;
    return {
      climate: configured?.startsWith("climate.") ? configured : pickClimate(ids, hass),
      room: this._config.room_entity || pickDomain(ids, hass, "sensor", ["room_temp", "room_temperature", "комнат"]),
      outdoor: this._config.outdoor_entity || pickDomain(ids, hass, "sensor", ["outdoor_temp", "outdoor", "уличн"]),
      room_target: this._config.room_target_entity || pickDomain(ids, hass, "number", ["room_target", "room_setpoint"]),
      water: this._config.water_entity || pickDomain(ids, hass, "number", ["water_temp", "heating_water", "теплоносител", "teplonos"]),
      dhw: this._config.dhw_entity || pickDomain(ids, hass, "number", ["dhw_temp", "dhw", "гвс", "gvs"]),
      mode: this._config.mode_entity || pickDomain(ids, hass, "select", ["heating_mode"]),
      mode_sensor: pickDomain(ids, hass, "sensor", ["mode"]),
      power: this._config.power_entity || pickDomain(ids, hass, "switch", ["power", "отопление"]),
      away: this._config.away_entity || pickDomain(ids, hass, "switch", ["away"]),
      connected: this._config.connected_entity || pickDomain(ids, hass, "binary_sensor", ["connected", "controller_link", "connectivity"]),
      error: this._config.error_entity || pickDomain(ids, hass, "sensor", ["error", "ошиб"]),
    };
  }

  _call(domain, service, entityId, data = {}) {
    if (!this._hass || !entityId) return;
    this._hass.callService(domain, service, { entity_id: entityId, ...data });
  }

  _render() {
    const hass = this._hass;
    const root = this.shadowRoot;
    if (!root) return;
    const ids = this._entities();
    const climate = hass?.states?.[ids.climate];
    const room = hass?.states?.[ids.room];
    const outdoorTemp = num(hass?.states?.[ids.outdoor]?.state);
    const roomTarget = hass?.states?.[ids.room_target];
    const power = hass?.states?.[ids.power];
    const connected = hass?.states?.[ids.connected];
    const water = hass?.states?.[ids.water];
    const dhw = hass?.states?.[ids.dhw];
    const mode = hass?.states?.[ids.mode];
    const modeSensor = hass?.states?.[ids.mode_sensor];
    const away = hass?.states?.[ids.away];
    const error = hass?.states?.[ids.error];
    const deviceId = normalizeDeviceId(this._config.device);
    const deviceName = hass?.devices?.[deviceId]?.name_by_user || hass?.devices?.[deviceId]?.name;
    const name = this._config.name || climate?.attributes?.friendly_name || deviceName || t(hass, "title");
    const online = connected
      ? connected.state === "on"
      : Boolean(climate || room || water || dhw);
    const heating = climate?.attributes?.hvac_action === "heating";
    const current = num(climate?.attributes?.current_temperature) ?? num(room?.state);
    const target = num(climate?.attributes?.temperature) ?? num(roomTarget?.state);
    const min = num(climate?.attributes?.min_temp) ?? num(roomTarget?.attributes?.min) ?? 10;
    const max = num(climate?.attributes?.max_temp) ?? num(roomTarget?.attributes?.max) ?? 40;
    const modeValue = [mode?.state, modeSensor?.state].find(
      (value) => value && !["unknown", "unavailable"].includes(value)
    );
    const heatOn = climate?.state === "heat" || power?.state === "on"
      || ["on", "room", "water", "away", "heat"].includes(modeValue);
    const awayOn = away?.state === "on" || climate?.attributes?.preset_mode === "away" || modeValue === "away";
    const errorText =
      error && error.state && !OK_ERRORS.includes(String(error.state).trim().toLowerCase())
        ? error.state
        : null;
    const ready = Boolean(climate || room || roomTarget || water || dhw || mode || power || away);
    const hasDevice = Boolean(deviceId || this._config.entity);
    const canSetRoom = Boolean(ids.climate || ids.room_target);
    const canPower = Boolean(ids.climate || ids.power);
    const subtitle = heating
      ? t(hass, "heating")
      : heatOn
        ? t(hass, "idle")
        : t(hass, "off");

    root.innerHTML = `
      <style>${STYLE}</style>
      <ha-card>
        <div class="wrap">
          <div class="header">
            <div class="brand">
              <div class="logo ${heating ? "heating" : ""}" aria-hidden="true">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 22c4.97 0 8-3.36 8-7.5 0-3.27-2.25-6.18-4.2-8.05C14.17 4.86 13 3.5 13 2c-2.4 2.67-4 5.43-4 8.5 0 1.3.4 2.5 1 3.5-.9-.6-1.5-1.7-1.5-3C6.2 13.4 4 16 4 18.5 4 21.04 6.46 22 12 22z"/>
                </svg>
              </div>
              <div>
                <div class="title">${this._escape(name)}</div>
                <div class="subtitle">${subtitle}</div>
              </div>
            </div>
            <div class="pill">
              <span class="dot ${online ? (heating ? "heat" : "on") : ""}"></span>
              ${online ? t(hass, "connected") : t(hass, "disconnected")}
            </div>
          </div>
          ${!hasDevice && !ready ? `<div class="warning">${t(hass, "pick")}</div>` : ""}
          ${hasDevice && !ready ? `<div class="warning">${t(hass, "missing")}</div>` : ""}
          ${ready && !online ? `<div class="warning">${t(hass, "offline")}</div>` : ""}
          ${ready ? `
            <div class="hero">
              <div>
                <div class="temp">${current ?? "–"}<small>°</small></div>
                <div class="temp-meta">${t(hass, "room")}${outdoorTemp != null ? ` · ${t(hass, "outdoor")} ${outdoorTemp}°` : ""}</div>
              </div>
              ${canSetRoom ? `
              <div class="setpoint">
                <button class="btn" data-act="temp-down" ${target <= min ? "disabled" : ""}>−</button>
                <div>
                  <div class="target-value">${target ?? "–"}°</div>
                  <div class="temp-meta">${t(hass, "target")}</div>
                </div>
                <button class="btn" data-act="temp-up" ${target >= max ? "disabled" : ""}>+</button>
              </div>
              ` : ""}
            </div>
            ${canPower || away ? `
            <div class="row">
              ${canPower ? `
              <div class="seg">
                <button data-act="off" class="${heatOn ? "" : "active"}">${t(hass, "off")}</button>
                <button data-act="heat" class="${heatOn ? "active" : ""}">${t(hass, "heat")}</button>
              </div>
              ` : ""}
              ${away ? `
                <button class="chip ${awayOn ? "active" : ""}" data-act="away">${t(hass, "away")}</button>
              ` : ""}
            </div>
            ` : ""}
            ${mode ? `
              <div class="seg">
                <button data-act="mode-room" class="${isRoom(modeValue) ? "active" : ""}">${t(hass, "mode_room")}</button>
                <button data-act="mode-water" class="${isWater(modeValue) ? "active" : ""}">${t(hass, "mode_water")}</button>
              </div>
            ` : ""}
            <div class="sliders">
              ${water ? this._slider("water", t(hass, "water"), water) : ""}
              ${dhw ? this._slider("dhw", t(hass, "dhw"), dhw) : ""}
            </div>
            <div class="banner ${errorText ? "" : "ok"}">${errorText ? this._escape(error.state) : t(hass, "no_error")}</div>
          ` : ""}
        </div>
      </ha-card>
    `;
    this._bind({ min, max, target, awayOn, heatOn, ids });
  }

  _slider(kind, label, state) {
    const value = num(state.state) ?? 0;
    const min = num(state.attributes.min) ?? 30;
    const max = num(state.attributes.max) ?? 80;
    const step = num(state.attributes.step) ?? 1;
    return `
      <div class="slider-row">
        <label>${label}</label>
        <div class="value">${value}°</div>
        <input type="range" data-slider="${kind}" min="${min}" max="${max}" step="${step}" value="${value}">
      </div>
    `;
  }

  _bind(ctx) {
    const root = this.shadowRoot;
    const setRoom = (value) => {
      if (ctx.ids.climate) {
        this._call("climate", "set_temperature", ctx.ids.climate, { temperature: value });
      } else {
        this._call("number", "set_value", ctx.ids.room_target, { value });
      }
    };
    root.querySelector('[data-act="temp-down"]')?.addEventListener("click", () => {
      if (ctx.target == null) return;
      setRoom(ctx.target - 1);
    });
    root.querySelector('[data-act="temp-up"]')?.addEventListener("click", () => {
      if (ctx.target == null) return;
      setRoom(ctx.target + 1);
    });
    root.querySelector('[data-act="off"]')?.addEventListener("click", () => {
      if (ctx.ids.climate) {
        this._call("climate", "set_hvac_mode", ctx.ids.climate, { hvac_mode: "off" });
      } else {
        this._call("switch", "turn_off", ctx.ids.power);
      }
    });
    root.querySelector('[data-act="heat"]')?.addEventListener("click", () => {
      if (ctx.ids.climate) {
        this._call("climate", "set_hvac_mode", ctx.ids.climate, { hvac_mode: "heat" });
      } else {
        this._call("switch", "turn_on", ctx.ids.power);
      }
    });
    root.querySelector('[data-act="away"]')?.addEventListener("click", () => {
      if (ctx.ids.away) {
        this._call("switch", ctx.awayOn ? "turn_off" : "turn_on", ctx.ids.away);
      } else {
        this._call("climate", "set_preset_mode", ctx.ids.climate, { preset_mode: ctx.awayOn ? "none" : "away" });
      }
    });
    root.querySelector('[data-act="mode-room"]')?.addEventListener("click", () => {
      this._call("select", "select_option", ctx.ids.mode, {
        option: optionFor(this._hass?.states?.[ctx.ids.mode], ROOM_OPTIONS),
      });
    });
    root.querySelector('[data-act="mode-water"]')?.addEventListener("click", () => {
      this._call("select", "select_option", ctx.ids.mode, {
        option: optionFor(this._hass?.states?.[ctx.ids.mode], WATER_OPTIONS),
      });
    });
    root.querySelectorAll("input[type=range]").forEach((input) => {
      input.addEventListener("input", (event) => {
        const label = event.target.closest(".slider-row")?.querySelector(".value");
        if (label) label.textContent = `${event.target.value}°`;
      });
      input.addEventListener("change", (event) => {
        const kind = event.target.dataset.slider;
        const entityId = kind === "water" ? ctx.ids.water : ctx.ids.dhw;
        this._call("number", "set_value", entityId, { value: Number(event.target.value) });
      });
    });
  }

  _escape(value) {
    return String(value ?? "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }
}

if (!customElements.get(CARD_TYPE)) {
  customElements.define(CARD_TYPE, NavienNr40dCard);
}

window.customCards = window.customCards || [];
if (!window.customCards.some((card) => card.type === CARD_TYPE)) {
  window.customCards.push({
    type: CARD_TYPE,
    name: "Navien NR-40D",
    description: "Navien NR-40D boiler card",
    preview: false,
  });
}

console.info(`%c NAVIEN-NR40D-CARD %c ${CARD_VERSION} `, "background:#f97316;color:#fff;font-weight:700", "background:transparent;color:#f97316");
