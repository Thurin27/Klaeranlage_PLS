# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
#     "numpy",
#     "plotly",
# ]
# ///

import marimo

__generated_with = "0.13.0"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    return mo, np


@app.cell
def _(mo):
    # === CSS Styles ===
    mo.Html("""<style>
    :root {
        --bg:#1a1a2e; --panel:#16213e; --border:#0f3460;
        --accent:#e94560; --ok:#00b894; --warn:#fdcb6e;
        --danger:#e17055; --txt:#dfe6e9; --val:#74b9ff;
    }
    .pls { background:var(--bg); color:var(--txt); padding:12px; border-radius:8px; font-family:'Consolas','Courier New',monospace; }
    .pls-hdr { background:linear-gradient(90deg,var(--panel),var(--border)); padding:10px 20px; border-radius:6px; display:flex; justify-content:space-between; align-items:center; margin-bottom:12px; border:1px solid var(--border); }
    .pls-hdr h2 { margin:0; color:#74b9ff; font-size:1.3em; }
    .pls-st { display:flex; gap:15px; align-items:center; font-size:0.85em; }
    .pls-dot { width:10px; height:10px; border-radius:50%; display:inline-block; margin-right:4px; animation:pulse 2s infinite; }
    @keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.4} }
    .pls-c { background:var(--panel); border:1px solid var(--border); border-radius:6px; padding:12px; margin-bottom:10px; }
    .pls-c h3 { margin:0 0 8px 0; color:#74b9ff; font-size:1em; border-bottom:1px solid var(--border); padding-bottom:6px; }
    .pls-tbl { width:100%; border-collapse:separate; border-spacing:12px 2px; }
    .pls-tbl td { padding:5px 14px !important; font-size:0.9em; white-space:nowrap; }
    .pls-tbl td:first-child { color:#b2bec3; padding-right:24px !important; }
    .pls-tbl td:last-child { text-align:right; font-weight:bold; padding-left:24px !important; }
    .pls-overview-tbl { width:100%; border-collapse:separate; border-spacing:14px 2px; font-size:0.88em; color:#ffffff; background:#16213e; border-radius:4px; }
    .pls-overview-tbl th { text-align:left; padding:8px 16px !important; color:#74b9ff; border-bottom:2px solid #0f3460; background:#0f1a30; white-space:nowrap; }
    .pls-overview-tbl td { padding:6px 16px !important; border-bottom:1px solid #0f3460; white-space:nowrap; }
    .pls-overview-tbl tr:hover { background:#1e2d4d; }
    .c-v { color:var(--val); } .c-ok { color:var(--ok); } .c-w { color:var(--warn); } .c-d { color:var(--danger); }
    .pls-g2 { display:grid; grid-template-columns:1fr 1fr; gap:10px; }
    .pls-g3 { display:grid; grid-template-columns:1fr 1fr 1fr; gap:10px; }
    .pls-bar { height:16px; border-radius:3px; background:#2d3436; overflow:hidden; margin:4px 0; }
    .pls-bar-f { height:100%; border-radius:3px; transition:width 0.5s; }
    .pls-alarm { background:rgba(233,69,96,0.15); border:1px solid var(--accent); border-radius:4px; padding:6px 10px; margin:4px 0; font-size:0.85em; }
    .pls-sep { border-top:1px solid var(--border); margin:8px 0; padding-top:8px; }
    .pls-time-display { background:#0a0a1a; border:2px solid #74b9ff; border-radius:6px; padding:8px 16px; display:inline-block; font-size:1.1em; color:#74b9ff; margin:4px 0; }
    </style>""")
    return


@app.cell
def _(mo):
    # === STEUERUNGSPARAMETER ===
    o2_soll = mo.ui.slider(start=0.5, stop=4.0, step=0.1, value=2.0, label="O₂-Sollwert Belebung [mg/L]")
    rs_verhaeltnis = mo.ui.slider(start=0.3, stop=1.5, step=0.05, value=0.75, label="Rücklaufschlammverhältnis [-]")
    ues_menge = mo.ui.slider(start=50, stop=500, step=10, value=200, label="Überschussschlamm [m³/d]")
    faellmittel = mo.ui.slider(start=0, stop=50, step=1, value=15, label="Fällmitteldosierung Fe³⁺ [L/h]")
    zulauf_q = mo.ui.slider(start=5000, stop=30000, step=500, value=12000, label="Zulauf Trockenwetter [m³/d]")
    regen_faktor = mo.ui.slider(start=1.0, stop=3.0, step=0.1, value=1.0, label="Regenfaktor [-]")
    temperatur = mo.ui.slider(start=6, stop=22, step=0.5, value=14.0, label="Abwassertemperatur [°C]")
    abschlag_schwelle = mo.ui.slider(start=10000, stop=40000, step=1000, value=20000, label="Abschlagschwelle [m³/d]")
    return abschlag_schwelle, faellmittel, o2_soll, regen_faktor, rs_verhaeltnis, temperatur, ues_menge, zulauf_q


@app.cell
def _(mo):
    # === ZEITSTEUERUNG ===
    btn_1h = mo.ui.button(label="⏩ +1 Stunde", value=0, on_click=lambda v: v + 1)
    btn_6h = mo.ui.button(label="⏩ +6 Stunden", value=0, on_click=lambda v: v + 1)
    btn_24h = mo.ui.button(label="⏩ +24 Stunden", value=0, on_click=lambda v: v + 1)
    btn_7d = mo.ui.button(label="⏩ +7 Tage", value=0, on_click=lambda v: v + 1)
    btn_reset = mo.ui.button(label="🔄 Reset", value=0, on_click=lambda v: v + 1)
    return btn_1h, btn_24h, btn_6h, btn_7d, btn_reset


@app.cell
def _(mo):
    # === PUMPEN-DETAILANSICHT SWITCHES ===
    detail_p11 = mo.ui.switch(label="📊 P1.1 Zulaufpumpe – Wartungstrend", value=False)
    detail_p51 = mo.ui.switch(label="📊 P5.1 ÜS-Pumpe – Wartungstrend", value=False)
    return detail_p11, detail_p51


@app.cell
def _(mo):
    # === ANLAGENMODIFIKATIONEN ===
    mod_p_online = mo.ui.switch(label="Online-P-Messung am Zulauf (Störgrößenaufschaltung)")
    mod_nh4_sensor = mo.ui.switch(label="NH₄-Sensor im BB (NH₄-geführte Belüftung)")
    mod_spektral = mo.ui.switch(label="Spektralsonde am Zulauf (UV/VIS CSB/TOC)")
    mod_truebung = mo.ui.switch(label="Trübungsmessung NK-Ablauf")
    mod_membran = mo.ui.switch(label="Feinblasige Membranbelüfter")
    mod_turbo = mo.ui.switch(label="Turboverdichter statt Drehkolbengebläse")
    mod_intermit = mo.ui.switch(label="Intermittierende Belüftung (SBR-ähnlich)")
    mod_anammox = mo.ui.switch(label="Seitenstromentstickung (Deammonifikation)")
    mod_stufe4 = mo.ui.switch(label="4. Reinigungsstufe (GAK-Filter)")
    mod_pv = mo.ui.switch(label="PV-Anlage (Dachflächen)")
    return mod_anammox, mod_intermit, mod_membran, mod_nh4_sensor, mod_p_online, mod_pv, mod_spektral, mod_stufe4, mod_truebung, mod_turbo


@app.cell
def _(mo):
    # === LABOR UI ===
    lab_analyse_btn = mo.ui.button(label="🧪 Probenahme + Analyse durchführen", value=0, on_click=lambda v: v + 1)
    lab_woche_btn = mo.ui.button(label="📋 Neue Wochendaten generieren", value=0, on_click=lambda v: v + 1)
    lab_kal_btn = mo.ui.button(label="📈 Kalibrierung durchführen", value=0, on_click=lambda v: v + 1)
    lab_show_isv = mo.ui.switch(label="ISV-Absetzversuch anzeigen")
    lab_show_proto = mo.ui.switch(label="Eigenüberwachung Wochenbericht")
    lab_show_qs = mo.ui.switch(label="QS: Kalibrierung & Fehlersuche")
    return lab_analyse_btn, lab_kal_btn, lab_show_isv, lab_show_proto, lab_show_qs, lab_woche_btn


@app.cell
def _(mo):
    # === ARMATUREN UI ===
    # Dropdown zur Auswahl einer Armatur für die Wartungsanmeldung.
    # Die Optionen werden im Render-Block synchron gehalten – dort ist der
    # zentrale Datenkatalog ARMATUREN definiert.
    armatur_auswahl = mo.ui.dropdown(
        options=[
            "—",
            "HS-101  Plattenschieber  Zulauf Hebewerk",
            "SV-201  Regelklappe  Regenüberlauf",
            "HS-202  Plattenschieber  Zulauf Vorklärung",
            "RK-301  Rückschlagklappe  Druckstutzen P1.1",
            "V-401   Absperrschieber  Interne Rezirkulation",
            "V-402   Absperrschieber  Rücklaufschlamm",
            "V-501   Absperrschieber  Überschussschlamm",
            "V-601   Absperrschieber  Primärschlamm",
            "V-001   Absperrschieber  Druckstutzen P-001 (PW Talstr.)",
            "V-002   Absperrschieber  Druckstutzen P-002 (PW Talstr.)",
            "RK-001  Rückschlagklappe P-001 (PW Talstr.)",
            "RK-002  Rückschlagklappe P-002 (PW Talstr.)",
            "V-003   Absperrschieber  Abzweig Speicherbecken 1",
            "V-004   Absperrschieber  Abzweig Speicherbecken 2",
            "LA-001  Be-/Entlüftungsventil  Hauptleitung DN 200",
            "LA-002  Be-/Entlüftungsventil  Hauptleitung DN 125",
        ],
        value="—",
        label="Armatur auswählen",
    )
    wartung_btn = mo.ui.run_button(label="🔧 Wartung bei Leitwarte anmelden", kind="warn")
    return armatur_auswahl, wartung_btn


@app.cell
def _(mo):
    # === PUMPENTECHNIK: Umbauplanung (Auswahl gemäß verfügbaren Herstellerkennlinien) ===
    _opt_tal = {
        "Bestand – Sewabloc F 100-316, Laufrad ø279": "Sewabloc F 100-316|279",
        "Laufradtausch – Sewabloc F 100-316, Laufrad ø310": "Sewabloc F 100-316|310",
        "Neupumpe – Sewatec E 100-317, Laufrad ø286": "Sewatec E 100-317|286",
        "Neupumpe – Sewatec E 100-317, Laufrad ø299": "Sewatec E 100-317|299",
        "Neupumpe – Sewatec E 100-317, Laufrad ø315": "Sewatec E 100-317|315",
        "Neupumpe – Sewatec E 100-317, Laufrad ø328": "Sewatec E 100-317|328",
    }
    _opt_rs = {
        "Bestand – Sewabloc F 100-252, Laufrad ø235": "Sewabloc F 100-252|235",
        "Umsetzen – vorhandene Sewabloc F 100-316 (bisher P-001), Laufrad ø279": "Sewabloc F 100-316|279|umsetzen",
        "Umsetzen – vorhandene Sewabloc F 100-316 (bisher P-001), Laufrad ø310": "Sewabloc F 100-316|310|umsetzen",
    }
    _opt_ft = {
        "Bestand – Sewabloc F 100-254, Laufrad ø200": "Sewabloc F 100-254|200",
        "Laufradtausch – Sewabloc F 100-254, Laufrad ø265": "Sewabloc F 100-254|265",
        "Neupumpe – Sewabloc F 80-252, Laufrad ø180": "Sewabloc F 80-252|180",
        "Neupumpe – Sewabloc F 80-252, Laufrad ø200": "Sewabloc F 80-252|200",
        "Neupumpe – Sewabloc F 80-252, Laufrad ø210": "Sewabloc F 80-252|210",
    }
    kf_tal = mo.ui.dropdown(options=_opt_tal, value="Bestand – Sewabloc F 100-316, Laufrad ø279", label="Aggregat")
    kf_tal_fu = mo.ui.switch(label="Frequenzumrichter")
    kf_tal_n = mo.ui.slider(start=725, stop=1540, step=5, value=1450, label="Drehzahl bei FU-Betrieb [1/min]", show_value=True)
    kf_rs = mo.ui.dropdown(options=_opt_rs, value="Bestand – Sewabloc F 100-252, Laufrad ø235", label="Aggregat")
    kf_rs_fu = mo.ui.switch(label="Frequenzumrichter")
    kf_rs_n = mo.ui.slider(start=725, stop=1540, step=5, value=1450, label="Drehzahl bei FU-Betrieb [1/min]", show_value=True)
    kf_ft = mo.ui.dropdown(options=_opt_ft, value="Bestand – Sewabloc F 100-254, Laufrad ø200", label="Aggregat")
    kf_ft_fu = mo.ui.switch(label="Frequenzumrichter")
    kf_ft_n = mo.ui.slider(start=725, stop=1540, step=5, value=1450, label="Drehzahl bei FU-Betrieb [1/min]", show_value=True)
    kf_umbau_btn = mo.ui.run_button(label="🔧 Umbau durchführen und in Betrieb nehmen", kind="success")
    kf_reset_btn = mo.ui.run_button(label="↺ Bestand wiederherstellen", kind="neutral")
    return (kf_ft, kf_ft_fu, kf_ft_n, kf_reset_btn, kf_rs, kf_rs_fu, kf_rs_n,
            kf_tal, kf_tal_fu, kf_tal_n, kf_umbau_btn)


@app.cell
def _(mo):
    # === Installierter Zustand der Pumpentechnik (persistent) ===
    PK_BESTAND = dict(
        tal=dict(typ="Sewabloc F 100-316", d=279, fu=False, n=1450),
        rs=dict(typ="Sewabloc F 100-252", d=235, fu=False, n=1450, umsetzen=False),
        ft=dict(typ="Sewabloc F 100-254", d=200, fu=False, n=1450),
        protokoll=[],
    )
    get_pk, set_pk = mo.state(PK_BESTAND)
    return PK_BESTAND, get_pk, set_pk


@app.cell
def _(PK_BESTAND, get_pk, kf_ft, kf_ft_fu, kf_ft_n, kf_reset_btn, kf_rs, kf_rs_fu, kf_rs_n,
      kf_tal, kf_tal_fu, kf_tal_n, kf_umbau_btn, set_pk):
    # === Umbau ausführen: Auswahl → installierter Zustand ===
    kf_meldung = ""
    if kf_reset_btn.value:
        set_pk(PK_BESTAND)
        kf_meldung = "↺ Pumpentechnik auf Bestand zurückgesetzt."
    elif kf_umbau_btn.value:
        _t = kf_tal.value.split("|")
        _r = kf_rs.value.split("|")
        _f = kf_ft.value.split("|")
        if len(_r) > 2 and _t[0] == "Sewabloc F 100-316":
            kf_meldung = ("⚠️ Umbau nicht möglich: Die Sewabloc F 100-316 (P-001) wird im PW Talstraße weiter benötigt. "
                          "Sie kann nur umgesetzt werden, wenn P-001 durch eine Neupumpe ersetzt wird.")
        else:
            _alt = get_pk()
            _neu = dict(
                tal=dict(typ=_t[0], d=int(_t[1]), fu=kf_tal_fu.value, n=kf_tal_n.value if kf_tal_fu.value else 1450),
                rs=dict(typ=_r[0], d=int(_r[1]), fu=kf_rs_fu.value, n=kf_rs_n.value if kf_rs_fu.value else 1450,
                        umsetzen=len(_r) > 2),
                ft=dict(typ=_f[0], d=int(_f[1]), fu=kf_ft_fu.value, n=kf_ft_n.value if kf_ft_fu.value else 1450),
            )
            _eintr = []
            for _key, _name in [("tal", "P-001 PW Talstraße"), ("rs", "P3.1 RS-Pumpwerk"), ("ft", "P10.1 Faulturm")]:
                _c = _neu[_key]
                if _c != _alt[_key]:
                    _txt = f"{_name}: {_c['typ']}, Laufrad ø{_c['d']} mm, " + (f"FU {_c['n']} 1/min" if _c["fu"] else "Festdrehzahl")
                    _eintr.append(_txt)
            _neu["protokoll"] = list(_alt.get("protokoll", [])) + _eintr
            if _eintr:
                set_pk(_neu)
                kf_meldung = "✅ Umbau durchgeführt und in Betrieb genommen: " + "; ".join(_eintr)
            else:
                kf_meldung = "ℹ️ Keine Änderung gegenüber dem installierten Zustand."
    return (kf_meldung,)


@app.cell
def _(get_pk, np):
    # === PUMPENMODELL: KSB-Kennlinien · Anlagenkennlinien · Betriebspunkte ===
    # Kennlinien digitalisiert aus KSB Kennlinienheft Sewatec/Sewabloc.
    # H-Stützstellen im Abstand 10 m³/h ab Q = 0 (letzter Wert = Kurvenende q_end),
    # η-Stützstellen = Markierungen im Diagramm (Q in m³/h, η in %).
    # Betriebspunkt = Schnittpunkt Pumpenkennlinie / Anlagenkennlinie (kein fester Wert).

    def _pchip(xs, ys, x):
        """Monotone kubische Hermite-Interpolation (Fritsch-Carlson), lineare Extrapolation."""
        n = len(xs)
        hh = [xs[i + 1] - xs[i] for i in range(n - 1)]
        dd = [(ys[i + 1] - ys[i]) / hh[i] for i in range(n - 1)]
        m = [0.0] * n
        for k in range(1, n - 1):
            if dd[k - 1] * dd[k] > 0:
                w1 = 2 * hh[k] + hh[k - 1]
                w2 = hh[k] + 2 * hh[k - 1]
                m[k] = (w1 + w2) / (w1 / dd[k - 1] + w2 / dd[k])
        if n > 2:
            m0 = ((2 * hh[0] + hh[1]) * dd[0] - hh[0] * dd[1]) / (hh[0] + hh[1])
            if m0 * dd[0] <= 0: m0 = 0.0
            elif dd[0] * dd[1] <= 0 and abs(m0) > abs(3 * dd[0]): m0 = 3 * dd[0]
            m[0] = m0
            mn = ((2 * hh[-1] + hh[-2]) * dd[-1] - hh[-1] * dd[-2]) / (hh[-1] + hh[-2])
            if mn * dd[-1] <= 0: mn = 0.0
            elif dd[-1] * dd[-2] <= 0 and abs(mn) > abs(3 * dd[-1]): mn = 3 * dd[-1]
            m[-1] = mn
        else:
            m[0] = m[-1] = dd[0]
        if x <= xs[0]:
            return ys[0] + m[0] * (x - xs[0])
        if x >= xs[-1]:
            return ys[-1] + m[-1] * (x - xs[-1])
        i = 0
        while xs[i + 1] < x:
            i += 1
        t = (x - xs[i]) / hh[i]
        h00 = (1 + 2 * t) * (1 - t) ** 2
        h10 = t * (1 - t) ** 2
        h01 = t ** 2 * (3 - 2 * t)
        h11 = t ** 2 * (t - 1)
        return h00 * ys[i] + h10 * hh[i] * m[i] + h01 * ys[i + 1] + h11 * hh[i] * m[i + 1]

    KENNLINIEN = dict()
    def _kl(typ, d, n, q_end, h, eta, q_min=None, q_max=None):
        qs = [10.0 * i for i in range(len(h) - 1)] + [float(q_end)]
        KENNLINIEN[(typ, d, n)] = dict(typ=typ, d=d, n=n, q_end=float(q_end), q=qs, h=h,
                                        eta_q=[0.0] + [p[0] for p in eta], eta_v=[0.0] + [p[1] for p in eta],
                                        q_min=q_min, q_max=q_max)

    # --- Bestand ---
    _kl("Sewabloc F 100-316", 279, 1450, 206,
        [30.01, 29.52, 29.04, 28.56, 28.10, 27.64, 27.19, 26.75, 26.31, 25.88, 25.45, 25.01,
         24.58, 24.15, 23.72, 23.28, 22.84, 22.39, 21.93, 21.47, 21.00, 20.71],
        [(31.7, 30), (50.6, 40), (89.5, 50), (123, 54), (165, 55.8), (206, 54.6)])
    _kl("Sewabloc F 100-252", 235, 1450, 184,
        [15.30, 15.14, 14.89, 14.56, 14.17, 13.71, 13.20, 12.66, 12.08, 11.48, 10.86, 10.25,
         9.64, 9.05, 8.48, 7.95, 7.46, 7.03, 6.66, 6.53],
        [(23, 20), (39, 30), (61.7, 40), (85, 45), (109, 46.5), (136.3, 45), (184, 38)], q_max=127)
    _kl("Sewabloc F 100-254", 200, 1450, 118,
        [10.68, 10.49, 10.21, 9.85, 9.42, 8.91, 8.33, 7.67, 6.95, 6.15, 5.30, 4.38, 3.60],
        [(19.5, 20), (33.3, 30), (60.9, 40), (70.2, 41.0), (84.2, 40), (114.8, 30)])
    # --- Optimierungsvarianten (Kennlinienblatt Maßnahmen) ---
    _kl("Sewabloc F 100-316", 310, 1450, 237,
        [37.51, 37.03, 36.54, 36.06, 35.59, 35.11, 34.64, 34.18, 33.71, 33.25, 32.80, 32.34,
         31.90, 31.45, 31.01, 30.57, 30.13, 29.70, 29.27, 28.84, 28.41, 27.99, 27.57, 27.16, 26.87],
        [(38.6, 30), (62, 40), (106, 50), (161, 54), (193.6, 54.7), (221.4, 54), (237, 53.2)])
    _kl("Sewabloc F 100-316", 310, 905, 148,
        [14.30, 14.09, 13.87, 13.62, 13.36, 13.09, 12.82, 12.53, 12.25, 11.97, 11.69, 11.41,
         11.15, 10.90, 10.67, 10.49],
        [(29, 30), (46, 40), (60, 45), (97, 50), (130, 51.1), (155, 50)])
    _kl("Sewatec E 100-317", 286, 1450, 219,
        [29.68, 28.77, 27.90, 27.07, 26.27, 25.50, 24.75, 24.02, 23.31, 22.61, 21.92, 21.23,
         20.53, 19.84, 19.13, 18.40, 17.66, 16.90, 16.11, 15.29, 14.43, 13.53, 12.68],
        [(66.6, 55), (83, 60), (111.4, 65), (145.4, 66.8), (184.4, 65), (217.8, 60)], q_min=44)
    _kl("Sewatec E 100-317", 299, 1450, 229,
        [32.32, 31.30, 30.35, 29.47, 28.64, 27.87, 27.14, 26.45, 25.79, 25.15, 24.53, 23.92,
         23.31, 22.69, 22.06, 21.40, 20.73, 20.01, 19.26, 18.46, 17.60, 16.67, 15.68, 14.72],
        [(66.8, 55), (81.9, 60), (104, 65), (140.5, 69), (158.7, 69.4), (176, 69), (211.8, 65)], q_min=48)
    _kl("Sewatec E 100-317", 315, 1450, 239,
        [36.52, 35.42, 34.41, 33.49, 32.64, 31.87, 31.15, 30.48, 29.85, 29.25, 28.67, 28.11,
         27.55, 26.98, 26.39, 25.79, 25.14, 24.46, 23.72, 22.92, 22.05, 21.10, 20.07, 18.93, 17.81],
        [(68.5, 55), (82.8, 60), (103.3, 65), (129, 69), (176, 71.7), (219.5, 69)], q_min=52)
    _kl("Sewatec E 100-317", 328, 1450, 250,
        [39.46, 38.31, 37.27, 36.33, 35.48, 34.71, 34.00, 33.36, 32.77, 32.21, 31.69, 31.18,
         30.67, 30.17, 29.65, 29.11, 28.53, 27.91, 27.23, 26.49, 25.67, 24.77, 23.77, 22.66, 21.44, 20.09],
        [(69.9, 55), (84.9, 60), (104.4, 65), (126.8, 69), (151, 72), (190.9, 74.1), (225, 72), (241.3, 69)], q_min=56)
    _kl("Sewabloc F 80-252", 180, 1450, 119,
        [10.55, 10.53, 10.24, 9.70, 8.97, 8.10, 7.12, 6.09, 5.05, 4.05, 3.12, 2.32, 1.75],
        [(7.9, 20), (13.8, 30), (22.4, 40), (39.3, 50), (46.8, 51.5), (58, 50), (81, 40), (100, 30), (116, 20)])
    _kl("Sewabloc F 100-254", 265, 960, 90,
        [10.08, 10.02, 9.91, 9.75, 9.53, 9.27, 8.97, 8.62, 8.23, 7.81],
        [(22.5, 30), (34.3, 40), (50.5, 50), (73.3, 58), (97, 60.3)])
    _kl("Sewabloc F 100-254", 265, 1210, 120,
        [16.10, 16.07, 15.91, 15.68, 15.43, 15.13, 14.86, 14.48, 14.07, 13.64, 13.13, 12.61, 12.21],
        [(27.8, 30), (41.9, 40), (61.5, 50), (86.9, 58), (117.7, 61.4), (156, 58), (191.8, 50)])
    _kl("Sewabloc F 80-252", 200, 1450, 132,
        [12.85, 12.85, 12.54, 12.02, 11.38, 10.61, 9.76, 8.78, 7.78, 6.90, 6.03, 5.17, 4.36, 3.63, 3.50],
        [(7.9, 20), (12.8, 30), (20.8, 40), (34.9, 50), (59.7, 55.0), (84.9, 50), (114.8, 40)])
    _kl("Sewabloc F 80-252", 210, 1450, 139,
        [14.17, 14.17, 13.85, 13.26, 12.63, 11.93, 11.06, 10.08, 9.11, 8.10, 7.19, 6.39, 5.62, 4.91, 4.18],
        [(12.7, 30), (20.2, 40), (32.7, 50), (50.6, 56), (64.9, 57.1), (78.2, 56), (104.2, 50)])

    def _ns(typ, d):
        return sorted(kk[2] for kk in KENNLINIEN if kk[0] == typ and kk[1] == d)

    def _basis(kl):
        """Nächstgelegene gezeichnete Drehzahlkurve und Drehzahlverhältnis."""
        typ, d, n = kl
        if kl in KENNLINIEN:
            return KENNLINIEN[kl], 1.0
        n0 = min(_ns(typ, d), key=lambda x: abs(x - n))
        return KENNLINIEN[(typ, d, n0)], n / n0

    def h_pumpe(kl, q):
        """Förderhöhe; Drehzahlen ohne eigene Kurve über Affinitätsgesetze (Q ~ n, H ~ n²)."""
        k, r = _basis(kl)
        return r * r * _pchip(k["q"], k["h"], q / r)

    def eta_pumpe(kl, q):
        """Wirkungsgrad; zwischen gezeichneten Drehzahlkurven linear interpoliert (wie im KSB-Diagramm)."""
        typ, d, n = kl
        _e = lambda k, qq: _pchip(k["eta_q"], k["eta_v"], qq)
        if kl in KENNLINIEN:
            v = _e(KENNLINIEN[kl], q)
        else:
            ns = _ns(typ, d)
            if len(ns) >= 2:
                lo = max([x for x in ns if x <= n], default=ns[0])
                hi = min([x for x in ns if x >= n], default=ns[-1])
                if lo == hi:
                    v = _e(KENNLINIEN[(typ, d, lo)], q)
                else:
                    w = (n - lo) / (hi - lo)
                    v = (1 - w) * _e(KENNLINIEN[(typ, d, lo)], q) + w * _e(KENNLINIEN[(typ, d, hi)], q)
            else:
                k, r = _basis(kl)
                v = _e(k, q / r)
        return max(0.01, v / 100.0)

    def q_end(kl):
        k, r = _basis(kl)
        return k["q_end"] * r

    def grenzen(kl):
        k, r = _basis(kl)
        return (k["q_min"] * r if k["q_min"] else None, k["q_max"] * r if k["q_max"] else None)

    # --- Anlagenkennlinien je Standort: H = H_geo + k·Q² ---
    STANDORTE = dict(
        APW03=dict(name="PW Talstraße → Speicherbecken B-002/B-003", z_aus=75.00, z_ref=55.00,
                   h_geo=20.0, k=6.1 / 85.0 ** 2, rho=1000.0),
        RS=dict(name="RS-Pumpwerk → Verteilerbauwerk BB", h_geo=6.0, k=6.08 / 80.0 ** 2, rho=1003.0),
        FT=dict(name="Umwälzkreis Faulturm (geschlossen)", h_geo=0.0, k=9.64 / 35.0 ** 2, rho=1100.0),
    )

    def h_anlage(ort, q, h_geo=None):
        s = STANDORTE[ort]
        hg = s["h_geo"] if h_geo is None else h_geo
        return hg + s["k"] * q * q

    def betriebspunkt(kl, ort, n_par=1, h_geo=None):
        """Schnittpunkt Pumpen-/Anlagenkennlinie. n_par gleiche Pumpen parallel."""
        f = lambda qg: h_pumpe(kl, qg / n_par) - h_anlage(ort, qg, h_geo)
        lo, hi = 0.5, q_end(kl) * n_par
        if f(lo) <= 0:
            return dict(Q=0.0, Q_ges=0.0, H=h_pumpe(kl, 0.0), eta=0.0, gefoerdert=False)
        if f(hi) > 0:
            qg = hi
        else:
            for _ in range(60):
                mid = 0.5 * (lo + hi)
                if f(mid) > 0: lo = mid
                else: hi = mid
            qg = 0.5 * (lo + hi)
        q1 = qg / n_par
        return dict(Q=q1, Q_ges=qg, H=h_pumpe(kl, q1), eta=eta_pumpe(kl, q1), gefoerdert=True)

    # --- Aggregate (Stammdaten, Typenschild, Messstellen) ---
    _MOT15 = dict(hersteller="VEM", typ="K21R 160 L4", pn=15.0, un="400 V Δ", i_n=27.4, cos=0.85,
                  n_n=1460, ie="IE3", eta=(93.0, 93.1, 92.4), ip="IP55", isokl="F", bg="160L")
    _MOT75 = dict(hersteller="VEM", typ="K21R 132 M4", pn=7.5, un="400 V Δ", i_n=14.0, cos=0.84,
                  n_n=1455, ie="IE3", eta=(92.0, 92.1, 91.3), ip="IP55", isokl="F", bg="132M")
    _MOT4 = dict(hersteller="VEM", typ="K21R 112 M4", pn=4.0, un="400 V Δ", i_n=7.9, cos=0.82,
                 n_n=1445, ie="IE3", eta=(89.0, 89.2, 88.1), ip="IP55", isokl="F", bg="112M")
    _BS_RS = dict(zip(["P3.1", "P3.2", "P3.3", "P3.4", "P3.5", "P3.6"],
                      [118420, 121050, 116880, 119730, 104210, 31560]))
    AGGREGATE = dict()
    AGGREGATE["P-001"] = dict(kks="P-001", bez="Förderpumpe PW Talstraße (Grundlast)", ort="APW03",
        kl=("Sewabloc F 100-316", 279, 1450), eta_m=0.93, motor=_MOT15, baujahr=2012, serien="9971018342/100",
        ausl_q=100, ausl_h=25.4, medium="Rohabwasser", rho=1000, t_med="10–20", dn_s=150, dn_d=100,
        fi="APW03-FI 01", fi_bez="Durchfluss Druckleitung", pi_s="APW03-PI 11", pi_d="APW03-PI 12",
        bh0=63480, anlauf="Stern-Dreieck")
    AGGREGATE["P-002"] = dict(AGGREGATE["P-001"], kks="P-002", bez="Förderpumpe PW Talstraße (Spitzenlast/Reserve)",
        serien="9971018343/100", pi_s="APW03-PI 13", pi_d="APW03-PI 14", bh0=2960)
    for _i, _k in enumerate(["P3.1", "P3.2", "P3.3", "P3.4", "P3.5", "P3.6"]):
        AGGREGATE[_k] = dict(kks=_k, bez="Rücklaufschlammpumpe", ort="RS",
            kl=("Sewabloc F 100-252", 235, 1450), eta_m=0.92, motor=_MOT75, baujahr=2011,
            serien=f"9968204{17 + _i}/100", ausl_q=95, ausl_h=11.2, medium="Rücklaufschlamm", rho=1003,
            t_med="10–20", dn_s=125, dn_d=100, fi=f"FI 41{_i + 1}", fi_bez="Förderstrom",
            pi_s=f"PI 42{_i + 1}", pi_d=f"PI 43{_i + 1}",
            bh0=_BS_RS[_k], anlauf="Stern-Dreieck")
    AGGREGATE["P10.1"] = dict(kks="P10.1", bez="Umwälzpumpe Faulturm (Betrieb)", ort="FT",
        kl=("Sewabloc F 100-254", 200, 1450), eta_m=0.89, motor=_MOT4, baujahr=2014, serien="9973556120/100",
        ausl_q=50, ausl_h=8.9, medium="eingedickter Schlamm / Faulschlamm", rho=1100, t_med="35–38",
        dn_s=125, dn_d=100, fi="FI 601", fi_bez="Durchfluss Sammelleitung", pi_s="PI 602", pi_d="PI 603",
        bh0=98640, anlauf="direkt")
    AGGREGATE["P10.2"] = dict(AGGREGATE["P10.1"], kks="P10.2", bez="Umwälzpumpe Faulturm (Reserve)",
        serien="9973556121/100", pi_s="PI 604", pi_d="PI 605", bh0=7410)

    for _ag in AGGREGATE.values():
        _ag["n_nenn"] = 1450
        _ag["fu"] = False
        _ag["umbau"] = ""
    _pk = get_pk()
    _p001_alt = dict(AGGREGATE["P-001"])
    _NEU = {
        "Sewatec E 100-317": dict(motor=_MOT15, eta_m=0.93, ausl_q=85, ausl_h=26.0, serien="9985120447/100"),
        "Sewabloc F 80-252": dict(motor=_MOT4, eta_m=0.89, ausl_q=35, ausl_h=9.6, serien="9985120452/100"),
    }
    for _kks, _key in [("P-001", "tal"), ("P3.1", "rs"), ("P10.1", "ft")]:
        _c = _pk[_key]
        _ag = AGGREGATE[_kks]
        if _c.get("umsetzen"):
            _ag.update(motor=_p001_alt["motor"], eta_m=_p001_alt["eta_m"], baujahr=_p001_alt["baujahr"],
                       serien=_p001_alt["serien"], ausl_q=_p001_alt["ausl_q"], ausl_h=_p001_alt["ausl_h"],
                       bh0=_p001_alt["bh0"], umbau="umgesetzt aus PW Talstraße")
        elif _c["typ"] != _ag["kl"][0]:
            _ag.update(_NEU[_c["typ"]], baujahr=2026, bh0=0, umbau="Neupumpe")
        elif _c["d"] != _ag["kl"][1]:
            _ag["umbau"] = "Laufrad getauscht"
        _ag["kl"] = (_c["typ"], _c["d"], _c["n"] if _c["fu"] else 1450)
        _ag["fu"] = bool(_c["fu"])
        if _ag["fu"]:
            _ag["anlauf"] = "über FU"
            _ag["umbau"] = (_ag["umbau"] + ", FU nachgerüstet").lstrip(", ")

    RS_N_MAX = 6
    RS_Q_PUMPE = betriebspunkt(AGGREGATE["P3.2"]["kl"], "RS")["Q"]
    RS_Q_P31 = betriebspunkt(AGGREGATE["P3.1"]["kl"], "RS")["Q"]

    def rs_stufen(q_zu_m3d, rv):
        """Anzahl RS-Pumpen in Betrieb (Stufenschaltung auf RS-Sollwert)."""
        return int(min(RS_N_MAX, max(1, round(q_zu_m3d * rv / 24.0 / max(RS_Q_PUMPE, 1.0)))))

    # --- PW Talstraße: Schaltbetrieb über Pumpensumpf (Minutenschritte) ---
    TAL = dict(A_sumpf=25.0, z_sohle=53.90, z_aus1=54.60, z_ein1=55.40, z_ein2=55.80, z_aus2=55.10,
               z_hw=56.20, z_nue=56.60, z_achse=51.80, q_tw=42.5, V_sb=800.0, q_dr=42.0)
    _TG = [0.55, 0.45, 0.40, 0.38, 0.40, 0.50, 0.75, 1.05, 1.25, 1.35, 1.35, 1.30,
           1.25, 1.20, 1.15, 1.10, 1.10, 1.15, 1.20, 1.20, 1.10, 0.95, 0.80, 0.65]
    _tgm = sum(_TG) / 24.0
    TAGESGANG = [v / _tgm for v in _TG]

    def talstrasse_sim(hist, th, q_tw_ka=12000.0):
        """Schaltbetrieb PW Talstraße der letzten 48 h (2-min-Schritte, 12 h Vorlauf)."""
        kl1 = AGGREGATE["P-001"]["kl"]
        s = STANDORTE["APW03"]
        z0, dz = 54.2, 0.1
        zg = [z0 + dz * i for i in range(26)]
        bp1 = [betriebspunkt(kl1, "APW03", 1, s["z_aus"] - z) for z in zg]
        bp2 = [betriebspunkt(kl1, "APW03", 2, s["z_aus"] - z) for z in zg]
        q1g = [b["Q"] for b in bp1]; h1g = [b["H"] for b in bp1]
        q2g = [b["Q"] for b in bp2]; h2g = [b["H"] for b in bp2]
        def _zi(arr, z):
            x = min(max((z - z0) / dz, 0.0), len(arr) - 1.001)
            i = int(x); return arr[i] + (arr[i + 1] - arr[i]) * (x - i)
        ht = [p["t"] for p in hist] if hist else [0.0]
        fq = [p.get("Q_roh", q_tw_ka) / q_tw_ka for p in hist] if hist else [1.0]
        t0 = int(th) - 60
        qin_h = [TAL["q_tw"] * TAGESGANG[(t0 + j) % 24] * float(np.interp(t0 + j + 0.5, ht, fq)) for j in range(61)]
        dt = 2.0 / 60.0
        n = int(round(60.0 / dt))
        z = 55.00; on1 = False; on2 = False; V = 380.0
        T, Z, QF, Q1, O1, O2, H1, VS, UEB, NUE = [], [], [], [], [], [], [], [], [], []
        for i in range(n):
            t = t0 + i * dt
            q_in = qin_h[int(i * dt)]
            if z >= TAL["z_ein1"]: on1 = True
            if z <= TAL["z_aus1"]: on1 = False
            if z >= TAL["z_ein2"]: on2 = True
            if z <= TAL["z_aus2"]: on2 = False
            if on1 and on2:
                qp = _zi(q2g, z); q_out = 2 * qp; hp = _zi(h2g, z)
            elif on1:
                qp = _zi(q1g, z); q_out = qp; hp = _zi(h1g, z)
            else:
                qp = 0.0; q_out = 0.0; hp = 0.0
            q_dr = min(TAL["q_dr"], V / dt + q_out)
            V = V + (q_out - q_dr) * dt
            ueb = V > TAL["V_sb"]
            V = min(max(V, 0.0), TAL["V_sb"])
            nue = z >= TAL["z_nue"]
            if t >= th - 48.0:
                T.append(t); Z.append(z); QF.append(q_out); Q1.append(qp if on1 else 0.0)
                O1.append(on1); O2.append(on1 and on2); H1.append(hp); VS.append(V)
                UEB.append(ueb); NUE.append(nue)
            z = min(z + (q_in - q_out) * dt / TAL["A_sumpf"], TAL["z_nue"])
        d = int(th // 24)
        a, b = 24.0 * (d - 1), 24.0 * d
        lz1 = sum(1 for t, o in zip(T, O1) if a <= t < b and o) * dt
        lz2 = sum(1 for t, o in zip(T, O2) if a <= t < b and o) * dt
        sp1 = sum(1 for j in range(1, len(T)) if a <= T[j] < b and O1[j] and not O1[j - 1])
        sp2 = sum(1 for j in range(1, len(T)) if a <= T[j] < b and O2[j] and not O2[j - 1])
        q_ref = _zi(q1g, 55.0)
        vor = 0.0
        for p in hist:
            if p["t"] < th - 48.0:
                vor += min(1.0, TAL["q_tw"] * p.get("Q_roh", q_tw_ka) / q_tw_ka / q_ref)
        bh1 = AGGREGATE["P-001"]["bh0"] + vor + sum(O1) * dt
        bh2 = AGGREGATE["P-002"]["bh0"] + sum(O2) * dt
        return dict(t=T, z=Z, q=QF, q1=Q1, on1=O1, on2=O2, h1=H1, v_sb=VS, ueb=UEB, nue=NUE,
                    lz1=lz1, lz2=lz2, sp1=sp1, sp2=sp2, bh1=bh1, bh2=bh2, dt=dt)

    # --- Typenschilder (SVG) ---
    def typenschild_pumpe_svg(a):
        kl = a["kl"]
        _uid = a["kks"].replace(".", "_").replace("-", "_")
        return f'''<svg viewBox="0 0 420 230" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:420px;height:auto">
  <defs><linearGradient id="tp{_uid}" x1="0%" y1="0%" x2="0%" y2="100%">
    <stop offset="0%" style="stop-color:#ececf0"/><stop offset="100%" style="stop-color:#b4b4ba"/></linearGradient></defs>
  <rect x="3" y="3" width="414" height="224" rx="6" fill="url(#tp{_uid})" stroke="#6a6a78" stroke-width="1"/>
  <rect x="3" y="3" width="414" height="38" rx="6" fill="#1a4a90"/>
  <text x="34" y="30" fill="#ffffff" font-family="Arial,sans-serif" font-size="21" font-weight="bold" letter-spacing="3">KSB</text>
  <text x="386" y="28" text-anchor="end" fill="#ffffff" font-family="Arial,sans-serif" font-size="12">Frankenthal · Germany</text>
  <text x="20" y="64" fill="#1a1a1a" font-family="Arial,sans-serif" font-size="10.5" font-weight="bold">Typ</text>
  <text x="95" y="64" fill="#1a1a1a" font-family="Arial,sans-serif" font-size="13" font-weight="bold">{kl[0]}</text>
  <line x1="95" y1="68" x2="400" y2="68" stroke="#404050" stroke-width="0.5"/>
  <text x="20" y="88" fill="#1a1a1a" font-family="Arial,sans-serif" font-size="10.5" font-weight="bold">Nr.</text>
  <text x="95" y="88" fill="#1a1a1a" font-family="Arial,sans-serif" font-size="11">{a["serien"]}</text>
  <text x="270" y="88" fill="#1a1a1a" font-family="Arial,sans-serif" font-size="10.5" font-weight="bold">Baujahr</text>
  <text x="335" y="88" fill="#1a1a1a" font-family="Arial,sans-serif" font-size="11">{a["baujahr"]}</text>
  <line x1="20" y1="96" x2="400" y2="96" stroke="#1a4a90" stroke-width="1"/>
  <text x="20" y="118" fill="#1a1a1a" font-family="Arial,sans-serif" font-size="10.5" font-weight="bold">Q</text>
  <text x="60" y="118" fill="#1a1a1a" font-family="Arial,sans-serif" font-size="12">{a["ausl_q"]:.0f}&#160;m³/h</text>
  <text x="160" y="118" fill="#1a1a1a" font-family="Arial,sans-serif" font-size="10.5" font-weight="bold">H</text>
  <text x="185" y="118" fill="#1a1a1a" font-family="Arial,sans-serif" font-size="12">{a["ausl_h"]:.1f}&#160;m</text>
  <text x="270" y="118" fill="#1a1a1a" font-family="Arial,sans-serif" font-size="10.5" font-weight="bold">n</text>
  <text x="290" y="118" fill="#1a1a1a" font-family="Arial,sans-serif" font-size="12">{a.get("n_nenn", 1450)}&#160;1/min</text>
  <text x="20" y="142" fill="#1a1a1a" font-family="Arial,sans-serif" font-size="10.5" font-weight="bold">Laufrad-Ø</text>
  <text x="95" y="142" fill="#1a1a1a" font-family="Arial,sans-serif" font-size="12">{kl[1]}&#160;mm</text>
  <text x="270" y="142" fill="#1a1a1a" font-family="Arial,sans-serif" font-size="10.5" font-weight="bold">PN</text>
  <text x="300" y="142" fill="#1a1a1a" font-family="Arial,sans-serif" font-size="12">10</text>
  <text x="20" y="166" fill="#1a1a1a" font-family="Arial,sans-serif" font-size="10.5" font-weight="bold">Werkstoff</text>
  <text x="95" y="166" fill="#1a1a1a" font-family="Arial,sans-serif" font-size="11">Gehäuse EN-GJL-250 · Laufrad EN-GJL-250</text>
  <line x1="20" y1="178" x2="400" y2="178" stroke="#1a4a90" stroke-width="1"/>
  <text x="210" y="200" text-anchor="middle" fill="#1a1a1a" font-family="Arial,sans-serif" font-size="10">Auslegungspunkt lt. Auftrag · Kennlinie siehe Herstellerunterlagen</text>
  <circle cx="18" cy="20" r="3.5" fill="#707080"/><circle cx="402" cy="20" r="3.5" fill="#707080"/>
  <circle cx="18" cy="212" r="3.5" fill="#707080"/><circle cx="402" cy="212" r="3.5" fill="#707080"/>
</svg>'''

    def typenschild_motor_svg(a):
        m = a["motor"]
        _uid = a["kks"].replace(".", "_").replace("-", "_")
        return f'''<svg viewBox="0 0 420 230" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:420px;height:auto">
  <defs><linearGradient id="tm{_uid}" x1="0%" y1="0%" x2="0%" y2="100%">
    <stop offset="0%" style="stop-color:#e4e6e8"/><stop offset="100%" style="stop-color:#a8acb0"/></linearGradient></defs>
  <rect x="3" y="3" width="414" height="224" rx="4" fill="url(#tm{_uid})" stroke="#5a5e66" stroke-width="1"/>
  <text x="34" y="30" fill="#1a1a1a" font-family="Arial,sans-serif" font-size="18" font-weight="bold">{m["hersteller"]}</text>
  <text x="386" y="30" text-anchor="end" fill="#1a1a1a" font-family="Arial,sans-serif" font-size="11">3~Mot  {m["typ"]}</text>
  <line x1="15" y1="40" x2="405" y2="40" stroke="#303038" stroke-width="1"/>
  <text x="20" y="62" fill="#1a1a1a" font-family="Arial,sans-serif" font-size="11">Nr. {a["serien"][:7]}-{a["baujahr"]}</text>
  <text x="300" y="62" fill="#1a1a1a" font-family="Arial,sans-serif" font-size="11">{m["ip"]} · Th.Cl. {m["isokl"]}</text>
  <text x="20" y="90" fill="#1a1a1a" font-family="Arial,sans-serif" font-size="13" font-weight="bold">{m["un"]}</text>
  <text x="130" y="90" fill="#1a1a1a" font-family="Arial,sans-serif" font-size="13" font-weight="bold">{m["i_n"]:.1f}&#160;A</text>
  <text x="220" y="90" fill="#1a1a1a" font-family="Arial,sans-serif" font-size="13" font-weight="bold">{m["pn"]:.1f}&#160;kW</text>
  <text x="310" y="90" fill="#1a1a1a" font-family="Arial,sans-serif" font-size="13" font-weight="bold">50&#160;Hz</text>
  <text x="20" y="116" fill="#1a1a1a" font-family="Arial,sans-serif" font-size="12">cos φ {m["cos"]:.2f}</text>
  <text x="130" y="116" fill="#1a1a1a" font-family="Arial,sans-serif" font-size="12">{m["n_n"]}&#160;1/min</text>
  <text x="220" y="116" fill="#1a1a1a" font-family="Arial,sans-serif" font-size="12">S1</text>
  <text x="310" y="116" fill="#1a1a1a" font-family="Arial,sans-serif" font-size="12">BG {m["bg"]}</text>
  <line x1="15" y1="130" x2="405" y2="130" stroke="#303038" stroke-width="0.8"/>
  <rect x="20" y="142" width="46" height="26" rx="3" fill="#1a1a1a"/>
  <text x="43" y="160" text-anchor="middle" fill="#ffffff" font-family="Arial,sans-serif" font-size="13" font-weight="bold">{m["ie"]}</text>
  <text x="80" y="153" fill="#1a1a1a" font-family="Arial,sans-serif" font-size="11">η 100 % · 75 % · 50 % Last</text>
  <text x="80" y="168" fill="#1a1a1a" font-family="Arial,sans-serif" font-size="12" font-weight="bold">{m["eta"][0]:.1f} · {m["eta"][1]:.1f} · {m["eta"][2]:.1f}&#160;%</text>
  <line x1="15" y1="182" x2="405" y2="182" stroke="#303038" stroke-width="0.8"/>
  <text x="20" y="204" fill="#1a1a1a" font-family="Arial,sans-serif" font-size="10">IEC/EN 60034 · Made in Germany</text>
  <circle cx="400" cy="212" r="3.5" fill="#60646c"/><circle cx="20" cy="18" r="3.5" fill="#60646c"/>
</svg>'''

    def p_el(kks, n_par=1, h_geo=None):
        """Elektrische Leistungsaufnahme einer Pumpe im Betriebspunkt [kW]."""
        a = AGGREGATE[kks]
        b = betriebspunkt(a["kl"], a["ort"], n_par, h_geo)
        if not b["gefoerdert"]:
            _q = 0.5 * q_end(a["kl"])
            return 0.4 * a["rho"] * 9.81 * _q / 3600.0 * h_pumpe(a["kl"], _q) / eta_pumpe(a["kl"], _q) / a["eta_m"] / 1000.0
        return a["rho"] * 9.81 * b["Q"] / 3600.0 * b["H"] / b["eta"] / a["eta_m"] / 1000.0

    # --- Energieversorgung: Stromliefervertrag, Stromkennzeichnung, BHKW ---
    # Vertragswerte sind Beispielwerte der Simulation und können hier angepasst werden.
    STROM = dict(
        lieferant="Stadtwerke Meckelberg GmbH", vertrag="Sondervertrag Gewerbe SV-G",
        vertragsnr="SV-2026-04471", laufzeit="01.01.2026 – 31.12.2027",
        arbeitspreise=[("Energiepreis (Arbeitspreis)", 10.30), ("Netzentgelt Mittelspannung (Arbeitspreis)", 4.60),
                       ("Konzessionsabgabe (Sondervertragskunde)", 0.11),
                       ("Umlagen (KWKG, Offshore-Netz, Aufschlag bes. Netznutzung)", 2.40),
                       ("Stromsteuer (ermäßigt, Produzierendes Gewerbe)", 0.05)],
        leistungspreis=96.0, grundpreis=480.0, mwst=19,
        mix=[("Erneuerbare Energien, finanziert aus der EEG-Umlage", 58), ("Sonstige erneuerbare Energien", 14),
             ("Erdgas", 13), ("Kohle", 12), ("Sonstige fossile Energieträger", 3), ("Kernkraft", 0)],
        co2_g_kwh=285, rad_g_kwh=0.0000, stand_mix="Stromkennzeichnung gem. § 42 EnWG, Bezugsjahr 2025",
        apw=dict(vertragsnr="SV-2026-04472", vertrag="Gewerbe Niederspannung (SLP)",
                 lieferstelle="PW Talstraße (APW-03), Zähler APW03-EZ 01",
                 arbeitspreise=[("Energiepreis (Arbeitspreis)", 11.20), ("Netzentgelt Niederspannung (Arbeitspreis)", 8.90),
                                ("Konzessionsabgabe (Tarifkunde)", 1.32),
                                ("Umlagen (KWKG, Offshore-Netz, Aufschlag bes. Netznutzung)", 2.40),
                                ("Stromsteuer (ermäßigt, Produzierendes Gewerbe)", 0.05)],
                 grundpreis=150.0),
    )
    BHKW = dict(bez="BHKW-Modul 1 (G10.1)", typ="Gas-Otto-Motor, 6 Zylinder, Faulgasbetrieb", p_el=125.0, eta_el=0.36,
                eta_th=0.47, hu=6.4, ch4=62, baujahr=2014, gas_nenn=1000.0)
    PV = dict(kwp=100.0, e_d=350.0)

    pm = dict(
        kennlinien=KENNLINIEN, standorte=STANDORTE, aggregate=AGGREGATE, p_el=p_el,
        q_end=q_end, grenzen=grenzen, konfig=_pk, rs_q_p31=RS_Q_P31, rs_stufen=rs_stufen,
        tagesgang=TAGESGANG, strom=STROM, bhkw=BHKW, pv=PV,
        h_pumpe=h_pumpe, eta_pumpe=eta_pumpe, h_anlage=h_anlage, betriebspunkt=betriebspunkt,
        rs_n_max=RS_N_MAX, rs_q_pumpe=RS_Q_PUMPE, tal=TAL, talstrasse_sim=talstrasse_sim,
        typenschild_pumpe_svg=typenschild_pumpe_svg, typenschild_motor_svg=typenschild_motor_svg,
    )
    return (pm,)


@app.cell
def _(mo):
    # === PERSISTENTER ZUSTAND mit mo.state ===
    get_sim_state, set_sim_state = mo.state(None)
    return get_sim_state, set_sim_state


@app.cell
def _(
    abschlag_schwelle, btn_1h, btn_24h, btn_6h, btn_7d, btn_reset,
    faellmittel, get_sim_state,
    mod_anammox, mod_intermit, mod_membran, mod_nh4_sensor,
    mod_p_online, mod_pv, mod_spektral, mod_stufe4, mod_truebung, mod_turbo,
    np, o2_soll, pm, regen_faktor, rs_verhaeltnis, set_sim_state,
    temperatur, ues_menge, zulauf_q,
):
    # === SIMULATIONSMODELL MIT ZEITDYNAMIK ===

    def calc_targets(ctrl):
        """Berechne stationäre Zielwerte aus Steuerungsparametern + Modifikationen."""
        rf = ctrl["regen_faktor"]
        Q_roh = ctrl["zulauf_q"] * rf
        T = ctrl["temperatur"]
        mods = ctrl.get("mods", {})

        abschlag_sw = ctrl["abschlag_schwelle"]
        Q_abschlag = max(0, Q_roh - abschlag_sw)
        Q = Q_roh - Q_abschlag

        csb_zu = 600 / rf
        bsb_zu = 300 / rf
        nh4_zu = 45 / rf
        no3_zu = 0.5
        p_zu = 10 / rf
        afs_zu = 350 / rf

        # Vorklärung — Spektralsonde verbessert VK-Steuerung
        vk_csb = 0.75 if mods.get("spektral") else 0.70
        csb_vk = csb_zu * 0.95 * vk_csb
        bsb_vk = bsb_zu * (0.80 if mods.get("spektral") else 0.75)
        afs_vk = afs_zu * 0.85 * 0.45
        nh4_vk = nh4_zu * 0.98
        p_vk = p_zu * 0.90

        # O₂-Sollwert — NH₄-geführte Belüftung optimiert automatisch
        o2_eff = ctrl["o2_soll"]
        if mods.get("nh4_sensor"):
            # Regelt O₂ dynamisch runter wenn NH₄ niedrig → Energiesparen
            o2_eff = min(ctrl["o2_soll"], max(1.0, ctrl["o2_soll"] * 0.75))

        # Belüftungseffizienz — Membranbelüfter verbessern O₂-Eintrag
        o2_faktor = 1.0
        if mods.get("membran"):
            o2_faktor = 1.35  # 35% besserer O₂-Transfer → gleiche Wirkung bei weniger Luft

        tf = 1.072 ** (T - 15)
        nitri = min(1.0, 0.6 * tf * (o2_eff * o2_faktor / 2.0))

        ts = float(np.clip(3.5 + (300 - ctrl["ues_menge"]) * 0.005, 2.0, 6.0))
        t_ts = max(4.0, 25 - ctrl["ues_menge"] * 0.04)

        # Rücklaufschlamm: Stufenschaltung P3.1–P3.6 (Kreiselpumpen ohne FU, je ca. 80 m³/h)
        q_rs_soll = Q * ctrl["rs_verhaeltnis"]
        q_rsp = ctrl.get("q_rs_pumpe", 80.0) * 24.0
        n_rs = int(min(ctrl.get("n_rs_max", 6), max(1, round(q_rs_soll / max(q_rsp, 1.0)))))
        Q_rs = ctrl.get("q_rs_p31", 80.0) * 24.0 + (n_rs - 1) * q_rsp
        rv_ist = Q_rs / max(Q, 1.0)

        # Denitrifikation — intermittierende Belüftung verbessert Deni deutlich
        deni_basis = min(0.90, 0.5 + rv_ist * 0.25)
        deni = min(0.95, deni_basis + 0.08) if mods.get("intermit") else deni_basis

        csb_bio = csb_vk * (1 - 0.85 * min(1.0, o2_eff * o2_faktor / 1.5))
        bsb_bio = bsb_vk * (1 - 0.95 * min(1.0, o2_eff * o2_faktor / 1.5))
        nh4_bio = nh4_vk * (1 - nitri)
        no3_bio = (nh4_vk - nh4_bio) * (1 - deni) + no3_zu

        # Seitenstromentstickung — reduziert interne N-Rückbelastung
        n_intern_red = 0.0
        if mods.get("anammox"):
            # Prozesswasser aus Entwässerung: ca. 15% der N-Fracht zurück
            # Anammox entfernt davon ~80% → Netto -12% auf Gesamt-N
            n_intern_red = 0.12
        n_bio = (nh4_bio + no3_bio + 1.5) * (1 - n_intern_red)

        # P-Elimination — Online-P-Messung ermöglicht effizientere Dosierung
        fm_eff = ctrl["faellmittel"]
        if mods.get("p_online"):
            fm_eff = ctrl["faellmittel"] * 1.25  # gleiche Menge wirkt 25% besser durch Timing

        bio_p = min(0.4, ts * 0.05)
        chem_p = min(0.7, fm_eff * 0.04)
        p_bio = max(0.15, p_vk * (1 - bio_p - chem_p))

        isv = float(np.clip(80 + (ts - 3.5) * 30 + max(0, (o2_eff - 3.0)) * 20, 60, 200))
        # Intermittierende Belüftung kann ISV leicht verbessern
        if mods.get("intermit"):
            isv = max(60, isv * 0.92)

        # Nachklärung — Trübungsmessung ermöglicht Frühwarnung + bessere RS-Steuerung
        nk_bonus = 0.02 if mods.get("truebung") else 0.0
        nk_w = max(0.85, min(0.98, 0.95 + nk_bonus - (Q / 3000 - 0.5) * 0.1 - (isv - 100) * 0.0005))
        afs_ab = float(np.clip(afs_vk * 0.1 * (1 - nk_w) + (4 if mods.get("truebung") else 5), 2, 30))

        csb_ab = max(15.0, csb_bio * (1 + afs_ab * 0.01))
        bsb_ab = max(3.0, bsb_bio * (1 + afs_ab * 0.005))

        # 4. Reinigungsstufe — GAK-Filter nach NK
        if mods.get("stufe4"):
            csb_ab = csb_ab * 0.55  # ~45% zusätzliche CSB-Elimination
            bsb_ab = bsb_ab * 0.65
            # Spurenstoffelimination (nicht direkt sichtbar, aber als Merkmal)

        ss_nk = float(np.clip(ts * isv / 1000 * 100, 20, 200))
        ts_rs = float(np.clip(ts * (1 + 1 / rv_ist) * 0.7, 5, 15))

        csb_abschlag = csb_zu * 0.70
        afs_abschlag = afs_zu * 0.50
        nh4_abschlag = nh4_zu * 0.95
        p_abschlag = p_zu * 0.90

        return dict(
            Q_zu=Q, Q_roh=Q_roh, Q_abschlag=Q_abschlag, T=T,
            csb_zu=csb_zu, bsb_zu=bsb_zu, nh4_zu=nh4_zu, no3_zu=no3_zu,
            p_zu=p_zu, afs_zu=afs_zu,
            csb_abschlag=csb_abschlag, afs_abschlag=afs_abschlag,
            nh4_abschlag=nh4_abschlag, p_abschlag=p_abschlag,
            csb_vk=csb_vk, bsb_vk=bsb_vk, afs_vk=afs_vk, nh4_vk=nh4_vk, p_vk=p_vk,
            csb_bio=csb_bio, bsb_bio=bsb_bio, nh4_bio=nh4_bio, no3_bio=no3_bio,
            n_bio=n_bio, p_bio=p_bio,
            ts=ts, t_ts=t_ts, isv=isv, nitri=nitri, deni=deni,
            ss_nk=ss_nk, nk_w=nk_w, afs_ab=afs_ab,
            csb_ab=csb_ab, bsb_ab=bsb_ab, nh4_ab=nh4_bio, no3_ab=no3_bio,
            n_ab=n_bio, p_ab=p_bio, ph_ab=7.0 - ctrl["faellmittel"] * 0.005,
            Q_rs=Q_rs, ts_rs=ts_rs,
        )

    # Zeitkonstanten in Stunden (realistisch!)
    TAU = dict(
        Q_zu=1, T=2,  # hydraulisch: schnell
        csb_zu=1, bsb_zu=1, nh4_zu=1, no3_zu=1, p_zu=1, afs_zu=1,  # Zulauf: direkt
        csb_vk=2, bsb_vk=2, afs_vk=2, nh4_vk=1, p_vk=2,  # Vorklärung: Stunden
        csb_bio=6, bsb_bio=6,  # CSB-Abbau: Stunden
        nh4_bio=18, no3_bio=12, n_bio=18,  # Nitrifikation: langsam
        p_bio=8,  # P-Elimination: mittel
        ts=120, t_ts=168, isv=240,  # Schlamm: Tage bis Wochen
        nitri=24, deni=12,  # Raten: ~1 Tag
        ss_nk=24, nk_w=12, afs_ab=6,
        csb_ab=6, bsb_ab=6, nh4_ab=18, no3_ab=12, n_ab=18, p_ab=8,
        ph_ab=4, Q_rs=1, ts_rs=48,
        Q_roh=1, Q_abschlag=0.5,
        csb_abschlag=1, afs_abschlag=1, nh4_abschlag=1, p_abschlag=1,
    )

    # Relative Streuung (Variationskoeffizient) – realistisch für Kläranlagen
    NOISE = dict(
        Q_zu=0.08, T=0.01,  # Zulauf Q schwankt stark, T kaum
        csb_zu=0.12, bsb_zu=0.15, nh4_zu=0.10, no3_zu=0.20,  # Zulauf: hohe Streuung
        p_zu=0.10, afs_zu=0.15,
        csb_vk=0.08, bsb_vk=0.10, afs_vk=0.10, nh4_vk=0.08, p_vk=0.08,
        csb_bio=0.06, bsb_bio=0.06,  # Nach Biologie: moderater
        nh4_bio=0.08, no3_bio=0.10, n_bio=0.07, p_bio=0.06,
        ts=0.01, t_ts=0.005, isv=0.02,  # Schlamm: sehr stabil
        nitri=0.02, deni=0.02,
        ss_nk=0.03, nk_w=0.01, afs_ab=0.10,
        csb_ab=0.06, bsb_ab=0.08, nh4_ab=0.08, no3_ab=0.10,
        n_ab=0.07, p_ab=0.06, ph_ab=0.005,
        Q_rs=0.01, ts_rs=0.02,
        Q_roh=0.08, Q_abschlag=0.05,
        csb_abschlag=0.12, afs_abschlag=0.15, nh4_abschlag=0.10, p_abschlag=0.10,
    )

    def advance(state, targets, dt_hours):
        """Bewege aktuelle Werte Richtung Zielwerte mit Zeitkonstanten + Streuung."""
        new = {}
        for k in targets:
            tau = TAU.get(k, 12)
            old = state.get(k, targets[k])
            # Exponentieller Ansatz an Zielwert
            alpha = 1 - np.exp(-dt_hours / tau)
            base = old + (targets[k] - old) * alpha
            # Zufällige Streuung (proportional zum Wert)
            sigma = abs(targets[k]) * NOISE.get(k, 0.03)
            noise = np.random.normal(0, sigma) if sigma > 0 else 0
            new[k] = max(0.0, base + noise)
        return new

    # Aktuelle Steuerungswerte + Modifikationen
    mods = dict(
        p_online=mod_p_online.value, nh4_sensor=mod_nh4_sensor.value,
        spektral=mod_spektral.value, truebung=mod_truebung.value,
        membran=mod_membran.value, turbo=mod_turbo.value,
        intermit=mod_intermit.value, anammox=mod_anammox.value,
        stufe4=mod_stufe4.value, pv=mod_pv.value,
    )
    ctrl = dict(
        o2_soll=o2_soll.value, rs_verhaeltnis=rs_verhaeltnis.value,
        ues_menge=ues_menge.value, faellmittel=faellmittel.value,
        zulauf_q=zulauf_q.value, regen_faktor=regen_faktor.value,
        temperatur=temperatur.value, abschlag_schwelle=abschlag_schwelle.value,
        mods=mods, q_rs_pumpe=pm["rs_q_pumpe"], n_rs_max=pm["rs_n_max"], q_rs_p31=pm["rs_q_p31"],
    )
    targets = calc_targets(ctrl)

    # TAU dynamisch — Modifikationen beschleunigen bestimmte Regelungen
    TAU["p_ab"] = 3 if mods["p_online"] else 8  # Störgrößenaufschaltung halbiert Totzeit
    TAU["nh4_ab"] = 8 if mods["nh4_sensor"] else 18  # NH₄-geführt reagiert schneller
    TAU["nh4_bio"] = 8 if mods["nh4_sensor"] else 18
    TAU["n_ab"] = 8 if mods["nh4_sensor"] else 18
    TAU["csb_vk"] = 1 if mods["spektral"] else 2  # vorausschauende VK-Steuerung

    # Welcher Button wurde gedrückt?
    _b1 = btn_1h.value
    _b6 = btn_6h.value
    _b24 = btn_24h.value
    _b7d = btn_7d.value
    _breset = btn_reset.value

    prev = get_sim_state()

    # Bestimme Zeitschritt
    dt = 0
    do_reset = False
    if prev is not None:
        if _b1 != prev.get("_b1", 0): dt = 1
        elif _b6 != prev.get("_b6", 0): dt = 6
        elif _b24 != prev.get("_b24", 0): dt = 24
        elif _b7d != prev.get("_b7d", 0): dt = 168
        if _breset != prev.get("_breset", 0): do_reset = True

    if prev is None or do_reset:
        # Initialisierung: Start im stationären Zustand mit 48h Vorgeschichte
        np.random.seed(2026)  # reproduzierbar: identischer Startzustand bei allen Nutzern
        current = dict(targets)
        history = []
        for t_init in range(0, 49):
            noisy = {}
            for k in targets:
                sigma = abs(targets[k]) * NOISE.get(k, 0.03)
                noisy[k] = max(0.0, targets[k] + np.random.normal(0, sigma))
            noisy["t"] = t_init
            history.append(noisy)
        current = {k: v for k, v in history[-1].items() if k != "t"}
        total_hours = 48
    else:
        current = prev.get("current", dict(targets))
        history = prev.get("history", [])
        total_hours = prev.get("total_hours", 0)

        if dt > 0:
            # Bei großen Zeitschritten: in Teilschritten rechnen
            n_steps = max(1, dt)
            sub_dt = dt / n_steps
            for _ in range(n_steps):
                current = advance(current, targets, sub_dt)
                total_hours += sub_dt
                # Alle 1h einen History-Punkt speichern
                if len(history) == 0 or (total_hours - history[-1]["t"]) >= 0.99:
                    history.append(dict(current, t=total_hours))

            # History auf max 500 Punkte begrenzen
            if len(history) > 500:
                history = history[-500:]

    # Wirkungsgrade aus aktuellen Werten
    eta_csb = (1 - current["csb_ab"] / max(1, current["csb_zu"])) * 100
    eta_n = (1 - current["n_ab"] / max(1, current["nh4_zu"] + current["no3_zu"] + 2)) * 100
    eta_p = (1 - current["p_ab"] / max(0.1, current["p_zu"])) * 100

    # Frachten
    Q = current["Q_zu"]
    fr_csb_zu = current["csb_zu"] * Q / 1000
    fr_csb_ab = current["csb_ab"] * Q / 1000
    fr_n_zu = (current["nh4_zu"] + current["no3_zu"] + 2) * Q / 1000
    fr_n_ab = current["n_ab"] * Q / 1000
    fr_p_zu = current["p_zu"] * Q / 1000
    fr_p_ab = current["p_ab"] * Q / 1000

    # === ENERGIE (kWh/d) je Unterverteilung ===
    def _energie(Q, _csb, _qroh):
        # UV-2 Gebläsestation: spez. ca. 0,20 kWh/m³ bei O₂-Soll 2 mg/L
        e_geblaese_ref = Q * 0.20 * (0.55 + 0.225 * ctrl["o2_soll"])
        e_belueftung = e_geblaese_ref
        if mods["nh4_sensor"]: e_belueftung *= 0.75  # NH₄-geführt spart ~25%
        if mods["membran"]: e_belueftung *= 0.70  # besserer O₂-Transfer
        if mods["intermit"]: e_belueftung *= 0.85  # Belüftungspausen
        e_geblaese = e_belueftung
        if mods["turbo"]: e_geblaese *= 0.82  # ~18% effizienter als Drehkolben
        # UV-1 Zulauf/Hebewerk: P1.1 (gleiches Modell wie Pumpen-Tab) + Rechen, Sandfang
        _qh = Q / 24
        _zh = 6.5 + 0.8 + (_qh / 600) ** 2 * 2.5
        _zeta = max(0.45, 0.72 - abs(_qh - _qh * 1.3 * 0.85) / max(1.0, _qh * 1.3) * 0.3)
        p_hebewerk = _qh / 3600 * 9810 * _zh / _zeta / 1000 / 0.93
        e_uv1 = p_hebewerk * 24 + 150
        # UV-3 Biologie/NK: RS-Pumpwerk (Stufenschaltung), Rezirkulation P4.1, Rührwerke, Räumer, ÜS
        n_rs_akt = pm["rs_stufen"](Q, ctrl["rs_verhaeltnis"])
        p_rs = pm["p_el"]("P3.1") + (n_rs_akt - 1) * pm["p_el"]("P3.2")
        p_rez = 2 * _qh / 3600 * 9810 * 0.4 / 0.65 / 1000 / 0.90
        e_uv3 = (p_rs + p_rez) * 24 + 150
        # UV-4 Schlammbehandlung: Umwälzpumpe Faulturm P10.1, Eindickung, Entwässerung, Dosierung
        p_ft = pm["p_el"]("P10.1")
        e_uv4 = p_ft * 24 + 200
        # UV-5 Betriebsgebäude / Grundlast (Labor, EMSR, Beleuchtung, Werkstatt, Hilfsenergie Heizung)
        e_uv5 = 450
        e_stufe4 = Q * 0.05 if mods["stufe4"] else 0  # GAK: ~0,05 kWh/m³
        e_anammox = 30 if mods["anammox"] else 0  # Heizung + Mischer
        e_pumpen = (p_hebewerk + p_rs + p_rez + p_ft) * 24
        e_uv = dict(uv1=e_uv1, uv2=e_geblaese, uv3=e_uv3 + e_anammox, uv4=e_uv4, uv5=e_uv5, uv6=e_stufe4)
        e_gesamt = sum(e_uv.values())
        # Außenstation PW Talstraße (eigener Netzanschluss): P-001 + Nebenverbraucher 1,2 kW
        _q_tal = pm["betriebspunkt"](pm["aggregate"]["P-001"]["kl"], "APW03")["Q"]
        _lauf_tal = min(1.0, pm["tal"]["q_tw"] * _qroh / 12000.0 / max(1.0, _q_tal))
        e_apw03 = pm["p_el"]("P-001") * 24 * _lauf_tal + 1.2 * 24

        # Energieerzeugung: BHKW (Faulgas, Bestand) + PV (Modifikation)
        _lf = _csb * Q / (600.0 * 12000.0)
        gas_nm3 = pm["bhkw"]["gas_nenn"] * _lf
        e_bhkw = min(gas_nm3 * pm["bhkw"]["hu"] * pm["bhkw"]["eta_el"], pm["bhkw"]["p_el"] * 24)
        e_pv = pm["pv"]["e_d"] if mods["pv"] else 0
        e_erzeugung = e_bhkw + e_pv
        e_netto = e_gesamt - e_erzeugung
        return dict(e_geblaese_ref=e_geblaese_ref, e_geblaese=e_geblaese, p_hebewerk=p_hebewerk, p_rs=p_rs,
                    p_rez=p_rez, p_ft=p_ft, e_stufe4=e_stufe4, e_pumpen=e_pumpen, e_uv=e_uv, e_gesamt=e_gesamt,
                    e_apw03=e_apw03, gas_nm3=gas_nm3, e_bhkw=e_bhkw, e_pv=e_pv, e_erzeugung=e_erzeugung,
                    e_netto=e_netto)

    _qroh_24 = float(np.mean([p.get("Q_roh", Q) for p in history[-24:]])) if history else Q
    _ea = _energie(Q, current["csb_zu"], _qroh_24)
    e_geblaese_ref, e_geblaese, p_hebewerk = _ea["e_geblaese_ref"], _ea["e_geblaese"], _ea["p_hebewerk"]
    p_rs, p_rez, p_ft, e_stufe4, e_pumpen = _ea["p_rs"], _ea["p_rez"], _ea["p_ft"], _ea["e_stufe4"], _ea["e_pumpen"]
    e_uv, e_gesamt, e_apw03, gas_nm3 = _ea["e_uv"], _ea["e_gesamt"], _ea["e_apw03"], _ea["gas_nm3"]
    e_bhkw, e_pv, e_erzeugung, e_netto = _ea["e_bhkw"], _ea["e_pv"], _ea["e_erzeugung"], _ea["e_netto"]
    # Vortag = Tagesmittel des letzten vollständigen Kalendertags (Zählerauswertung)
    _tag = int(total_hours // 24)
    _vt = [p for p in history if 24 * (_tag - 1) <= p["t"] < 24 * _tag] or history[-24:]
    _mq = float(np.mean([p["Q_zu"] for p in _vt])) if _vt else Q
    _mc = float(np.mean([p["csb_zu"] for p in _vt])) if _vt else current["csb_zu"]
    _mr = float(np.mean([p.get("Q_roh", _mq) for p in _vt])) if _vt else _qroh_24
    e_vortag = _energie(_mq, _mc, _mr)
    # Zählerwerte des Vortags ändern sich erst beim nächsten Tageswechsel (auch nach Umbauten/Sollwertänderungen)
    if prev is not None and not do_reset and prev.get("vt_tag") == _tag and prev.get("e_vortag"):
        e_vortag = prev["e_vortag"]

    # Betriebskosten Fällmittel
    fm_kosten = ctrl["faellmittel"] * 24 * 0.35 / 1000  # €/d, ~0.35 €/kg FeCl3 40%
    if mods["p_online"]: fm_kosten *= 0.80  # 20% weniger Verbrauch durch besseres Timing

    energie = e_netto  # Netto-Verbrauch für Anzeige

    # Alarme
    alarme = []
    if current["nh4_ab"] > 10: alarme.append(("⚠️", f"NH₄-N Ablauf: {current['nh4_ab']:.1f} > 10 mg/L"))
    if current["csb_ab"] > 75: alarme.append(("🔴", f"CSB Ablauf: {current['csb_ab']:.1f} > 75 mg/L"))
    if current["p_ab"] > 1.0: alarme.append(("⚠️", f"P-ges Ablauf: {current['p_ab']:.2f} > 1.0 mg/L"))
    if current["ss_nk"] > 150: alarme.append(("🔴", f"Schlammschicht NK: {current['ss_nk']:.0f} > 150 cm"))
    if current["ts"] > 5.0: alarme.append(("⚠️", f"TS Belebung: {current['ts']:.1f} > 5.0 g/L"))
    if current["isv"] > 150: alarme.append(("⚠️", f"ISV: {current['isv']:.0f} mL/g – Blähschlammgefahr"))
    if current.get("Q_abschlag", 0) > 10: alarme.append(("🚨", f"ABSCHLAG aktiv: {current['Q_abschlag']:.0f} m³/d in Vorfluter (nur mech. gereinigt)"))
    _rs_kap = pm["rs_n_max"] * pm["rs_q_pumpe"] * 24
    if Q * rs_verhaeltnis.value > _rs_kap * 1.04:
        alarme.append(("⚠️", f"RS-Pumpwerk an Förderkapazität: alle {pm['rs_n_max']} Pumpen in Betrieb ({_rs_kap:.0f} m³/d)"))

    # State speichern
    set_sim_state({
        "current": current, "targets": targets, "history": history,
        "total_hours": total_hours,
        "_b1": _b1, "_b6": _b6, "_b24": _b24, "_b7d": _b7d, "_breset": _breset,
        "eta_csb": eta_csb, "eta_n": eta_n, "eta_p": eta_p,
        "fr_csb_zu": fr_csb_zu, "fr_csb_ab": fr_csb_ab,
        "fr_n_zu": fr_n_zu, "fr_n_ab": fr_n_ab,
        "fr_p_zu": fr_p_zu, "fr_p_ab": fr_p_ab,
        "energie": energie, "alarme": alarme,
        "mods": mods, "e_gesamt": e_gesamt, "e_erzeugung": e_erzeugung,
        "e_netto": e_netto, "e_geblaese": e_geblaese, "e_pumpen": e_pumpen,
        "e_stufe4": e_stufe4, "e_bhkw": e_bhkw, "e_pv": e_pv,
        "e_uv": e_uv, "e_apw03": e_apw03, "e_geblaese_ref": e_geblaese_ref, "gas_nm3": gas_nm3,
        "e_vortag": e_vortag, "vt_tag": _tag,
        "p_hebewerk": p_hebewerk, "p_rs": p_rs, "p_rez": p_rez, "p_ft": p_ft,
        "fm_kosten": fm_kosten,
    })
    return


@app.cell
def _(
    abschlag_schwelle, btn_1h, btn_24h, btn_6h, btn_7d, btn_reset,
    detail_p11, detail_p51,
    armatur_auswahl, wartung_btn,
    faellmittel, get_sim_state,
    lab_analyse_btn, lab_kal_btn, lab_show_isv, lab_show_proto, lab_show_qs, lab_woche_btn,
    mod_anammox, mod_intermit, mod_membran, mod_nh4_sensor,
    mod_p_online, mod_pv, mod_spektral, mod_stufe4, mod_truebung, mod_turbo,
    mo, np, o2_soll, pm, get_pk, kf_meldung,
    kf_ft, kf_ft_fu, kf_ft_n, kf_reset_btn, kf_rs, kf_rs_fu, kf_rs_n,
    kf_tal, kf_tal_fu, kf_tal_n, kf_umbau_btn,
    regen_faktor, rs_verhaeltnis, temperatur,
    ues_menge, zulauf_q,
):
    import datetime as _dt

    st = get_sim_state()
    if st is None:
        mo.output.replace(mo.md("⏳ Initialisiere Simulation..."))
    else:
        c = st["current"]  # aktuelle Werte
        tgt = st["targets"]  # Zielwerte
        hist = st["history"]
        th = st["total_hours"]

        # === Hilfsfunktionen ===
        def vc(val, wl=None, wh=None, dl=None, dh=None):
            try: v = float(val)
            except: return "c-v"
            if dh is not None and v > dh: return "c-d"
            if dl is not None and v < dl: return "c-d"
            if wh is not None and v > wh: return "c-w"
            if wl is not None and v < wl: return "c-w"
            return "c-ok"

        def vr(label, val, unit, **kw):
            cls = vc(val, **kw) if kw else "c-v"
            return f'<tr><td style="padding:3px 8px 3px 0;color:#b2bec3;white-space:nowrap">{label}</td><td style="padding:3px 0 3px 8px;white-space:nowrap;font-weight:bold" class="{cls}">{val}&ensp;{unit}</td></tr>'

        def vtbl(rows):
            return f'<table style="border-collapse:collapse">{rows}</table>'

        def bar(pct, color="#0984e3"):
            pct = max(0, min(100, pct))
            return f'<div class="pls-bar"><div class="pls-bar-f" style="width:{pct}%;background:{color}"></div></div>'

        def delta_arrow(current_val, target_val, key=""):
            """Zeige Trend-Pfeil basierend auf Differenz zum Ziel."""
            try:
                diff = target_val - current_val
                if abs(diff) < 0.01 * max(abs(target_val), 0.1):
                    return '<span style="color:#b2bec3">→</span>'
                elif diff > 0:
                    return '<span style="color:#00b894">↑</span>'
                else:
                    return '<span style="color:#e17055">↓</span>'
            except:
                return ""

        zeit = _dt.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        tage = int(th // 24)
        stunden = int(th % 24)
        sim_zeit = f"Tag {tage}, {stunden:02d}:00"

        # Alarme
        if st["alarme"]:
            alm = '<div class="pls-c" style="border-color:#e94560"><h3 style="color:#e94560">⚡ Alarme & Meldungen</h3>'
            for typ, msg in st["alarme"]:
                alm += f'<div class="pls-alarm">{typ} {msg}</div>'
            alm += '</div>'
        else:
            alm = '<div class="pls-c" style="border-color:#00b894"><h3 style="color:#00b894">✅ Keine aktiven Alarme</h3></div>'

        # Header
        hdr = f'''<div class="pls"><div class="pls-hdr">
            <h2>🏭 Kläranlage Musterstadt – Prozessleitsystem</h2>
            <div class="pls-st">
                <span><span class="pls-dot" style="background:#00b894"></span> ONLINE</span>
                <span>EW: 50.000</span>
                <span>Q: {c["Q_zu"]:.0f} m³/d</span>
                <span class="pls-time-display">⏱ {sim_zeit}</span>
            </div>
        </div></div>'''

        # ====== ÜBERSICHT ======
        overview = mo.Html(f'''<div class="pls">
        {alm}
        <div class="pls-c" style="overflow-x:auto">
            <h3>Verfahrensschema (Live-Werte)</h3>
            <svg viewBox="0 0 1000 200" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto">
                <defs><marker id="ah" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" fill="#0984e3"/></marker></defs>
                <rect x="10" y="60" width="120" height="80" rx="6" fill="#2d3436" stroke="#0984e3" stroke-width="2"/>
                <text x="70" y="85" fill="#74b9ff" text-anchor="middle" font-size="12" font-family="monospace">Zulauf</text>
                <text x="70" y="105" fill="#dfe6e9" text-anchor="middle" font-size="10" font-family="monospace">{c["Q_zu"]:.0f} m³/d</text>
                <text x="70" y="120" fill="#dfe6e9" text-anchor="middle" font-size="10" font-family="monospace">CSB {c["csb_zu"]:.0f} mg/L</text>
                <line x1="130" y1="100" x2="170" y2="100" stroke="#0984e3" stroke-width="3" marker-end="url(#ah)"/>
                <rect x="170" y="60" width="120" height="80" rx="6" fill="#2d3436" stroke="#6c5ce7" stroke-width="2"/>
                <text x="230" y="85" fill="#a29bfe" text-anchor="middle" font-size="12" font-family="monospace">Vorklärung</text>
                <text x="230" y="105" fill="#dfe6e9" text-anchor="middle" font-size="10" font-family="monospace">CSB {c["csb_vk"]:.0f} mg/L</text>
                <text x="230" y="120" fill="#dfe6e9" text-anchor="middle" font-size="10" font-family="monospace">AFS {c["afs_vk"]:.0f} mg/L</text>
                <line x1="290" y1="100" x2="340" y2="100" stroke="#0984e3" stroke-width="3" marker-end="url(#ah)"/>
                <rect x="340" y="40" width="180" height="120" rx="6" fill="#2d3436" stroke="#00b894" stroke-width="2"/>
                <text x="430" y="65" fill="#55efc4" text-anchor="middle" font-size="12" font-family="monospace">Belebung</text>
                <text x="430" y="85" fill="#dfe6e9" text-anchor="middle" font-size="10" font-family="monospace">TS {c["ts"]:.1f} g/L | tTS {c["t_ts"]:.0f} d</text>
                <text x="430" y="105" fill="#dfe6e9" text-anchor="middle" font-size="10" font-family="monospace">NH₄→ {c["nh4_bio"]:.1f} mg/L</text>
                <text x="430" y="125" fill="#dfe6e9" text-anchor="middle" font-size="10" font-family="monospace">CSB→ {c["csb_bio"]:.1f} mg/L</text>
                <line x1="520" y1="100" x2="570" y2="100" stroke="#0984e3" stroke-width="3" marker-end="url(#ah)"/>
                <rect x="570" y="60" width="140" height="80" rx="6" fill="#2d3436" stroke="#fdcb6e" stroke-width="2"/>
                <text x="640" y="85" fill="#ffeaa7" text-anchor="middle" font-size="12" font-family="monospace">Nachklärung</text>
                <text x="640" y="105" fill="#dfe6e9" text-anchor="middle" font-size="10" font-family="monospace">Schicht {c["ss_nk"]:.0f} cm</text>
                <text x="640" y="120" fill="#dfe6e9" text-anchor="middle" font-size="10" font-family="monospace">ISV {c["isv"]:.0f} mL/g</text>
                <line x1="710" y1="100" x2="760" y2="100" stroke="#0984e3" stroke-width="3" marker-end="url(#ah)"/>
                <rect x="760" y="60" width="120" height="80" rx="6" fill="#2d3436" stroke="{'#00b894' if c['csb_ab']<75 else '#e17055'}" stroke-width="2"/>
                <text x="820" y="85" fill="{'#55efc4' if c['csb_ab']<75 else '#e17055'}" text-anchor="middle" font-size="12" font-family="monospace">Ablauf</text>
                <text x="820" y="105" fill="#dfe6e9" text-anchor="middle" font-size="10" font-family="monospace">CSB {c["csb_ab"]:.1f} mg/L</text>
                <text x="820" y="120" fill="#dfe6e9" text-anchor="middle" font-size="10" font-family="monospace">NH₄ {c["nh4_ab"]:.1f} mg/L</text>
                <path d="M 640 140 L 640 175 L 430 175 L 430 160" stroke="#e17055" stroke-width="2" fill="none" stroke-dasharray="5,3"/>
                <text x="535" y="190" fill="#e17055" text-anchor="middle" font-size="9" font-family="monospace">RS: {c["Q_rs"]:.0f} m³/d, TS {c["ts_rs"]:.1f} g/L</text>
            </svg>
        </div>
        <div class="pls-g3">
            <div class="pls-c"><h3>📊 Wirkungsgrade</h3>
                {vtbl(vr("CSB-Elimination", f"{st['eta_csb']:.1f}", "%", wl=90))}
                {bar(st['eta_csb'], '#00b894' if st['eta_csb']>90 else '#fdcb6e')}
                {vtbl(vr("N-Elimination", f"{st['eta_n']:.1f}", "%", wl=70))}
                {bar(st['eta_n'], '#00b894' if st['eta_n']>70 else '#fdcb6e')}
                {vtbl(vr("P-Elimination", f"{st['eta_p']:.1f}", "%", wl=80))}
                {bar(st['eta_p'], '#00b894' if st['eta_p']>80 else '#fdcb6e')}
            </div>
            <div class="pls-c"><h3>⚡ Energie & Betrieb</h3>
                {vtbl(
                    vr("Verbrauch brutto", f"{st.get('e_gesamt', st['energie']):.0f}", "kWh/d")
                    + vr("Erzeugung", f"{st.get('e_erzeugung', 0):.0f}", "kWh/d")
                    + vr("Netto", f"{st['energie']:.0f}", "kWh/d")
                    + vr("spez. Verbrauch", f"{st.get('e_gesamt', 0) * 365 / 50000:.1f}", "kWh/(EW·a)")
                    + vr("Temperatur", f"{c['T']:.1f}", "°C", wl=10, dl=8)
                    + vr("Modifikationen", f"{sum(1 for v in st.get('mods', dict()).values() if v)}", "aktiv")
                )}
            </div>
            <div class="pls-c"><h3>📋 Grenzwertüberwachung</h3>
                {vtbl(
                    vr("CSB < 75", f"{c['csb_ab']:.1f}", "mg/L", wh=60, dh=75)
                    + vr("BSB₅ < 15", f"{c['bsb_ab']:.1f}", "mg/L", wh=10, dh=15)
                    + vr("NH₄-N < 10", f"{c['nh4_ab']:.1f}", "mg/L", wh=7, dh=10)
                    + vr("P-ges < 1.0", f"{c['p_ab']:.2f}", "mg/L", wh=0.7, dh=1.0)
                    + vr("AFS < 15", f"{c['afs_ab']:.1f}", "mg/L", wh=10, dh=15)
                )}
            </div>
        </div>
        </div>''')

        # ====== ZULAUF ======
        zulauf = mo.Html(f'''<div class="pls"><div class="pls-g2">
            <div class="pls-c"><h3>🚰 Zulauf – Aktuelle Messwerte</h3>
                {vtbl(
                    vr("Volumenstrom Q", f"{c['Q_zu']:.0f}", "m³/d")
                    + vr("CSB", f"{c['csb_zu']:.0f}", "mg/L")
                    + vr("BSB₅", f"{c['bsb_zu']:.0f}", "mg/L")
                    + vr("NH₄-N", f"{c['nh4_zu']:.1f}", "mg/L")
                    + vr("NO₃-N", f"{c['no3_zu']:.1f}", "mg/L")
                    + vr("P-ges", f"{c['p_zu']:.1f}", "mg/L")
                    + vr("AFS", f"{c['afs_zu']:.0f}", "mg/L")
                    + vr("Temperatur", f"{c['T']:.1f}", "°C")
                )}
            </div>
            <div class="pls-c"><h3>📦 Frachten & Vorklärung</h3>
                {vtbl(
                    vr("CSB-Fracht", f"{st['fr_csb_zu']:.0f}", "kg/d")
                    + vr("N-Fracht", f"{st['fr_n_zu']:.0f}", "kg/d")
                    + vr("P-Fracht", f"{st['fr_p_zu']:.0f}", "kg/d")
                )}
                <div class="pls-sep"></div>
                <h3 style="color:#74b9ff;font-size:0.95em;margin:4px 0">Nach Vorklärung</h3>
                {vtbl(
                    vr("CSB", f"{c['csb_vk']:.0f}", "mg/L")
                    + vr("BSB₅", f"{c['bsb_vk']:.0f}", "mg/L")
                    + vr("AFS", f"{c['afs_vk']:.0f}", "mg/L")
                    + vr("NH₄-N", f"{c['nh4_vk']:.1f}", "mg/L")
                    + vr("P-ges", f"{c['p_vk']:.1f}", "mg/L")
                )}
            </div>
        </div></div>''')

        # ====== BIOLOGIE ======
        bc = "#00b894" if c["nitri"] > 0.8 else ("#fdcb6e" if c["nitri"] > 0.5 else "#e17055")
        biologie = mo.Html(f'''<div class="pls"><div class="pls-g2">
            <div class="pls-c"><h3>🔬 Belebung – Betriebsdaten</h3>
                {vtbl(
                    vr("TS-Gehalt", f"{c['ts']:.2f}", "g/L", wh=4.5, dh=5.5)
                    + vr("Schlammalter tTS", f"{c['t_ts']:.0f}", "d", wl=8, dl=5)
                    + vr("ISV", f"{c['isv']:.0f}", "mL/g", wh=120, dh=150)
                    + vr("O₂-Sollwert", f"{o2_soll.value:.1f}", "mg/L")
                    + vr("Temperatur", f"{c['T']:.1f}", "°C", wl=10, dl=8)
                )}
                <div class="pls-sep"></div>
                <p style="font-size:0.8em;color:#b2bec3">
                    TS Ziel: {tgt['ts']:.2f} g/L {delta_arrow(c['ts'], tgt['ts'])} |
                    ISV Ziel: {tgt['isv']:.0f} mL/g {delta_arrow(c['isv'], tgt['isv'])}
                </p>
            </div>
            <div class="pls-c"><h3>🧪 Biologische Leistung</h3>
                {vtbl(vr("Nitrifikationsrate", f"{c['nitri']*100:.0f}", "%"))}
                {bar(c['nitri']*100, bc)}
                {vtbl(vr("Denitrifikationsrate", f"{c['deni']*100:.0f}", "%"))}
                {bar(c['deni']*100, '#0984e3')}
                <div class="pls-sep"></div>
                {vtbl(
                    vr("CSB Ein → Aus", f"{c['csb_vk']:.0f} → {c['csb_bio']:.1f}", "mg/L")
                    + vr("NH₄-N Ein → Aus", f"{c['nh4_vk']:.1f} → {c['nh4_bio']:.1f}", "mg/L")
                    + vr("NO₃-N gebildet", f"{c['no3_bio']:.1f}", "mg/L")
                    + vr("P nach Bio+Fällung", f"{c['p_bio']:.2f}", "mg/L")
                )}
            </div>
        </div></div>''')

        # ====== NACHKLÄRUNG ======
        nc = "#00b894" if c["ss_nk"] < 100 else ("#fdcb6e" if c["ss_nk"] < 150 else "#e17055")
        nachklaerung = mo.Html(f'''<div class="pls"><div class="pls-g2">
            <div class="pls-c"><h3>⬇️ Nachklärung</h3>
                {vtbl(
                    vr("Schlammschicht", f"{c['ss_nk']:.0f}", "cm", wh=100, dh=150)
                )}
                {bar(min(100, c['ss_nk']/2), nc)}
                {vtbl(
                    vr("Feststoff-η", f"{c['nk_w']*100:.1f}", "%")
                    + vr("ISV", f"{c['isv']:.0f}", "mL/g", wh=120, dh=150)
                    + vr("AFS Ablauf", f"{c['afs_ab']:.1f}", "mg/L", wh=10, dh=15)
                )}
            </div>
            <div class="pls-c"><h3>🔄 Rücklauf- & Überschussschlamm</h3>
                {vtbl(
                    vr("Q Rücklaufschlamm", f"{c['Q_rs']:.0f}", "m³/d")
                    + vr("RS-Verhältnis", f"{rs_verhaeltnis.value:.2f}", "-")
                    + vr("TS Rücklaufschlamm", f"{c['ts_rs']:.1f}", "g/L")
                )}
                <div class="pls-sep"></div>
                {vtbl(
                    vr("ÜS-Menge", f"{ues_menge.value:.0f}", "m³/d")
                    + vr("Schlammalter", f"{c['t_ts']:.0f}", "d", wl=8, dl=5)
                )}
            </div>
        </div></div>''')

        # ====== ABLAUF + VERLAUFSDIAGRAMME ======
        import plotly.graph_objects as go
        from plotly.subplots import make_subplots

        if len(hist) >= 2:
            t_h = [h["t"] for h in hist]
            fig = make_subplots(rows=3, cols=2,
                subplot_titles=("CSB Ablauf [mg/L]", "NH₄-N Ablauf [mg/L]",
                                "P-ges Ablauf [mg/L]", "TS Belebung [g/L]",
                                "N-ges Ablauf [mg/L]", "ISV [mL/g]"),
                vertical_spacing=0.18, horizontal_spacing=0.08)

            def add_line(fig, hist, key, row, col, color, name):
                y = [h[key] for h in hist]
                fig.add_trace(go.Scatter(x=t_h, y=y, mode='lines', name=name,
                    line=dict(color=color, width=2)), row=row, col=col)

            add_line(fig, hist, "csb_ab", 1, 1, "#00b894", "CSB")
            fig.add_hline(y=75, line_dash="dash", line_color="#e17055", row=1, col=1)
            add_line(fig, hist, "nh4_ab", 1, 2, "#fdcb6e", "NH₄-N")
            fig.add_hline(y=10, line_dash="dash", line_color="#e17055", row=1, col=2)
            add_line(fig, hist, "p_ab", 2, 1, "#a29bfe", "P-ges")
            fig.add_hline(y=1.0, line_dash="dash", line_color="#e17055", row=2, col=1)
            add_line(fig, hist, "ts", 2, 2, "#74b9ff", "TS")
            add_line(fig, hist, "n_ab", 3, 1, "#fd79a8", "N-ges")
            fig.add_hline(y=18, line_dash="dash", line_color="#e17055", row=3, col=1)
            add_line(fig, hist, "isv", 3, 2, "#ffeaa7", "ISV")
            fig.add_hline(y=150, line_dash="dash", line_color="#e17055", row=3, col=2)

            fig.update_layout(height=750, template="plotly_dark",
                paper_bgcolor="#1a1a2e", plot_bgcolor="#16213e",
                showlegend=False,
                font=dict(family="Consolas,monospace", size=10, color="#dfe6e9"),
                margin=dict(t=40, b=40, l=50, r=20))
            fig.update_xaxes(gridcolor="#0f3460", title_text="")
            fig.update_xaxes(title_text="Stunden", row=3, col=1)
            fig.update_xaxes(title_text="Stunden", row=3, col=2)
            fig.update_yaxes(gridcolor="#0f3460")
            chart = fig
        else:
            chart = mo.md("*Drücke einen Zeitschritt-Button um den Verlauf zu starten...*")

        ablauf = mo.vstack([
            mo.Html(f'''<div class="pls"><div class="pls-g2">
                <div class="pls-c"><h3>🌊 Ablauf – Überwachungswerte</h3>
                    {vtbl(
                        vr("CSB", f"{c['csb_ab']:.1f}", "mg/L  (GW: 75)", wh=60, dh=75)
                        + vr("BSB₅", f"{c['bsb_ab']:.1f}", "mg/L  (GW: 15)", wh=10, dh=15)
                        + vr("NH₄-N", f"{c['nh4_ab']:.1f}", "mg/L  (GW: 10)", wh=7, dh=10)
                        + vr("NO₃-N", f"{c['no3_ab']:.1f}", "mg/L")
                        + vr("N-ges", f"{c['n_ab']:.1f}", "mg/L  (GW: 18)", wh=14, dh=18)
                        + vr("P-ges", f"{c['p_ab']:.2f}", "mg/L  (GW: 1.0)", wh=0.7, dh=1.0)
                        + vr("AFS", f"{c['afs_ab']:.1f}", "mg/L  (GW: 15)", wh=10, dh=15)
                        + vr("pH", f"{c['ph_ab']:.1f}", "", wl=6.5, dl=6.0)
                    )}
                </div>
                <div class="pls-c"><h3>📊 Frachten & Wirkungsgrade</h3>
                    <table style="width:100%;border-collapse:collapse;font-size:0.88em;color:#ffffff;background:#16213e;border-radius:4px">
                        <tr style="border-bottom:2px solid #0f3460;background:#0f1a30">
                            <th style="text-align:left;padding:8px 16px;color:#74b9ff">Parameter</th>
                            <th style="text-align:right;padding:8px 16px;color:#74b9ff">Zulauf</th>
                            <th style="text-align:right;padding:8px 16px;color:#74b9ff">Ablauf</th>
                            <th style="text-align:right;padding:8px 16px;color:#74b9ff">η [%]</th>
                        </tr>
                        <tr style="border-bottom:1px solid #0f3460"><td style="padding:6px 16px">CSB</td>
                            <td style="text-align:right;padding:6px 16px">{st['fr_csb_zu']:.0f}&ensp;kg/d</td>
                            <td style="text-align:right;padding:6px 16px">{st['fr_csb_ab']:.0f}&ensp;kg/d</td>
                            <td style="text-align:right;padding:6px 16px;color:{'#00b894' if st['eta_csb']>90 else '#fdcb6e'};font-weight:bold">{st['eta_csb']:.1f}</td></tr>
                        <tr style="border-bottom:1px solid #0f3460"><td style="padding:6px 16px">N-ges</td>
                            <td style="text-align:right;padding:6px 16px">{st['fr_n_zu']:.0f}&ensp;kg/d</td>
                            <td style="text-align:right;padding:6px 16px">{st['fr_n_ab']:.0f}&ensp;kg/d</td>
                            <td style="text-align:right;padding:6px 16px;color:{'#00b894' if st['eta_n']>70 else '#fdcb6e'};font-weight:bold">{st['eta_n']:.1f}</td></tr>
                        <tr style="border-bottom:1px solid #0f3460"><td style="padding:6px 16px">P-ges</td>
                            <td style="text-align:right;padding:6px 16px">{st['fr_p_zu']:.0f}&ensp;kg/d</td>
                            <td style="text-align:right;padding:6px 16px">{st['fr_p_ab']:.0f}&ensp;kg/d</td>
                            <td style="text-align:right;padding:6px 16px;color:{'#00b894' if st['eta_p']>80 else '#fdcb6e'};font-weight:bold">{st['eta_p']:.1f}</td></tr>
                    </table>
                </div>
            </div></div>'''),
            mo.Html('<div class="pls"><div class="pls-c"><h3>📈 Zeitlicher Verlauf (alle Ablaufwerte & Betriebsparameter)</h3></div></div>'),
            chart,
        ])

        # ====== STEUERUNG ======
        # Abschlag-Daten
        Q_roh_c = c.get("Q_roh", c["Q_zu"])
        Q_abschlag_c = c.get("Q_abschlag", 0)
        abschlag_aktiv = Q_abschlag_c > 10

        abschlag_html = ""
        if abschlag_aktiv:
            csb_abs = c.get("csb_abschlag", c["csb_zu"] * 0.7)
            nh4_abs = c.get("nh4_abschlag", c["nh4_zu"] * 0.95)
            p_abs = c.get("p_abschlag", c["p_zu"] * 0.9)
            afs_abs = c.get("afs_abschlag", c["afs_zu"] * 0.5)
            fracht_csb_abs = csb_abs * Q_abschlag_c / 1000
            fracht_p_abs = p_abs * Q_abschlag_c / 1000
            abschlag_html = f'''<div class="pls-c" style="border-color:#e17055;border-width:2px">
                <h3 style="color:#e17055">🚨 Mischwasserabschlag aktiv!</h3>
                <p style="font-size:0.85em;margin:4px 0 8px">
                    Der Gesamtzulauf ({Q_roh_c:.0f} m³/d) überschreitet die Abschlagschwelle
                    ({abschlag_schwelle.value:.0f} m³/d). {Q_abschlag_c:.0f} m³/d werden nach
                    mechanischer Reinigung (Rechen + Vorklärung) direkt in den Vorfluter abgeschlagen.
                </p>
                {vtbl(
                    vr("Gesamtzulauf Q_roh", f"{Q_roh_c:.0f}", "m³/d")
                    + vr("→ zur Biologie", f"{c['Q_zu']:.0f}", "m³/d")
                    + vr("→ Abschlag", f"{Q_abschlag_c:.0f}", "m³/d", wh=1, dh=1)
                )}
                <div class="pls-sep"></div>
                <p style="font-size:0.85em;color:#e17055;margin:4px 0">Abschlagqualität (nur mechanisch gereinigt):</p>
                {vtbl(
                    vr("CSB Abschlag", f"{csb_abs:.0f}", "mg/L", wh=200, dh=300)
                    + vr("NH₄-N Abschlag", f"{nh4_abs:.1f}", "mg/L")
                    + vr("P-ges Abschlag", f"{p_abs:.1f}", "mg/L")
                    + vr("AFS Abschlag", f"{afs_abs:.0f}", "mg/L")
                )}
                <div class="pls-sep"></div>
                <p style="font-size:0.85em;color:#e17055;margin:4px 0">Schadstofffracht in den Vorfluter:</p>
                {vtbl(
                    vr("CSB-Fracht Abschlag", f"{fracht_csb_abs:.0f}", "kg/d")
                    + vr("P-Fracht Abschlag", f"{fracht_p_abs:.1f}", "kg/d")
                )}
            </div>'''

        # Gebläse-Berechnung aus O2-Sollwert
        o2_val = o2_soll.value
        geblaese_drehzahl = 1200 + (o2_val - 0.5) * 800 / 3.5  # U/min, linear skaliert
        geblaese_luft = c["Q_zu"] * o2_val * 1.5 / 24  # Nm³/h, vereinfacht
        geblaese_p = geblaese_luft * 0.5 * 0.04  # kW, vereinfacht

        # RS-Pumpwerk aus Verhältnis (Stufenschaltung P3.1–P3.6)
        rs_q_soll = tgt["Q_zu"] / 24 * rs_verhaeltnis.value
        rs_n_ein = pm["rs_stufen"](tgt["Q_zu"], rs_verhaeltnis.value)
        rs_q = c["Q_rs"] / 24

        # ÜS aus Menge
        ues_q_h = ues_menge.value / 24
        ues_laufzeit = min(24, ues_menge.value / max(1, ues_q_h * 3) * 24) if ues_q_h > 0 else 0

        steuerung = mo.vstack([
            mo.Html('<div class="pls"><div class="pls-c" style="border-color:#e94560"><h3 style="color:#e94560">⏱ Zeitsimulation</h3><p style="font-size:0.85em;color:#b2bec3">Stelle zuerst die Steuerungsparameter ein, dann drücke einen Zeitschritt-Button. Änderungen wirken sich verzögert aus – genau wie in der Realität!</p></div></div>'),
            mo.hstack([btn_1h, btn_6h, btn_24h, btn_7d, btn_reset], justify="start", gap=0.5),
            mo.Html(f'<div class="pls"><p style="font-size:0.9em">Simulationszeit: <strong>{sim_zeit}</strong> ({th:.0f} Stunden gesamt)</p></div>'),

            # --- ZULAUFBEDINGUNGEN ---
            # Regler stehen sichtbar im Vordergrund, der technische Hintergrund
            # wird über ein Accordion auf Wunsch ausgeklappt.
            mo.Html('<div class="pls"><div class="pls-c"><h3>🌊 Zulaufbedingungen & Abschlag</h3></div></div>'),
            mo.vstack([zulauf_q, regen_faktor, temperatur, abschlag_schwelle]),
            mo.accordion({
                "💡 Technischer Hintergrund – Zulauf · Regen · Temperatur · Abschlag": mo.Html('''<div class="pls" style="font-size:0.85em">
                    <div class="pls-c">
                        <p><strong>Zulauf Q:</strong> Trockenwetterzulauf × Regenfaktor. Die Zulaufpumpe P1.1
                        (FU-geregelt) passt ihre Drehzahl automatisch an den Wasserstand im Pumpensumpf an.</p>
                        <p><strong>Regenfaktor:</strong> Faktor 1.0 = Trockenwetter, 2.0 = starker Regen,
                        3.0 = Starkregen. Im Mischsystem steigt Q, aber die Konzentrationen sinken (Verdünnung).</p>
                        <p><strong>Temperatur:</strong> Beeinflusst direkt die Nitrifikationsrate
                        (Temperaturkoeffizient θ = 1,072). Unter 10°C wird die Nitrifikation kritisch langsam.</p>
                        <p><strong>Abschlagschwelle:</strong> Maximaler Durchfluss zur biologischen Stufe.
                        Darüber wird Mischwasser nach mechanischer Reinigung (Rechen, Sandfang, Vorklärung)
                        direkt in den Vorfluter abgeschlagen – nur teilgereinigt!</p>
                    </div>
                </div>'''),
            }),
            mo.Html(f'<div class="pls">{abschlag_html}</div>') if abschlag_aktiv else mo.Html(""),

            # --- BIOLOGISCHE STUFE ---
            # Drei einzeln aufklappbare Abschnitte; multiple=True erlaubt das
            # parallele Öffnen z.B. von O₂ und RS zum Vergleich.
            mo.Html('<div class="pls"><div class="pls-c"><h3>🔬 Biologische Stufe</h3></div></div>'),
            mo.vstack([o2_soll, rs_verhaeltnis, ues_menge]),
            mo.accordion({
                "💡 O₂-Sollwert → Gebläse & Belüftung": mo.Html(f'''<div class="pls" style="font-size:0.85em">
                    <div class="pls-c">
                        <p>Der O₂-Sollwert wird über einen <strong>PID-Regler</strong> gehalten.
                        Stellglied ist das <strong>Drehkolbengebläse</strong> (FU-geregelt).</p>
                        {vtbl(
                            vr("Gebläse-Drehzahl", f"{geblaese_drehzahl:.0f}", "min⁻¹")
                            + vr("Luftvolumenstrom", f"{geblaese_luft:.0f}", "Nm³/h")
                            + vr("elektr. Leistung", f"{geblaese_p:.1f}", "kW")
                        )}
                        <p>Höherer O₂ → mehr Luft → bessere Nitrifikation, aber auch höherer Energieverbrauch
                        und bei O₂ > 3 mg/L verschlechterte Denitrifikation (ISV steigt).</p>
                    </div>
                </div>'''),
                "💡 RS-Verhältnis → Rücklaufschlammpumpen P3.1–P3.6": mo.Html(f'''<div class="pls" style="font-size:0.85em">
                    <div class="pls-c">
                        <p>Das RS-Verhältnis ist der Sollwert für das <strong>RS-Pumpwerk</strong>
                        (6 × KSB Sewabloc F 100-252, Festdrehzahl ohne FU). Die Steuerung schaltet
                        so viele Pumpen zu, dass der Sollwert möglichst genau erreicht wird (Stufenschaltung).</p>
                        {vtbl(
                            vr("RS-Sollwert", f"{rs_q_soll:.0f}", "m³/h")
                            + vr("Pumpen in Betrieb", f"{rs_n_ein} von {pm['rs_n_max']}", "")
                            + vr("RS-Förderstrom FI 402", f"{rs_q:.0f}", "m³/h")
                            + vr("RS-Verhältnis Ist", f"{c['Q_rs'] / max(1, c['Q_zu']):.2f}", "-")
                            + vr("TS Rücklaufschlamm", f"{c['ts_rs']:.1f}", "g/L")
                        )}
                        <p>Höheres RS-Verhältnis → bessere Denitrifikation (mehr NO₃-Rückführung),
                        aber dünnerer RS → niedrigerer TS im Belebungsbecken. Außerdem steigt
                        die hydraulische Belastung der Nachklärung.</p>
                    </div>
                </div>'''),
                "💡 Überschussschlamm → ESP P5.1 (Seepex BN 52-6L)": mo.Html(f'''<div class="pls" style="font-size:0.85em">
                    <div class="pls-c">
                        <p>Die ÜS-Abzugsmenge bestimmt TS und Schlammalter.
                        Gefördert durch die <strong>Exzenterschneckenpumpe P5.1</strong> (drehzahlgeregelt).</p>
                        {vtbl(
                            vr("ÜS-Förderstrom", f"{ues_q_h:.1f}", "m³/h")
                            + vr("Tägliche Laufzeit", f"{ues_laufzeit:.1f}", "h/d")
                            + vr("→ TS Belebung", f"{c['ts']:.2f}", "g/L")
                            + vr("→ Schlammalter", f"{c['t_ts']:.0f}", "d")
                        )}
                        <p>Mehr ÜS → niedrigerer TS, kürzeres Schlammalter. Zu kurz (&lt;8d bei &lt;12°C)
                        gefährdet die Nitrifikation! Zu wenig ÜS → hoher TS, ISV steigt → Blähschlammgefahr.</p>
                    </div>
                </div>'''),
            }, multiple=True),

            # --- CHEMISCHE STUFE ---
            mo.Html('<div class="pls"><div class="pls-c"><h3>🧪 Chemische Stufe</h3></div></div>'),
            mo.vstack([faellmittel]),
            mo.accordion({
                "💡 Fällmitteldosierung → Kolbenmembranpumpe P7.1": mo.Html(f'''<div class="pls" style="font-size:0.85em">
                    <div class="pls-c">
                        <p>Die Dosierung von <strong>FeCl₃ 40%</strong> (ρ = 1,42 kg/L) erfolgt über die
                        <strong>ProMinent Sigma S2Cb</strong> (Kolbenmembranpumpe). Die Hublänge wird
                        proportional zum Dosierstrom eingestellt.</p>
                        {vtbl(
                            vr("Dosierstrom", f"{faellmittel.value:.0f}", "L/h")
                            + vr("Hublänge", f"{min(100, max(10, faellmittel.value / 50 * 100)):.0f}", "%")
                            + vr("β(Fe) Dosierung", f"{faellmittel.value * 1.42 * 0.34:.1f}", "kg Fe/d")
                            + vr("→ P-ges Ablauf", f"{c['p_ab']:.2f}", "mg/L", wh=0.7, dh=1.0)
                        )}
                        <p>Regelung: PI-Regler mit Totzeit (~30 min Fließstrecke). Messstelle P-ges
                        im Ablauf NK. Höhere Dosierung senkt P, aber auch den pH-Wert
                        (pH aktuell: {c['ph_ab']:.2f}). Bei pH &lt; 6,8 springt die Kalkmilchpumpe P9.1 an.</p>
                    </div>
                </div>'''),
            }),

            # --- IST/ZIEL-TABELLE ---
            mo.callout(mo.md(f"""
**Aktuelle Ist-Werte → Zielwerte:**

| Parameter | Ist | Ziel | Trend |
|---|---|---|---|
| TS Belebung | {c['ts']:.2f} g/L | {tgt['ts']:.2f} g/L | {delta_arrow(c['ts'], tgt['ts'])} τ ≈ 5 Tage |
| Schlammalter | {c['t_ts']:.0f} d | {tgt['t_ts']:.0f} d | {delta_arrow(c['t_ts'], tgt['t_ts'])} τ ≈ 7 Tage |
| ISV | {c['isv']:.0f} mL/g | {tgt['isv']:.0f} mL/g | {delta_arrow(c['isv'], tgt['isv'])} τ ≈ 10 Tage |
| NH₄-N Ablauf | {c['nh4_ab']:.1f} mg/L | {tgt['nh4_ab']:.1f} mg/L | {delta_arrow(c['nh4_ab'], tgt['nh4_ab'])} τ ≈ 18 h |
| CSB Ablauf | {c['csb_ab']:.1f} mg/L | {tgt['csb_ab']:.1f} mg/L | {delta_arrow(c['csb_ab'], tgt['csb_ab'])} τ ≈ 6 h |
| P Ablauf | {c['p_ab']:.2f} mg/L | {tgt['p_ab']:.2f} mg/L | {delta_arrow(c['p_ab'], tgt['p_ab'])} τ ≈ 8 h |
            """), kind="info"),
        ])

        # ====== PUMPENTECHNIK ======
        # Betriebsdaten aus Simulation ableiten
        Q_h = c["Q_zu"] / 24  # m³/h Zulauf
        Q_rs_h = c["Q_rs"] / 24  # m³/h Rücklaufschlamm
        Q_ues_h = ues_menge.value / 24  # m³/h Überschussschlamm
        Q_fm_lh = faellmittel.value  # L/h Fällmittel

        # --- KREISELPUMPEN ---
        # Zulaufpumpwerk: 2 Pumpen (1 Betrieb, 1 Reserve), Typ: Abwasser-Tauchmotorpumpe
        zp_n = 2  # Anzahl
        zp_Q_nenn = Q_h * 1.3  # Nennförderstrom etwas über Bedarf
        zp_Q_ist = Q_h  # aktueller Förderstrom
        zp_H_geo = 6.5  # m geodätische Höhe
        zp_H_verl = 0.8 + (zp_Q_ist / 600) ** 2 * 2.5  # Rohrleitungsverluste
        zp_H_ist = zp_H_geo + zp_H_verl  # Förderhöhe
        zp_H_nenn = 10.0
        zp_eta = max(0.45, 0.72 - abs(zp_Q_ist - zp_Q_nenn * 0.85) / zp_Q_nenn * 0.3)
        zp_P = zp_Q_ist / 3600 * 9810 * zp_H_ist / zp_eta / 1000 if zp_eta > 0 else 0  # kW
        zp_f = min(50, max(25, 50 * zp_Q_ist / (zp_Q_nenn * 0.85)))  # Hz (FU-geregelt)
        zp_bh = 14280 + th  # Betriebsstunden
        zp_U = 400.0 * zp_f / 50.0  # FU-Ausgangsspannung (U/f-Kennlinie)
        zp_cos = 0.84
        zp_I = zp_P / 0.93 * 1000 / (3 ** 0.5 * zp_U * zp_cos)  # Motorstrom [A], η_Motor 93 %


        # Interne Rezirkulation (Denizone → Nitrifikation)
        irez_Q_ist = Q_h * 2.0  # ca. 2× Qzu
        irez_Q_nenn = Q_h * 2.5
        irez_H_ist = 0.4
        irez_eta = 0.65
        irez_P = irez_Q_ist / 3600 * 9810 * irez_H_ist / irez_eta / 1000 if irez_eta > 0 else 0
        irez_f = min(50, max(30, 50 * irez_Q_ist / max(1, irez_Q_nenn * 0.85)))
        irez_bh = 11800 + th
        irez_U = 400.0 * irez_f / 50.0
        irez_cos = 0.78
        irez_I = irez_P / 0.90 * 1000 / (3 ** 0.5 * irez_U * irez_cos)  # η_Motor 90 %

        # SVG-Pumpenkennlinie Generator (Kreiselpumpe)
        def pump_curve_svg(Q_nenn, H_nenn, Q_ist, H_ist, eta_ist, title, width=380, height=220):
            """Erzeugt SVG mit Q-H-Kennlinie, Anlagenkennlinie und Betriebspunkt."""
            # Normierte Stützpunkte für Pumpenkennlinie (typisch KP)
            qs = [0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.15]
            hs = [1.20, 1.18, 1.12, 1.02, 0.88, 0.70, 0.50]
            # Skalierung
            Q_max = Q_nenn * 1.3
            H_max = H_nenn * 1.4
            mx, my, pw, ph = 50, 15, width - 70, height - 50  # margins

            def px(q): return mx + q / Q_max * pw
            def py(h): return my + ph - h / H_max * ph

            # Pumpenkennlinie Punkte
            pts_pump = " ".join([f"{px(q * Q_nenn):.0f},{py(h * H_nenn):.0f}" for q, h in zip(qs, hs)])
            # Anlagenkennlinie (parabolisch: H = H_geo + k*Q²)
            H_geo = H_ist - (H_ist - H_nenn * 0.5) * (Q_ist / Q_nenn) ** 2 if Q_ist > 0 else H_ist * 0.65
            H_geo = max(0.3, min(H_geo, H_ist * 0.95))
            k_anl = (H_ist - H_geo) / max(0.01, Q_ist ** 2) if Q_ist > 0 else 0.001
            anl_pts = []
            for i in range(20):
                q = Q_max * i / 19
                h = H_geo + k_anl * q ** 2
                if h <= H_max:
                    anl_pts.append(f"{px(q):.0f},{py(h):.0f}")
            pts_anl = " ".join(anl_pts)

            # Gitterlinien
            grid = ""
            for i in range(5):
                gy = my + ph * i / 4
                gq = Q_max * (i + 1) / 5
                grid += f'<line x1="{mx}" y1="{gy:.0f}" x2="{mx + pw}" y2="{gy:.0f}" stroke="#0f3460" stroke-width="0.5"/>'
                gx = px(gq)
                grid += f'<line x1="{gx:.0f}" y1="{my}" x2="{gx:.0f}" y2="{my + ph}" stroke="#0f3460" stroke-width="0.5"/>'
                # Beschriftung Y
                hv = H_max * (4 - i) / 4
                grid += f'<text x="{mx - 5}" y="{gy + 4:.0f}" fill="#b2bec3" text-anchor="end" font-size="9" font-family="monospace">{hv:.1f}</text>'
            # Beschriftung X
            for i in range(6):
                qv = Q_max * i / 5
                grid += f'<text x="{px(qv):.0f}" y="{my + ph + 14}" fill="#b2bec3" text-anchor="middle" font-size="9" font-family="monospace">{qv:.0f}</text>'

            bp_x = px(Q_ist)
            bp_y = py(H_ist)
            eta_pct = eta_ist * 100

            return f'''<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:{width}px;height:auto">
                <rect width="{width}" height="{height}" fill="#1a1a2e" rx="4"/>
                <text x="{width // 2}" y="12" fill="#74b9ff" text-anchor="middle" font-size="10" font-family="monospace">{title}</text>
                {grid}
                <rect x="{mx}" y="{my}" width="{pw}" height="{ph}" fill="none" stroke="#0f3460" stroke-width="1"/>
                <polyline points="{pts_pump}" fill="none" stroke="#0984e3" stroke-width="2.5"/>
                <polyline points="{pts_anl}" fill="none" stroke="#e17055" stroke-width="1.5" stroke-dasharray="6,3"/>
                <circle cx="{bp_x:.0f}" cy="{bp_y:.0f}" r="5" fill="#00b894" stroke="#fff" stroke-width="1.5"/>
                <text x="{bp_x + 8:.0f}" y="{bp_y - 6:.0f}" fill="#00b894" font-size="9" font-family="monospace">BP: {Q_ist:.0f} m³/h / {H_ist:.1f} m</text>
                <text x="{bp_x + 8:.0f}" y="{bp_y + 6:.0f}" fill="#fdcb6e" font-size="8" font-family="monospace">η = {eta_pct:.0f}%</text>
                <text x="{mx + pw}" y="{my + ph + 14}" fill="#b2bec3" text-anchor="end" font-size="8" font-family="monospace">Q [m³/h]</text>
                <text x="{mx - 5}" y="{my - 2}" fill="#b2bec3" text-anchor="end" font-size="8" font-family="monospace">H [m]</text>
                <line x1="{mx + pw - 55}" y1="{my + 6}" x2="{mx + pw - 35}" y2="{my + 6}" stroke="#0984e3" stroke-width="2"/>
                <text x="{mx + pw - 32}" y="{my + 9}" fill="#0984e3" font-size="7" font-family="monospace">Pumpe</text>
                <line x1="{mx + pw - 55}" y1="{my + 16}" x2="{mx + pw - 35}" y2="{my + 16}" stroke="#e17055" stroke-width="1.5" stroke-dasharray="4,2"/>
                <text x="{mx + pw - 32}" y="{my + 19}" fill="#e17055" font-size="7" font-family="monospace">Anlage</text>
            </svg>'''

        # --- EXZENTERSCHNECKENPUMPEN ---
        # Primärschlammpumpe (aus Vorklärung)
        ps_Q = c["Q_zu"] * 0.005  # ca. 0.5% des Zulaufs als Primärschlamm, m³/d
        ps_Q_h = ps_Q / 24
        ps_ts = 35  # g/L TS Primärschlamm
        ps_p = 2.5  # bar Förderdruck
        ps_n = 180  # U/min
        ps_P = 2.2  # kW
        ps_bh = 8900 + th * 0.3

        # Überschussschlammpumpe
        ues_Q_h = Q_ues_h
        ues_ts = c["ts"] * 1.2  # TS etwas höher als BB
        ues_p = 3.0
        ues_n = 220
        ues_P = 3.0
        ues_bh = 9200 + th * 0.4

        # Dickschlammpumpe (zur Entwässerung)
        ds_Q_h = (ps_Q_h + ues_Q_h) * 0.8
        ds_ts = 50  # g/L eingedickter Schlamm
        ds_p = 4.5
        ds_n = 150
        ds_P = 4.0
        ds_bh = 6500 + th * 0.2

        # --- KOLBENMEMBRANPUMPEN ---
        # Fällmitteldosierung Fe³⁺ (FeCl₃, ρ ≈ 1.42 kg/L)
        fm_Q = Q_fm_lh
        fm_hub = 65  # mm
        fm_hub_pct = min(100, max(10, fm_Q / 50 * 100))  # Hublänge in %
        fm_freq = 120  # Hübe/min
        fm_p = 6.0  # bar Gegendruck
        fm_P = 0.37  # kW Antrieb
        fm_bh = 10200 + th * 0.5

        # Polymerdosierung (Flockungshilfsmittel für Schlammentwässerung)
        poly_Q = ds_Q_h * 1000 * 0.004  # ca. 4 mL/L Schlamm → L/h
        poly_hub_pct = min(100, max(10, poly_Q / 20 * 100))
        poly_freq = 60
        poly_p = 3.0
        poly_P = 0.25
        poly_bh = 5800 + th * 0.15

        # Kalkmilchdosierung (pH-Korrektur, nur bei Bedarf)
        kalk_aktiv = c["ph_ab"] < 6.8
        kalk_Q = 8.0 if kalk_aktiv else 0
        kalk_hub_pct = 50 if kalk_aktiv else 0
        kalk_freq = 90
        kalk_p = 4.0
        kalk_P = 0.25 if kalk_aktiv else 0
        kalk_bh = 2100 + (th * 0.1 if kalk_aktiv else 0)

        def pump_status(on=True):
            if on:
                return '<span style="color:#00b894;font-weight:bold">● EIN</span>'
            return '<span style="color:#636e72">○ AUS</span>'

        def pump_status_reserve():
            return '<span style="color:#fdcb6e">◐ RESERVE</span>'

        # ESP-Schnittbild SVG (vereinfacht)
        def esp_svg(title, Q, ts_val, p, n, P_val):
            return f'''<svg viewBox="0 0 380 140" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:380px;height:auto">
                <rect width="380" height="140" fill="#1a1a2e" rx="4"/>
                <text x="190" y="14" fill="#74b9ff" text-anchor="middle" font-size="10" font-family="monospace">{title}</text>
                <!-- Gehäuse -->
                <rect x="80" y="35" width="200" height="60" rx="8" fill="#2d3436" stroke="#6c5ce7" stroke-width="2"/>
                <!-- Rotor (Exzenter) -->
                <ellipse cx="180" cy="65" rx="60" ry="18" fill="none" stroke="#a29bfe" stroke-width="2" stroke-dasharray="4,2"/>
                <circle cx="160" cy="60" r="6" fill="#a29bfe" opacity="0.6"/>
                <circle cx="200" cy="70" r="6" fill="#a29bfe" opacity="0.6"/>
                <!-- Welle -->
                <line x1="30" y1="65" x2="80" y2="65" stroke="#b2bec3" stroke-width="3"/>
                <!-- Motor -->
                <rect x="10" y="48" width="25" height="34" rx="3" fill="#2d3436" stroke="#fdcb6e" stroke-width="1.5"/>
                <text x="22" y="69" fill="#fdcb6e" text-anchor="middle" font-size="7" font-family="monospace">M</text>
                <!-- Einlass/Auslass -->
                <line x1="80" y1="50" x2="55" y2="35" stroke="#0984e3" stroke-width="3"/>
                <text x="45" y="32" fill="#0984e3" font-size="8" font-family="monospace">↓ Einlass</text>
                <line x1="280" y1="65" x2="320" y2="65" stroke="#0984e3" stroke-width="3"/>
                <polygon points="320,60 330,65 320,70" fill="#0984e3"/>
                <text x="335" y="68" fill="#0984e3" font-size="8" font-family="monospace">Auslass</text>
                <!-- Daten -->
                <text x="100" y="118" fill="#dfe6e9" font-size="8" font-family="monospace">Q={Q:.1f} m³/h | TS={ts_val:.0f} g/L | p={p:.1f} bar | n={n} min⁻¹ | P={P_val:.1f} kW</text>
            </svg>'''

        # KMP-Schema SVG
        def kmp_svg(title, Q_lh, hub_pct, freq, p, P_val, medium):
            return f'''<svg viewBox="0 0 380 140" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:380px;height:auto">
                <rect width="380" height="140" fill="#1a1a2e" rx="4"/>
                <text x="190" y="14" fill="#74b9ff" text-anchor="middle" font-size="10" font-family="monospace">{title}</text>
                <!-- Pumpenkopf -->
                <rect x="120" y="30" width="80" height="55" rx="6" fill="#2d3436" stroke="#e94560" stroke-width="2"/>
                <!-- Membran -->
                <path d="M 135 57 Q 160 {"42" if hub_pct > 50 else "67"} 185 57" fill="none" stroke="#fdcb6e" stroke-width="2"/>
                <text x="160" y="50" fill="#fdcb6e" text-anchor="middle" font-size="7" font-family="monospace">Membran</text>
                <!-- Kolben -->
                <rect x="75" y="50" width="45" height="14" rx="2" fill="#636e72" stroke="#b2bec3" stroke-width="1"/>
                <text x="97" y="60" fill="#b2bec3" text-anchor="middle" font-size="6" font-family="monospace">Kolben</text>
                <!-- Hydraulikraum -->
                <rect x="60" y="44" width="15" height="26" rx="2" fill="#2d3436" stroke="#0984e3" stroke-width="1"/>
                <!-- Ventile -->
                <polygon points="145,30 155,20 165,30" fill="#00b894" stroke="#00b894" stroke-width="1"/>
                <text x="155" y="17" fill="#00b894" text-anchor="middle" font-size="7" font-family="monospace">Druckventil</text>
                <polygon points="165,85 175,95 185,85" fill="#0984e3" stroke="#0984e3" stroke-width="1"/>
                <text x="175" y="107" fill="#0984e3" text-anchor="middle" font-size="7" font-family="monospace">Saugventil</text>
                <!-- Ein/Auslass -->
                <line x1="175" y1="95" x2="175" y2="112" stroke="#0984e3" stroke-width="2"/>
                <line x1="155" y1="20" x2="155" y2="3" stroke="#00b894" stroke-width="2"/>
                <!-- Motor -->
                <rect x="20" y="44" width="30" height="26" rx="3" fill="#2d3436" stroke="#fdcb6e" stroke-width="1.5"/>
                <text x="35" y="60" fill="#fdcb6e" text-anchor="middle" font-size="7" font-family="monospace">M</text>
                <!-- Exzenter -->
                <circle cx="55" cy="57" r="5" fill="#b2bec3" opacity="0.6"/>
                <!-- Daten rechts -->
                <text x="220" y="42" fill="#dfe6e9" font-size="9" font-family="monospace">Medium: {medium}</text>
                <text x="220" y="55" fill="#dfe6e9" font-size="9" font-family="monospace">Q = {Q_lh:.1f} L/h</text>
                <text x="220" y="68" fill="#dfe6e9" font-size="9" font-family="monospace">Hub = {hub_pct:.0f}%</text>
                <text x="220" y="81" fill="#dfe6e9" font-size="9" font-family="monospace">f = {freq} min⁻¹ | p = {p:.0f} bar</text>
                <text x="220" y="94" fill="#dfe6e9" font-size="9" font-family="monospace">P = {P_val:.2f} kW</text>
            </svg>'''

        # --- Pumpen mit KSB-Kennlinien (Betriebspunkt über Anlagenkennlinie, Pumpenmodell-Zelle) ---
        lp_agg = pm["aggregate"]
        lp_rng = np.random.default_rng(int(th * 13) + 7)

        def lp_mess(kks, laeuft, h_zulauf, n_par=1, h_geo=None):
            """Messwerte FI/PI einer Pumpe: Drücke auf Höhe Pumpenachse, h_zulauf in m."""
            a = lp_agg[kks]
            rho = a["rho"]
            p_s = rho * 9.81 * h_zulauf / 1e5
            if laeuft:
                b = pm["betriebspunkt"](a["kl"], a["ort"], n_par, h_geo)
                q = b["Q"] * (1 + lp_rng.normal(0, 0.004))
                p_d = p_s + rho * 9.81 * b["H"] / 1e5
            else:
                q, p_d = 0.0, p_s
            warn = ""
            if laeuft:
                _qmin, _qmax = pm["grenzen"](a["kl"])
                if not b["gefoerdert"]:
                    warn = "Pumpe läuft, kein Durchfluss – Förderhöhe reicht nicht aus"
                elif _qmin and q < _qmin:
                    warn = "Förderstrom unter Mindestförderstrom lt. Hersteller"
                elif _qmax and q > _qmax:
                    warn = "Förderstrom über Maximalförderstrom lt. Hersteller"
            return dict(q=q, p_s=p_s + lp_rng.normal(0, 0.003), p_d=p_d + lp_rng.normal(0, 0.003), warn=warn)

        def lp_status(on, bereit=True):
            if on:
                return '<span style="color:#00b894;font-weight:bold">● EIN</span>'
            if bereit:
                return '<span style="color:#fdcb6e">◐ BEREIT</span>'
            return '<span style="color:#636e72">○ AUS</span>'

        def lp_datenblatt(a, messort):
            mt = a["motor"]
            zeilen = [
                ("Baureihe / Größe", "KSB " + a["kl"][0]),
                ("Laufrad-Ø / Nenndrehzahl", f"{a['kl'][1]} mm / {a['n_nenn']} 1/min"),
                ("Fördermedium", a["medium"]),
                ("Dichte Fördermedium", f"{a['rho']:.0f} kg/m³"),
                ("Temperatur Fördermedium", a["t_med"] + " °C"),
                ("Auslegungspunkt Q / H", f"{a['ausl_q']:.0f} m³/h / {a['ausl_h']:.1f} m"),
                ("Aufstellung", "trocken, horizontal, Blockbauweise"),
                ("Antrieb", f"{mt['hersteller']} {mt['typ']}, {mt['pn']:.1f} kW, {mt['ie']}, Anlauf {a['anlauf']}"
                            + (" (Frequenzumrichter)" if a["fu"] else "")),
                ("Druckmessstellen (anlagenseitig)", messort),
            ]
            trs = ""
            for _j, (_kk, _vv) in enumerate(zeilen):
                _bg = "#f5f0d8" if _j % 2 else "transparent"
                trs += (f'<tr style="background:{_bg}"><td style="padding:4px 12px;color:#5a4820;width:42%">{_kk}</td>'
                        f'<td style="padding:4px 12px;font-weight:bold;color:#1a1a2e">{_vv}</td></tr>')
            return (f'<div style="background:#fffef5;color:#1a1a2e;border:2px solid #5a4820;border-radius:6px;padding:10px;margin-top:6px">'
                    f'<div style="font-size:0.75em;color:#5a4820;letter-spacing:2px">KSB · DATENBLATT (AUSZUG) · Kom.-Nr. {a["serien"][:7]}</div>'
                    f'<table style="border-collapse:collapse;font-size:0.85em;margin-top:6px">{trs}</table></div>')

        def lp_details(a, messort):
            return (f'<details style="margin-top:8px"><summary style="cursor:pointer;color:#74b9ff;font-size:0.85em">'
                    f'Typenschilder Pumpe / Motor ({a["kks"]})</summary>'
                    f'<div class="pls-g2" style="margin-top:6px"><div>{pm["typenschild_pumpe_svg"](a)}</div>'
                    f'<div>{pm["typenschild_motor_svg"](a)}</div></div></details>'
                    f'<details style="margin-top:4px"><summary style="cursor:pointer;color:#74b9ff;font-size:0.85em">'
                    f'Datenblatt (Auszug Herstellerunterlagen)</summary>{lp_datenblatt(a, messort)}</details>')

        def lp_faceplate(kks, mess, on, bh, lz, sp, messort, bereit=True, q_fi=None):
            a = lp_agg[kks]
            _q_anz = mess["q"] if q_fi is None else q_fi
            _fu_row = vr("Drehzahl (FU)", f"{a['kl'][2]} 1/min / {a['kl'][2] / a['n_nenn'] * 50:.1f}", "Hz") if a["fu"] else ""
            tab = vtbl(
                vr(f"{a['fi_bez']} {a['fi']}", f"{_q_anz:.1f}", "m³/h")
                + _fu_row
                + vr(f"Druck saugseitig {a['pi_s']}", f"{mess['p_s']:.2f}", "bar")
                + vr(f"Druck druckseitig {a['pi_d']}", f"{mess['p_d']:.2f}", "bar")
                + vr("Betriebsstunden", f"{bh:.0f}", "h")
                + vr("Laufzeit Vortag", f"{lz:.1f}", "h")
                + vr("Schaltspiele Vortag", f"{sp}", "")
            )
            return (f'<div class="pls-c"><h3>{kks} {a["bez"]} {lp_status(on, bereit)}</h3>'
                    f'<p style="font-size:0.8em;color:#b2bec3;margin:0 0 6px">KSB {a["kl"][0]} · Laufrad ø{a["kl"][1]} mm · '
                    f'Motor {a["motor"]["pn"]:.1f} kW · '
                    + ("drehzahlgeregelt über Frequenzumrichter" if a["fu"] else f'Anlauf {a["anlauf"]} · Festdrehzahl, ohne Frequenzumrichter')
                    + (f' · {a["umbau"]}' if a["umbau"] else "") + '</p>'
                    + (f'<div class="pls-alarm">⚠️ Meldung: {mess["warn"]}</div>' if mess.get("warn") else "")
                    + f'{tab}{lp_details(a, messort)}</div>')

        # --- Rücklaufschlamm-Pumpwerk P3.1–P3.6 ---
        rs_n_ein = pm["rs_stufen"](tgt["Q_zu"], rs_verhaeltnis.value)
        rs_rows = ""
        rs_q_sum = 0.0
        for _i in range(pm["rs_n_max"]):
            _k = f"P3.{_i + 1}"
            _a = lp_agg[_k]
            _on = _i < rs_n_ein
            _m = lp_mess(_k, _on, 2.20)
            rs_q_sum += _m["q"]
            _bh = _a["bh0"] + (th if _on else 0.0)
            _td = 'style="padding:5px 14px;text-align:right;white-space:nowrap"'
            rs_rows += (f'<tr style="border-bottom:1px solid #0f3460">'
                        f'<td style="padding:5px 14px;white-space:nowrap">{_k}</td>'
                        f'<td style="padding:5px 14px;text-align:center;white-space:nowrap">{lp_status(_on)}'
                        f'{(" · FU " + str(_a["kl"][2])) if _a["fu"] else ""}{" ⚠️" if _m.get("warn") else ""}</td>'
                        f'<td {_td}><span style="color:#b2bec3">{_a["fi"]}</span>&ensp;<b style="color:#74b9ff">{_m["q"]:.1f}</b>&ensp;m³/h</td>'
                        f'<td {_td}><span style="color:#b2bec3">{_a["pi_s"]}</span>&ensp;<b style="color:#74b9ff">{_m["p_s"]:.2f}</b>&ensp;bar</td>'
                        f'<td {_td}><span style="color:#b2bec3">{_a["pi_d"]}</span>&ensp;<b style="color:#74b9ff">{_m["p_d"]:.2f}</b>&ensp;bar</td>'
                        f'<td {_td}>{_bh:.0f}&ensp;h</td>'
                        f'<td {_td}>{(24.0 if _on else 0.0):.1f}&ensp;h</td></tr>')
        rs_th_style = 'style="padding:8px 14px;color:#74b9ff;text-align:right;white-space:nowrap"'
        if lp_agg["P3.1"]["kl"][:2] == lp_agg["P3.2"]["kl"][:2] and not lp_agg["P3.1"]["fu"]:
            rs_titel = f"6 × KSB {lp_agg['P3.2']['kl'][0]}"
        else:
            rs_titel = f"P3.1: KSB {lp_agg['P3.1']['kl'][0]} · P3.2–P3.6: KSB {lp_agg['P3.2']['kl'][0]}"
        rs_block_html = f'''<div class="pls-c" style="margin-top:10px">
            <h3>Rücklaufschlamm-Pumpwerk P3.1 – P3.6 ({rs_titel})</h3>
            <p style="font-size:0.8em;color:#b2bec3;margin:0 0 8px">Trocken aufgestellt neben NK1/NK2 · Pumpen ohne FU mit Festdrehzahl (Stern-Dreieck-Anlauf) ·
               jede Pumpe fördert über eine eigene Druckleitung DN 125 mit freiem Auslauf in das Verteilerbauwerk vor dem Belebungsbecken ·
               Stufenschaltung nach RS-Sollwert</p>
            <table style="border-collapse:collapse;font-size:0.86em;color:#ffffff;background:#16213e">
                <tr style="border-bottom:2px solid #0f3460;background:#0f1a30">
                    <th style="padding:8px 14px;color:#74b9ff;text-align:left">Pumpe</th>
                    <th style="padding:8px 14px;color:#74b9ff;text-align:center">Status</th>
                    <th {rs_th_style}>Förderstrom</th><th {rs_th_style}>Druck saugseitig</th><th {rs_th_style}>Druck druckseitig</th>
                    <th {rs_th_style}>Betriebsstunden</th><th {rs_th_style}>Laufzeit Vortag</th>
                </tr>
                {rs_rows}
            </table>
            {vtbl(
                vr("Summe Rücklaufschlamm FI 402", f"{c['Q_rs'] / 24:.0f}", "m³/h")
                + vr("RS-Sollwert (RS-Verhältnis × Q_zu)", f"{tgt['Q_zu'] / 24 * rs_verhaeltnis.value:.0f}", "m³/h")
                + vr("Pumpen in Betrieb", f"{rs_n_ein} von {pm['rs_n_max']}", "")
                + vr("TS Rücklaufschlamm", f"{c['ts_rs']:.1f}", "g/L")
            )}
            {lp_details(lp_agg["P3.1"], "PI 421–426 saugseitig, PI 431–436 druckseitig; Saug- und Druckleitung je DN 125, Messstellen auf Höhe Pumpenachse")}
            {lp_details(lp_agg["P3.2"], "PI 421–426 saugseitig, PI 431–436 druckseitig; Saug- und Druckleitung je DN 125, Messstellen auf Höhe Pumpenachse") if lp_agg["P3.1"]["kl"][:2] != lp_agg["P3.2"]["kl"][:2] else ""}
        </div>'''

        # --- Faulturm FT-1: Umwälzpumpen P10.1 / P10.2 ---
        ft_m1 = lp_mess("P10.1", True, 18.0)
        ft_m2 = lp_mess("P10.2", False, 18.0)
        ft_messort = "Saug- und Druckleitung je DN 125, Messstellen auf Höhe Pumpenachse"
        ft_temp = 37.0 + 0.3 * np.sin(th / 7.0)
        ft_gas = st.get("gas_nm3", 1000.0) / 24
        ft_block_html = f'''<div class="pls-c" style="margin-top:10px">
            <h3>Faulturm FT-1 – Umwälzung / Beheizung (Umwälzkreis über Wärmetauscher W10.1)</h3>
            <p style="font-size:0.8em;color:#b2bec3;margin:0 0 8px">Mesophiler Faulturm, Nutzvolumen 2.200 m³ ·
               Umwälzpumpen im Dauerbetrieb, Wechsel nur bei Störung · geschlossener Kreislauf Faulturm → W10.1 → Faulturm</p>
            {vtbl(
                vr("Temperatur Faulturm TI 606", f"{ft_temp:.1f}", "°C")
                + vr("Füllstand Faulturm LI 607", "96", "%")
                + vr("Faulgas FI 608", f"{ft_gas:.0f}", "Nm³/h")
            )}
        </div>
        <div class="pls-g2">
            {lp_faceplate("P10.1", ft_m1, True, lp_agg["P10.1"]["bh0"] + th, 24.0, 0, "PI 602 saugseitig, PI 603 druckseitig; " + ft_messort)}
            {lp_faceplate("P10.2", ft_m2, False, lp_agg["P10.2"]["bh0"], 0.0, 0, "PI 604 saugseitig, PI 605 druckseitig; " + ft_messort, q_fi=ft_m1["q"])}
        </div>'''

        pumpen_html = mo.Html(f'''<div class="pls">

        <!-- KREISELPUMPEN -->
        <div class="pls-c"><h3>🔵 Kreiselpumpen</h3></div>

        <div class="pls-g3">
            <div class="pls-c">
                <h3>Zulaufpumpe P1.1 (Betrieb) {pump_status(True)}</h3>
                <p style="font-size:0.8em;color:#b2bec3;margin:0 0 6px">Flygt NP 3153 – Tauchmotorpumpe, FU-geregelt</p>
                {vtbl(
                    vr("Förderstrom Q", f"{zp_Q_ist:.0f}", "m³/h")
                    + vr("Förderhöhe H", f"{zp_H_ist:.1f}", "m")
                    + vr("Drehzahl (FU)", f"{zp_f:.0f}", "Hz")
                    + vr("Motorstrom I (FU)", f"{zp_I:.1f}", "A")
                    + vr("Motorspannung U (FU)", f"{zp_U:.0f}", "V")
                    + vr("Leistungsfaktor cos φ (FU)", f"{zp_cos:.2f}", "")
                    + vr("Motorwirkungsgrad (Datenblatt)", "93", "%")
                    + vr("Wirkungsgrad η", f"{zp_eta*100:.0f}", "%", wl=60, dl=50)
                    + vr("Betriebsstunden", f"{zp_bh:.0f}", "h")
                    + vr("Nenn-Q / Nenn-H", f"{zp_Q_nenn:.0f} / {zp_H_nenn:.0f}", "m³/h / m")
                )}
                {pump_curve_svg(zp_Q_nenn, zp_H_nenn, zp_Q_ist, zp_H_ist, zp_eta, "Zulaufpumpe P1.1")}
            </div>
            <div class="pls-c">
                <h3>Zulaufpumpe P1.2 (Reserve) {pump_status_reserve()}</h3>
                <p style="font-size:0.8em;color:#b2bec3;margin:0 0 6px">Flygt NP 3153 – Tauchmotorpumpe, FU-geregelt</p>
                {vtbl(
                    vr("Status", "Standby", "")
                    + vr("Nenn-Q / Nenn-H", f"{zp_Q_nenn:.0f} / {zp_H_nenn:.0f}", "m³/h / m")
                    + vr("Betriebsstunden", f"{zp_bh - 2400:.0f}", "h")
                    + vr("Letzter Wechsel", "vor 14 d", "")
                )}
                <p style="font-size:0.8em;color:#b2bec3;margin-top:8px">
                    Automatische Umschaltung bei:<br>
                    • Motorschutzauslösung P1.1<br>
                    • Überflutungsalarm Pumpensumpf<br>
                    • Wochenweise Wechselbetrieb
                </p>
            </div>
            <div class="pls-c">
                <h3>Rezirkulationspumpe P4.1 {pump_status(True)}</h3>
                <p style="font-size:0.8em;color:#b2bec3;margin:0 0 6px">Propellerpumpe, trocken aufgestellt, FU-geregelt</p>
                {vtbl(
                    vr("Förderstrom Q", f"{irez_Q_ist:.0f}", "m³/h")
                    + vr("Förderhöhe H", f"{irez_H_ist:.1f}", "m")
                    + vr("Drehzahl (FU)", f"{irez_f:.0f}", "Hz")
                    + vr("Motorstrom I (FU)", f"{irez_I:.1f}", "A")
                    + vr("Motorspannung U (FU)", f"{irez_U:.0f}", "V")
                    + vr("Leistungsfaktor cos φ (FU)", f"{irez_cos:.2f}", "")
                    + vr("Motorwirkungsgrad (Datenblatt)", "90", "%")
                    + vr("Wirkungsgrad η", f"{irez_eta*100:.0f}", "%")
                    + vr("Betriebsstunden", f"{irez_bh:.0f}", "h")
                    + vr("Rez.-Verhältnis", f"{irez_Q_ist/max(1,Q_h):.1f}", "× Q_zu")
                )}
            </div>
        </div>

        {rs_block_html}
        {ft_block_html}

        <!-- EXZENTERSCHNECKENPUMPEN -->
        <div class="pls-c" style="margin-top:15px"><h3>🟣 Exzenterschneckenpumpen</h3></div>

        <div class="pls-g3">
            <div class="pls-c">
                <h3>Primärschlamm P2.1 {pump_status(True)}</h3>
                <p style="font-size:0.8em;color:#b2bec3;margin:0 0 6px">Seepex BN 35-6L – drehzahlgeregelt</p>
                {vtbl(
                    vr("Förderstrom Q", f"{ps_Q_h:.2f}", "m³/h")
                    + vr("TS Primärschlamm", f"{ps_ts}", "g/L")
                    + vr("Förderdruck", f"{ps_p:.1f}", "bar")
                    + vr("Drehzahl", f"{ps_n}", "min⁻¹")
                    + vr("Leistung P₁", f"{ps_P:.1f}", "kW")
                    + vr("Betriebsstunden", f"{ps_bh:.0f}", "h")
                    + vr("Stator-Zustand", "gut", "", wh=99)
                )}
                {esp_svg("Primärschlammpumpe P2.1", ps_Q_h, ps_ts, ps_p, ps_n, ps_P)}
            </div>
            <div class="pls-c">
                <h3>Überschussschlamm P5.1 {pump_status(True)}</h3>
                <p style="font-size:0.8em;color:#b2bec3;margin:0 0 6px">Seepex BN 52-6L – drehzahlgeregelt</p>
                {vtbl(
                    vr("Förderstrom Q", f"{ues_Q_h:.2f}", "m³/h")
                    + vr("TS Überschussschlamm", f"{ues_ts:.1f}", "g/L")
                    + vr("Förderdruck", f"{ues_p:.1f}", "bar")
                    + vr("Drehzahl", f"{ues_n}", "min⁻¹")
                    + vr("Leistung P₁", f"{ues_P:.1f}", "kW")
                    + vr("Betriebsstunden", f"{ues_bh:.0f}", "h")
                    + vr("Stator-Zustand", "verschlissen", "", dl=99)
                )}
                {esp_svg("ÜS-Pumpe P5.1", ues_Q_h, ues_ts, ues_p, ues_n, ues_P)}
            </div>
            <div class="pls-c">
                <h3>Dickschlamm P6.1 {pump_status(ds_Q_h > 0.1)}</h3>
                <p style="font-size:0.8em;color:#b2bec3;margin:0 0 6px">Seepex BN 70-6L – drehzahlgeregelt</p>
                {vtbl(
                    vr("Förderstrom Q", f"{ds_Q_h:.2f}", "m³/h")
                    + vr("TS Dickschlamm", f"{ds_ts}", "g/L")
                    + vr("Förderdruck", f"{ds_p:.1f}", "bar")
                    + vr("Drehzahl", f"{ds_n}", "min⁻¹")
                    + vr("Leistung P₁", f"{ds_P:.1f}", "kW")
                    + vr("Betriebsstunden", f"{ds_bh:.0f}", "h")
                    + vr("Stator-Zustand", "gut", "", wh=99)
                )}
                {esp_svg("Dickschlammpumpe P6.1", ds_Q_h, ds_ts, ds_p, ds_n, ds_P)}
            </div>
        </div>

        <!-- KOLBENMEMBRANPUMPEN -->
        <div class="pls-c" style="margin-top:15px"><h3>🔴 Kolbenmembranpumpen</h3></div>

        <div class="pls-g3">
            <div class="pls-c">
                <h3>Fällmittel P7.1 (Fe³⁺) {pump_status(fm_Q > 0)}</h3>
                <p style="font-size:0.8em;color:#b2bec3;margin:0 0 6px">ProMinent Sigma S2Cb – FeCl₃ 40%, ρ=1,42 kg/L</p>
                {vtbl(
                    vr("Dosierstrom Q", f"{fm_Q:.1f}", "L/h")
                    + vr("Hublänge", f"{fm_hub_pct:.0f}", "%")
                    + vr("Hubfrequenz", f"{fm_freq}", "min⁻¹")
                    + vr("Gegendruck", f"{fm_p:.0f}", "bar")
                    + vr("Leistung P₁", f"{fm_P:.2f}", "kW")
                    + vr("Betriebsstunden", f"{fm_bh:.0f}", "h")
                    + vr("Membran-Zustand", "gut", "")
                )}
                {kmp_svg("Fällmittelpumpe P7.1", fm_Q, fm_hub_pct, fm_freq, fm_p, fm_P, "FeCl₃ 40%")}
            </div>
            <div class="pls-c">
                <h3>Polymer P8.1 (FHM) {pump_status(poly_Q > 0.5)}</h3>
                <p style="font-size:0.8em;color:#b2bec3;margin:0 0 6px">ProMinent Sigma S1Cb – Polyelektrolyt 0,1%</p>
                {vtbl(
                    vr("Dosierstrom Q", f"{poly_Q:.1f}", "L/h")
                    + vr("Hublänge", f"{poly_hub_pct:.0f}", "%")
                    + vr("Hubfrequenz", f"{poly_freq}", "min⁻¹")
                    + vr("Gegendruck", f"{poly_p:.0f}", "bar")
                    + vr("Leistung P₁", f"{poly_P:.2f}", "kW")
                    + vr("Betriebsstunden", f"{poly_bh:.0f}", "h")
                    + vr("Membran-Zustand", "gut", "")
                )}
                {kmp_svg("Polymerpumpe P8.1", poly_Q, poly_hub_pct, poly_freq, poly_p, poly_P, "Polyelektrolyt")}
            </div>
            <div class="pls-c">
                <h3>Kalkmilch P9.1 {pump_status(kalk_aktiv)}</h3>
                <p style="font-size:0.8em;color:#b2bec3;margin:0 0 6px">ProMinent Sigma S1Cb – Ca(OH)₂ 5%, pH-geregelt</p>
                {vtbl(
                    vr("Dosierstrom Q", f"{kalk_Q:.1f}", "L/h")
                    + vr("Hublänge", f"{kalk_hub_pct:.0f}", "%")
                    + vr("Hubfrequenz", f"{kalk_freq}", "min⁻¹")
                    + vr("Gegendruck", f"{kalk_p:.0f}", "bar")
                    + vr("Leistung P₁", f"{kalk_P:.2f}", "kW")
                    + vr("Betriebsstunden", f"{kalk_bh:.0f}", "h")
                    + vr("pH Ablauf (Regelgröße)", f"{c['ph_ab']:.2f}", "", wl=6.8, dl=6.5)
                )}
                {kmp_svg("Kalkmilchpumpe P9.1", kalk_Q, kalk_hub_pct, kalk_freq, kalk_p, kalk_P, "Ca(OH)₂ 5%")}
            </div>
        </div>

        <!-- Pumpen-Zusammenfassung -->
        <div class="pls-c" style="margin-top:10px"><h3>📊 Pumpen-Gesamtübersicht</h3>
            <table style="width:100%;border-collapse:collapse;font-size:0.88em;color:#ffffff;background:#16213e">
                <tr style="border-bottom:2px solid #0f3460;background:#0f1a30">
                    <th style="padding:8px 16px;color:#74b9ff;text-align:left">Pumpe</th>
                    <th style="padding:8px 16px;color:#74b9ff;text-align:left">Typ</th>
                    <th style="padding:8px 16px;color:#74b9ff;text-align:right">Q</th>
                    <th style="padding:8px 16px;color:#74b9ff;text-align:right">P [kW] / I [A]</th>
                    <th style="padding:8px 16px;color:#74b9ff;text-align:center">Status</th>
                </tr>
                <tr style="border-bottom:1px solid #0f3460"><td style="padding:5px 16px">P1.1 Zulauf</td><td style="padding:5px 16px">Kreiselpumpe</td><td style="text-align:right;padding:5px 16px">{zp_Q_ist:.0f}&ensp;m³/h</td><td style="text-align:right;padding:5px 16px">{zp_I:.1f}&ensp;A</td><td style="text-align:center;padding:5px 16px">{pump_status(True)}</td></tr>
                <tr style="border-bottom:1px solid #0f3460"><td style="padding:5px 16px">P1.2 Zulauf</td><td style="padding:5px 16px">Kreiselpumpe</td><td style="text-align:right;padding:5px 16px">–</td><td style="text-align:right;padding:5px 16px">–</td><td style="text-align:center;padding:5px 16px">{pump_status_reserve()}</td></tr>
                <tr style="border-bottom:1px solid #0f3460"><td style="padding:5px 16px">P3.1–3.6 RS</td><td style="padding:5px 16px">Kreiselpumpe (6×)</td><td style="text-align:right;padding:5px 16px">{rs_q_sum:.0f}&ensp;m³/h</td><td style="text-align:right;padding:5px 16px">–</td><td style="text-align:center;padding:5px 16px"><span style="color:#00b894;font-weight:bold">● {rs_n_ein}/{pm['rs_n_max']} EIN</span></td></tr>
                <tr style="border-bottom:1px solid #0f3460"><td style="padding:5px 16px">P10.1 Umwälz. FT</td><td style="padding:5px 16px">Kreiselpumpe</td><td style="text-align:right;padding:5px 16px">{ft_m1['q']:.0f}&ensp;m³/h</td><td style="text-align:right;padding:5px 16px">–</td><td style="text-align:center;padding:5px 16px">{pump_status(True)}</td></tr>
                <tr style="border-bottom:1px solid #0f3460"><td style="padding:5px 16px">P10.2 Umwälz. FT</td><td style="padding:5px 16px">Kreiselpumpe</td><td style="text-align:right;padding:5px 16px">–</td><td style="text-align:right;padding:5px 16px">–</td><td style="text-align:center;padding:5px 16px">{pump_status_reserve()}</td></tr>
                <tr style="border-bottom:1px solid #0f3460"><td style="padding:5px 16px">P4.1 Rez.</td><td style="padding:5px 16px">Propellerpumpe</td><td style="text-align:right;padding:5px 16px">{irez_Q_ist:.0f}&ensp;m³/h</td><td style="text-align:right;padding:5px 16px">{irez_P:.2f}</td><td style="text-align:center;padding:5px 16px">{pump_status(True)}</td></tr>
                <tr style="border-bottom:1px solid #0f3460"><td style="padding:5px 16px">P2.1 PS</td><td style="padding:5px 16px">Exz.schnecke</td><td style="text-align:right;padding:5px 16px">{ps_Q_h:.2f}&ensp;m³/h</td><td style="text-align:right;padding:5px 16px">{ps_P:.1f}</td><td style="text-align:center;padding:5px 16px">{pump_status(True)}</td></tr>
                <tr style="border-bottom:1px solid #0f3460"><td style="padding:5px 16px">P5.1 ÜS</td><td style="padding:5px 16px">Exz.schnecke</td><td style="text-align:right;padding:5px 16px">{ues_Q_h:.2f}&ensp;m³/h</td><td style="text-align:right;padding:5px 16px">{ues_P:.1f}</td><td style="text-align:center;padding:5px 16px">{pump_status(True)}</td></tr>
                <tr style="border-bottom:1px solid #0f3460"><td style="padding:5px 16px">P6.1 DS</td><td style="padding:5px 16px">Exz.schnecke</td><td style="text-align:right;padding:5px 16px">{ds_Q_h:.2f}&ensp;m³/h</td><td style="text-align:right;padding:5px 16px">{ds_P:.1f}</td><td style="text-align:center;padding:5px 16px">{pump_status(ds_Q_h > 0.1)}</td></tr>
                <tr style="border-bottom:1px solid #0f3460"><td style="padding:5px 16px">P7.1 Fe³⁺</td><td style="padding:5px 16px">Kolbenmembran</td><td style="text-align:right;padding:5px 16px">{fm_Q:.1f}&ensp;L/h</td><td style="text-align:right;padding:5px 16px">{fm_P:.2f}</td><td style="text-align:center;padding:5px 16px">{pump_status(fm_Q > 0)}</td></tr>
                <tr style="border-bottom:1px solid #0f3460"><td style="padding:5px 16px">P8.1 Poly</td><td style="padding:5px 16px">Kolbenmembran</td><td style="text-align:right;padding:5px 16px">{poly_Q:.1f}&ensp;L/h</td><td style="text-align:right;padding:5px 16px">{poly_P:.2f}</td><td style="text-align:center;padding:5px 16px">{pump_status(poly_Q > 0.5)}</td></tr>
                <tr style="border-bottom:1px solid #0f3460"><td style="padding:5px 16px">P9.1 Kalk</td><td style="padding:5px 16px">Kolbenmembran</td><td style="text-align:right;padding:5px 16px">{kalk_Q:.1f}&ensp;L/h</td><td style="text-align:right;padding:5px 16px">{kalk_P:.2f}</td><td style="text-align:center;padding:5px 16px">{pump_status(kalk_aktiv)}</td></tr>
                <tr style="border-top:2px solid #74b9ff"><td colspan="3" style="padding:6px 16px;font-weight:bold;color:#74b9ff">Σ angezeigte Leistungen [kW]</td>
                    <td style="text-align:right;padding:6px 16px;font-weight:bold;color:#74b9ff">{ps_P + ues_P + ds_P + fm_P + poly_P + kalk_P:.1f}</td>
                    <td></td></tr>
            </table>
        </div>
        </div>''')

        # === PREDICTIVE MAINTENANCE DETAIL PANELS ===
        import plotly.graph_objects as _go
        from plotly.subplots import make_subplots as _mp

        np.random.seed(42)
        _tage = np.arange(56)

        # --- P1.1 Zulaufpumpe: leichter Lagerverschleiß ---
        p11_strom = zp_I * np.ones(56) + np.random.normal(0, zp_I * 0.03, 56) + _tage * 0.006
        p11_strom[-7:] += 0.3
        p11_flow = zp_Q_ist * 1.02 * np.ones(56) + np.random.normal(0, zp_Q_ist * 0.04, 56) - _tage * 0.02
        p11_vib = 2.5 + np.random.normal(0, 0.3, 56) + _tage * 0.015
        p11_vib[-5:] += np.array([0.3, 0.5, 0.2, 0.8, 0.6])
        p11_tlager = 45 + np.random.normal(0, 1.5, 56) + _tage * 0.08
        p11_tlager[-7:] += 3

        if detail_p11.value:
            fig11 = _mp(rows=2, cols=2,
                subplot_titles=("Stromaufnahme I [A]", "Förderstrom Q [m³/h]",
                                "Vibration [mm/s]", "Lagertemperatur [°C]"),
                vertical_spacing=0.18, horizontal_spacing=0.10)
            fig11.add_trace(_go.Scatter(x=_tage, y=p11_strom, mode='lines+markers',
                line=dict(color='#0984e3', width=1.5), marker=dict(size=3)), row=1, col=1)
            fig11.add_hline(y=zp_I*1.15, line_dash="dash", line_color="#e17055", row=1, col=1,
                annotation_text="Warn", annotation_font_color="#e17055", annotation_font_size=9)
            _z1 = np.polyfit(_tage, p11_strom, 1)
            fig11.add_trace(_go.Scatter(x=_tage, y=np.polyval(_z1, _tage), mode='lines',
                line=dict(color='#fdcb6e', width=2, dash='dash')), row=1, col=1)
            fig11.add_trace(_go.Scatter(x=_tage, y=p11_flow, mode='lines+markers',
                line=dict(color='#00b894', width=1.5), marker=dict(size=3)), row=1, col=2)
            fig11.add_trace(_go.Scatter(x=_tage, y=p11_vib, mode='lines+markers',
                line=dict(color='#fdcb6e', width=1.5), marker=dict(size=3)), row=2, col=1)
            fig11.add_hline(y=4.5, line_dash="dash", line_color="#e17055", row=2, col=1,
                annotation_text="Warn", annotation_font_color="#e17055", annotation_font_size=9)
            fig11.add_trace(_go.Scatter(x=_tage, y=p11_tlager, mode='lines+markers',
                line=dict(color='#e17055', width=1.5), marker=dict(size=3)), row=2, col=2)
            fig11.add_hline(y=55, line_dash="dash", line_color="#e17055", row=2, col=2,
                annotation_text="Warn", annotation_font_color="#e17055", annotation_font_size=9)
            fig11.update_layout(height=500, template="plotly_dark",
                paper_bgcolor="#1a1a2e", plot_bgcolor="#16213e", showlegend=False,
                font=dict(family="Consolas,monospace", size=10, color="#dfe6e9"),
                margin=dict(t=35, b=35, l=50, r=20))
            fig11.update_xaxes(gridcolor="#0f3460", title_text="")
            fig11.update_xaxes(title_text="Tage", row=2, col=1)
            fig11.update_xaxes(title_text="Tage", row=2, col=2)
            fig11.update_yaxes(gridcolor="#0f3460")

            _st1 = (p11_strom[-7:].mean() - p11_strom[:7].mean()) / p11_strom[:7].mean() * 100
            _vb1 = p11_vib[-1]
            _tl1 = p11_tlager[-1]
            if _vb1 > 4.5 or _tl1 > 55:
                _bew1 = '<span style="color:#e17055;font-weight:bold">⚠️ Wartung empfohlen</span>'
                _det1 = "Vibration und/oder Lagertemperatur erhöht → Verdacht Lagerverschleiß. Lager prüfen, Schmierfettaustausch oder Lagertausch einplanen."
            elif _st1 > 5:
                _bew1 = '<span style="color:#fdcb6e;font-weight:bold">🔶 Beobachten</span>'
                _det1 = f"Stromaufnahme +{_st1:.1f}%. Mögliche Ursache: Anlagerungen am Laufrad oder beginnender Lagerverschleiß. Nächste Inspektion vorziehen."
            else:
                _bew1 = '<span style="color:#00b894;font-weight:bold">✅ Unauffällig</span>'
                _det1 = "Alle Parameter im Normbereich."

            panel_p11 = mo.vstack([
                mo.Html(f'''<div class="pls"><div class="pls-c" style="border-color:#0984e3;border-width:2px">
                    <h3 style="color:#0984e3">🔍 Predictive Maintenance – P1.1 Zulaufpumpe (Flygt NP 3153)</h3>
                    <p style="font-size:0.85em;margin:4px 0 8px">Trendanalyse der letzten 8 Wochen (Tageswerte aus BDE).</p>
                    {vtbl(
                        vr("Bewertung", _bew1, "")
                        + vr("Stromtrend (8 Wo.)", f"+{_st1:.1f}", "%", wh=5, dh=10)
                        + vr("Vibration aktuell", f"{_vb1:.1f}", "mm/s", wh=4.0, dh=4.5)
                        + vr("Lagertemperatur", f"{_tl1:.0f}", "°C", wh=52, dh=58)
                    )}
                    <p style="font-size:0.85em;color:#b2bec3;margin:8px 0 4px"><strong>Diagnose:</strong> {_det1}</p>
                    <p style="font-size:0.8em;color:#636e72;margin:2px 0">
                        Messgrößen: Stromaufnahme (Motorschutzrelais), Förderstrom (MID DN250),
                        Schwinggeschwindigkeit (Piezo-Sensor Lagerdeckel), Lagertemperatur (PT100 Antriebslager).
                    </p>
                </div></div>'''),
                fig11,
            ])
        else:
            panel_p11 = mo.Html("")

        # --- P5.1 ÜS-Pumpe: Statorverschleiß ---
        p51_strom = ues_P * np.ones(56) + np.random.normal(0, ues_P * 0.03, 56) + _tage * 0.012
        p51_strom[-14:] += np.arange(14) * 0.005
        p51_flow0 = ues_Q_h * 1.1
        p51_flow = p51_flow0 * np.ones(56) + np.random.normal(0, p51_flow0 * 0.04, 56) - _tage * 0.008
        p51_flow[-14:] -= np.arange(14) * 0.003
        p51_druck = ues_p * np.ones(56) + np.random.normal(0, 0.15, 56) + _tage * 0.01
        p51_spalt = 0.3 + _tage * 0.008 + np.random.normal(0, 0.03, 56)
        p51_spalt[-14:] += np.arange(14) * 0.003

        if detail_p51.value:
            fig51 = _mp(rows=2, cols=2,
                subplot_titles=("Stromaufnahme P₁ [kW]", "Förderstrom Q [m³/h]",
                                "Förderdruck [bar]", "Spaltmaß Rotor/Stator [mm]"),
                vertical_spacing=0.18, horizontal_spacing=0.10)
            fig51.add_trace(_go.Scatter(x=_tage, y=p51_strom, mode='lines+markers',
                line=dict(color='#a29bfe', width=1.5), marker=dict(size=3)), row=1, col=1)
            fig51.add_hline(y=ues_P*1.25, line_dash="dash", line_color="#e17055", row=1, col=1,
                annotation_text="Warn", annotation_font_color="#e17055", annotation_font_size=9)
            _z5 = np.polyfit(_tage, p51_strom, 1)
            fig51.add_trace(_go.Scatter(x=_tage, y=np.polyval(_z5, _tage), mode='lines',
                line=dict(color='#fdcb6e', width=2, dash='dash')), row=1, col=1)
            fig51.add_trace(_go.Scatter(x=_tage, y=p51_flow, mode='lines+markers',
                line=dict(color='#00b894', width=1.5), marker=dict(size=3)), row=1, col=2)
            _z5q = np.polyfit(_tage, p51_flow, 1)
            fig51.add_trace(_go.Scatter(x=_tage, y=np.polyval(_z5q, _tage), mode='lines',
                line=dict(color='#fdcb6e', width=2, dash='dash')), row=1, col=2)
            fig51.add_trace(_go.Scatter(x=_tage, y=p51_druck, mode='lines+markers',
                line=dict(color='#fdcb6e', width=1.5), marker=dict(size=3)), row=2, col=1)
            fig51.add_trace(_go.Scatter(x=_tage, y=p51_spalt, mode='lines+markers',
                line=dict(color='#e17055', width=1.5), marker=dict(size=3)), row=2, col=2)
            fig51.add_hline(y=0.6, line_dash="dash", line_color="#fdcb6e", row=2, col=2,
                annotation_text="Warn", annotation_font_color="#fdcb6e", annotation_font_size=9)
            fig51.add_hline(y=0.8, line_dash="dash", line_color="#e17055", row=2, col=2,
                annotation_text="Grenz", annotation_font_color="#e17055", annotation_font_size=9)
            fig51.update_layout(height=500, template="plotly_dark",
                paper_bgcolor="#1a1a2e", plot_bgcolor="#16213e", showlegend=False,
                font=dict(family="Consolas,monospace", size=10, color="#dfe6e9"),
                margin=dict(t=35, b=35, l=50, r=20))
            fig51.update_xaxes(gridcolor="#0f3460", title_text="")
            fig51.update_xaxes(title_text="Tage", row=2, col=1)
            fig51.update_xaxes(title_text="Tage", row=2, col=2)
            fig51.update_yaxes(gridcolor="#0f3460")

            _st5 = (p51_strom[-7:].mean() - p51_strom[:7].mean()) / p51_strom[:7].mean() * 100
            _fl5 = (p51_flow[:7].mean() - p51_flow[-7:].mean()) / p51_flow[:7].mean() * 100
            _sp5 = p51_spalt[-1]
            _zsp = np.polyfit(_tage, p51_spalt, 1)
            _rest = max(0, (0.8 - _zsp[1]) / _zsp[0] - 56) if _zsp[0] > 0 else 999

            if _sp5 > 0.8:
                _bew5 = '<span style="color:#e17055;font-weight:bold">🔴 Stator tauschen!</span>'
                _det5 = "Spaltmaß hat den Grenzwert überschritten. Stator muss getauscht werden. Volumetrischer Wirkungsgrad sinkt, Stromaufnahme steigt → höhere Betriebskosten und Ausfallgefahr."
            elif _sp5 > 0.6:
                _bew5 = '<span style="color:#fdcb6e;font-weight:bold">⚠️ Statortausch einplanen</span>'
                _det5 = f"Spaltmaß im Warnbereich ({_sp5:.2f} mm). Bei aktuellem Trend wird der Grenzwert (0,8 mm) in ca. {_rest:.0f} Tagen erreicht. Ersatzstator bestellen."
            else:
                _bew5 = '<span style="color:#00b894;font-weight:bold">✅ Unauffällig</span>'
                _det5 = "Alle Parameter im Normbereich."

            panel_p51 = mo.vstack([
                mo.Html(f'''<div class="pls"><div class="pls-c" style="border-color:#a29bfe;border-width:2px">
                    <h3 style="color:#a29bfe">🔍 Predictive Maintenance – P5.1 ÜS-Pumpe (Seepex BN 52-6L)</h3>
                    <p style="font-size:0.85em;margin:4px 0 8px">
                        Trendanalyse der letzten 8 Wochen. Das Spaltmaß Rotor/Stator ist der zentrale
                        Verschleißindikator bei Exzenterschneckenpumpen.
                    </p>
                    {vtbl(
                        vr("Bewertung", _bew5, "")
                        + vr("Stromtrend (8 Wo.)", f"+{_st5:.1f}", "%", wh=10, dh=20)
                        + vr("Förderstromverlust", f"-{_fl5:.1f}", "%", wh=10, dh=20)
                        + vr("Spaltmaß aktuell", f"{_sp5:.2f}", "mm", wh=0.6, dh=0.8)
                        + vr("Prognose Grenzwert", f"~{_rest:.0f}", "Tage")
                    )}
                    <p style="font-size:0.85em;color:#b2bec3;margin:8px 0 4px"><strong>Diagnose:</strong> {_det5}</p>
                    <p style="font-size:0.8em;color:#636e72;margin:2px 0">
                        Messgrößen: Stromaufnahme (FU-Rückmeldung), Förderstrom (MID DN80),
                        Förderdruck (Druckmessumformer Druckseite), Spaltmaß (berechnet aus Q/n-Verhältnis).
                    </p>
                </div></div>'''),
                fig51,
            ])
        else:
            panel_p51 = mo.Html("")

        pumpen = mo.vstack([
            pumpen_html,
            mo.Html('<div class="pls"><div class="pls-c"><h3>🔧 Vorausschauende Wartung (Predictive Maintenance)</h3><p style="font-size:0.85em;color:#b2bec3;margin:4px 0">Schalter aktivieren um 8-Wochen-Trendanalysen mit Verschleißindikatoren und Handlungsempfehlungen anzuzeigen.</p></div></div>'),
            mo.hstack([detail_p11, detail_p51], justify="start", gap=1),
            panel_p11,
            panel_p51,
            mo.Html('''<div class="pls">
            <div class="pls-c" style="border-color:#0984e3;margin-top:10px">
                <h3 style="color:#0984e3">📈 Simulation: Kennlinien messen</h3>
                <p style="font-size:0.85em;margin:6px 0">
                    Interaktive Marimo-Simulation zur Aufnahme der <strong>Pumpen- und Anlagenkennlinie</strong>
                    einer Kreiselpumpe. Über simulierte Manometerdrücke (Saug- und Druckseite) und einen
                    magnetisch-induktiven Durchflussmesser (MID) werden die Betriebspunkte bei verschiedenen
                    Drehzahlen und Schieberstellungen ermittelt und grafisch dargestellt.
                </p>
                <p style="font-size:0.85em;margin:6px 0">
                    <strong>Bezug zur Kläranlage:</strong> Genau so werden die Kennlinien der Zulaufpumpen
                    P1.1/P1.2 und RS-Pumpen P3.1–P3.6 im Rahmen der Inbetriebnahme und bei
                    Wartungsprüfungen aufgenommen. Ein Vergleich mit der Werkskennlinie zeigt
                    Verschleiß an Laufrad oder Gehäuse.
                </p>
                <a href="https://thurin27.github.io/Kennlinien_messen/"
                   target="_blank"
                   style="display:inline-block;padding:8px 20px;background:#0984e3;color:#fff;
                          border-radius:4px;text-decoration:none;font-weight:bold;font-size:0.9em;margin-top:4px">
                    ▶ Simulation Kennlinien messen öffnen
                </a>
            </div>
            </div>'''),
        ])

        # ====== REGELUNG ======
        regelung = mo.Html('''<div class="pls">
        <div class="pls-c"><h3>📐 Regelungstechnik – Simulationen</h3>
            <p style="font-size:0.9em;margin:8px 0">
                Die folgenden interaktiven Marimo-Simulationen vertiefen zentrale Regelungskonzepte,
                die auf der Kläranlage zum Einsatz kommen. Beide laufen direkt im Browser.
            </p>
        </div>

        <div class="pls-g2">
            <div class="pls-c" style="border-color:#0984e3">
                <h3 style="color:#0984e3">🏗️ Füllstandsregelung</h3>
                <table class="pls-tbl">
                    <tr><td>Regelgröße</td><td class="c-v">Füllstand h [m]</td></tr>
                    <tr><td>Stellgröße</td><td class="c-v">Pumpendrehzahl / Ventilstellung</td></tr>
                    <tr><td>Störgrößen</td><td class="c-v">Zulaufschwankungen, Verbraucher</td></tr>
                    <tr><td>Reglertyp</td><td class="c-v">P-, PI-, PID-Regler (wählbar)</td></tr>
                    <tr><td>Besonderheit</td><td class="c-v">Vergleich der Reglertypen</td></tr>
                </table>
                <div style="margin-top:12px;padding:10px;background:#2d3436;border-radius:6px">
                    <p style="font-size:0.85em;color:#dfe6e9;margin:0 0 6px">
                        <strong style="color:#0984e3">Lernziele:</strong> Unterschied P/PI/PID-Regler verstehen,
                        bleibende Regelabweichung beim P-Regler beobachten,
                        Einfluss von Kp, Tn, Tv auf Sprungantwort analysieren.
                    </p>
                    <p style="font-size:0.85em;color:#dfe6e9;margin:0 0 8px">
                        <strong style="color:#0984e3">Bezug zur Kläranlage:</strong>
                        Im Zulaufpumpwerk regelt der FU der Zulaufpumpe P1.1 den Wasserstand im Pumpensumpf.
                        Bei steigendem Zulauf (z.B. Regen) muss die Drehzahl schnell nachgeführt werden,
                        um Überflutung zu vermeiden – ein klassisches Füllstandsregelungsproblem.
                    </p>
                    <a href="https://thurin27.github.io/Fuellstandsregelung/"
                       target="_blank"
                       style="display:inline-block;padding:8px 20px;background:#0984e3;color:#fff;
                              border-radius:4px;text-decoration:none;font-weight:bold;font-size:0.9em">
                        ▶ Simulation Füllstandsregelung öffnen
                    </a>
                </div>
            </div>

            <div class="pls-c" style="border-color:#a29bfe">
                <h3 style="color:#a29bfe">🧪 Phosphatfällung mit Totzeit</h3>
                <table class="pls-tbl">
                    <tr><td>Regelgröße</td><td class="c-v">P-ges Ablauf [mg/L]</td></tr>
                    <tr><td>Stellgröße</td><td class="c-v">Fällmitteldosierung FeCl₃ [L/h]</td></tr>
                    <tr><td>Störgrößen</td><td class="c-v">P-Fracht Zulauf, pH, Temperatur</td></tr>
                    <tr><td>Reglertyp</td><td class="c-v">PI-Regler mit Totzeit</td></tr>
                    <tr><td>Besonderheit</td><td class="c-v">Totzeit durch Fließstrecke & Reaktionskinetik</td></tr>
                </table>
                <div style="margin-top:12px;padding:10px;background:#2d3436;border-radius:6px">
                    <p style="font-size:0.85em;color:#dfe6e9;margin:0 0 6px">
                        <strong style="color:#a29bfe">Lernziele:</strong> Einfluss der Totzeit auf die Regelgüte verstehen,
                        Kp und Tn eines PI-Reglers einstellen, Überschwingen und Ausregelzeit beobachten,
                        Störgrößenaufschaltung als Verbesserung erkennen.
                    </p>
                    <p style="font-size:0.85em;color:#dfe6e9;margin:0 0 8px">
                        <strong style="color:#a29bfe">Bezug zur Kläranlage:</strong>
                        Die Fällmittelpumpe P7.1 (Kolbenmembranpumpe, ProMinent Sigma) dosiert FeCl₃
                        basierend auf dem P-ges-Messwert im Ablauf. Die Totzeit entsteht durch die
                        Fließstrecke zwischen Dosierstelle und Messstelle (ca. 20–45 min).
                    </p>
                    <a href="https://thurin27.github.io/Simulation_Phosphatfaellung/"
                       target="_blank"
                       style="display:inline-block;padding:8px 20px;background:#a29bfe;color:#1a1a2e;
                              border-radius:4px;text-decoration:none;font-weight:bold;font-size:0.9em">
                        ▶ Simulation Phosphatfällung öffnen
                    </a>
                </div>
            </div>
        </div>

        <div class="pls-c" style="margin-top:10px"><h3>🔗 Regelkreise auf dieser Kläranlage</h3>
            <table style="width:100%;border-collapse:collapse;font-size:0.88em;color:#ffffff;background:#16213e">
                <tr style="border-bottom:2px solid #0f3460;background:#0f1a30"><th style="padding:8px 16px;color:#74b9ff;text-align:left">Regelkreis</th><th style="padding:8px 16px;color:#74b9ff;text-align:left">Regelgröße</th><th style="padding:8px 16px;color:#74b9ff;text-align:left">Stellglied</th><th style="padding:8px 16px;color:#74b9ff;text-align:left">Reglertyp</th></tr>
                <tr style="border-bottom:1px solid #0f3460"><td style="padding:5px 16px">Zulauf-Füllstand</td><td style="padding:5px 16px">Wasserstand Pumpensumpf</td><td style="padding:5px 16px">P1.1 Zulaufpumpe (FU)</td><td style="padding:5px 16px">PI</td></tr>
                <tr style="border-bottom:1px solid #0f3460"><td style="padding:5px 16px">O₂-Regelung BB</td><td style="padding:5px 16px">O₂-Gehalt [mg/L]</td><td style="padding:5px 16px">Gebläse / Belüfter</td><td style="padding:5px 16px">PID</td></tr>
                <tr style="border-bottom:1px solid #0f3460"><td style="padding:5px 16px">RS-Regelung</td><td style="padding:5px 16px">Schlammschicht NK [cm]</td><td style="padding:5px 16px">P3.1–P3.6 RS-Pumpen (Stufenschaltung)</td><td style="padding:5px 16px">Mehrpunkt</td></tr>
                <tr style="border-bottom:1px solid #0f3460"><td style="padding:5px 16px">P-Elimination</td><td style="padding:5px 16px">P-ges Ablauf [mg/L]</td><td style="padding:5px 16px">P7.1 Fällmittel-KMP</td><td style="padding:5px 16px">PI + Totzeit</td></tr>
                <tr style="border-bottom:1px solid #0f3460"><td style="padding:5px 16px">pH-Korrektur</td><td style="padding:5px 16px">pH Ablauf [-]</td><td style="padding:5px 16px">P9.1 Kalkmilch-KMP</td><td style="padding:5px 16px">Zweipunkt</td></tr>
                <tr style="border-bottom:1px solid #0f3460"><td style="padding:5px 16px">Polymer-Dosierung</td><td style="padding:5px 16px">TS Filtrat [mg/L]</td><td style="padding:5px 16px">P8.1 Polymer-KMP</td><td style="padding:5px 16px">Festwert</td></tr>
            </table>
        </div>
        </div>''')

        # ====== MODIFIKATIONEN TAB ======
        m = st.get("mods", {})
        n_aktiv = sum(1 for v in m.values() if v)

        # Kosten-Datenbank
        MOD_DB = {
            "p_online": {"name": "Online-P-Messung am Zulauf", "kat": "Messtechnik", "inv": 25000, "betr": 2000,
                "icon": "🟢", "color": "#00b894",
                "tech": "Photometrische Phosphat-Sonde (z.B. Hach Phosphax sc) am Zulauf. Messwert wird als Störgrößenaufschaltung auf den PI-Regler der Fällmittelpumpe P7.1 geschaltet.",
                "wirkung": "Reduziert effektive Totzeit von ~30 min auf ~5 min. Fällmittel wird proportional zur P-Zulauffracht dosiert → ca. 20% weniger FeCl₃-Verbrauch bei gleicher Ablaufqualität."},
            "nh4_sensor": {"name": "NH₄-Sensor im Belebungsbecken", "kat": "Messtechnik", "inv": 18000, "betr": 3000,
                "icon": "🟢", "color": "#00b894",
                "tech": "Ionenselektive NH₄-Sonde (z.B. WTW VARiON) im BB-Auslauf. Kaskaden-Regelung: NH₄-Regler (Führungsregler) gibt O₂-Sollwert vor → O₂-Regler (Folgeregler) steuert Gebläse.",
                "wirkung": "Belüftung wird nur bei Bedarf hochgefahren → ca. 25% Energieeinsparung bei der Belüftung. Gleichzeitig stabilere NH₄-Ablaufwerte."},
            "spektral": {"name": "Spektralsonde am Zulauf (UV/VIS)", "kat": "Messtechnik", "inv": 35000, "betr": 4000,
                "icon": "🟢", "color": "#00b894",
                "tech": "UV/VIS-Spektralphotometer (z.B. s::can spectro::lyser) am Zulauf. Liefert CSB, TOC, TSS, NO₃ in Echtzeit. Ermöglicht vorausschauende Steuerung der Vorklärung und Dosierung.",
                "wirkung": "VK-Wirkungsgrad CSB verbessert sich von 30% auf 25% (= 5% mehr entfernt). Bessere Frachterkennung für Frühwarnung bei Stoßbelastungen."},
            "truebung": {"name": "Trübungsmessung NK-Ablauf", "kat": "Messtechnik", "inv": 8000, "betr": 1000,
                "icon": "🟢", "color": "#00b894",
                "tech": "Nephelometrische Trübungssonde (z.B. Hach Solitax sc) im NK-Ablauf. Erkennt Schlammabtrieb innerhalb von Sekunden → Alarm + RS-Pumpe hochfahren.",
                "wirkung": "AFS-Ablauf sinkt um ca. 1 mg/L. Frühwarnung bei Schlammflucht verhindert Grenzwertüberschreitungen. Verbesserte RS-Steuerung."},
            "membran": {"name": "Feinblasige Membranbelüfter", "kat": "Verfahren", "inv": 180000, "betr": 8000,
                "icon": "🔵", "color": "#0984e3",
                "tech": "Austausch grobblasiger Belüfter gegen Plattenmembranbelüfter (z.B. SSI AFD 350). SOTE steigt von ~3% auf ~6% pro m Einblastiefe. Gesamter O₂-Ertrag +35%.",
                "wirkung": "Gleiche biologische Leistung bei ca. 30% weniger Luftbedarf → direkte Energieeinsparung bei Gebläsen. Amortisation typisch 3-5 Jahre."},
            "turbo": {"name": "Turboverdichter statt Drehkolbengebläse", "kat": "Verfahren", "inv": 120000, "betr": 5000,
                "icon": "🔵", "color": "#0984e3",
                "tech": "Hocheffiziente Turboverdichter (z.B. HST Turbogebläse) mit Magnetlagerung, ölfreier Betrieb, stufenlose FU-Regelung. Wirkungsgrad ~80% vs. ~65% bei Drehkolben.",
                "wirkung": "Ca. 18% Energieeinsparung bei der Belüftung. Zusätzlich: wartungsarm (keine Ölwechsel, keine Riemen), leiser. Amortisation 4-6 Jahre."},
            "intermit": {"name": "Intermittierende Belüftung", "kat": "Verfahren", "inv": 30000, "betr": 2000,
                "icon": "🔵", "color": "#0984e3",
                "tech": "Taktbetrieb der Belüftung: Wechsel zwischen belüfteten (Nitrifikation) und unbelüfteten Phasen (Denitrifikation) im selben Becken. Steuerung über NH₄/NO₃-Sensoren oder Zeitprogramm.",
                "wirkung": "Denitrifikationsrate verbessert sich um ~8 Prozentpunkte. Belüftungsenergie sinkt um ~15%. ISV kann sich leicht verbessern (weniger Blähschlamm)."},
            "anammox": {"name": "Seitenstromentstickung (Deammonifikation)", "kat": "Verfahren", "inv": 350000, "betr": 15000,
                "icon": "🔵", "color": "#0984e3",
                "tech": "Anammox-Reaktor (z.B. DEMON®) für Prozesswasser aus Schlammentwässerung. Hochbelastetes Zentrat (500-1500 mg/L NH₄-N) wird separat behandelt. Anammox-Bakterien wandeln NH₄ + NO₂ → N₂ ohne externe C-Quelle.",
                "wirkung": "Interne N-Rückbelastung sinkt um ~80% → N-Ablauf ca. 12% niedriger. Weniger Belüftungsbedarf im Hauptstrom. Spart ca. 60% Energie gegenüber konventioneller Nitrifikation/Denitrifikation."},
            "stufe4": {"name": "4. Reinigungsstufe (GAK-Filter)", "kat": "Umbau", "inv": 800000, "betr": 60000,
                "icon": "🟣", "color": "#a29bfe",
                "tech": "Granulierte Aktivkohle (GAK) als Festbettfilter nach der NK. Eliminiert Spurenstoffe (Arzneimittel, Pestizide, PFAS), reduziert CSB/BSB zusätzlich um ~45%. Pflicht ab 2035 (EU-Kommunalabwasser-RL) für KA >100.000 EW, ab 2040 für >10.000 EW.",
                "wirkung": "CSB-Ablauf sinkt um ~45%, BSB um ~35%. Spurenstoffelimination >80%. Erhöhter Energiebedarf (~0.05 kWh/m³) und GAK-Kosten. Amortisation durch mögliche Abwasserabgabe-Erstattung."},
            "pv": {"name": "PV-Anlage (Dachflächen)", "kat": "Umbau", "inv": 100000, "betr": 1500,
                "icon": "🟣", "color": "#a29bfe",
                "tech": "100 kWp PV auf Betriebsgebäuden und NK-Abdeckungen. ~950 kWh/(kWp·a) in NRW → ~350 kWh/d im Jahresmittel. Eigenverbrauchsanteil auf KA typisch >85%.",
                "wirkung": "Ca. 350 kWh/d Eigenstromerzeugung im Jahresmittel, fast vollständig selbst verbraucht (Erzeugung nur tagsüber). Amortisation 7-10 Jahre. Kombinierbar mit Batteriespeicher für Spitzenabdeckung."},
        }

        # Karten generieren
        def mod_card(key, switch):
            d = MOD_DB[key]
            aktiv = m.get(key, False)
            border = d["color"] if aktiv else "#0f3460"
            opacity = "1" if aktiv else "0.7"
            return f'''<div class="pls-c" style="border-color:{border};border-width:{'2px' if aktiv else '1px'};opacity:{opacity}">
                <h3 style="color:{d['color']}">{d['icon']} {d['name']}</h3>
                <p style="font-size:0.8em;color:#636e72;margin:2px 0">Kategorie: {d['kat']} | Investition: {d['inv']:,.0f} € | Betriebskosten: {d['betr']:,.0f} €/a</p>
                <p style="font-size:0.85em;margin:6px 0"><strong>Technik:</strong> {d['tech']}</p>
                <p style="font-size:0.85em;margin:6px 0"><strong>Wirkung:</strong> {d['wirkung']}</p>
            </div>'''

        # Investitions-Summe
        inv_total = sum(MOD_DB[k]["inv"] for k in m if m.get(k))
        betr_total = sum(MOD_DB[k]["betr"] for k in m if m.get(k))

        # Energiebilanz
        e = st
        e_spar = max(0, e.get("e_geblaese_ref", 0) - e.get("e_geblaese", 0))

        # --- Unter-Tab Pumpentechnik: Umbauplanung, installierter Zustand, Preisliste ---
        _pkz = get_pk()
        def _kf_zeile(kks, ort):
            _a = pm["aggregate"][kks]
            _antr = f"FU, {_a['kl'][2]} 1/min" if _a["fu"] else "Festdrehzahl 1450 1/min"
            return (f'<tr style="border-bottom:1px solid #0f3460"><td style="padding:5px 12px;white-space:nowrap">{kks}</td>'
                    f'<td style="padding:5px 12px;white-space:nowrap">{ort}</td>'
                    f'<td style="padding:5px 12px;white-space:nowrap">KSB {_a["kl"][0]}</td>'
                    f'<td style="padding:5px 12px;text-align:right;white-space:nowrap">ø{_a["kl"][1]} mm</td>'
                    f'<td style="padding:5px 12px;white-space:nowrap">{_antr}</td>'
                    f'<td style="padding:5px 12px;white-space:nowrap;color:#b2bec3">{_a["umbau"] or "Bestand"}</td></tr>')
        kf_bestand_html = f'''<div class="pls-c"><h3>📋 Installierter Zustand</h3>
            <table style="border-collapse:collapse;font-size:0.85em;color:#ffffff;background:#16213e">
              <tr style="border-bottom:2px solid #0f3460;background:#0f1a30">
                <th style="padding:6px 12px;color:#74b9ff;text-align:left">KKS</th><th style="padding:6px 12px;color:#74b9ff;text-align:left">Standort</th>
                <th style="padding:6px 12px;color:#74b9ff;text-align:left">Pumpe</th><th style="padding:6px 12px;color:#74b9ff;text-align:right">Laufrad</th>
                <th style="padding:6px 12px;color:#74b9ff;text-align:left">Antrieb</th><th style="padding:6px 12px;color:#74b9ff;text-align:left">Stand</th></tr>
              {_kf_zeile("P-001", "PW Talstraße")}{_kf_zeile("P3.1", "RS-Pumpwerk")}{_kf_zeile("P10.1", "Faulturm-Umwälzung")}
            </table>
            <p style="font-size:0.8em;color:#b2bec3;margin:8px 0 2px">Umbauprotokoll:</p>
            <ul style="font-size:0.8em;color:#dfe6e9;margin:0 0 0 18px;padding:0">
              {"".join(f"<li>{_x}</li>" for _x in _pkz.get("protokoll", [])) or "<li>keine Umbauten durchgeführt</li>"}
            </ul></div>'''
        kf_preis_html = '''<div class="pls-c" style="background:#fffef5;color:#1a1a2e;border:2px solid #5a4820">
          <div style="display:flex;justify-content:space-between;border-bottom:2px solid #1a1a2e;padding-bottom:6px;margin-bottom:8px">
            <div><div style="font-size:0.75em;color:#5a4820;letter-spacing:2px">KSB SE &amp; CO. KGAA · VERTRIEBSBÜRO WEST</div>
                 <div style="font-size:1.05em;font-weight:bold">RICHTPREISANGEBOT PUMPENTECHNIK</div></div>
            <div style="text-align:right;font-size:0.75em;color:#5a4820">Angebot Nr. 4471-2026-118<br>gültig bis 31.12.2026</div>
          </div>
          <table style="border-collapse:collapse;font-size:0.85em;color:#1a1a2e">
            <tr><td style="padding:4px 12px;color:#5a4820">Sewatec E 100-317, komplett mit Motor 15 kW IE3, Laufrad nach Wahl</td><td style="padding:4px 12px;text-align:right;font-weight:bold;white-space:nowrap">18.618,00&ensp;€</td></tr>
            <tr style="background:#f5f0d8"><td style="padding:4px 12px;color:#5a4820">Sewabloc F 80-252, komplett mit Motor 4 kW IE3, Laufrad nach Wahl</td><td style="padding:4px 12px;text-align:right;font-weight:bold;white-space:nowrap">9.480,00&ensp;€</td></tr>
            <tr><td style="padding:4px 12px;color:#5a4820">Ersatzlaufrad ø310 mm für Sewabloc F 100-316</td><td style="padding:4px 12px;text-align:right;font-weight:bold;white-space:nowrap">1.457,00&ensp;€</td></tr>
            <tr style="background:#f5f0d8"><td style="padding:4px 12px;color:#5a4820">Ersatzlaufrad ø265 mm für Sewabloc F 100-254</td><td style="padding:4px 12px;text-align:right;font-weight:bold;white-space:nowrap">1.165,00&ensp;€</td></tr>
            <tr><td style="padding:4px 12px;color:#5a4820">Dichtungssatz (Gleitringdichtung, Spaltring, O-Ringe) je Pumpe – empfohlen bei Öffnung</td><td style="padding:4px 12px;text-align:right;font-weight:bold;white-space:nowrap">780,00&ensp;€</td></tr>
          </table>
          <p style="font-size:0.76em;color:#5a4820;margin:6px 0 10px;font-style:italic">Preise netto ab Werk. Montage durch Betreiber.</p>
          <div style="font-size:0.75em;color:#5a4820;letter-spacing:2px;border-top:1px dashed #5a4820;padding-top:8px">ELEKTRO-FACHHANDEL · ANGEBOT ANTRIEBSTECHNIK</div>
          <table style="border-collapse:collapse;font-size:0.85em;color:#1a1a2e;margin-top:4px">
            <tr><td style="padding:4px 12px;color:#5a4820">Frequenzumrichter 15 kW, IP21, EMV-Klasse C2 (Gerät)</td><td style="padding:4px 12px;text-align:right;font-weight:bold;white-space:nowrap">1.650,00&ensp;€</td></tr>
            <tr style="background:#f5f0d8"><td style="padding:4px 12px;color:#5a4820">Frequenzumrichter 4 kW, IP21, EMV-Klasse C2 (Gerät)</td><td style="padding:4px 12px;text-align:right;font-weight:bold;white-space:nowrap">690,00&ensp;€</td></tr>
            <tr><td style="padding:4px 12px;color:#5a4820">Einbaumaterial je FU (Schrankumbau, geschirmte Motorleitung, Schutzorgane)</td><td style="padding:4px 12px;text-align:right;font-weight:bold;white-space:nowrap">1.200,00&ensp;€</td></tr>
          </table>
          <div style="font-size:0.75em;color:#5a4820;letter-spacing:2px;border-top:1px dashed #5a4820;padding-top:8px">ABWASSERBETRIEB · INTERNE RICHTWERTE MONTAGE</div>
          <table style="border-collapse:collapse;font-size:0.85em;color:#1a1a2e;margin-top:4px">
            <tr><td style="padding:4px 12px;color:#5a4820">Stundensatz Monteur (Betriebshandwerker, inkl. Arbeitsplatz- und Gemeinkosten)</td><td style="padding:4px 12px;text-align:right;font-weight:bold;white-space:nowrap">52,00&ensp;€/h</td></tr>
            <tr style="background:#f5f0d8"><td style="padding:4px 12px;color:#5a4820">Austausch Pumpenaggregat (je Standort, 2 Monteure)</td><td style="padding:4px 12px;text-align:right;font-weight:bold;white-space:nowrap">je 32&ensp;h</td></tr>
            <tr><td style="padding:4px 12px;color:#5a4820">Umsetzen einer vorhandenen Pumpe an anderen Standort (2 Monteure)</td><td style="padding:4px 12px;text-align:right;font-weight:bold;white-space:nowrap">je 16&ensp;h</td></tr>
            <tr style="background:#f5f0d8"><td style="padding:4px 12px;color:#5a4820">Laufradwechsel (2 Monteure)</td><td style="padding:4px 12px;text-align:right;font-weight:bold;white-space:nowrap">je 8&ensp;h</td></tr>
            <tr><td style="padding:4px 12px;color:#5a4820">Nachrüstung Frequenzumrichter inkl. Verkabelung (2 Monteure)</td><td style="padding:4px 12px;text-align:right;font-weight:bold;white-space:nowrap">je 8&ensp;h</td></tr>
          </table>
        </div>'''
        kf_tab = mo.vstack([
            mo.Html('''<div class="pls"><div class="pls-c" style="border-color:#0984e3"><h3 style="color:#74b9ff">🔧 Pumpentechnik – Umbauplanung</h3>
                <p style="font-size:0.85em;color:#b2bec3;margin:0">Auswahl der Aggregate an den drei Standorten. Zur Auswahl stehen die Pumpen und
                Laufräder, für die Herstellerkennlinien vorliegen. Nach „Umbau durchführen“ arbeitet die Anlage mit der neuen Ausrüstung –
                Messwerte, Betriebsstunden und Zähler zeigen den neuen Betrieb.</p></div></div>'''),
            mo.Html('<div class="pls"><div class="pls-c"><h3>PW Talstraße – P-001 (Grundlast)</h3></div></div>'),
            mo.hstack([kf_tal, kf_tal_fu, kf_tal_n], justify="start", gap=1.5),
            mo.Html('<div class="pls"><div class="pls-c"><h3>RS-Pumpwerk – P3.1</h3></div></div>'),
            mo.hstack([kf_rs, kf_rs_fu, kf_rs_n], justify="start", gap=1.5),
            mo.Html('<div class="pls"><div class="pls-c"><h3>Faulturm-Umwälzung – P10.1</h3></div></div>'),
            mo.hstack([kf_ft, kf_ft_fu, kf_ft_n], justify="start", gap=1.5),
            mo.hstack([kf_umbau_btn, kf_reset_btn], justify="start", gap=1),
            mo.Html(f'<div class="pls"><div class="pls-c" style="border-color:#fdcb6e;font-size:0.9em">{kf_meldung}</div></div>') if kf_meldung else mo.Html(""),
            mo.Html(f'<div class="pls">{kf_bestand_html}</div>'),
            mo.Html(f'<div class="pls"><div style="max-width:820px">{kf_preis_html}</div></div>'),
        ])

        modifikationen = mo.vstack([
            # Dashboard-Kopf: Investitions-/Betriebskosten-/Energiebilanz bleibt
            # unabhängig vom gewählten Unter-Tab sichtbar.
            mo.Html(f'''<div class="pls">
            <div class="pls-c"><h3>🏗️ Anlagenmodifikationen – Virtueller Umbau</h3>
                <p style="font-size:0.9em;margin:6px 0">
                    Aktiviere Modifikationen um deren Auswirkungen auf Ablaufqualität, Energieverbrauch und
                    Betriebskosten direkt in der Simulation zu sehen. Die Effekte werden sofort in allen Tabs sichtbar.
                </p>
                {vtbl(
                    vr("Aktive Modifikationen", f"{n_aktiv}", "von 10")
                    + vr("Investitionssumme", f"{inv_total:,.0f}", "€")
                    + vr("Zusätzl. Betriebskosten", f"{betr_total:,.0f}", "€/a")
                    + vr("Energieeinsparung Belüftung", f"{e_spar:.0f}", "kWh/d")
                    + vr("Energieerzeugung", f"{e.get('e_erzeugung',0):.0f}", "kWh/d")
                    + vr("Netto-Energieverbrauch", f"{e.get('e_netto',0):.0f}", "kWh/d")
                    + vr("Fällmittelkosten", f"{e.get('fm_kosten',0):.1f}", "€/d")
                )}
            </div>
            </div>'''),

            # Drei Kategorien als Unter-Tabs: Messtechnik / Verfahrenstechnik / Umbauten.
            mo.ui.tabs({
                "🟢 Messtechnik": mo.vstack([
                    mo.Html('<div class="pls"><div class="pls-c" style="border-color:#00b894"><h3 style="color:#00b894">🟢 Messtechnik & Regelungsoptimierung</h3><p style="font-size:0.85em;color:#b2bec3;margin:0">Geringe Investition, schneller Effekt, oft die wirtschaftlichste Maßnahme.</p></div></div>'),
                    mo.hstack([mod_p_online, mod_nh4_sensor, mod_spektral, mod_truebung], justify="start", gap=0.5),
                    mo.Html(f'''<div class="pls"><div class="pls-g2">
                        {mod_card("p_online", mod_p_online)}
                        {mod_card("nh4_sensor", mod_nh4_sensor)}
                    </div><div class="pls-g2">
                        {mod_card("spektral", mod_spektral)}
                        {mod_card("truebung", mod_truebung)}
                    </div></div>'''),
                ]),
                "🔵 Verfahrenstechnik": mo.vstack([
                    mo.Html('<div class="pls"><div class="pls-c" style="border-color:#0984e3"><h3 style="color:#0984e3">🔵 Verfahrenstechnische Erweiterungen</h3><p style="font-size:0.85em;color:#b2bec3;margin:0">Mittlere Investition, erhebliche Betriebsverbesserung.</p></div></div>'),
                    mo.hstack([mod_membran, mod_turbo, mod_intermit, mod_anammox], justify="start", gap=0.5),
                    mo.Html(f'''<div class="pls"><div class="pls-g2">
                        {mod_card("membran", mod_membran)}
                        {mod_card("turbo", mod_turbo)}
                    </div><div class="pls-g2">
                        {mod_card("intermit", mod_intermit)}
                        {mod_card("anammox", mod_anammox)}
                    </div></div>'''),
                ]),
                "🟣 Umbauten": mo.vstack([
                    mo.Html('<div class="pls"><div class="pls-c" style="border-color:#a29bfe"><h3 style="color:#a29bfe">🟣 Größere Umbauten & Neubauten</h3><p style="font-size:0.85em;color:#b2bec3;margin:0">Hohe Investition, transformative Wirkung.</p></div></div>'),
                    mo.hstack([mod_stufe4, mod_pv], justify="start", gap=0.5),
                    mo.Html(f'''<div class="pls"><div class="pls-g2">
                        {mod_card("stufe4", mod_stufe4)}
                        {mod_card("pv", mod_pv)}
                    </div></div>'''),
                ]),
                "🔧 Pumpentechnik": kf_tab,
            }, lazy=True),
        ])

        # ====== LABOR TAB ======
        import plotly.graph_objects as _lgo

        # Seed basierend auf Button-Klicks für Reproduzierbarkeit pro Klick
        _lab_seed = lab_analyse_btn.value * 17 + lab_woche_btn.value * 31 + lab_kal_btn.value * 53
        _rng = np.random.RandomState(max(1, _lab_seed))

        # Wahre Werte aus Simulation
        _true = {
            "CSB": c["csb_ab"], "BSB5": c["bsb_ab"], "NH4": c["nh4_ab"],
            "NO3": c["no3_ab"], "Pges": c["p_ab"], "AFS": c["afs_ab"],
            "pH": c["ph_ab"], "TS": c["ts"], "ISV": c["isv"],
        }

        # ---- 1. VIRTUELLES LABOR: Einzelanalysen ----
        # Analysenmethoden mit realistischer Messpräzision
        METHODEN = {
            "CSB": {"name": "CSB Küvetten-Schnelltest", "norm": "DIN 38409-H41",
                    "methode": "Kaliumdichromat-Aufschluss 148°C / 2h, photometrische Bestimmung bei 620 nm",
                    "geraet": "Hach DR 3900 Photometer + HT 200S Thermostat",
                    "cv": 0.05, "bias": 0.02, "einheit": "mg/L", "probe": "24h-Mischprobe Ablauf NK",
                    "bereich": "10–150 mg/L (LCK 314)", "dauer": "2 h 15 min"},
            "BSB5": {"name": "BSB₅ respirometrisch", "norm": "DIN EN 1899-2",
                     "methode": "Manometrische Messung O₂-Verbrauch über 5 d bei 20°C im Dunkeln, Nitrifikationshemmung mit ATH",
                     "geraet": "WTW OxiTop-i IS 6",
                     "cv": 0.08, "bias": 0.0, "einheit": "mg/L", "probe": "24h-Mischprobe Ablauf NK",
                     "bereich": "0–40 mg/L (Messbereich 6)", "dauer": "5 Tage"},
            "NH4": {"name": "NH₄-N photometrisch", "norm": "DIN 38406-E5",
                    "methode": "Indophenolblau-Methode: NH₄ + Hypochlorit + Salicylat → blauer Farbkomplex, Messung 655 nm",
                    "geraet": "Hach DR 3900 + LCK 304",
                    "cv": 0.06, "bias": 0.01, "einheit": "mg/L", "probe": "Qualifizierte Stichprobe Ablauf NK",
                    "bereich": "0,015–2,0 / 2–47 mg/L", "dauer": "15 min"},
            "Pges": {"name": "P-ges photometrisch", "norm": "DIN EN ISO 6878",
                     "methode": "Aufschluss mit K₂S₂O₈ bei 120°C, Molybdänblau-Methode, Messung 880 nm",
                     "geraet": "Hach DR 3900 + LCK 349/350",
                     "cv": 0.07, "bias": 0.015, "einheit": "mg/L", "probe": "24h-Mischprobe Ablauf NK",
                     "bereich": "0,05–1,50 / 1,0–10,0 mg/L", "dauer": "30 min + 30 min Aufschluss"},
            "AFS": {"name": "Abfiltrierbare Stoffe", "norm": "DIN 38409-H2",
                    "methode": "Filtration über Glasfaserfilter (0,45 µm), Trocknung 105°C / 2h, Differenzwägung",
                    "geraet": "Sartorius Analysenwaage + Trockenschrank",
                    "cv": 0.10, "bias": 0.0, "einheit": "mg/L", "probe": "24h-Mischprobe Ablauf NK",
                    "bereich": "ab 2 mg/L", "dauer": "3–4 h"},
            "pH": {"name": "pH-Wert", "norm": "DIN 38404-C5",
                   "methode": "Potentiometrisch mit Glaselektrode, Zweipunktkalibrierung pH 4,01 / 7,00",
                   "geraet": "WTW pH 3310 + SenTix 41",
                   "cv": 0.005, "bias": 0.0, "einheit": "", "probe": "Stichprobe, sofort messen",
                   "bereich": "0–14", "dauer": "2 min"},
            "TS": {"name": "Trockensubstanz Belebung", "norm": "DIN 38414-S2",
                   "methode": "Eindampfen bei 105°C bis Gewichtskonstanz, Differenzwägung. oTS zusätzlich bei 550°C (Glühverlust).",
                   "geraet": "Sartorius Analysenwaage + Muffelofen",
                   "cv": 0.03, "bias": 0.0, "einheit": "g/L", "probe": "Stichprobe Belebungsbecken",
                   "bereich": "ab 0,1 g/L", "dauer": "4–6 h (105°C) + 2 h (550°C)"},
        }

        # Messwerte simulieren (Doppelbestimmung)
        def sim_analyse(param):
            m = METHODEN[param]
            true_val = _true[param]
            mess1 = true_val * (1 + m["bias"]) + _rng.normal(0, true_val * m["cv"])
            mess2 = true_val * (1 + m["bias"]) + _rng.normal(0, true_val * m["cv"])
            return max(0, mess1), max(0, mess2)

        # Einzelanalyse-Ergebnisse
        analysen_html = ""
        if lab_analyse_btn.value > 0:
            analysen_rows = ""
            for param in ["CSB", "BSB5", "NH4", "Pges", "AFS", "pH", "TS"]:
                m = METHODEN[param]
                v1, v2 = sim_analyse(param)
                mw = (v1 + v2) / 2
                diff_pct = abs(v1 - v2) / max(0.001, mw) * 100
                akzeptanz = "✅" if diff_pct < (m["cv"] * 100 * 2.8) else "⚠️ wiederholen"
                fmt = ".2f" if param in ["Pges", "pH", "TS"] else ".1f"
                analysen_rows += f'''<tr style="border-bottom:1px solid #0f3460">
                    <td style="padding:5px 12px;font-weight:bold;color:#74b9ff">{m["name"]}</td>
                    <td style="padding:5px 12px;text-align:right">{v1:{fmt}} {m["einheit"]}</td>
                    <td style="padding:5px 12px;text-align:right">{v2:{fmt}} {m["einheit"]}</td>
                    <td style="padding:5px 12px;text-align:right;font-weight:bold;color:#74b9ff">{mw:{fmt}} {m["einheit"]}</td>
                    <td style="padding:5px 12px;text-align:center">{diff_pct:.1f}%</td>
                    <td style="padding:5px 12px;text-align:center">{akzeptanz}</td>
                </tr>'''

            analysen_html = f'''<div class="pls-c" style="border-color:#00b894">
                <h3 style="color:#00b894">🧪 Analysenergebnisse (Probenahme #{lab_analyse_btn.value})</h3>
                <p style="font-size:0.8em;color:#b2bec3;margin:2px 0 8px">Doppelbestimmung – Akzeptanz nach Variationskoeffizient der Methode × 2,8 (95%-Vertrauensintervall)</p>
                <table style="width:100%;border-collapse:collapse;font-size:0.85em;color:#ffffff;background:#16213e">
                    <tr style="background:#0f1a30;border-bottom:2px solid #0f3460">
                        <th style="padding:6px 12px;color:#74b9ff;text-align:left">Analyse</th>
                        <th style="padding:6px 12px;color:#74b9ff;text-align:right">Messung 1</th>
                        <th style="padding:6px 12px;color:#74b9ff;text-align:right">Messung 2</th>
                        <th style="padding:6px 12px;color:#74b9ff;text-align:right">Mittelwert</th>
                        <th style="padding:6px 12px;color:#74b9ff;text-align:center">Δ rel.</th>
                        <th style="padding:6px 12px;color:#74b9ff;text-align:center">Akzeptanz</th>
                    </tr>
                    {analysen_rows}
                </table>
            </div>'''

        # Methodensteckbriefe
        methoden_cards = ""
        for param in ["CSB", "BSB5", "NH4", "Pges", "AFS", "pH", "TS"]:
            m = METHODEN[param]
            methoden_cards += f'''<div class="pls-c">
                <h3>{m["name"]}</h3>
                {vtbl(
                    vr("Norm", m["norm"], "")
                    + vr("Gerät", m["geraet"], "")
                    + vr("Messbereich", m["bereich"], "")
                    + vr("Dauer", m["dauer"], "")
                    + vr("Probe", m["probe"], "")
                    + vr("VK (Präzision)", f"{m['cv']*100:.0f}", "%")
                )}
                <p style="font-size:0.8em;color:#b2bec3;margin:4px 0 0">{m["methode"]}</p>
            </div>'''

        # ---- 2. ISV-ABSETZVERSUCH (visuell) ----
        isv_panel = mo.Html("")
        if lab_show_isv.value:
            isv_val = c["isv"]
            ts_val = c["ts"]
            # Absetzzeiten simulieren
            t_min = np.array([0, 1, 2, 3, 5, 7, 10, 15, 20, 25, 30])
            # Absetzkurve: Exponentiell, beeinflusst durch ISV
            h_start = 1000  # mL Messzylinder
            h_end = ts_val * isv_val  # mL/L * g/L → mL Volumen
            tau_isv = 5 + (isv_val - 80) * 0.05  # höherer ISV → langsameres Absetzen
            h_schlammsp = h_start - (h_start - h_end) * (1 - np.exp(-t_min / tau_isv))

            fig_isv = _lgo.Figure()
            fig_isv.add_trace(_lgo.Scatter(x=t_min, y=h_schlammsp, mode='lines+markers',
                line=dict(color='#e17055', width=2.5), marker=dict(size=6, color='#e17055'),
                name='Schlammspiegelstand', fill='tozeroy', fillcolor='rgba(165,94,60,0.2)'))
            fig_isv.add_hline(y=h_end, line_dash="dot", line_color="#fdcb6e",
                annotation_text=f"ISV = {isv_val:.0f} mL/g", annotation_font_color="#fdcb6e")
            fig_isv.update_layout(height=350, template="plotly_dark",
                paper_bgcolor="#1a1a2e", plot_bgcolor="#16213e",
                xaxis_title="Zeit [min]", yaxis_title="Schlammspiegelstand [mL/L]",
                yaxis=dict(range=[0, 1050]),
                showlegend=False,
                font=dict(family="Consolas,monospace", size=11, color="#dfe6e9"),
                margin=dict(t=20, b=40, l=60, r=20))
            fig_isv.update_xaxes(gridcolor="#0f3460")
            fig_isv.update_yaxes(gridcolor="#0f3460")

            isv_beurt = "gut" if isv_val < 100 else ("mäßig" if isv_val < 150 else "schlecht – Blähschlammgefahr!")
            isv_color = "#00b894" if isv_val < 100 else ("#fdcb6e" if isv_val < 150 else "#e17055")

            isv_panel = mo.vstack([
                mo.Html(f'''<div class="pls"><div class="pls-c" style="border-color:#e17055">
                    <h3 style="color:#e17055">🔬 ISV-Absetzversuch (30 min, 1L-Messzylinder)</h3>
                    {vtbl(
                        vr("TS Belebung", f"{ts_val:.2f}", "g/L")
                        + vr("Schlammvolumen (30 min)", f"{h_end:.0f}", "mL/L")
                        + vr("ISV = SV/TS", f"{isv_val:.0f}", "mL/g")
                        + vr("Beurteilung", f'<span style="color:{isv_color}">{isv_beurt}</span>', "")
                    )}
                    <p style="font-size:0.8em;color:#b2bec3;margin:6px 0 0">
                        Durchführung: 1 L Belebtschlamm in Messzylinder füllen, Schlammspiegelstand
                        nach 0, 1, 2, 3, 5, 7, 10, 15, 20, 25 und 30 Minuten ablesen.
                        ISV = Schlammvolumen nach 30 min / TS-Gehalt. Richtwert: &lt;100 mL/g gut,
                        100–150 mL/g mäßig, &gt;150 mL/g Blähschlammgefahr.
                    </p>
                </div></div>'''),
                fig_isv,
            ])

        # ---- 3. EIGENÜBERWACHUNG WOCHENBERICHT ----
        proto_panel = mo.Html("")
        if lab_show_proto.value:
            _rng2 = np.random.RandomState(max(1, lab_woche_btn.value * 7 + 42))
            # 5 Messungen pro Woche (Mo, Di, Mi, Do, Fr)
            tage_w = ["Mo", "Di", "Mi", "Do", "Fr"]
            # Parameter mit Grenzwerten nach AbwV Anhang 1 (GK 4, 50.000 EW)
            GW = {"CSB": 75, "BSB5": 15, "NH4": 10, "Nges": 18, "Pges": 1.0}
            true_w = {"CSB": c["csb_ab"], "BSB5": c["bsb_ab"], "NH4": c["nh4_ab"],
                      "Nges": c["n_ab"], "Pges": c["p_ab"]}

            wochendaten = {}
            for p in GW:
                cv = {"CSB": 0.08, "BSB5": 0.12, "NH4": 0.10, "Nges": 0.09, "Pges": 0.10}[p]
                wochendaten[p] = [max(0.1, true_w[p] + _rng2.normal(0, true_w[p] * cv)) for _ in range(5)]

            # 2-aus-5-Regel prüfen
            def pruefe_2aus5(werte, gw):
                ueber = sum(1 for w in werte if w > gw)
                return ueber

            proto_rows = ""
            gesamt_ok = True
            for p in GW:
                werte = wochendaten[p]
                mw = np.mean(werte)
                std = np.std(werte, ddof=1)
                n_ueber = pruefe_2aus5(werte, GW[p])
                ok = n_ueber < 2
                if not ok:
                    gesamt_ok = False
                status = '<span style="color:#00b894">✅ eingehalten</span>' if ok else '<span style="color:#e17055">❌ überschritten</span>'
                fmt = ".2f" if p == "Pges" else ".1f"
                werte_str = " | ".join([f"{w:{fmt}}" for w in werte])
                proto_rows += f'''<tr style="border-bottom:1px solid #0f3460">
                    <td style="padding:5px 12px;font-weight:bold">{p}</td>
                    <td style="padding:5px 12px;text-align:center;font-size:0.85em">{werte_str}</td>
                    <td style="padding:5px 12px;text-align:right">{mw:{fmt}}</td>
                    <td style="padding:5px 12px;text-align:right">{std:{fmt}}</td>
                    <td style="padding:5px 12px;text-align:center;font-weight:bold">{GW[p]}</td>
                    <td style="padding:5px 12px;text-align:center">{n_ueber}/5</td>
                    <td style="padding:5px 12px;text-align:center">{status}</td>
                </tr>'''

            gesamt_status = '<span style="color:#00b894;font-size:1.1em">✅ Alle Überwachungswerte eingehalten</span>' if gesamt_ok else '<span style="color:#e17055;font-size:1.1em">❌ Grenzwertüberschreitung – Maßnahmen erforderlich!</span>'

            proto_panel = mo.vstack([
                mo.Html(f'''<div class="pls"><div class="pls-c" style="border-color:#74b9ff">
                    <h3 style="color:#74b9ff">📋 Eigenüberwachung – Wochenbericht #{max(1, lab_woche_btn.value)}</h3>
                    <p style="font-size:0.85em;margin:4px 0">{gesamt_status}</p>
                    <p style="font-size:0.8em;color:#b2bec3;margin:2px 0 8px">
                        Bewertung nach <strong>SüwVO Abw NRW, 2-aus-5-Regel</strong>: Ein Überwachungswert gilt als
                        überschritten, wenn in 5 aufeinanderfolgenden Messungen 2 oder mehr über dem Grenzwert liegen.
                        Probenahme: 24h-Mischprobe (mengenproportional) am Ablauf NK, Analysen im Betriebslabor.
                    </p>
                    <table style="width:100%;border-collapse:collapse;font-size:0.85em;color:#ffffff;background:#16213e">
                        <tr style="background:#0f1a30;border-bottom:2px solid #0f3460">
                            <th style="padding:6px 12px;color:#74b9ff;text-align:left">Parameter</th>
                            <th style="padding:6px 12px;color:#74b9ff;text-align:center">Mo | Di | Mi | Do | Fr</th>
                            <th style="padding:6px 12px;color:#74b9ff;text-align:right">x̄</th>
                            <th style="padding:6px 12px;color:#74b9ff;text-align:right">s</th>
                            <th style="padding:6px 12px;color:#74b9ff;text-align:center">GW</th>
                            <th style="padding:6px 12px;color:#74b9ff;text-align:center">n &gt; GW</th>
                            <th style="padding:6px 12px;color:#74b9ff;text-align:center">2/5-Regel</th>
                        </tr>
                        {proto_rows}
                    </table>
                </div></div>'''),
                mo.Html(f'''<div class="pls"><div class="pls-c">
                    <h3>📅 Probenahmeplan (GK 4, 50.000 EW)</h3>
                    <table style="width:100%;border-collapse:collapse;font-size:0.85em;color:#ffffff;background:#16213e">
                        <tr style="background:#0f1a30;border-bottom:2px solid #0f3460">
                            <th style="padding:6px 12px;color:#74b9ff;text-align:left">Parameter</th>
                            <th style="padding:6px 12px;color:#74b9ff;text-align:left">Häufigkeit</th>
                            <th style="padding:6px 12px;color:#74b9ff;text-align:left">Probenahmeart</th>
                            <th style="padding:6px 12px;color:#74b9ff;text-align:left">Probenahmeort</th>
                        </tr>
                        <tr style="border-bottom:1px solid #0f3460"><td style="padding:5px 12px">CSB</td><td style="padding:5px 12px">2×/Woche</td><td style="padding:5px 12px">24h-MP (mengenproportional)</td><td style="padding:5px 12px">Ablauf NK</td></tr>
                        <tr style="border-bottom:1px solid #0f3460"><td style="padding:5px 12px">BSB₅</td><td style="padding:5px 12px">2×/Woche</td><td style="padding:5px 12px">24h-MP (mengenproportional)</td><td style="padding:5px 12px">Ablauf NK</td></tr>
                        <tr style="border-bottom:1px solid #0f3460"><td style="padding:5px 12px">NH₄-N</td><td style="padding:5px 12px">2×/Woche</td><td style="padding:5px 12px">qual. Stichprobe</td><td style="padding:5px 12px">Ablauf NK</td></tr>
                        <tr style="border-bottom:1px solid #0f3460"><td style="padding:5px 12px">N-ges</td><td style="padding:5px 12px">2×/Woche</td><td style="padding:5px 12px">24h-MP (mengenproportional)</td><td style="padding:5px 12px">Ablauf NK</td></tr>
                        <tr style="border-bottom:1px solid #0f3460"><td style="padding:5px 12px">P-ges</td><td style="padding:5px 12px">2×/Woche</td><td style="padding:5px 12px">24h-MP (mengenproportional)</td><td style="padding:5px 12px">Ablauf NK</td></tr>
                        <tr style="border-bottom:1px solid #0f3460"><td style="padding:5px 12px">pH, T</td><td style="padding:5px 12px">täglich</td><td style="padding:5px 12px">Stichprobe</td><td style="padding:5px 12px">Zulauf + Ablauf</td></tr>
                        <tr style="border-bottom:1px solid #0f3460"><td style="padding:5px 12px">AFS</td><td style="padding:5px 12px">2×/Woche</td><td style="padding:5px 12px">24h-MP (mengenproportional)</td><td style="padding:5px 12px">Ablauf NK</td></tr>
                        <tr style="border-bottom:1px solid #0f3460"><td style="padding:5px 12px">TS, ISV</td><td style="padding:5px 12px">täglich</td><td style="padding:5px 12px">Stichprobe</td><td style="padding:5px 12px">Belebungsbecken</td></tr>
                        <tr style="border-bottom:1px solid #0f3460"><td style="padding:5px 12px">Schlammsp.</td><td style="padding:5px 12px">täglich</td><td style="padding:5px 12px">Sichtprüfung</td><td style="padding:5px 12px">Nachklärbecken</td></tr>
                    </table>
                </div></div>'''),
            ])

        # ---- 4. QS: KALIBRIERUNG & FEHLERSUCHE ----
        qs_panel = mo.Html("")
        if lab_show_qs.value:
            _rng3 = np.random.RandomState(max(1, lab_kal_btn.value * 13 + 99))

            # Kalibriergerade NH₄-N (photometrisch)
            kal_konz = np.array([0, 2, 5, 10, 20, 40])
            eps_nh4 = 0.032  # Extinktionskoeffizient
            kal_ext_ideal = kal_konz * eps_nh4
            kal_ext = kal_ext_ideal + _rng3.normal(0, 0.008, len(kal_konz))
            kal_ext[0] = max(0, 0.005 + _rng3.normal(0, 0.003))  # Blindwert

            # Lineare Regression
            _zk = np.polyfit(kal_konz[1:], kal_ext[1:], 1)
            _r2 = 1 - np.sum((kal_ext[1:] - np.polyval(_zk, kal_konz[1:])) ** 2) / np.sum((kal_ext[1:] - np.mean(kal_ext[1:])) ** 2)

            fig_kal = _lgo.Figure()
            fig_kal.add_trace(_lgo.Scatter(x=kal_konz, y=kal_ext, mode='markers',
                marker=dict(size=10, color='#0984e3'), name='Messwerte'))
            x_fit = np.linspace(0, 45, 100)
            fig_kal.add_trace(_lgo.Scatter(x=x_fit, y=np.polyval(_zk, x_fit), mode='lines',
                line=dict(color='#fdcb6e', width=2, dash='dash'), name='Regression'))
            fig_kal.update_layout(height=350, template="plotly_dark",
                paper_bgcolor="#1a1a2e", plot_bgcolor="#16213e",
                xaxis_title="Konzentration NH₄-N [mg/L]",
                yaxis_title="Extinktion [-]",
                showlegend=True,
                legend=dict(x=0.02, y=0.98),
                font=dict(family="Consolas,monospace", size=11, color="#dfe6e9"),
                margin=dict(t=20, b=45, l=60, r=20))
            fig_kal.update_xaxes(gridcolor="#0f3460")
            fig_kal.update_yaxes(gridcolor="#0f3460")

            # Aufstockungsversuch (Wiederfindung)
            spike_soll = 10.0  # mg/L NH₄-N aufgestockt
            probe_wert = _true["NH4"] + _rng3.normal(0, _true["NH4"] * 0.06)
            probe_spike = probe_wert + spike_soll * (1 + _rng3.normal(0, 0.04))
            wiederfindung = (probe_spike - probe_wert) / spike_soll * 100

            # Fehlerhafte Messwerte identifizieren (5 Messungen, davon 1 Ausreißer)
            fehler_messungen = [
                _true["CSB"] * (1 + _rng3.normal(0, 0.05)),
                _true["CSB"] * (1 + _rng3.normal(0, 0.05)),
                _true["CSB"] * (1 + _rng3.normal(0, 0.05)),
                _true["CSB"] * 1.8 + _rng3.normal(0, 2),  # Ausreißer!
                _true["CSB"] * (1 + _rng3.normal(0, 0.05)),
            ]
            fm_mw = np.mean(fehler_messungen)
            fm_std = np.std(fehler_messungen, ddof=1)
            # Grubbs-Test vereinfacht
            fm_ausreisser = [i for i, v in enumerate(fehler_messungen) if abs(v - fm_mw) > 2 * fm_std]

            fehler_rows = ""
            for i, v in enumerate(fehler_messungen):
                is_out = i in fm_ausreisser
                c_str = 'color:#e17055;font-weight:bold' if is_out else ''
                mark = ' ⚠️ Ausreißer!' if is_out else ''
                fehler_rows += f'<tr style="border-bottom:1px solid #0f3460"><td style="padding:5px 12px">Messung {i+1}</td><td style="padding:5px 12px;text-align:right;{c_str}">{v:.1f} mg/L{mark}</td></tr>'

            qs_panel = mo.vstack([
                mo.Html(f'''<div class="pls"><div class="pls-c" style="border-color:#a29bfe">
                    <h3 style="color:#a29bfe">📈 Kalibrierung – NH₄-N Photometrie (Indophenolblau)</h3>
                    <p style="font-size:0.85em;margin:4px 0 8px">
                        6-Punkt-Kalibrierung mit Standardlösungen (0 / 2 / 5 / 10 / 20 / 40 mg/L NH₄-N).
                        Lambert-Beer: E = ε · c · d (ε = Extinktionskoeffizient, d = Schichtdicke).
                    </p>
                    {vtbl(
                        vr("Steigung ε", f"{_zk[0]:.4f}", "L/(mg·cm)")
                        + vr("Achsenabschnitt", f"{_zk[1]:.4f}", "")
                        + vr("Bestimmtheitsmaß R²", f"{_r2:.5f}", "", wl=0.995)
                        + vr("Blindwert E₀", f"{kal_ext[0]:.4f}", "")
                    )}
                    <p style="font-size:0.8em;color:#b2bec3;margin:4px 0">
                        R² muss &gt; 0,995 sein für eine gültige Kalibrierung. Blindwert &lt; 0,010 erforderlich.
                    </p>
                </div></div>'''),
                fig_kal,
                mo.Html(f'''<div class="pls"><div class="pls-g2">
                    <div class="pls-c" style="border-color:#00b894">
                        <h3 style="color:#00b894">🔄 Aufstockungsversuch (Wiederfindung)</h3>
                        <p style="font-size:0.85em;margin:4px 0 8px">
                            Probe + bekannte Menge Standard → Wiederfindung prüft systematische Fehler.
                        </p>
                        {vtbl(
                            vr("Probenwert", f"{probe_wert:.1f}", "mg/L NH₄-N")
                            + vr("Aufstockung", f"{spike_soll:.1f}", "mg/L")
                            + vr("Probe + Spike", f"{probe_spike:.1f}", "mg/L")
                            + vr("Wiederfindung", f"{wiederfindung:.1f}", "%", wl=90, dl=80, wh=110, dh=120)
                        )}
                        <p style="font-size:0.8em;color:#b2bec3;margin:4px 0">
                            Akzeptanzbereich: 90–110%. Außerhalb → Matrixeffekte oder Methodenfehler prüfen.
                        </p>
                    </div>
                    <div class="pls-c" style="border-color:#e17055">
                        <h3 style="color:#e17055">🔍 Ausreißertest – CSB 5-fach-Bestimmung</h3>
                        <p style="font-size:0.85em;margin:4px 0 8px">
                            Identifiziere den fehlerhaften Messwert! (Grubbs-Test: |xi − x̄| &gt; 2·s)
                        </p>
                        <table style="width:100%;border-collapse:collapse;font-size:0.88em;color:#fff;background:#16213e">
                            {fehler_rows}
                            <tr style="border-top:2px solid #0f3460">
                                <td style="padding:5px 12px;font-weight:bold;color:#74b9ff">Mittelwert x̄</td>
                                <td style="padding:5px 12px;text-align:right;font-weight:bold;color:#74b9ff">{fm_mw:.1f} mg/L</td>
                            </tr>
                            <tr><td style="padding:5px 12px;color:#74b9ff">Standardabw. s</td>
                                <td style="padding:5px 12px;text-align:right;color:#74b9ff">{fm_std:.1f} mg/L</td></tr>
                        </table>
                        <p style="font-size:0.8em;color:#b2bec3;margin:4px 0">
                            Mögliche Ursachen für Ausreißer: Verschmutzte Küvette, falsches Reagenz,
                            Probe nicht homogenisiert, Verdünnungsfehler, Gerät nicht kalibriert.
                        </p>
                    </div>
                </div></div>'''),
            ])

        # === LABOR TAB ZUSAMMENBAUEN ===
        labor = mo.vstack([
            # Header bleibt über den Unter-Tabs sichtbar.
            mo.Html(f'''<div class="pls"><div class="pls-c">
                <h3>🔬 Betriebslabor – Analysentechnik & Qualitätssicherung</h3>
                <p style="font-size:0.9em;margin:6px 0">
                    Das Betriebslabor führt die Eigenüberwachung nach SüwVO Abw NRW durch.
                    Hier können Analysen simuliert, Messprotokolle ausgewertet und die
                    Qualitätssicherung geprüft werden. Alle Messwerte basieren auf den
                    aktuellen Simulationsdaten der Kläranlage.
                </p>
            </div></div>'''),

            # Vier Arbeitsbereiche als Unter-Tabs.
            mo.ui.tabs({
                "🧪 Analytik": mo.vstack([
                    # Analysen-Bereich
                    mo.Html('<div class="pls"><div class="pls-c" style="border-color:#00b894"><h3 style="color:#00b894">🧪 Probenahme & Analyse</h3><p style="font-size:0.85em;color:#b2bec3;margin:0">Führe eine virtuelle Probenahme mit Doppelbestimmung durch. Jeder Klick = neue Probe mit realistischer Messstreuung.</p></div></div>'),
                    mo.hstack([lab_analyse_btn], justify="start"),
                    mo.Html(f'<div class="pls">{analysen_html}</div>') if analysen_html else mo.Html(""),

                    # Methodensteckbriefe
                    mo.Html(f'''<div class="pls"><div class="pls-c"><h3>📖 Analysenmethoden (Steckbriefe)</h3></div>
                    <div class="pls-g3">{methoden_cards}</div></div>'''),
                ]),
                "🔬 Schlammanalytik": mo.vstack([
                    mo.Html('<div class="pls"><div class="pls-c" style="border-color:#e17055"><h3 style="color:#e17055">🔬 Schlammanalytik</h3><p style="font-size:0.85em;color:#b2bec3;margin:0">ISV-Absetzversuch nach DIN 38414 – Kenngröße für Schlammeigenschaften und Blähschlammgefahr.</p></div></div>'),
                    lab_show_isv,
                    isv_panel,
                ]),
                "📋 Eigenüberwachung": mo.vstack([
                    mo.Html('<div class="pls"><div class="pls-c" style="border-color:#74b9ff"><h3 style="color:#74b9ff">📋 Eigenüberwachung & Probenahmeplan</h3><p style="font-size:0.85em;color:#b2bec3;margin:0">Wochenbericht nach SüwVO Abw NRW mit Probenahmeplan, Analysenergebnissen und Grenzwertkontrolle.</p></div></div>'),
                    mo.hstack([lab_show_proto, lab_woche_btn], justify="start", gap=1),
                    proto_panel,
                ]),
                "📈 Qualitätssicherung": mo.vstack([
                    mo.Html('<div class="pls"><div class="pls-c" style="border-color:#a29bfe"><h3 style="color:#a29bfe">📈 Qualitätssicherung</h3><p style="font-size:0.85em;color:#b2bec3;margin:0">Kalibrierung, Kontrollkarten und Fehlersuche bei Analysenmethoden.</p></div></div>'),
                    mo.hstack([lab_show_qs, lab_kal_btn], justify="start", gap=1),
                    qs_panel,
                ]),
            }, lazy=True),
        ])

        # === FLIESSSCHEMA TAB ===
        fliessschema = mo.Html('''<div style="background:#f0f4f8; border-radius:8px; padding:10px; overflow:auto;">
<style>
  .p-aw   { stroke:#1e90e8; stroke-width:3;   fill:none; }
  .p-rs   { stroke:#c07828; stroke-width:2.2; fill:none; stroke-dasharray:9,4; }
  .p-ues  { stroke:#c89030; stroke-width:1.8; fill:none; stroke-dasharray:5,4; }
  .p-luft { stroke:#c8a020; stroke-width:2;   fill:none; stroke-dasharray:8,3; }
  .p-fm   { stroke:#9050c8; stroke-width:1.6; fill:none; stroke-dasharray:4,3; }
  .p-ab   { stroke:#18c870; stroke-width:3;   fill:none; }
  .p-abs  { stroke:#e03848; stroke-width:2;   fill:none; stroke-dasharray:7,3; }
  .p-sig  { stroke:#486880; stroke-width:0.9; fill:none; stroke-dasharray:3,3; }
  .p-ir   { stroke:#9050d8; stroke-width:1.8; fill:none; stroke-dasharray:6,3; }
</style>
<svg viewBox="0 0 1600 950" xmlns="http://www.w3.org/2000/svg">
<defs>
  <marker id="aaw"  markerWidth="7" markerHeight="5" refX="6" refY="2.5" orient="auto"><polygon points="0 0,7 2.5,0 5" fill="#1e90e8"/></marker>
  <marker id="ars"  markerWidth="7" markerHeight="5" refX="6" refY="2.5" orient="auto"><polygon points="0 0,7 2.5,0 5" fill="#8a5010"/></marker>
  <marker id="aues" markerWidth="7" markerHeight="5" refX="6" refY="2.5" orient="auto"><polygon points="0 0,7 2.5,0 5" fill="#c89030"/></marker>
  <marker id="aluft"markerWidth="7" markerHeight="5" refX="6" refY="2.5" orient="auto"><polygon points="0 0,7 2.5,0 5" fill="#c8a020"/></marker>
  <marker id="afm"  markerWidth="7" markerHeight="5" refX="6" refY="2.5" orient="auto"><polygon points="0 0,7 2.5,0 5" fill="#9050c8"/></marker>
  <marker id="aab"  markerWidth="7" markerHeight="5" refX="6" refY="2.5" orient="auto"><polygon points="0 0,7 2.5,0 5" fill="#18c870"/></marker>
  <marker id="aabs" markerWidth="7" markerHeight="5" refX="6" refY="2.5" orient="auto"><polygon points="0 0,7 2.5,0 5" fill="#e03848"/></marker>
  <marker id="air"  markerWidth="7" markerHeight="5" refX="6" refY="2.5" orient="auto"><polygon points="0 0,7 2.5,0 5" fill="#9050d8"/></marker>
</defs>

<!-- HINTERGRUND -->
<rect width="1600" height="950" fill="#f0f4f8"/>

<!-- TITELBLOCK -->
<rect x="5" y="4" width="1590" height="42" rx="3" fill="#ffffff" stroke="#1e3050" stroke-width="1.2"/>
<text x="16" y="22" fill="#0c4fa0" font-size="13.5" font-weight="bold">R&amp;I-FLIESSSCHEMA – KLÄRANLAGE MUSTERSTADT</text>
<text x="16" y="37" fill="#1a3050" font-size="8.5">Mechanisch-Biologische Reinigung mit N/P-Elimination und Schlammfaulung | 50.000 EW | Q_TW = 12.000 m³/d | Q_max = 30.000 m³/d | angelehnt an DIN EN ISO 10628-2</text>
<text x="1588" y="22" fill="#1a3050" font-size="8" text-anchor="end">2026-09 | Rev.02</text>

<!-- STUFENRAHMEN -->
<rect x="6"   y="52" width="430" height="390" rx="4" fill="#edf2f8" stroke="#1a3050" stroke-width="1" stroke-dasharray="7,4"/>
<text x="221" y="65" text-anchor="middle" fill="#0e2040" font-size="8.5" letter-spacing="2">MECHANISCHE REINIGUNGSSTUFE</text>
<rect x="440" y="52" width="355" height="390" rx="4" fill="#edf7f0" stroke="#1a4828" stroke-width="1" stroke-dasharray="7,4"/>
<text x="617" y="65" text-anchor="middle" fill="#1a4028" font-size="8.5" letter-spacing="2">BIOLOGISCHE STUFE</text>
<rect x="799" y="52" width="195" height="390" rx="4" fill="#fdf8ee" stroke="#604c10" stroke-width="1" stroke-dasharray="7,4"/>
<text x="896" y="65" text-anchor="middle" fill="#403808" font-size="8.5" letter-spacing="2">NACHKLÄRUNG</text>
<rect x="998" y="52" width="225" height="390" rx="4" fill="#edf8f3" stroke="#184828" stroke-width="1" stroke-dasharray="7,4"/>
<text x="1110" y="65" text-anchor="middle" fill="#1a4830" font-size="8.5" letter-spacing="2">ABLAUF / MESSSCHACHT</text>

<!-- ═══ KANALZULAUF (offenes Gerinne) ═══ -->
<line x1="6"  y1="240" x2="6"  y2="350" stroke="#1e5080" stroke-width="2"/>
<line x1="6"  y1="350" x2="36" y2="350" stroke="#1e5080" stroke-width="2"/>
<line x1="36" y1="240" x2="36" y2="280" stroke="#1e5080" stroke-width="2"/>
<rect x="7" y="290" width="28" height="59" fill="#cce0f5" fill-opacity="0.5"/>
<text x="21" y="276" text-anchor="middle" fill="#1050a0" font-size="8">Kanal-</text>
<text x="21" y="286" text-anchor="middle" fill="#1050a0" font-size="8">zulauf</text>
<!-- FI 101 -->
<circle cx="21" cy="254" r="10" fill="#ffffff" stroke="#3a6090" stroke-width="1.2"/>
<text x="21" y="252" text-anchor="middle" fill="#1050a0" font-size="7">FI</text>
<text x="21" y="260" text-anchor="middle" fill="#1a3050" font-size="6">101</text>
<line class="p-sig" x1="21" y1="264" x2="21" y2="278"/>
<!-- QI 102 Spektralsonde -->
<circle cx="21" cy="234" r="10" fill="#ffffff" stroke="#3a6090" stroke-width="1.2"/>
<text x="21" y="232" text-anchor="middle" fill="#1050a0" font-size="7">QI</text>
<text x="21" y="240" text-anchor="middle" fill="#1a3050" font-size="6">102</text>
<line class="p-aw" x1="36" y1="280" x2="48" y2="280" marker-end="url(#aaw)"/>

<!-- ═══ HEBEWERK ═══ -->
<rect x="48" y="168" width="150" height="232" rx="3" fill="#f7f9fc" stroke="#1a3060" stroke-width="1.5"/>
<text x="123" y="182" text-anchor="middle" fill="#1840a0" font-size="9.5" font-weight="bold">HEBEWERK</text>
<text x="123" y="193" text-anchor="middle" fill="#0e2040" font-size="8">Zulaufpumpwerk</text>
<rect x="56" y="228" width="134" height="162" rx="2" fill="#eef3fa" stroke="#1a3050" stroke-width="1"/>
<rect x="57" y="298" width="132" height="91" fill="#cce0f540"/>
<text x="123" y="278" text-anchor="middle" fill="#0a2848" font-size="8">Nassschacht</text>
<!-- LI 103 -->
<circle cx="202" cy="310" r="10" fill="#ffffff" stroke="#3a6090" stroke-width="1.2"/>
<text x="202" y="308" text-anchor="middle" fill="#1050a0" font-size="7">LI</text>
<text x="202" y="316" text-anchor="middle" fill="#1a3050" font-size="6">103</text>
<line class="p-sig" x1="192" y1="310" x2="183" y2="310"/>

<!-- P1.1 Kreiselpumpe: cx=90, cy=355, r=12 -->
<circle cx="90" cy="355" r="12" fill="#ffffff" stroke="#3a80c0" stroke-width="1.6"/>
<path d="M 83,348 L 101,355 L 83,362 Z" fill="#3a80c0"/>
<line x1="90" y1="343" x2="90" y2="330" stroke="#385870" stroke-width="1.5"/>
<rect x="83" y="321" width="14" height="10" rx="1.5" fill="#e8edf8" stroke="#203050" stroke-width="1"/>
<text x="90" y="328" text-anchor="middle" fill="#304060" font-size="6.5">M</text>
<text x="90" y="375" text-anchor="middle" fill="#3a80c0" font-size="7.5">P1.1</text>
<text x="90" y="384" text-anchor="middle" fill="#1e3858" font-size="7">Betr./FU</text>

<!-- P1.2: cx=148 -->
<circle cx="148" cy="355" r="12" fill="#ffffff" stroke="#3a80c0" stroke-width="1.6"/>
<path d="M 141,348 L 159,355 L 141,362 Z" fill="#3a80c0"/>
<line x1="148" y1="343" x2="148" y2="330" stroke="#385870" stroke-width="1.5"/>
<rect x="141" y="321" width="14" height="10" rx="1.5" fill="#e8edf8" stroke="#203050" stroke-width="1"/>
<text x="148" y="328" text-anchor="middle" fill="#304060" font-size="6.5">M</text>
<text x="148" y="375" text-anchor="middle" fill="#3a80c0" font-size="7.5">P1.2</text>
<text x="148" y="384" text-anchor="middle" fill="#1e3858" font-size="7">Reserve</text>

<!-- Rückschlagventile (RV) vertikal, Förderrichtung ↑ -->
<!-- RV P1.1: Dreieck Spitze nach oben + Sperrlinie oben -->
<polygon points="82,310 98,300 82,290" fill="none" stroke="#8090a0" stroke-width="1.5"/>
<line x1="82" y1="289" x2="82" y2="311" stroke="#8090a0" stroke-width="2"/>
<line x1="90" y1="311" x2="90" y2="330" stroke="#7080a0" stroke-width="1"/>
<!-- RV P1.2 -->
<polygon points="140,310 156,300 140,290" fill="none" stroke="#8090a0" stroke-width="1.5"/>
<line x1="140" y1="289" x2="140" y2="311" stroke="#8090a0" stroke-width="2"/>
<line x1="148" y1="311" x2="148" y2="330" stroke="#7080a0" stroke-width="1"/>
<!-- Sammelleitung y=280 -->
<line class="p-aw" x1="90" y1="280" x2="148" y2="280"/>
<line class="p-aw" x1="90" y1="280" x2="90" y2="290"/>
<line class="p-aw" x1="148" y1="280" x2="148" y2="290"/>
<!-- Absperrschieber (horizontal) Ausgang HW -->
<path d="M 170,273 L 178,280 L 170,287 Z" fill="#506080"/>
<path d="M 194,273 L 186,280 L 194,287 Z" fill="#506080"/>
<line x1="182" y1="267" x2="182" y2="273" stroke="#8898a8" stroke-width="1.5"/>
<line x1="176" y1="267" x2="188" y2="267" stroke="#8898a8" stroke-width="2"/>
<line class="p-aw" x1="148" y1="280" x2="170" y2="280"/>
<line class="p-aw" x1="194" y1="280" x2="208" y2="280" marker-end="url(#aaw)"/>

<!-- ═══ SIEBRECHENANLAGE ═══ -->
<rect x="208" y="240" width="38" height="80" rx="2" fill="#eef2f8" stroke="#182848" stroke-width="1.2"/>
<line x1="214" y1="244" x2="220" y2="316" stroke="#3a5890" stroke-width="2.2"/>
<line x1="223" y1="244" x2="229" y2="316" stroke="#3a5890" stroke-width="2.2"/>
<line x1="232" y1="244" x2="238" y2="316" stroke="#3a5890" stroke-width="2.2"/>
<rect x="208" y="240" width="38" height="6" rx="1" fill="#c8d4e8"/>
<rect x="208" y="314" width="38" height="6" rx="1" fill="#c8d4e8"/>
<text x="227" y="231" text-anchor="middle" fill="#1a3870" font-size="7.5">R1.1</text>
<text x="227" y="222" text-anchor="middle" fill="#182848" font-size="7">Rechen</text>
<line class="p-aw" x1="208" y1="280" x2="246" y2="280"/>
<line x1="227" y1="320" x2="227" y2="338" stroke="#383028" stroke-width="1.2" stroke-dasharray="3,2"/>
<rect x="220" y="338" width="14" height="10" rx="2" fill="#0c0a08" stroke="#383028" stroke-width="1"/>
<text x="227" y="347" text-anchor="middle" fill="#f0e8d8" font-size="6.5">Gut</text>

<!-- ═══ SANDFANG ═══ -->
<rect x="250" y="196" width="130" height="208" rx="3" fill="#f5f8fa" stroke="#1e3060" stroke-width="1.5"/>
<text x="315" y="212" text-anchor="middle" fill="#185080" font-size="9.5" font-weight="bold">SANDFANG</text>
<path d="M 252,396 L 315,378 L 378,396 Z" fill="#c8b870" fill-opacity="0.5"/>
<!-- G2.1 Sandfanggebläse (kleines Symbol) -->
<circle cx="362" cy="268" r="9" fill="#f5f8fd" stroke="#a08010" stroke-width="1.2"/>
<text x="362" y="265" text-anchor="middle" fill="#6a5208" font-size="7" font-weight="bold">G</text>
<text x="362" y="280" text-anchor="middle" fill="#6a5208" font-size="7">G2.1</text>
<!-- FI 104 -->
<circle cx="315" cy="178" r="10" fill="#ffffff" stroke="#3a6090" stroke-width="1.2"/>
<text x="315" y="176" text-anchor="middle" fill="#1050a0" font-size="7">FI</text>
<text x="315" y="184" text-anchor="middle" fill="#1a3050" font-size="6">104</text>
<line class="p-sig" x1="315" y1="188" x2="315" y2="196"/>
<line class="p-aw" x1="246" y1="280" x2="250" y2="280"/>
<line class="p-aw" x1="380" y1="280" x2="388" y2="280" marker-end="url(#aaw)"/>
<line x1="315" y1="404" x2="315" y2="420" stroke="#483820" stroke-width="1.5" stroke-dasharray="4,2"/>
<text x="315" y="430" text-anchor="middle" fill="#382810" font-size="7">Sand → Entsorgung</text>

<!-- ═══ VORKLÄRUNG ═══ -->
<rect x="388" y="196" width="58" height="208" rx="3" fill="#f5f7fb" stroke="#203060" stroke-width="1.5"/>
<text x="417" y="212" text-anchor="middle" fill="#204090" font-size="8.5" font-weight="bold">VK-</text>
<text x="417" y="223" text-anchor="middle" fill="#204090" font-size="8.5" font-weight="bold">LÄR.</text>
<text x="417" y="234" text-anchor="middle" fill="#0e1838" font-size="7">VK1+VK2</text>
<!-- Räumbrücke -->
<line x1="392" y1="295" x2="443" y2="295" stroke="#404870" stroke-width="2.5" stroke-dasharray="7,3"/>
<rect x="397" y="290" width="6" height="10" rx="1" fill="#203050"/>
<rect x="413" y="290" width="6" height="10" rx="1" fill="#203050"/>
<rect x="429" y="290" width="6" height="10" rx="1" fill="#203050"/>
<text x="417" y="316" text-anchor="middle" fill="#203050" font-size="7">Räumer</text>
<!-- QI 105 -->
<circle cx="417" cy="178" r="10" fill="#ffffff" stroke="#3a6090" stroke-width="1.2"/>
<text x="417" y="176" text-anchor="middle" fill="#1050a0" font-size="7">QI</text>
<text x="417" y="184" text-anchor="middle" fill="#1a3050" font-size="6">105</text>
<line class="p-sig" x1="417" y1="188" x2="417" y2="196"/>
<line class="p-aw" x1="380" y1="280" x2="388" y2="280"/>
<line class="p-aw" x1="446" y1="280" x2="456" y2="280" marker-end="url(#aaw)"/>

<!-- REGENÜBERLAUF-BYPASS -->
<path class="p-abs" d="M 430,240 L 430,100 L 1075,100 L 1075,260" marker-end="url(#aabs)"/>
<!-- Regelklappe SV201 -->
<path d="M 423,229 L 430,237 L 437,229 Z" fill="#c03040"/>
<path d="M 423,245 L 430,237 L 437,245 Z" fill="#c03040"/>
<text x="530" y="94" fill="#c03040" font-size="7.5" font-weight="bold">REGENÜBERLAUF / MISCHWASSERABSCHLAG (nur mech. gereinigt)</text>
<text x="450" y="234" fill="#c03040" font-size="7">SV201</text>

<!-- P6.1 Primärschlamm-ESP aus VK -->
<rect x="405" y="418" width="24" height="16" rx="6" fill="#ffffff" stroke="#7040a0" stroke-width="1.4"/>
<path d="M 409,426 Q 413,420 417,426 Q 421,432 425,426" fill="none" stroke="#7040a0" stroke-width="1.5" stroke-linecap="round"/>
<!-- Schieber vor P6.1 -->
<path d="M 411,410 L 417,405 L 423,410 Z" fill="#405070"/>
<path d="M 411,400 L 417,405 L 423,400 Z" fill="#405070"/>
<line class="p-ues" x1="417" y1="404" x2="417" y2="418"/>
<text x="417" y="443" text-anchor="middle" fill="#5020a0" font-size="7.5">P6.1</text>
<text x="417" y="452" text-anchor="middle" fill="#2a10a0" font-size="7">Primärschl.</text>
<!-- Primärschlamm-Leitung seitlich zum Eindicker (rechts neben NK) -->
<path class="p-ues" d="M 417,434 L 417,468 L 990,468 L 990,432" marker-end="url(#aues)"/>
<text x="660" y="460" text-anchor="middle" fill="#6a5008" font-size="7.5">Primärschlamm PS</text>

<!-- ═══ GEBLÄSESTATION ═══ -->
<rect x="510" y="70" width="162" height="76" rx="3" fill="#f5f8fc" stroke="#382808" stroke-width="1.5"/>
<text x="591" y="84" text-anchor="middle" fill="#382808" font-size="8.5" letter-spacing="1">GEBLÄSESTATION</text>
<!-- G1.1 -->
<circle cx="548" cy="120" r="16" fill="#f5f8fd" stroke="#a08010" stroke-width="1.5"/>
<path d="M 537,113 Q 535,120 537,127 Q 548,131 559,127 Q 561,120 559,113 Q 548,109 537,113 Z" fill="none" stroke="#a08010" stroke-width="1.3"/>
<text x="548" y="121" text-anchor="middle" fill="#6a5208" font-size="8" font-weight="bold">G</text>
<text x="548" y="140" text-anchor="middle" fill="#6a5208" font-size="7.5">G1.1 Betr.</text>
<!-- G1.2 -->
<circle cx="620" cy="120" r="16" fill="#f5f8fd" stroke="#a08010" stroke-width="1.5"/>
<path d="M 609,113 Q 607,120 609,127 Q 620,131 631,127 Q 633,120 631,113 Q 620,109 609,113 Z" fill="none" stroke="#a08010" stroke-width="1.3"/>
<text x="620" y="121" text-anchor="middle" fill="#6a5208" font-size="8" font-weight="bold">G</text>
<text x="620" y="140" text-anchor="middle" fill="#6a5208" font-size="7.5">G1.2 Res.</text>
<!-- FIC 201 -->
<circle cx="658" cy="110" r="10" fill="#ffffff" stroke="#806010" stroke-width="1.2"/>
<text x="658" y="108" text-anchor="middle" fill="#6a5208" font-size="7">FIC</text>
<text x="658" y="116" text-anchor="middle" fill="#382808" font-size="6">201</text>
<line class="p-sig" x1="648" y1="110" x2="636" y2="110"/>
<!-- Druckluft-Sammelleitung -->
<line class="p-luft" x1="548" y1="104" x2="548" y2="88"/>
<line class="p-luft" x1="620" y1="104" x2="620" y2="88"/>
<line class="p-luft" x1="548" y1="88"  x2="620" y2="88"/>
<!-- Hauptleitung → BB -->
<line class="p-luft" x1="584" y1="88" x2="584" y2="150" marker-end="url(#aluft)"/>

<!-- ═══ FÄLLMITTELDOSIERUNG ═══ -->
<!-- FeCl3-Lagerbehälter -->
<rect x="1378" y="70" width="50" height="68" rx="3" fill="#f5f0fa" stroke="#4030a0" stroke-width="1.5"/>
<rect x="1380" y="100" width="46" height="34" rx="1" fill="#e0c8f830"/>
<line x1="1380" y1="100" x2="1428" y2="100" stroke="#4030a0" stroke-width="1"/>
<text x="1403" y="87" text-anchor="middle" fill="#5030a0" font-size="8">FeCl₃</text>
<text x="1403" y="96" text-anchor="middle" fill="#3020a0" font-size="7">40 %</text>
<text x="1403" y="115" text-anchor="middle" fill="#3020a0" font-size="7">Lager-</text>
<text x="1403" y="124" text-anchor="middle" fill="#3020a0" font-size="7">behält.</text>
<!-- LI 501 -->
<circle cx="1440" cy="100" r="10" fill="#ffffff" stroke="#3a4080" stroke-width="1.2"/>
<text x="1440" y="98" text-anchor="middle" fill="#7050a0" font-size="7">LI</text>
<text x="1440" y="106" text-anchor="middle" fill="#3020a0" font-size="6">501</text>
<line class="p-sig" x1="1430" y1="100" x2="1428" y2="100"/>
<!-- P7.1 KMP -->
<rect x="1342" y="122" width="22" height="16" rx="2" fill="#ffffff" stroke="#6030a0" stroke-width="1.4"/>
<path d="M 1346,129 Q 1353,122 1360,129" fill="none" stroke="#6030a0" stroke-width="1.5"/>
<line x1="1353" y1="120" x2="1353" y2="122" stroke="#507090" stroke-width="1.5"/>
<rect x="1347" y="110" width="12" height="10" rx="1" fill="#e8edf8" stroke="#203050" stroke-width="1"/>
<text x="1353" y="149" text-anchor="middle" fill="#4010a0" font-size="7.5">P7.1</text>
<text x="1353" y="158" text-anchor="middle" fill="#2a10a0" font-size="7">ProMinent</text>
<line class="p-fm" x1="1378" y1="130" x2="1364" y2="130"/>
<!-- RV Druckseite -->
<path d="M 1338,125 L 1328,130 L 1338,135 Z" fill="none" stroke="#8090a0" stroke-width="1.3"/>
<line x1="1328" y1="124" x2="1328" y2="136" stroke="#8090a0" stroke-width="1.8"/>
<!-- FIC 502 -->
<circle cx="1140" cy="130" r="10" fill="#ffffff" stroke="#4030a0" stroke-width="1.2"/>
<text x="1140" y="128" text-anchor="middle" fill="#4010a0" font-size="7">FIC</text>
<text x="1140" y="136" text-anchor="middle" fill="#2a10a0" font-size="6">502</text>
<!-- Dosierleitung -->
<path class="p-fm" d="M 1318,130 L 700,130 L 700,175" marker-end="url(#afm)"/>

<!-- ═══ BELEBUNGSBECKEN ═══ -->
<rect x="450" y="175" width="310" height="250" rx="4" fill="#edf5ef" stroke="#1a4830" stroke-width="2"/>
<text x="605" y="192" text-anchor="middle" fill="#106030" font-size="11" font-weight="bold">BELEBUNGSBECKEN</text>
<!-- Trennwand -->
<line x1="590" y1="183" x2="590" y2="385" stroke="#1c3820" stroke-width="1.8" stroke-dasharray="6,4"/>
<rect x="587" y="292" width="6" height="32" fill="#edf5ef"/>
<text x="590" y="288" text-anchor="middle" fill="#1c3820" font-size="6.5">Öffn.</text>
<!-- DENI Zone -->
<text x="518" y="212" text-anchor="middle" fill="#0d5520" font-size="9" font-weight="bold">DENI</text>
<text x="518" y="224" text-anchor="middle" fill="#0a4818" font-size="7.5">Denitrifikation</text>
<text x="518" y="234" text-anchor="middle" fill="#0a3818" font-size="7">anoxisch</text>
<!-- Rührwerk Rw1.1 (kompakt) -->
<line x1="518" y1="275" x2="518" y2="328" stroke="#5840a0" stroke-width="1.5"/>
<line x1="500" y1="318" x2="536" y2="318" stroke="#5840a0" stroke-width="3.5" stroke-linecap="round"/>
<line x1="505" y1="308" x2="531" y2="308" stroke="#5840a0" stroke-width="2.5" stroke-linecap="round"/>
<rect x="512" y="265" width="12" height="10" rx="2" fill="#f5f7fb" stroke="#282060" stroke-width="1"/>
<text x="518" y="273" text-anchor="middle" fill="#3828a0" font-size="6">M</text>
<text x="518" y="344" text-anchor="middle" fill="#3020a0" font-size="7.5">Rw1.1</text>
<!-- NITRI Zone -->
<text x="668" y="212" text-anchor="middle" fill="#0d5520" font-size="9" font-weight="bold">NITRI</text>
<text x="668" y="224" text-anchor="middle" fill="#0a4818" font-size="7.5">Nitrifikation</text>
<text x="668" y="234" text-anchor="middle" fill="#0a3818" font-size="7">aerob</text>
<!-- Belüfter-Verteilerrohr -->
<line class="p-luft" x1="597" y1="415" x2="755" y2="415"/>
<line class="p-luft" x1="584" y1="150" x2="584" y2="175"/>
<line class="p-luft" x1="584" y1="175" x2="676" y2="175"/>
<line class="p-luft" x1="676" y1="175" x2="676" y2="183"/>
<line class="p-luft" x1="640" y1="385" x2="640" y2="415"/>
<line class="p-luft" x1="710" y1="385" x2="710" y2="415"/>
<!-- Belüfter-Platten -->
<rect x="608" y="381" width="60" height="5" rx="2" fill="#0e2030" stroke="#1e5080" stroke-width="1"/>
<rect x="678" y="381" width="60" height="5" rx="2" fill="#0e2030" stroke="#1e5080" stroke-width="1"/>
<!-- Blasen -->
<circle cx="620" cy="372" r="3" fill="none" stroke="#1e5080" stroke-width="0.8" opacity="0.6"/>
<circle cx="635" cy="367" r="2.5" fill="none" stroke="#1e5080" stroke-width="0.8" opacity="0.5"/>
<circle cx="650" cy="373" r="3" fill="none" stroke="#1e5080" stroke-width="0.8" opacity="0.6"/>
<circle cx="692" cy="372" r="3" fill="none" stroke="#1e5080" stroke-width="0.8" opacity="0.6"/>
<circle cx="710" cy="366" r="2.5" fill="none" stroke="#1e5080" stroke-width="0.8" opacity="0.5"/>
<circle cx="728" cy="373" r="3" fill="none" stroke="#1e5080" stroke-width="0.8" opacity="0.6"/>
<text x="668" y="400" text-anchor="middle" fill="#0e2e58" font-size="7">Membranbelüfter</text>
<!-- QI 301 O2-Sonde -->
<circle cx="755" cy="240" r="10" fill="#ffffff" stroke="#286848" stroke-width="1.2"/>
<text x="755" y="238" text-anchor="middle" fill="#106030" font-size="7">QI</text>
<text x="755" y="246" text-anchor="middle" fill="#0c4028" font-size="6">301</text>
<line class="p-sig" x1="755" y1="250" x2="755" y2="280"/>
<text x="768" y="256" fill="#0a4818" font-size="6.5">O₂</text>
<!-- FeCl3 Dosierpunkt -->
<circle cx="700" cy="178" r="4" fill="#6020b0" fill-opacity="0.9"/>
<text x="712" y="177" fill="#6020b0" font-size="7">FeCl₃</text>
<!-- AW in/aus BB -->
<line class="p-aw" x1="516" y1="280" x2="450" y2="280"/>
<line class="p-aw" x1="760" y1="280" x2="800" y2="280" marker-end="url(#aaw)"/>
<!-- Interne Rezirkulation P2.1 -->
<path class="p-ir" d="M 748,196 L 748,158 L 476,158 L 476,183" marker-end="url(#air)"/>
<circle cx="614" cy="158" r="10" fill="#ffffff" stroke="#8040c0" stroke-width="1.4"/>
<path d="M 608,153 L 622,158 L 608,163 Z" fill="#6020a8"/>
<text x="614" y="148" text-anchor="middle" fill="#6020a8" font-size="7.5">P2.1</text>
<text x="640" y="148" fill="#2a10a0" font-size="7">Int.Rez.</text>

<!-- ═══ NACHKLÄRBECKEN (Kreis r=70) ═══ -->
<circle cx="896" cy="285" r="70" fill="#fafaf0" stroke="#604c10" stroke-width="2"/>
<text x="896" y="279" text-anchor="middle" fill="#7a5c08" font-size="10" font-weight="bold">NACH-</text>
<text x="896" y="293" text-anchor="middle" fill="#7a5c08" font-size="10" font-weight="bold">KLÄRUNG</text>
<text x="896" y="306" text-anchor="middle" fill="#504210" font-size="7.5">NK1 + NK2</text>
<!-- Kreisräumer -->
<line x1="826" y1="285" x2="896" y2="285" stroke="#685820" stroke-width="2.2"/>
<rect x="820" y="279" width="10" height="12" rx="1.5" fill="#382808"/>
<circle cx="896" cy="285" r="5" fill="#382808"/>
<line x1="896" y1="285" x2="940" y2="285" stroke="#685820" stroke-width="1.5"/>
<rect x="936" y="280" width="8" height="9" rx="1" fill="#302008"/>
<!-- Einlaufbauwerk -->
<circle cx="896" cy="285" r="10" fill="#f5f8f0" stroke="#2a4010" stroke-width="1"/>
<!-- LI 401 -->
<circle cx="814" cy="358" r="10" fill="#ffffff" stroke="#3a6090" stroke-width="1.2"/>
<text x="814" y="356" text-anchor="middle" fill="#a07830" font-size="7">LI</text>
<text x="814" y="364" text-anchor="middle" fill="#706020" font-size="6">401</text>
<line class="p-sig" x1="814" y1="348" x2="828" y2="330"/>
<!-- NK Ablauf (Ringrinne → Ablaufleitung) -->
<path class="p-ab" d="M 896,215 L 896,185 L 1010,185 L 1010,268" marker-end="url(#aab)"/>
<text x="952" y="178" text-anchor="middle" fill="#18b060" font-size="7.5">Ablauf (gereinigt)</text>

<!-- ═══ RÜCKLAUFSCHLAMM ═══ -->
<!-- RS: NK Boden → nach unten → links zu P3.x -->
<path class="p-rs" d="M 896,355 L 896,390 L 961,390"/>
<!-- ÜS-Abzweig am Knickpunkt (896,390) schon im ÜS-Block behandelt -->
<path class="p-rs" d="M 896,390 L 896,438 L 778,438"/>
<!-- P3.1–P3.5 KSB Sewabloc F 100-252 (cx=754, cy=438) -->
<circle cx="754" cy="438" r="11" fill="#ffffff" stroke="#a06020" stroke-width="1.5"/>
<path d="M 761,432 L 745,438 L 761,444 Z" fill="#7a4010"/>
<line x1="754" y1="427" x2="754" y2="416" stroke="#385870" stroke-width="1.5"/>
<rect x="747" y="407" width="14" height="10" rx="1.5" fill="#e8edf8" stroke="#203050" stroke-width="1"/>
<text x="754" y="415" text-anchor="middle" fill="#304060" font-size="6.5">M</text>
<text x="756" y="456" text-anchor="middle" fill="#7a4010" font-size="7.5">P3.1–3.5</text>
<text x="756" y="465" text-anchor="middle" fill="#503810" font-size="7">Betrieb</text>
<!-- P3.6 Reserve (cx=714) -->
<circle cx="714" cy="438" r="11" fill="#ffffff" stroke="#a06020" stroke-width="1.5"/>
<path d="M 721,432 L 705,438 L 721,444 Z" fill="#7a4010"/>
<line x1="714" y1="427" x2="714" y2="416" stroke="#385870" stroke-width="1.5"/>
<rect x="707" y="407" width="14" height="10" rx="1.5" fill="#e8edf8" stroke="#203050" stroke-width="1"/>
<text x="714" y="415" text-anchor="middle" fill="#304060" font-size="6.5">M</text>
<text x="714" y="456" text-anchor="middle" fill="#7a4010" font-size="7.5">P3.6</text>
<text x="714" y="465" text-anchor="middle" fill="#503810" font-size="7">Reserve</text>
<!-- Schieber vor P3.1 -->
<path d="M 768,433 L 776,438 L 768,443 Z" fill="#506080"/>
<path d="M 784,433 L 776,438 L 784,443 Z" fill="#506080"/>
<!-- FI 402 -->
<circle cx="666" cy="438" r="10" fill="#ffffff" stroke="#806030" stroke-width="1.2"/>
<text x="666" y="436" text-anchor="middle" fill="#7a5020" font-size="7">FI</text>
<text x="666" y="444" text-anchor="middle" fill="#503810" font-size="6">402</text>
<!-- RS → BB -->
<path class="p-rs" d="M 648,438 L 460,438 L 460,385" marker-end="url(#ars)"/>
<text x="550" y="430" text-anchor="middle" fill="#8a5010" font-size="7.5">Rücklaufschlamm (RS)</text>

<!-- ═══ ÜBERSCHUSSSCHLAMM ═══ -->
<!-- ÜS-Abzweig aus RS-Leitung, geht nach rechts neben NK -->
<path class="p-ues" d="M 896,390 L 978,390"/>
<!-- P5.1 Seepex BN52 ESP (cx=990, cy=390 – rechts neben NK) -->
<rect x="976" y="382" width="28" height="17" rx="6" fill="#ffffff" stroke="#907028" stroke-width="1.5"/>
<path d="M 980,390 Q 984,383 990,390 Q 996,397 1000,390" fill="none" stroke="#907028" stroke-width="1.8" stroke-linecap="round"/>
<line x1="976" y1="390" x2="978" y2="390" stroke="#507090" stroke-width="1.5"/>
<!-- Schieber vor P5.1 -->
<path d="M 971,386 L 976,390 L 971,395 Z" fill="#506080"/>
<path d="M 961,386 L 966,390 L 961,395 Z" fill="#506080"/>
<line x1="966" y1="390" x2="971" y2="390" stroke="#8898a8" stroke-width="1.2"/>
<!-- Motor oben -->
<line x1="990" y1="382" x2="990" y2="374" stroke="#507090" stroke-width="1.5"/>
<rect x="984" y="365" width="12" height="9" rx="1.5" fill="#e8edf8" stroke="#203050" stroke-width="1"/>
<text x="990" y="373" text-anchor="middle" fill="#304060" font-size="6.5">M</text>
<text x="990" y="411" text-anchor="middle" fill="#907028" font-size="7.5">P5.1</text>
<text x="990" y="420" text-anchor="middle" fill="#503810" font-size="7">Seepex BN52</text>
<!-- FI 403 -->
<circle cx="1016" cy="410" r="10" fill="#ffffff" stroke="#806030" stroke-width="1.2"/>
<text x="1016" y="408" text-anchor="middle" fill="#7a5020" font-size="7">FI</text>
<text x="1016" y="416" text-anchor="middle" fill="#503810" font-size="6">403</text>
<line class="p-sig" x1="1006" y1="399" x2="1010" y2="405"/>

<!-- ═══ SCHLAMMBEHANDLUNG ═══ -->
<!-- Eindicker rechts neben NK, unter P5.1 und PS-Leitung -->
<path class="p-ues" d="M 1004,390 L 1060,390 L 1060,418" marker-end="url(#aues)"/>
<rect x="1024" y="418" width="100" height="50" rx="3" fill="#f0f5ee" stroke="#384810" stroke-width="1.2" stroke-dasharray="5,3"/>
<text x="1074" y="435" text-anchor="middle" fill="#303810" font-size="8">Eindicker /</text>
<text x="1074" y="447" text-anchor="middle" fill="#303810" font-size="8">Schlammstapel</text>
<text x="1074" y="459" text-anchor="middle" fill="#202808" font-size="7.5">PS + ÜS → Faulturm</text>


<!-- ═══ SCHLAMMFAULUNG (Rev.02) ═══ -->
<rect x="1227" y="168" width="367" height="274" rx="4" fill="#f7f4ee" stroke="#5a4020" stroke-width="1" stroke-dasharray="7,4"/>
<text x="1410" y="181" text-anchor="middle" fill="#403010" font-size="8.5" letter-spacing="2">SCHLAMMFAULUNG</text>
<!-- Dickschlamm Eindicker → Faulturm -->
<path class="p-ues" d="M 1124,430 L 1280,430 L 1280,250 L 1290,250" marker-end="url(#aues)"/>
<text x="1180" y="425" text-anchor="middle" fill="#806018" font-size="7.5">Dickschlamm</text>
<!-- Faulturm FT-1 -->
<path d="M 1290,215 Q 1330,190 1370,215 L 1370,345 L 1330,385 L 1290,345 Z" fill="#f3efe4" stroke="#4a3a10" stroke-width="1.8"/>
<line x1="1292" y1="226" x2="1368" y2="226" stroke="#6a5a30" stroke-width="0.8" stroke-dasharray="4,3"/>
<text x="1330" y="268" text-anchor="middle" fill="#3a2a08" font-size="10" font-weight="bold">FAULTURM</text>
<text x="1330" y="282" text-anchor="middle" fill="#3a2a08" font-size="8.5">FT-1</text>
<text x="1330" y="298" text-anchor="middle" fill="#4a3a18" font-size="7.5">2.200 m³</text>
<text x="1330" y="310" text-anchor="middle" fill="#4a3a18" font-size="7.5">mesophil 37 °C</text>
<!-- Faulgas → BHKW -->
<path d="M 1330,202 L 1330,190 L 1522,190" fill="none" stroke="#c8a020" stroke-width="1.8" stroke-dasharray="8,3"/>
<rect x="1522" y="178" width="66" height="24" rx="2" fill="#fffaf0" stroke="#8a6010" stroke-width="1.2"/>
<text x="1555" y="189" text-anchor="middle" fill="#6a4808" font-size="8" font-weight="bold">BHKW</text>
<text x="1555" y="198" text-anchor="middle" fill="#6a4808" font-size="6.5">Faulgas</text>
<circle cx="1500" cy="207" r="10" fill="#ffffff" stroke="#8a6010" stroke-width="1.2"/>
<text x="1500" y="205" text-anchor="middle" fill="#8a6010" font-size="7">FI</text>
<text x="1500" y="213" text-anchor="middle" fill="#5a4008" font-size="6">608</text>
<line class="p-sig" x1="1500" y1="197" x2="1500" y2="190"/>
<!-- Umwälzkreis: Konus → P10.1/P10.2 → W10.1 → Faulturm -->
<path d="M 1330,385 L 1330,413 L 1372,413" fill="none" stroke="#7a5018" stroke-width="2"/>
<line x1="1372" y1="396" x2="1372" y2="430" stroke="#7a5018" stroke-width="2"/>
<line x1="1372" y1="396" x2="1390" y2="396" stroke="#7a5018" stroke-width="2"/>
<line x1="1372" y1="430" x2="1390" y2="430" stroke="#7a5018" stroke-width="2"/>
<line x1="1410" y1="396" x2="1428" y2="396" stroke="#7a5018" stroke-width="2"/>
<line x1="1410" y1="430" x2="1428" y2="430" stroke="#7a5018" stroke-width="2"/>
<line x1="1428" y1="396" x2="1428" y2="430" stroke="#7a5018" stroke-width="2"/>
<path d="M 1428,413 L 1470,413 L 1470,316" fill="none" stroke="#7a5018" stroke-width="2"/>
<path d="M 1470,285 L 1470,222 L 1372,222" fill="none" stroke="#7a5018" stroke-width="2" marker-end="url(#ars)"/>
<!-- P10.1 -->
<circle cx="1400" cy="396" r="10" fill="#ffffff" stroke="#a06020" stroke-width="1.5"/>
<path d="M 1394,391 L 1408,396 L 1394,401 Z" fill="#7a4010"/>
<line x1="1400" y1="386" x2="1400" y2="384" stroke="#385870" stroke-width="1.5"/>
<rect x="1394" y="374" width="12" height="10" rx="1.5" fill="#e8edf8" stroke="#203050" stroke-width="1"/>
<text x="1400" y="382" text-anchor="middle" fill="#304060" font-size="6.5">M</text>
<text x="1366" y="392" text-anchor="end" fill="#7a4010" font-size="7.5">P10.1</text>
<!-- P10.2 -->
<circle cx="1400" cy="430" r="10" fill="#ffffff" stroke="#a06020" stroke-width="1.5"/>
<path d="M 1394,425 L 1408,430 L 1394,435 Z" fill="#7a4010"/>
<line x1="1400" y1="440" x2="1400" y2="442" stroke="#385870" stroke-width="1.5"/>
<rect x="1394" y="442" width="12" height="10" rx="1.5" fill="#e8edf8" stroke="#203050" stroke-width="1"/>
<text x="1400" y="450" text-anchor="middle" fill="#304060" font-size="6.5">M</text>
<text x="1366" y="447" text-anchor="end" fill="#7a4010" font-size="7.5">P10.2</text>
<!-- Wärmetauscher W10.1 -->
<circle cx="1470" cy="300" r="15" fill="#ffffff" stroke="#4a3a10" stroke-width="1.5"/>
<path d="M 1458,306 L 1463,294 L 1468,306 L 1473,294 L 1478,306 L 1482,297" fill="none" stroke="#c03030" stroke-width="1.3"/>
<text x="1490" y="328" fill="#4a3a18" font-size="7.5">W10.1</text>
<line x1="1485" y1="295" x2="1560" y2="295" stroke="#c03030" stroke-width="1.4"/>
<line x1="1560" y1="295" x2="1560" y2="202" stroke="#c03030" stroke-width="1.4"/>
<line x1="1485" y1="305" x2="1572" y2="305" stroke="#c03030" stroke-width="1.4" stroke-dasharray="5,3"/>
<line x1="1572" y1="305" x2="1572" y2="202" stroke="#c03030" stroke-width="1.4" stroke-dasharray="5,3"/>
<text x="1522" y="290" text-anchor="middle" fill="#a02020" font-size="6.5">Heizwasser</text>
<!-- MSR Faulung -->
<circle cx="1392" cy="245" r="10" fill="#ffffff" stroke="#3a6090" stroke-width="1.2"/>
<text x="1392" y="243" text-anchor="middle" fill="#3a5080" font-size="7">LI</text>
<text x="1392" y="251" text-anchor="middle" fill="#203060" font-size="6">607</text>
<line class="p-sig" x1="1382" y1="245" x2="1370" y2="245"/>
<circle cx="1392" cy="272" r="10" fill="#ffffff" stroke="#3a6090" stroke-width="1.2"/>
<text x="1392" y="270" text-anchor="middle" fill="#3a5080" font-size="7">TI</text>
<text x="1392" y="278" text-anchor="middle" fill="#203060" font-size="6">606</text>
<line class="p-sig" x1="1382" y1="272" x2="1370" y2="272"/>
<circle cx="1495" cy="372" r="10" fill="#ffffff" stroke="#806030" stroke-width="1.2"/>
<text x="1495" y="370" text-anchor="middle" fill="#7a5020" font-size="7">FI</text>
<text x="1495" y="378" text-anchor="middle" fill="#503810" font-size="6">601</text>
<line class="p-sig" x1="1485" y1="372" x2="1470" y2="372"/>
<circle cx="1305" cy="400" r="10" fill="#ffffff" stroke="#806030" stroke-width="1.2"/>
<text x="1305" y="398" text-anchor="middle" fill="#7a5020" font-size="7">PI</text>
<text x="1305" y="406" text-anchor="middle" fill="#503810" font-size="6">602</text>
<line class="p-sig" x1="1315" y1="402" x2="1330" y2="405"/>
<circle cx="1495" cy="425" r="10" fill="#ffffff" stroke="#806030" stroke-width="1.2"/>
<text x="1495" y="423" text-anchor="middle" fill="#7a5020" font-size="7">PI</text>
<text x="1495" y="431" text-anchor="middle" fill="#503810" font-size="6">603</text>
<line class="p-sig" x1="1485" y1="422" x2="1470" y2="413"/>
<!-- Faulschlamm → Entwässerung -->
<path class="p-ues" d="M 1330,413 L 1330,462 L 1236,462" marker-end="url(#aues)"/>
<text x="1240" y="474" fill="#806018" font-size="7.5">Faulschlamm → Entwässerung</text>

<!-- ═══ MESSSCHACHT / ABLAUF ═══ -->
<rect x="1010" y="248" width="90" height="88" rx="3" fill="#edf8f3" stroke="#1a5030" stroke-width="1.5"/>
<text x="1055" y="264" text-anchor="middle" fill="#0a6838" font-size="8.5">Mess-</text>
<text x="1055" y="276" text-anchor="middle" fill="#0a6838" font-size="8.5">schacht</text>
<!-- QI 501 -->
<circle cx="1000" cy="295" r="10" fill="#ffffff" stroke="#286848" stroke-width="1.2"/>
<text x="1000" y="293" text-anchor="middle" fill="#0a6838" font-size="7">QI</text>
<text x="1000" y="301" text-anchor="middle" fill="#085028" font-size="6">501</text>
<text x="1000" y="318" text-anchor="middle" fill="#085028" font-size="6.5">CSB/NH₄/P</text>
<!-- FI 502 -->
<circle cx="1108" cy="295" r="10" fill="#ffffff" stroke="#286848" stroke-width="1.2"/>
<text x="1108" y="293" text-anchor="middle" fill="#0a6838" font-size="7">FI</text>
<text x="1108" y="301" text-anchor="middle" fill="#085028" font-size="6">502</text>
<!-- Ablauf → Vorfluter -->
<line class="p-ab" x1="1100" y1="295" x2="1155" y2="295" marker-end="url(#aab)"/>
<text x="1165" y="288" fill="#0a6030" font-size="9.5" font-weight="bold">▶ VORFLUTER</text>
<text x="1165" y="300" fill="#106030" font-size="7.5">(Gewässereinleitung)</text>
<!-- Regenüberlauf-Einleitstelle -->
<circle cx="1075" cy="260" r="3.5" fill="#e03848" fill-opacity="0.5"/>
<!-- QI 503 Abschlagqualität -->
<circle cx="1048" cy="228" r="10" fill="#ffffff" stroke="#803040" stroke-width="1.2"/>
<text x="1048" y="226" text-anchor="middle" fill="#c03040" font-size="7">QI</text>
<text x="1048" y="234" text-anchor="middle" fill="#8a1818" font-size="6">503</text>
<text x="1030" y="218" text-anchor="end" fill="#8a1818" font-size="7">Abschlag-</text>
<text x="1030" y="208" text-anchor="end" fill="#8a1818" font-size="7">qualität</text>
<line class="p-sig" x1="1048" y1="238" x2="1048" y2="260"/>
<!-- pH 504 + P9.1 Kalkmilch -->
<circle cx="1055" cy="355" r="10" fill="#ffffff" stroke="#286848" stroke-width="1.2"/>
<text x="1055" y="353" text-anchor="middle" fill="#0a6838" font-size="7">pH</text>
<text x="1055" y="361" text-anchor="middle" fill="#085028" font-size="6">504</text>
<!-- P9.1 KMP -->
<rect x="1082" y="348" width="16" height="13" rx="2" fill="#ffffff" stroke="#5030a0" stroke-width="1.3"/>
<path d="M 1085,354 Q 1090,348 1095,354" fill="none" stroke="#5030a0" stroke-width="1.3"/>
<text x="1090" y="370" text-anchor="middle" fill="#2a10a0" font-size="7.5">P9.1</text>
<text x="1090" y="379" text-anchor="middle" fill="#2a10a0" font-size="7">Kalkmilch</text>
<text x="1090" y="388" text-anchor="middle" fill="#2a10a0" font-size="7">pH&lt;6,8</text>
<line class="p-fm" x1="1090" y1="345" x2="1090" y2="335" stroke="#8060c0"/>
<circle cx="1090" cy="332" r="2.5" fill="#8060c0"/>
<line class="p-sig" x1="1065" y1="355" x2="1080" y2="355"/>

<!-- ══════════════════════════════════════════════════════ -->
<!--   UNTERER BEREICH                                      -->
<!-- ══════════════════════════════════════════════════════ -->
<rect x="6" y="474" width="1588" height="2" fill="#0e2040" fill-opacity="0.4"/>

<!-- ─── LEGENDE ─── -->
<rect x="6" y="480" width="450" height="424" rx="4" fill="#f8fafc" stroke="#1a3050" stroke-width="1.2"/>
<text x="231" y="496" text-anchor="middle" fill="#1a4080" font-size="10" font-weight="bold">LEGENDE</text>

<text x="18" y="514" fill="#1a4080" font-size="8.5" font-weight="bold">Rohrleitungen:</text>
<line x1="18" y1="528" x2="72" y2="528" stroke="#1e90e8" stroke-width="3"/>
<text x="80" y="532" fill="#0e2040" font-size="8.5">Abwasser / Zulauf</text>
<line x1="18" y1="545" x2="72" y2="545" stroke="#c07828" stroke-width="2.2" stroke-dasharray="9,4"/>
<text x="80" y="549" fill="#0e2040" font-size="8.5">Rücklaufschlamm RS</text>
<line x1="18" y1="562" x2="72" y2="562" stroke="#c89030" stroke-width="1.8" stroke-dasharray="5,4"/>
<text x="80" y="566" fill="#0e2040" font-size="8.5">Übersch.-/Primärschlamm</text>
<line x1="18" y1="579" x2="72" y2="579" stroke="#c8a020" stroke-width="2" stroke-dasharray="8,3"/>
<text x="80" y="583" fill="#0e2040" font-size="8.5">Druckluft</text>
<line x1="18" y1="596" x2="72" y2="596" stroke="#9050c8" stroke-width="1.6" stroke-dasharray="4,3"/>
<text x="80" y="600" fill="#0e2040" font-size="8.5">Fällmittel / Chemikalie</text>
<line x1="18" y1="613" x2="72" y2="613" stroke="#18c870" stroke-width="3"/>
<text x="80" y="617" fill="#0e2040" font-size="8.5">Ablauf / gereinigtes Wasser</text>
<line x1="18" y1="630" x2="72" y2="630" stroke="#e03848" stroke-width="2" stroke-dasharray="7,3"/>
<text x="80" y="634" fill="#0e2040" font-size="8.5">Regenüberlauf / Abschlag</text>
<line x1="18" y1="647" x2="72" y2="647" stroke="#9050d8" stroke-width="1.8" stroke-dasharray="6,3"/>
<text x="80" y="651" fill="#0e2040" font-size="8.5">Interne Rezirkulation</text>
<line x1="18" y1="664" x2="72" y2="664" stroke="#486880" stroke-width="0.9" stroke-dasharray="3,3"/>
<text x="80" y="668" fill="#0e2040" font-size="8.5">Messignalleitung</text>

<text x="18" y="692" fill="#1a4080" font-size="8.5" font-weight="bold">Symbole (angelehnt an DIN EN ISO 10628-2):</text>

<!-- Spalte 1: Pumpen -->
<!-- KP -->
<circle cx="40" cy="718" r="11" fill="#ffffff" stroke="#3a80c0" stroke-width="1.6"/>
<path d="M 34,712 L 50,718 L 34,724 Z" fill="#3a80c0"/>
<line x1="40" y1="707" x2="40" y2="698" stroke="#385870" stroke-width="1.5"/>
<rect x="34" y="689" width="12" height="9" rx="1.5" fill="#e8edf8" stroke="#203050" stroke-width="1"/>
<text x="40" y="696" text-anchor="middle" fill="#304060" font-size="5.5">M</text>
<text x="60" y="720" fill="#0e2040" font-size="8">Kreiselpumpe</text>

<!-- ESP -->
<rect x="29" y="742" width="22" height="14" rx="6" fill="#ffffff" stroke="#7040a0" stroke-width="1.4"/>
<path d="M 33,749 Q 36,743 40,749 Q 44,755 47,749" fill="none" stroke="#7040a0" stroke-width="1.4" stroke-linecap="round"/>
<text x="60" y="752" fill="#0e2040" font-size="8">Exzenterschneckenpumpe</text>

<!-- KMP -->
<rect x="29" y="772" width="20" height="14" rx="2" fill="#ffffff" stroke="#6030a0" stroke-width="1.4"/>
<path d="M 33,779 Q 39,772 45,779" fill="none" stroke="#6030a0" stroke-width="1.4"/>
<text x="60" y="782" fill="#0e2040" font-size="8">Kolbenmembranpumpe</text>

<!-- Rührwerk -->
<line x1="40" y1="800" x2="40" y2="814" stroke="#5840a0" stroke-width="1.5"/>
<line x1="31" y1="811" x2="49" y2="811" stroke="#5840a0" stroke-width="3" stroke-linecap="round"/>
<text x="60" y="810" fill="#0e2040" font-size="8">Tauchmotorrührwerk</text>

<!-- Spalte 2: Armaturen + MSR -->
<!-- SV -->
<path d="M 248,712 L 256,718 L 248,724 Z" fill="#506080"/>
<path d="M 264,712 L 256,718 L 264,724 Z" fill="#506080"/>
<line x1="256" y1="706" x2="256" y2="712" stroke="#8898a8" stroke-width="1.5"/>
<line x1="250" y1="706" x2="262" y2="706" stroke="#8898a8" stroke-width="2"/>
<text x="274" y="720" fill="#0e2040" font-size="8">Absperrschieber</text>

<!-- RV -->
<polygon points="248,742 264,749 248,756" fill="none" stroke="#8090a0" stroke-width="1.5"/>
<line x1="248" y1="741" x2="248" y2="757" stroke="#8090a0" stroke-width="2"/>
<text x="274" y="752" fill="#0e2040" font-size="8">Rückschlagventil</text>

<!-- Messinstrument -->
<circle cx="256" cy="779" r="10" fill="#ffffff" stroke="#3a6090" stroke-width="1.2"/>
<text x="256" y="777" text-anchor="middle" fill="#1050a0" font-size="7">XX</text>
<text x="256" y="785" text-anchor="middle" fill="#1a3050" font-size="6">nnn</text>
<text x="274" y="776" fill="#0e2040" font-size="8">Messinstrument</text>
<text x="274" y="787" fill="#7090a0" font-size="7">FI / QI / LI / FIC …</text>

<!-- Gebläse -->
<circle cx="256" cy="810" r="11" fill="#f5f8fd" stroke="#a08010" stroke-width="1.5"/>
<path d="M 248,804 Q 246,810 248,816 Q 256,819 264,816 Q 266,810 264,804 Q 256,801 248,804 Z" fill="none" stroke="#a08010" stroke-width="1.1"/>
<text x="256" y="812" text-anchor="middle" fill="#6a5208" font-size="7" font-weight="bold">G</text>
<text x="274" y="812" fill="#0e2040" font-size="8">Drehkolbengebläse</text>

<!-- ─── AGGREGATLISTE ─── -->
<rect x="462" y="480" width="570" height="424" rx="4" fill="#f8fafc" stroke="#1a3050" stroke-width="1.2"/>
<text x="747" y="496" text-anchor="middle" fill="#1a4080" font-size="10" font-weight="bold">AGGREGATLISTE (Kurzform)</text>
<rect x="468" y="503" width="558" height="15" fill="#dce4f0"/>
<text x="476" y="514" fill="#1a4080" font-size="8" font-weight="bold">KKS</text>
<text x="514" y="514" fill="#1a4080" font-size="8" font-weight="bold">Bezeichnung</text>
<text x="780" y="514" fill="#1a4080" font-size="8" font-weight="bold">Typ / Hersteller</text>
<g fill="#0e2040" font-size="7.8">
  <text x="476" y="531">P1.1</text><text x="514" y="531">Zulaufpumpe (Betrieb), FU-geregelt</text><text x="780" y="531">Tauchmotorpumpe KP, Flygt/Grundfos</text>
  <line x1="468" y1="535" x2="1026" y2="535" stroke="#dce4f0" stroke-width="0.7"/>
  <text x="476" y="547">P1.2</text><text x="514" y="547">Zulaufpumpe (Reserve)</text><text x="780" y="547">Tauchmotorpumpe KP</text>
  <line x1="468" y1="551" x2="1026" y2="551" stroke="#dce4f0" stroke-width="0.7"/>
  <text x="476" y="563">P2.1</text><text x="514" y="563">Interne Rezirkulation Nitri→Deni, FU</text><text x="780" y="563">Axialpumpe/KP, ~2 × Q_ZU</text>
  <line x1="468" y1="567" x2="1026" y2="567" stroke="#dce4f0" stroke-width="0.7"/>
  <text x="476" y="579">P3.1–3.6</text><text x="514" y="579">Rücklaufschlammpumpen, Stufenschaltung</text><text x="780" y="579">6 × KSB Sewabloc F 100-252</text>
  <line x1="468" y1="583" x2="1026" y2="583" stroke="#dce4f0" stroke-width="0.7"/>
  <text x="476" y="595">P10.1/2</text><text x="514" y="595">Umwälzpumpen Faulturm (Betr. / Res.)</text><text x="780" y="595">KSB Sewabloc F 100-254</text>
  <line x1="468" y1="599" x2="1026" y2="599" stroke="#dce4f0" stroke-width="0.7"/>
  <text x="476" y="611">P5.1</text><text x="514" y="611">Überschussschlammpumpe, drehzahlgeregelt</text><text x="780" y="611">Seepex BN 52-6L, ESP</text>
  <line x1="468" y1="615" x2="1026" y2="615" stroke="#dce4f0" stroke-width="0.7"/>
  <text x="476" y="627">P6.1</text><text x="514" y="627">Primärschlammpumpe VK, drehzahlgeregelt</text><text x="780" y="627">Exzenterschneckenpumpe ESP</text>
  <line x1="468" y1="631" x2="1026" y2="631" stroke="#dce4f0" stroke-width="0.7"/>
  <text x="476" y="643">P7.1</text><text x="514" y="643">Fällmitteldosierpumpe FeCl₃ 40 %</text><text x="780" y="643">ProMinent Sigma S2Cb, KMP</text>
  <line x1="468" y1="647" x2="1026" y2="647" stroke="#dce4f0" stroke-width="0.7"/>
  <text x="476" y="659">P9.1</text><text x="514" y="659">Kalkmilchpumpe (bei pH &lt; 6,8)</text><text x="780" y="659">Kolbenmembranpumpe KMP</text>
  <line x1="468" y1="663" x2="1026" y2="663" stroke="#dce4f0" stroke-width="0.7"/>
  <text x="476" y="675">G1.1/2</text><text x="514" y="675">Drehkolbengebläse Belüftung BB, FU</text><text x="780" y="675">Aerzen/Roto, 1 Betr. + 1 Reserve</text>
  <line x1="468" y1="679" x2="1026" y2="679" stroke="#dce4f0" stroke-width="0.7"/>
  <text x="476" y="691">G2.1</text><text x="514" y="691">Sandfanggebläse (Luftheber)</text><text x="780" y="691">Drehkolbengebläse</text>
  <line x1="468" y1="695" x2="1026" y2="695" stroke="#dce4f0" stroke-width="0.7"/>
  <text x="476" y="707">Rw1.1</text><text x="514" y="707">Tauchmotorrührwerk Denizone</text><text x="780" y="707">ABS/Flygt, ~4 kW</text>
  <line x1="468" y1="711" x2="1026" y2="711" stroke="#dce4f0" stroke-width="0.7"/>
  <text x="476" y="723">R1.1</text><text x="514" y="723">Siebrechenanlage (mech. Reinigung)</text><text x="780" y="723">Treppenrechen / Bürstenrechen</text>
  <line x1="468" y1="727" x2="1026" y2="727" stroke="#dce4f0" stroke-width="0.7"/>
</g>
<text x="476" y="745" fill="#1a4080" font-size="8.5" font-weight="bold">MSR-Messgeräte:</text>
<g fill="#334860" font-size="7.8">
  <text x="476" y="760">FI 101</text><text x="528" y="760">Durchfluss Zulauf (MID / Ultraschall)</text>
  <text x="476" y="774">QI 102</text><text x="528" y="774">Spektralsonde Zulauf (UV/VIS → CSB, AFS)</text>
  <text x="476" y="788">LI 103</text><text x="528" y="788">Füllstand Pumpensumpf (Drucksensor)</text>
  <text x="476" y="802">FIC 201</text><text x="528" y="802">Luftdurchfluss Gebläsestation (Regelung)</text>
  <text x="476" y="816">QI 301</text><text x="528" y="816">O₂-Sonde Belebungsbecken Nitri-Zone</text>
  <text x="476" y="830">LI 401</text><text x="528" y="830">Schlammspiegelmessung NK (Ultraschall)</text>
  <text x="476" y="844">QI 501</text><text x="528" y="844">Ablaufanalyse CSB / NH₄-N / P-ges (online)</text>
  <text x="476" y="858">FI 502</text><text x="528" y="858">Ablauf-Durchfluss Messschacht (MID)</text>
  <text x="476" y="872">pH 504</text><text x="528" y="872">pH-Wert Ablauf (Glaselektrode)</text>
  <text x="476" y="886">QI 503</text><text x="528" y="886">Abschlagqualität (Regenüberlauf-Monitor)</text>
</g>

<!-- ─── ANMERKUNGEN ─── -->
<rect x="1038" y="480" width="556" height="424" rx="4" fill="#f8fafc" stroke="#1a3050" stroke-width="1.2"/>
<text x="1316" y="496" text-anchor="middle" fill="#1a4080" font-size="10" font-weight="bold">ANMERKUNGEN / VERFAHRENSSCHEMA</text>
<g font-size="8.5">
  <text x="1050" y="514" fill="#1a4080">Verfahren:</text>
  <text x="1050" y="527" fill="#334860">Vorklärung → Vorentst.-zone (Deni, anoxisch) → Nitrifikation (aerob)</text>
  <text x="1050" y="539" fill="#334860">→ Nachklärung → Simultanfällung P (FeCl₃) → Ablauf Vorfluter</text>
  <text x="1050" y="558" fill="#1a4080">Regelungen:</text>
  <text x="1050" y="570" fill="#334860">• O₂-Regelung: PID-Regler auf QI 301, Stellglied FU-Gebläse G1.1</text>
  <text x="1050" y="582" fill="#334860">• RS-Verhältnis: Stufenschaltung P3.1–P3.6, Sollwert ~0,75</text>
  <text x="1050" y="594" fill="#334860">• ÜS-Menge: Zeitprogramm P5.1, Schlammalter-gesteuert</text>
  <text x="1050" y="606" fill="#334860">• Fällmitteldos.: PI-Regler auf P-ges (QI 501), Stellglied P7.1</text>
  <text x="1050" y="618" fill="#334860">• Zulaufpumpe: FU-Regelung auf Füllstand LI 103</text>
  <text x="1050" y="630" fill="#334860">• Kalkmilch P9.1: Ein/Aus bei pH &lt; 6,8 / &gt; 7,2</text>
  <text x="1050" y="650" fill="#1a4080">Grenzwerte Ablauf (Eigenkontrolle):</text>
  <text x="1050" y="662" fill="#334860">• CSB &lt; 75 mg/L (GK 4)  |  BSB₅ &lt; 15 mg/L</text>
  <text x="1050" y="674" fill="#334860">• NH₄-N &lt; 10 mg/L  |  N-ges &lt; 18 mg/L</text>
  <text x="1050" y="686" fill="#334860">• P-ges &lt; 1,0 mg/L  |  AFS &lt; 15 mg/L</text>
  <text x="1050" y="706" fill="#1a4080">Besondere Betriebszustände:</text>
  <text x="1050" y="718" fill="#334860">• Mischwasserabschlag: SV201 öffnet bei Q_roh &gt; Abschlagschwelle</text>
  <text x="1050" y="730" fill="#334860">  → Direkteinleitung nach mech. Reinigung (Rechen + VK)</text>
  <text x="1050" y="742" fill="#334860">• Blähschlammgefahr: ISV &gt; 150 mL/g → ÜS erhöhen</text>
  <text x="1050" y="754" fill="#334860">• Turboverdichter (Mod.): ersetzt G1.1/G1.2, ~18 % Einsparung</text>
  <text x="1050" y="766" fill="#334860">• NH₄-gest. Belüftung (Mod.): O₂-Soll dynamisch geregelt</text>
  <text x="1050" y="778" fill="#334860">• Deammonifikation (Mod.): Seitenstromentstickung Prozesswasser</text>
  <text x="1050" y="798" fill="#1a4080">Schlamm:</text>
  <text x="1050" y="810" fill="#334860">• Primärschlamm: ~0,5 % von Q_ZU, TS ~35 g/L</text>
  <text x="1050" y="822" fill="#334860">• Rücklaufschlamm: Verhältnis ~0,75, TS ~8–12 g/L</text>
  <text x="1050" y="834" fill="#334860">• Überschussschlamm: ~200 m³/d, Schlammalter ~12–15 d</text>
  <text x="1050" y="846" fill="#334860">• PS + ÜS → Eindicker → Faulturm FT-1 (37 °C) → Entwässerung</text>
  <text x="1050" y="866" fill="#1a4080">Energetik:</text>
  <text x="1050" y="878" fill="#334860">• Gebläse ~50 %  |  Pumpen ~25–30 %  |  Schlamm, Gebäude ~20 %</text>
  <text x="1050" y="890" fill="#334860">• Eigenstrom BHKW (Faulgas) deckt ca. die Hälfte des Bedarfs</text>
</g>

</svg>
</div>''')

        # ====== AUSSENANLAGEN TAB ======
        # Externe Pumpwerke im Einzugsgebiet – Fernwirktechnik / Außenstation PLS
        rf = regen_faktor.value  # aktueller Regenfaktor aus Zulauf-Tab
        import math as _math

        # --- Kenndaten Druckrohrleitung DN 300 ---
        DN = 0.300  # m, Innendurchmesser
        A_DN = _math.pi * (DN / 2) ** 2  # m²
        v_TW = 0.6   # m/s bei Trockenwetter
        v_SR = 1.8   # m/s bei Starkregen
        Q_TW_Ls = A_DN * v_TW * 1000   # L/s  ≈ 42,4
        Q_SR_Ls = A_DN * v_SR * 1000   # L/s  ≈ 127,2

        # Aktuelle Fließgeschwindigkeit (linear zwischen TW und SR je nach Regenfaktor)
        # rf=1.0 → TW ; rf=3.0 → SR
        v_akt = v_TW + (v_SR - v_TW) * max(0, min(1, (rf - 1) / 2))
        Q_akt_Ls = A_DN * v_akt * 1000

        # --- Beckendaten Bahnhofstraße (Baujahr 1987, knapp dimensioniert) ---
        L_bhf, B_bhf, T_bhf = 8.0, 5.0, 5.0  # m
        V_bhf = L_bhf * B_bhf * T_bhf  # = 200 m³
        V_soll_SR = Q_SR_Ls / 1000 * 30 * 60  # Speicher 30 min bei SR ≈ 229 m³

        # Füllstand-Simulation: vereinfacht, nur Ist-Zustand als Funktion von rf
        # TW: Becken stabil bei ~25 %; RF=2: ~60 %; RF=3: ~95 %
        fuell_pct = min(98, 25 + (rf - 1) * 35)
        h_ist = fuell_pct / 100 * T_bhf
        V_ist = fuell_pct / 100 * V_bhf

        # Pumpen-Status
        pumpen_an = rf >= 1.2
        if rf < 1.2:
            pw_status, pw_status_farbe = "Grundlast (1 Pumpe intermittierend)", "#00b894"
        elif rf < 2.5:
            pw_status, pw_status_farbe = "Regenbetrieb (P1 Dauerlauf)", "#fdcb6e"
        else:
            pw_status, pw_status_farbe = "STARKREGEN – P1+P2 Volllast", "#e17055"

        # Warn-/Alarmschwelle
        if fuell_pct > 90:
            bhf_alarm = '<div class="pls-alarm" style="background:rgba(225,112,85,0.2);border-color:#e17055"><strong>🚨 KRITISCH:</strong> Beckenfüllstand > 90 % – Überlaufgefahr!</div>'
        elif fuell_pct > 70:
            bhf_alarm = '<div class="pls-alarm" style="background:rgba(253,203,110,0.15);border-color:#fdcb6e"><strong>⚠️ WARNUNG:</strong> Erhöhter Füllstand – Kapazitätsreserve prüfen</div>'
        else:
            bhf_alarm = ''

        # --- Andere Pumpwerke im Netz (Live-Deko, nur Übersicht) ---
        pw_ost_fuell = min(95, 30 + (rf - 1) * 25)
        tal = pm["talstrasse_sim"](hist, th, 12000.0)
        pw_tal_fuell = min(100.0, max(0.0, (tal["z"][-1] - pm["tal"]["z_sohle"]) / (pm["tal"]["z_nue"] - pm["tal"]["z_sohle"]) * 100))
        pw_ind_fuell = min(95, 20 + (rf - 1) * 30)

        def _pw_farbe(pct):
            if pct > 85: return "#e17055"
            if pct > 65: return "#fdcb6e"
            return "#00b894"

        # === NETZÜBERSICHT SVG ===
        netz_svg = f'''
        <svg viewBox="0 0 900 340" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto;background:#0a1428;border-radius:6px">
          <defs>
            <marker id="ah-net" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto">
              <polygon points="0 0,9 3.5,0 7" fill="#74b9ff"/>
            </marker>
            <pattern id="grid-net" width="40" height="40" patternUnits="userSpaceOnUse">
              <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#16213e" stroke-width="0.5"/>
            </pattern>
          </defs>
          <rect width="900" height="340" fill="url(#grid-net)"/>

          <!-- Titel -->
          <text x="20" y="28" fill="#74b9ff" font-size="14" font-weight="bold" font-family="monospace">Einzugsgebiet Meckelberg – Pumpwerksnetz (Live)</text>
          <text x="20" y="46" fill="#b2bec3" font-size="10" font-family="monospace">Regenfaktor aktuell: RF = {rf:.1f}</text>

          <!-- Fluss (Vorfluter) -->
          <path d="M 720,290 Q 760,280 790,300 Q 810,315 840,310" stroke="#3a6090" stroke-width="3" fill="none" opacity="0.6"/>
          <text x="775" y="285" fill="#3a6090" font-size="9" font-family="monospace">Vorfluter</text>

          <!-- KLÄRANLAGE (Zentrum rechts) -->
          <rect x="700" y="140" width="170" height="90" rx="6" fill="#16213e" stroke="#74b9ff" stroke-width="2"/>
          <text x="785" y="162" fill="#74b9ff" text-anchor="middle" font-size="12" font-weight="bold" font-family="monospace">KLÄRANLAGE</text>
          <text x="785" y="178" fill="#dfe6e9" text-anchor="middle" font-size="10" font-family="monospace">Musterstadt</text>
          <text x="785" y="198" fill="#dfe6e9" text-anchor="middle" font-size="9" font-family="monospace">50.000 EW</text>
          <text x="785" y="214" fill="#74b9ff" text-anchor="middle" font-size="9" font-family="monospace">Q = {c["Q_zu"]:.0f} m³/d</text>

          <!-- PW BAHNHOFSTRASSE -->
          <rect x="40" y="75" width="180" height="100" rx="6" fill="#16213e" stroke="#0984e3" stroke-width="1.5"/>
          <text x="130" y="96" fill="#74b9ff" text-anchor="middle" font-size="11" font-weight="bold" font-family="monospace">PW BAHNHOFSTRASSE</text>
          <text x="130" y="112" fill="#b2bec3" text-anchor="middle" font-size="9" font-family="monospace">KKS: APW-01</text>
          <!-- Füllstandsbalken -->
          <rect x="55" y="122" width="150" height="14" fill="#2d3436" stroke="#0f3460" stroke-width="1"/>
          <rect x="55" y="122" width="{1.5 * fuell_pct}" height="14" fill="{_pw_farbe(fuell_pct)}"/>
          <text x="130" y="133" fill="#ffffff" text-anchor="middle" font-size="9" font-weight="bold" font-family="monospace">FÜLLSTAND {fuell_pct:.0f} %</text>
          <text x="130" y="154" fill="#dfe6e9" text-anchor="middle" font-size="9" font-family="monospace">Q_zu = {Q_akt_Ls:.0f} L/s</text>
          <text x="130" y="168" fill="{pw_status_farbe}" text-anchor="middle" font-size="9" font-family="monospace">{pw_status.split(" (")[0]}</text>

          <!-- Druckleitung zur KA -->
          <line x1="220" y1="125" x2="700" y2="175" stroke="#74b9ff" stroke-width="2" marker-end="url(#ah-net)" stroke-dasharray="4,3"/>
          <text x="430" y="142" fill="#74b9ff" font-size="9" font-family="monospace">DN 300 Druckleitung</text>

          <!-- PW OST -->
          <rect x="40" y="195" width="150" height="70" rx="6" fill="#16213e" stroke="#0984e3" stroke-width="1.5"/>
          <text x="115" y="214" fill="#74b9ff" text-anchor="middle" font-size="10" font-weight="bold" font-family="monospace">PW OST</text>
          <text x="115" y="228" fill="#b2bec3" text-anchor="middle" font-size="8" font-family="monospace">KKS: APW-02</text>
          <rect x="50" y="236" width="130" height="10" fill="#2d3436" stroke="#0f3460" stroke-width="1"/>
          <rect x="50" y="236" width="{1.3 * pw_ost_fuell}" height="10" fill="{_pw_farbe(pw_ost_fuell)}"/>
          <text x="115" y="259" fill="#dfe6e9" text-anchor="middle" font-size="9" font-family="monospace">{pw_ost_fuell:.0f} %</text>
          <line x1="190" y1="225" x2="700" y2="195" stroke="#3a6090" stroke-width="1.5" marker-end="url(#ah-net)" stroke-dasharray="4,3"/>

          <!-- PW TALSTRASSE (Pumpstation mit 2 Pumpen → 2 Speicherbecken → Freigefälle zur KA) -->
          <rect x="260" y="220" width="190" height="90" rx="6" fill="#16213e" stroke="#0984e3" stroke-width="1.5"/>
          <text x="355" y="240" fill="#74b9ff" text-anchor="middle" font-size="10" font-weight="bold" font-family="monospace">PW TALSTRASSE</text>
          <text x="355" y="253" fill="#b2bec3" text-anchor="middle" font-size="8" font-family="monospace">KKS: APW-03 · 2 × KSB Sewabloc F 100</text>
          <rect x="270" y="262" width="170" height="10" fill="#2d3436" stroke="#0f3460" stroke-width="1"/>
          <rect x="270" y="262" width="{1.7 * pw_tal_fuell}" height="10" fill="{_pw_farbe(pw_tal_fuell)}"/>
          <text x="355" y="285" fill="#dfe6e9" text-anchor="middle" font-size="9" font-family="monospace">Füllstand Pumpensumpf {pw_tal_fuell:.0f} %</text>
          <text x="355" y="300" fill="#b2bec3" text-anchor="middle" font-size="8" font-family="monospace">Druckleitung → B-002 / B-003 → Freigefälle</text>

          <!-- Speicherbecken B-002 und B-003 als Zwischenstation -->
          <ellipse cx="535" cy="235" rx="28" ry="11" fill="#1a2a4a" stroke="#74b9ff" stroke-width="1" stroke-dasharray="2,2"/>
          <text x="535" y="238" fill="#b2bec3" text-anchor="middle" font-size="7.5" font-family="monospace">B-002</text>
          <ellipse cx="535" cy="278" rx="28" ry="11" fill="#1a2a4a" stroke="#74b9ff" stroke-width="1" stroke-dasharray="2,2"/>
          <text x="535" y="281" fill="#b2bec3" text-anchor="middle" font-size="7.5" font-family="monospace">B-003</text>
          <text x="535" y="306" fill="#b2bec3" text-anchor="middle" font-size="7" font-family="monospace">Speicherbecken</text>

          <!-- Druckleitung: PW Talstraße → Speicherbecken (gestrichelt, Druck) -->
          <line x1="450" y1="245" x2="507" y2="235" stroke="#0984e3" stroke-width="1.5" stroke-dasharray="4,3"/>
          <line x1="450" y1="265" x2="507" y2="278" stroke="#0984e3" stroke-width="1.5" stroke-dasharray="4,3"/>
          <!-- Freigefälle: Speicherbecken → KA (durchgezogen) -->
          <line x1="563" y1="235" x2="700" y2="195" stroke="#3a6090" stroke-width="1.5" marker-end="url(#ah-net)"/>
          <line x1="563" y1="278" x2="700" y2="210" stroke="#3a6090" stroke-width="1.5" marker-end="url(#ah-net)"/>
          <text x="630" y="247" fill="#3a6090" font-size="8" font-family="monospace">FG</text>

          <!-- PW INDUSTRIEPARK -->
          <rect x="460" y="75" width="180" height="70" rx="6" fill="#16213e" stroke="#0984e3" stroke-width="1.5"/>
          <text x="550" y="94" fill="#74b9ff" text-anchor="middle" font-size="10" font-weight="bold" font-family="monospace">PW INDUSTRIEPARK</text>
          <text x="550" y="108" fill="#b2bec3" text-anchor="middle" font-size="8" font-family="monospace">KKS: APW-04</text>
          <rect x="475" y="116" width="150" height="10" fill="#2d3436" stroke="#0f3460" stroke-width="1"/>
          <rect x="475" y="116" width="{1.5 * pw_ind_fuell}" height="10" fill="{_pw_farbe(pw_ind_fuell)}"/>
          <text x="550" y="139" fill="#dfe6e9" text-anchor="middle" font-size="9" font-family="monospace">{pw_ind_fuell:.0f} %</text>
          <line x1="640" y1="110" x2="700" y2="165" stroke="#3a6090" stroke-width="1.5" marker-end="url(#ah-net)" stroke-dasharray="4,3"/>

          <!-- Legende -->
          <rect x="40" y="285" width="200" height="30" rx="3" fill="#16213e" stroke="#0f3460" stroke-width="1"/>
          <text x="50" y="304" fill="#b2bec3" font-size="8" font-family="monospace">Füllstand: grün &lt; 65 %, gelb &lt; 85 %, rot &gt; 85 %</text>
        </svg>
        '''

        # === PW-AUSWAHL ===
        # (Aktuell ist nur Bahnhofstraße detailliert ausgebaut – andere PW zeigen Platzhalter)
        # Dropdown mit mo.ui.dropdown wäre optimal, braucht aber eigene Zelle oben.

        # === DETAIL BAHNHOFSTRASSE ===
        bhf_live_html = f'''
        <div class="pls-c">
          <h3>📡 Live-Werte PW Bahnhofstraße (Außenstation APW-01)</h3>
          {bhf_alarm}
          <table class="pls-tbl">
            <tr><td>Füllstand Sammelbecken</td><td class="c-v">{fuell_pct:.0f} % ({h_ist:.2f} m / {T_bhf:.1f} m)</td></tr>
            <tr><td>Füllvolumen aktuell</td><td class="c-v">{V_ist:.0f} m³ / {V_bhf:.0f} m³</td></tr>
            <tr><td>Zulauf (Druckrohr DN 300)</td><td class="c-v">{Q_akt_Ls:.1f} L/s</td></tr>
            <tr><td>Fließgeschw. aktuell</td><td class="c-v">{v_akt:.2f} m/s</td></tr>
            <tr><td>Pumpenstatus</td><td style="color:{pw_status_farbe};font-weight:bold;text-align:right">{pw_status}</td></tr>
            <tr><td>Betriebsstunden P1</td><td class="c-v">{26480 + int(th * 0.4):,} h</td></tr>
            <tr><td>Betriebsstunden P2</td><td class="c-v">{3120 + int(th * 0.05):,} h</td></tr>
          </table>
          <div class="pls-bar" style="margin-top:10px"><div class="pls-bar-f" style="width:{fuell_pct:.0f}%;background:{_pw_farbe(fuell_pct)}"></div></div>
          <p style="font-size:0.78em;color:#b2bec3;margin:6px 0 0 0">
            Fernwirk-Status: OK · letzter Telegrammempfang vor {1 + int(th * 0.01) % 5} s · Verbindung LWL
          </p>
        </div>
        '''

        # === BAUWERKSDATENBLATT ===
        bhf_datenblatt_html = f'''
        <div class="pls-c" style="background:#fffef5;color:#1a1a2e;border:2px solid #5a4820">
          <div style="display:flex;justify-content:space-between;align-items:flex-start;border-bottom:2px solid #1a1a2e;padding-bottom:6px;margin-bottom:8px">
            <div>
              <div style="font-size:0.75em;color:#5a4820;letter-spacing:2px">STADT MECKELBERG – ABWASSERBETRIEB</div>
              <div style="font-size:1.1em;font-weight:bold;color:#1a1a2e">BAUWERKSDATENBLATT</div>
            </div>
            <div style="text-align:right;font-size:0.75em;color:#5a4820">
              Blatt Nr.: APW-01/DB-02<br>
              Stand: 03/2021<br>
              Archiv: Ordner 47/B
            </div>
          </div>
          <h3 style="color:#1a1a2e;border-color:#5a4820;margin:8px 0">Pumpwerk Bahnhofstraße – Sammelbecken</h3>
          <table style="width:100%;border-collapse:collapse;font-size:0.88em;color:#1a1a2e">
            <tr><td style="padding:4px 12px;color:#5a4820;width:45%">Anlagenkennzeichen (KKS)</td><td style="padding:4px 12px;font-weight:bold">APW-01</td></tr>
            <tr style="background:#f5f0d8"><td style="padding:4px 12px;color:#5a4820">Baujahr</td><td style="padding:4px 12px;font-weight:bold">1987</td></tr>
            <tr><td style="padding:4px 12px;color:#5a4820">Bauart</td><td style="padding:4px 12px;font-weight:bold">Stahlbeton, rechteckig, unterirdisch</td></tr>
            <tr style="background:#f5f0d8"><td style="padding:4px 12px;color:#5a4820">Becken – Länge (innen)</td><td style="padding:4px 12px;font-weight:bold">L = 8,00 m</td></tr>
            <tr><td style="padding:4px 12px;color:#5a4820">Becken – Breite (innen)</td><td style="padding:4px 12px;font-weight:bold">B = 5,00 m</td></tr>
            <tr style="background:#f5f0d8"><td style="padding:4px 12px;color:#5a4820">Becken – nutzbare Tiefe</td><td style="padding:4px 12px;font-weight:bold">T = 5,00 m</td></tr>
            <tr><td style="padding:4px 12px;color:#5a4820">Zulauf</td><td style="padding:4px 12px;font-weight:bold">Druckrohrleitung DN 300</td></tr>
            <tr style="background:#f5f0d8"><td style="padding:4px 12px;color:#5a4820">Fließgeschw. Trockenwetter</td><td style="padding:4px 12px;font-weight:bold">v_TW = 0,60 m/s</td></tr>
            <tr><td style="padding:4px 12px;color:#5a4820">Fließgeschw. Starkregen</td><td style="padding:4px 12px;font-weight:bold">v_SR = 1,80 m/s</td></tr>
            <tr style="background:#f5f0d8"><td style="padding:4px 12px;color:#5a4820">Förderpumpen</td><td style="padding:4px 12px;font-weight:bold">2 × Tauchmotor-KP (1 Betrieb, 1 Reserve)</td></tr>
            <tr><td style="padding:4px 12px;color:#5a4820">Einleitung nach</td><td style="padding:4px 12px;font-weight:bold">KA Musterstadt, Hauptzulauf</td></tr>
          </table>
          <p style="font-size:0.78em;color:#5a4820;margin:10px 0 0 0;font-style:italic;border-top:1px dashed #5a4820;padding-top:6px">
            Anmerkung: Unterlagen aus dem Bauarchiv. Geometrieangaben aus
            Bestandsplan 1987 (vor Sanierung Dacheindeckung 2003). Spätere
            Umbauten am Sammelbecken selbst nicht dokumentiert.
          </p>
        </div>
        '''

        # === HANDSKIZZE (als SVG, absichtlich "grob") ===
        # Leicht verzogene Linien + handschriftliche Anmutung (Times als Schreibschrift-Ersatz)
        bhf_skizze_svg = '''
        <div class="pls-c" style="background:#f7f3e8;color:#2c1810;border:2px solid #5a4820">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px">
            <div style="font-size:0.85em;color:#5a4820;font-weight:bold">📐 Grobe Skizze aus Bauarchiv (Bestand)</div>
            <div style="font-size:0.7em;color:#5a4820;border:1.5px dashed #8a5020;padding:2px 8px;transform:rotate(-3deg);display:inline-block">ARCHIV · 1987</div>
          </div>
          <svg viewBox="0 0 600 340" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto;background:#f7f3e8;border:1px solid #c8b080;border-radius:4px">
            <!-- Karopapier-Raster -->
            <defs>
              <pattern id="karo" width="20" height="20" patternUnits="userSpaceOnUse">
                <path d="M 20 0 L 0 0 0 20" fill="none" stroke="#d4c090" stroke-width="0.4"/>
              </pattern>
            </defs>
            <rect width="600" height="340" fill="url(#karo)"/>

            <!-- TITEL (handschriftlich) -->
            <text x="20" y="30" fill="#2c1810" font-size="15" font-family="Georgia, serif" font-style="italic" font-weight="bold">Sammelbecken Bahnhofstr. - Seitenansicht</text>

            <!-- Becken-Seitenansicht (leicht wackelige Linien durch kleine Offsets) -->
            <!-- Oberkante -->
            <path d="M 60,80 L 360,82 L 361,79 L 359,81" stroke="#2c1810" stroke-width="2" fill="none" stroke-linecap="round"/>
            <!-- Unterkante -->
            <path d="M 58,230 L 362,231 L 361,228" stroke="#2c1810" stroke-width="2" fill="none" stroke-linecap="round"/>
            <!-- linke Wand -->
            <path d="M 60,80 L 59,230 L 61,229" stroke="#2c1810" stroke-width="2" fill="none" stroke-linecap="round"/>
            <!-- rechte Wand -->
            <path d="M 360,82 L 361,231 L 359,230" stroke="#2c1810" stroke-width="2" fill="none" stroke-linecap="round"/>

            <!-- Wasserlinie (Wellen) -->
            <path d="M 65,150 Q 85,145 105,150 T 145,150 T 185,150 T 225,150 T 265,150 T 305,150 T 345,150 T 358,150" stroke="#3a6090" stroke-width="1.3" fill="none" opacity="0.6"/>
            <!-- Wasser-Schraffur -->
            <g stroke="#3a6090" stroke-width="0.5" opacity="0.35">
              <line x1="70" y1="165" x2="80" y2="155"/>
              <line x1="100" y1="175" x2="110" y2="165"/>
              <line x1="140" y1="170" x2="150" y2="160"/>
              <line x1="180" y1="180" x2="190" y2="170"/>
              <line x1="220" y1="165" x2="230" y2="155"/>
              <line x1="260" y1="180" x2="270" y2="170"/>
              <line x1="300" y1="170" x2="310" y2="160"/>
              <line x1="340" y1="175" x2="350" y2="165"/>
              <line x1="90" y1="195" x2="100" y2="185"/>
              <line x1="170" y1="200" x2="180" y2="190"/>
              <line x1="250" y1="205" x2="260" y2="195"/>
              <line x1="330" y1="200" x2="340" y2="190"/>
            </g>

            <!-- Zulauf-Rohr (Druckrohr DN 300), von links oben -->
            <path d="M 10,100 L 60,100" stroke="#2c1810" stroke-width="2.5" fill="none"/>
            <path d="M 10,120 L 60,120" stroke="#2c1810" stroke-width="2.5" fill="none"/>
            <text x="15" y="95" fill="#2c1810" font-size="11" font-family="Georgia, serif" font-style="italic">DN 300</text>
            <!-- Pfeil Richtung Zulauf -->
            <path d="M 25,110 L 45,110" stroke="#a03040" stroke-width="1.5" fill="none" marker-end="url(#sk-arrow)"/>
            <defs>
              <marker id="sk-arrow" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
                <polygon points="0 0,8 3,0 6" fill="#a03040"/>
              </marker>
            </defs>
            <text x="20" y="138" fill="#a03040" font-size="10" font-family="Georgia, serif" font-style="italic">Zulauf</text>

            <!-- Pumpensumpf am Boden rechts + Pumpe -->
            <path d="M 300,230 L 300,260 L 360,260 L 360,230" stroke="#2c1810" stroke-width="1.5" fill="none"/>
            <circle cx="330" cy="280" r="12" fill="none" stroke="#2c1810" stroke-width="2"/>
            <text x="330" y="285" fill="#2c1810" font-size="13" font-family="Georgia, serif" text-anchor="middle" font-weight="bold">P</text>
            <text x="370" y="283" fill="#2c1810" font-size="10" font-family="Georgia, serif" font-style="italic">Pumpe</text>
            <!-- Förderleitung nach oben rechts raus -->
            <path d="M 330,268 L 330,240 L 410,240 L 410,60 L 450,60" stroke="#2c1810" stroke-width="1.8" fill="none"/>
            <text x="420" y="52" fill="#2c1810" font-size="10" font-family="Georgia, serif" font-style="italic">zur KA</text>

            <!-- Maßlinien -->
            <!-- Länge L (unten) -->
            <line x1="60" y1="255" x2="360" y2="255" stroke="#5a4820" stroke-width="0.8"/>
            <line x1="60" y1="250" x2="60" y2="260" stroke="#5a4820" stroke-width="0.8"/>
            <line x1="360" y1="250" x2="360" y2="260" stroke="#5a4820" stroke-width="0.8"/>
            <text x="210" y="275" fill="#5a4820" font-size="13" font-family="Georgia, serif" font-style="italic" text-anchor="middle">L ≈ 8,00 m</text>
            <!-- Tiefe T (rechts) -->
            <line x1="385" y1="80" x2="385" y2="230" stroke="#5a4820" stroke-width="0.8"/>
            <line x1="380" y1="80" x2="390" y2="80" stroke="#5a4820" stroke-width="0.8"/>
            <line x1="380" y1="230" x2="390" y2="230" stroke="#5a4820" stroke-width="0.8"/>
            <text x="400" y="160" fill="#5a4820" font-size="13" font-family="Georgia, serif" font-style="italic">T ≈ 5,00 m</text>

            <!-- Draufsicht (klein, rechts unten) -->
            <text x="470" y="95" fill="#2c1810" font-size="11" font-family="Georgia, serif" font-style="italic">Draufsicht:</text>
            <path d="M 475,105 L 575,106 L 576,166 L 474,165 L 475,105" stroke="#2c1810" stroke-width="1.5" fill="none"/>
            <line x1="480" y1="170" x2="570" y2="170" stroke="#5a4820" stroke-width="0.6"/>
            <text x="525" y="183" fill="#5a4820" font-size="10" font-family="Georgia, serif" font-style="italic" text-anchor="middle">L ≈ 8,00 m</text>
            <line x1="585" y1="110" x2="585" y2="160" stroke="#5a4820" stroke-width="0.6"/>
            <text x="595" y="140" fill="#5a4820" font-size="10" font-family="Georgia, serif" font-style="italic">B ≈ 5 m</text>

            <!-- Notiz unten -->
            <text x="20" y="315" fill="#8a5020" font-size="10" font-family="Georgia, serif" font-style="italic">Handskizze H. Breitenbach, Stadt Meckelberg, 14.09.1987 – n. maßstäblich!</text>

            <!-- Kaffeefleck zur Deko :-) -->
            <circle cx="540" cy="260" r="22" fill="#8a5020" opacity="0.12"/>
            <circle cx="540" cy="260" r="16" fill="#8a5020" opacity="0.15"/>
          </svg>
        </div>
        '''

        # === DETAIL PW TALSTRASSE (APW-03): Schaltbetrieb, Messwerte, Trend, Datenblatt ===
        tal_cfg = pm["tal"]
        tal_z = tal["z"][-1]
        tal_on1 = tal["on1"][-1]
        tal_on2 = tal["on2"][-1]
        tal_hgeo = pm["standorte"]["APW03"]["z_aus"] - tal_z
        tal_m1 = lp_mess("P-001", tal_on1, tal_z - tal_cfg["z_achse"], 2 if tal_on2 else 1, tal_hgeo)
        tal_m2 = lp_mess("P-002", tal_on2, tal_z - tal_cfg["z_achse"], 2, tal_hgeo)
        tal_vsb = tal["v_sb"][-1]
        tal_nue = any(tal["nue"][-30:])
        tal_ueb = any(tal["ueb"][-30:])
        if tal_on1 and tal_on2:
            tal_zust, tal_farbe = "P-001 + P-002 Parallelbetrieb", "#fdcb6e"
        elif tal_on1:
            tal_zust, tal_farbe = "P-001 in Betrieb", "#00b894"
        else:
            tal_zust, tal_farbe = "Pumpen aus – Sumpf füllt", "#b2bec3"
        tal_alarm = ""
        if tal_nue:
            tal_alarm += '<div class="pls-alarm"><strong>🚨 Notüberlauf Pumpensumpf APW-03 aktiv</strong> – Zufluss übersteigt Förderleistung</div>'
        if tal_ueb:
            tal_alarm += '<div class="pls-alarm"><strong>⚠️ Speicherbecken B-002/B-003 voll</strong> – Beckenüberlauf aktiv</div>'
        tal_messort = ("APW03-PI 11/12 (P-001), APW03-PI 13/14 (P-002) in Saug- bzw. Druckleitung je DN 200, "
                       "Messstellen auf Höhe Pumpenachse +51,80 m NHN")
        tal_zust_row = ('<tr><td style="padding:3px 8px 3px 0;color:#b2bec3;white-space:nowrap">Betriebszustand</td>'
                        f'<td style="padding:3px 0 3px 8px;white-space:nowrap;font-weight:bold;color:{tal_farbe}">{tal_zust}</td></tr>')
        tal_drossel = tal_cfg["q_dr"] if tal_vsb > 1 else 0.0
        tal_live_html = f'''<div class="pls-c">
            <h3>📡 Live-Werte PW Talstraße (Außenstation APW-03)</h3>
            {tal_alarm}
            {vtbl(
                vr("Füllstand Pumpensumpf APW03-LI 01", f"{tal_z:.2f}", "m NHN")
                + vr("Förderstrom Druckleitung APW03-FI 01", f"{tal_m1['q'] + tal_m2['q']:.1f}", "m³/h")
                + tal_zust_row
                + vr("Füllstand Speicherbecken B-002/B-003 APW03-LI 02", f"{tal_vsb / tal_cfg['V_sb'] * 100:.0f}", "%")
                + vr("Drosselabfluss zur KA APW03-FI 02", f"{tal_drossel:.1f}", "m³/h")
            )}
            <p style="font-size:0.78em;color:#b2bec3;margin:6px 0 0 0">
                Fernwirk-Status: OK · Datenübertragung zyklisch 60 s · Verbindung LWL
            </p>
        </div>'''

        tal_datenblatt_html = '''
        <div class="pls-c" style="background:#fffef5;color:#1a1a2e;border:2px solid #5a4820">
          <div style="display:flex;justify-content:space-between;align-items:flex-start;border-bottom:2px solid #1a1a2e;padding-bottom:6px;margin-bottom:8px">
            <div>
              <div style="font-size:0.75em;color:#5a4820;letter-spacing:2px">STADT MECKELBERG – ABWASSERBETRIEB</div>
              <div style="font-size:1.1em;font-weight:bold;color:#1a1a2e">BAUWERKSDATENBLATT</div>
            </div>
            <div style="text-align:right;font-size:0.75em;color:#5a4820">
              Blatt Nr.: APW-03/DB-01<br>Stand: 04/2012<br>Archiv: Ordner 51/A
            </div>
          </div>
          <h3 style="color:#1a1a2e;border-color:#5a4820;margin:8px 0">Pumpwerk Talstraße mit Speicherbecken B-002 / B-003</h3>
          <table style="border-collapse:collapse;font-size:0.86em;color:#1a1a2e">
            <tr><td style="padding:4px 12px;color:#5a4820">Anlagenkennzeichen (KKS)</td><td style="padding:4px 12px;font-weight:bold">APW-03</td></tr>
            <tr style="background:#f5f0d8"><td style="padding:4px 12px;color:#5a4820">Baujahr Bauwerk / Pumpentausch</td><td style="padding:4px 12px;font-weight:bold">1998 / 2012</td></tr>
            <tr><td style="padding:4px 12px;color:#5a4820">Bauart</td><td style="padding:4px 12px;font-weight:bold">Nasssumpf, Pumpen trocken aufgestellt (Pumpenkammer)</td></tr>
            <tr style="background:#f5f0d8"><td style="padding:4px 12px;color:#5a4820">Pumpensumpf, Grundfläche (innen)</td><td style="padding:4px 12px;font-weight:bold">5,00 m × 5,00 m</td></tr>
            <tr><td style="padding:4px 12px;color:#5a4820">Sohle Pumpensumpf</td><td style="padding:4px 12px;font-weight:bold">+53,90 m NHN</td></tr>
            <tr style="background:#f5f0d8"><td style="padding:4px 12px;color:#5a4820">Pumpenachse</td><td style="padding:4px 12px;font-weight:bold">+51,80 m NHN</td></tr>
            <tr><td style="padding:4px 12px;color:#5a4820">Schaltpunkte P-001 (Ein / Aus)</td><td style="padding:4px 12px;font-weight:bold">+55,40 / +54,60 m NHN</td></tr>
            <tr style="background:#f5f0d8"><td style="padding:4px 12px;color:#5a4820">Schaltpunkte P-002 (Ein / Aus)</td><td style="padding:4px 12px;font-weight:bold">+55,80 / +55,10 m NHN</td></tr>
            <tr><td style="padding:4px 12px;color:#5a4820">Hochwasseralarm / Notüberlauf</td><td style="padding:4px 12px;font-weight:bold">+56,20 / +56,60 m NHN</td></tr>
            <tr style="background:#f5f0d8"><td style="padding:4px 12px;color:#5a4820">Förderpumpen</td><td style="padding:4px 12px;font-weight:bold">2 × KSB Sewabloc F 100-316 (P-001 Grundlast, P-002 Spitzenlast/Reserve)</td></tr>
            <tr><td style="padding:4px 12px;color:#5a4820">Druckleitung</td><td style="padding:4px 12px;font-weight:bold">DN 200, GGG, L ≈ 1.650 m (Bj. 1998)</td></tr>
            <tr style="background:#f5f0d8"><td style="padding:4px 12px;color:#5a4820">Zweigleitungen zu B-002 / B-003</td><td style="padding:4px 12px;font-weight:bold">DN 125, je ca. 40 m</td></tr>
            <tr><td style="padding:4px 12px;color:#5a4820">Einlauf Speicherbecken (freier Auslauf)</td><td style="padding:4px 12px;font-weight:bold">+75,00 m NHN</td></tr>
            <tr style="background:#f5f0d8"><td style="padding:4px 12px;color:#5a4820">Speicherbecken B-002 / B-003</td><td style="padding:4px 12px;font-weight:bold">je 400 m³, Stahlbeton, offen</td></tr>
            <tr><td style="padding:4px 12px;color:#5a4820">Ablauf Speicherbecken</td><td style="padding:4px 12px;font-weight:bold">Freigefälle DN 250 zur KA, Drosselabfluss ca. 42 m³/h</td></tr>
          </table>
          <p style="font-size:0.78em;color:#5a4820;margin:10px 0 0 0;font-style:italic;border-top:1px dashed #5a4820;padding-top:6px">
            Anmerkung: Höhenangaben aus Bestandsvermessung 1998. Pumpen 2012 gegen KSB-Aggregate getauscht,
            Rohrleitungen und Armaturen im Bestand belassen. Erneuerung der Druckleitung in Planung.
          </p>
        </div>'''

        import plotly.graph_objects as _tgo
        from plotly.subplots import make_subplots as _tmp
        _rho_t = lp_agg["P-001"]["rho"]
        _ps = [_rho_t * 9.81 * (zz - tal_cfg["z_achse"]) / 1e5 for zz in tal["z"]]
        _pd = [p + (_rho_t * 9.81 * hh / 1e5 if o else 0.0) for p, hh, o in zip(_ps, tal["h1"], tal["on1"])]
        fig_tal = _tmp(rows=4, cols=1, shared_xaxes=True, vertical_spacing=0.06,
                       subplot_titles=("Füllstand Pumpensumpf APW03-LI 01 [m NHN]",
                                       "Förderstrom Druckleitung APW03-FI 01 [m³/h]",
                                       "Druck druckseitig P-001 APW03-PI 12 [bar]",
                                       "Füllstand Speicherbecken B-002/B-003 APW03-LI 02 [m³]"))
        fig_tal.add_trace(_tgo.Scatter(x=tal["t"], y=tal["z"], mode="lines", line=dict(color="#74b9ff", width=1.4)), row=1, col=1)
        for _zz, _lab in [(tal_cfg["z_ein1"], "Ein P-001"), (tal_cfg["z_aus1"], "Aus P-001"), (tal_cfg["z_ein2"], "Ein P-002")]:
            fig_tal.add_hline(y=_zz, line_dash="dot", line_color="#636e72", row=1, col=1,
                              annotation_text=_lab, annotation_position="top left",
                              annotation_font_size=8, annotation_font_color="#b2bec3")
        fig_tal.add_trace(_tgo.Scatter(x=tal["t"], y=tal["q"], mode="lines", line=dict(color="#00b894", width=1.2), line_shape="hv"), row=2, col=1)
        fig_tal.add_trace(_tgo.Scatter(x=tal["t"], y=_pd, mode="lines", line=dict(color="#fdcb6e", width=1.2), line_shape="hv"), row=3, col=1)
        fig_tal.add_trace(_tgo.Scatter(x=tal["t"], y=tal["v_sb"], mode="lines", line=dict(color="#a29bfe", width=1.4)), row=4, col=1)
        fig_tal.update_layout(height=640, template="plotly_dark", paper_bgcolor="#1a1a2e", plot_bgcolor="#16213e",
                              showlegend=False, font=dict(family="Consolas,monospace", size=10, color="#dfe6e9"),
                              margin=dict(t=35, b=35, l=55, r=20))
        fig_tal.update_xaxes(gridcolor="#0f3460")
        fig_tal.update_xaxes(title_text="Simulationszeit [h]", row=4, col=1)
        fig_tal.update_yaxes(gridcolor="#0f3460")
        fig_tal.update_annotations(font_size=10)

        talstrasse_detail = mo.vstack([
            mo.Html(f'''<div class="pls"><div class="pls-g2">
                <div>{tal_live_html}</div>
                <div>{tal_datenblatt_html}</div>
            </div></div>'''),
            mo.Html(f'''<div class="pls"><div class="pls-g2">
                {lp_faceplate("P-001", tal_m1, tal_on1, tal["bh1"], tal["lz1"], tal["sp1"], tal_messort, q_fi=tal_m1["q"] + tal_m2["q"])}
                {lp_faceplate("P-002", tal_m2, tal_on2, tal["bh2"], tal["lz2"], tal["sp2"], tal_messort, q_fi=tal_m1["q"] + tal_m2["q"])}
            </div></div>'''),
            mo.Html('<div class="pls"><div class="pls-c"><h3>📈 Trend PW Talstraße – letzte 48 h (Fernwirk-Archiv, 2-min-Werte)</h3></div></div>'),
            fig_tal,
        ])

        aussenanlagen = mo.vstack([
            # Netzübersicht oben
            mo.Html(f'''<div class="pls"><div class="pls-c">
                <h3>🗺️ Netzübersicht – Pumpwerke im Einzugsgebiet Meckelberg</h3>
                <p style="font-size:0.85em;color:#b2bec3;margin:0 0 8px 0">
                    Die Außenstationen werden per Fernwirktechnik (Funk / LWL) an das zentrale PLS
                    der Kläranlage angebunden. Jedes Pumpwerk verfügt über ein Sammelbecken und
                    Förderpumpen. Bei Regenfaktor RF &gt; 1,5 steigen Zuflüsse und Füllstände deutlich.
                </p>
                {netz_svg}
            </div></div>'''),

            # Detailansicht PW Bahnhofstraße: Live-Werte + Bauwerksdatenblatt
            mo.Html(f'''<div class="pls"><div class="pls-g2">
                <div>{bhf_live_html}</div>
                <div>{bhf_datenblatt_html}</div>
            </div></div>'''),

            # Handskizze aus Bauarchiv
            mo.Html(f'<div class="pls">{bhf_skizze_svg}</div>'),

            # Detailansicht PW Talstraße
            mo.Html('<div class="pls"><div class="pls-c" style="border-color:#0984e3"><h3 style="color:#74b9ff">🏗️ PW Talstraße (APW-03) – Detailansicht</h3></div></div>'),
            talstrasse_detail,

            # Hinweis zu den anderen Pumpwerken (neutral, ohne didaktischen Bezug)
            mo.Html('''<div class="pls"><div class="pls-c" style="border-color:#0984e3">
                <h3 style="color:#74b9ff">ℹ️ Weitere Pumpwerke (PW Ost, PW Industriepark)</h3>
                <p style="font-size:0.85em;color:#b2bec3;margin:0">
                    Für diese Außenstationen liegen aktuell nur die Live-Füllstände auf der Netzübersicht
                    vor. Ausführliche Bauwerksdatenblätter können auf Anforderung aus dem Bauarchiv
                    bereitgestellt werden.
                </p>
            </div></div>'''),
        ])

        # ====== ARMATUREN TAB ======
        # Zentraler Armaturen-Katalog der Gesamtanlage.
        # Jede Armatur hat Stammdaten (Typenschild), Betriebsdaten und einen Zustand.
        # SuS können eine Armatur auswählen und einen Wartungsauftrag an die Leitwarte senden.
        _th = th  # Simulationsstunden für Betriebsstunden-Fortschreibung

        ARMATUREN = {
            # --- HEBEWERK / MECHANISCHE REINIGUNG ---
            "HS-101": dict(
                kks="HS-101", kurz="Plattenschieber", einbau="Zulauf zum Pumpensumpf / Hebewerk",
                anlagenteil="Mech. Reinigung", hersteller="KSB", modell="HERA-BD",
                dn=300, pn=10, werkstoff="5.3106 / EPDM", baujahr=2020, serien="123456",
                medium="Abwasser", t_max=60, p_max=5, antrieb="Handrad",
                stellung="AUF", bh=32850, wartung="06/2023",
                zustand="defekt",
                meldung="Mechanischer Schaden – Bügel verformt, Handrad schwergängig. Seit 14:22 Uhr nicht mehr bedienbar.",
            ),
            "SV-201": dict(
                kks="SV-201", kurz="Regelklappe (motorisch)", einbau="Regenüberlauf / Mischwasserabschlag",
                anlagenteil="Mech. Reinigung", hersteller="Adams Armaturen", modell="REV MC",
                dn=400, pn=10, werkstoff="EN-GJS-400 / NBR", baujahr=2015, serien="A-47821",
                medium="Mischwasser", t_max=50, p_max=2, antrieb="E-Stellantrieb 24 V",
                stellung="ZU (Abschlag inaktiv)" if c.get("Q_abschlag", 0) < 10 else "TEILHUB",
                bh=59120, wartung="09/2024", zustand="ok", meldung="",
            ),
            "HS-202": dict(
                kks="HS-202", kurz="Plattenschieber", einbau="Zulauf Vorklärung VK1",
                anlagenteil="Mech. Reinigung", hersteller="KSB", modell="HERA-BD",
                dn=400, pn=10, werkstoff="5.3106 / EPDM", baujahr=2015, serien="098112",
                medium="Rohabwasser", t_max=60, p_max=5, antrieb="E-Stellantrieb / Handrad",
                stellung="AUF", bh=73410, wartung="04/2024", zustand="ok", meldung="",
            ),
            "RK-301": dict(
                kks="RK-301", kurz="Rückschlagklappe", einbau="Druckstutzen Zulaufpumpe P1.1",
                anlagenteil="Mech. Reinigung", hersteller="ERHARD", modell="ROCO wave",
                dn=300, pn=10, werkstoff="EN-GJS-500 / EPDM", baujahr=2015, serien="E-552103",
                medium="Abwasser", t_max=60, p_max=10, antrieb="selbsttätig",
                stellung="betriebsbedingt", bh=66300, wartung="04/2024", zustand="ok", meldung="",
            ),

            # --- BIOLOGISCHE STUFE ---
            "V-401": dict(
                kks="V-401", kurz="Absperrschieber", einbau="Interne Rezirkulation (Nitri → Deni)",
                anlagenteil="Biologische Stufe", hersteller="AVK", modell="Serie 06",
                dn=300, pn=10, werkstoff="EN-GJS-500 / EPDM", baujahr=2018, serien="AVK-331820",
                medium="Belebtschlamm", t_max=50, p_max=5, antrieb="Handrad",
                stellung="AUF", bh=48500, wartung="11/2024", zustand="ok", meldung="",
            ),
            "V-402": dict(
                kks="V-402", kurz="Absperrschieber", einbau="Rücklaufschlammleitung RS",
                anlagenteil="Biologische Stufe", hersteller="AVK", modell="Serie 06",
                dn=250, pn=10, werkstoff="EN-GJS-500 / EPDM", baujahr=2018, serien="AVK-331821",
                medium="Rücklaufschlamm", t_max=50, p_max=5, antrieb="Handrad",
                stellung="AUF", bh=48500, wartung="11/2024", zustand="ok", meldung="",
            ),

            # --- SCHLAMMBEHANDLUNG ---
            "V-501": dict(
                kks="V-501", kurz="Absperrschieber", einbau="ÜS-Leitung Richtung Eindicker",
                anlagenteil="Schlammbehandlung", hersteller="AVK", modell="Serie 02",
                dn=100, pn=10, werkstoff="EN-GJS-500 / EPDM", baujahr=2018, serien="AVK-110475",
                medium="Überschussschlamm", t_max=50, p_max=6, antrieb="Handrad",
                stellung="AUF", bh=38400, wartung="02/2025", zustand="ok", meldung="",
            ),
            "V-601": dict(
                kks="V-601", kurz="Absperrschieber", einbau="Primärschlamm-Leitung VK",
                anlagenteil="Schlammbehandlung", hersteller="AVK", modell="Serie 02",
                dn=150, pn=10, werkstoff="EN-GJS-500 / EPDM", baujahr=2018, serien="AVK-115502",
                medium="Primärschlamm", t_max=50, p_max=6, antrieb="Handrad",
                stellung="AUF", bh=38400, wartung="02/2025", zustand="ok", meldung="",
            ),

            # --- DRUCKROHRLEITUNG PW TALSTRASSE ---
            # (Korrosionsbefund, Sanierung geplant – alle Armaturen werden im Rahmen
            #  der Rohrleitungserneuerung mit getauscht. R&I-Schema siehe Anhang.)
            "V-001": dict(
                kks="V-001", kurz="Absperrschieber", einbau="Druckstutzen Pumpe P-001 (PW Talstraße)",
                anlagenteil="Druckrohrleitung PW Talstraße", hersteller="VAG", modell="EKO plus",
                dn=200, pn=10, werkstoff="EN-GJL-250 / EPDM", baujahr=1998, serien="VAG-22041",
                medium="Abwasser", t_max=45, p_max=7, antrieb="Handrad",
                stellung="AUF", bh=198200, wartung="05/2022",
                zustand="sanierung",
                meldung="Korrosionsbefund am Gehäuse – Sanierung im Zuge Rohrleitungserneuerung geplant.",
            ),
            "V-002": dict(
                kks="V-002", kurz="Absperrschieber", einbau="Druckstutzen Pumpe P-002 (PW Talstraße)",
                anlagenteil="Druckrohrleitung PW Talstraße", hersteller="VAG", modell="EKO plus",
                dn=200, pn=10, werkstoff="EN-GJL-250 / EPDM", baujahr=1998, serien="VAG-22042",
                medium="Abwasser", t_max=45, p_max=7, antrieb="Handrad",
                stellung="AUF", bh=42100, wartung="05/2022",
                zustand="sanierung",
                meldung="Korrosionsbefund am Gehäuse – Sanierung im Zuge Rohrleitungserneuerung geplant.",
            ),
            "RK-001": dict(
                kks="RK-001", kurz="Rückschlagklappe", einbau="nach P-001, vor Sammler (PW Talstraße)",
                anlagenteil="Druckrohrleitung PW Talstraße", hersteller="ERHARD", modell="ROCO check",
                dn=200, pn=10, werkstoff="EN-GJL-250 / NBR", baujahr=1998, serien="E-441207",
                medium="Abwasser", t_max=45, p_max=7, antrieb="selbsttätig",
                stellung="betriebsbedingt", bh=198200, wartung="05/2022",
                zustand="sanierung",
                meldung="Klappe weist Verschleißspuren auf – Austausch im Zuge Rohrleitungserneuerung.",
            ),
            "RK-002": dict(
                kks="RK-002", kurz="Rückschlagklappe", einbau="nach P-002, vor Sammler (PW Talstraße)",
                anlagenteil="Druckrohrleitung PW Talstraße", hersteller="ERHARD", modell="ROCO check",
                dn=200, pn=10, werkstoff="EN-GJL-250 / NBR", baujahr=1998, serien="E-441208",
                medium="Abwasser", t_max=45, p_max=7, antrieb="selbsttätig",
                stellung="betriebsbedingt", bh=42100, wartung="05/2022",
                zustand="sanierung",
                meldung="Klappe weist Verschleißspuren auf – Austausch im Zuge Rohrleitungserneuerung.",
            ),
            "V-003": dict(
                kks="V-003", kurz="Absperrschieber", einbau="Abzweig zu Speicherbecken 1 (B-002)",
                anlagenteil="Druckrohrleitung PW Talstraße", hersteller="VAG", modell="EKO plus",
                dn=125, pn=10, werkstoff="EN-GJL-250 / EPDM", baujahr=1998, serien="VAG-18812",
                medium="Abwasser", t_max=45, p_max=7, antrieb="Handrad",
                stellung="AUF", bh=198200, wartung="05/2022",
                zustand="sanierung",
                meldung="Korrosion am Flansch, Undichtigkeit dokumentiert. Austausch im Sanierungspaket.",
            ),
            "V-004": dict(
                kks="V-004", kurz="Absperrschieber", einbau="Abzweig zu Speicherbecken 2 (B-003)",
                anlagenteil="Druckrohrleitung PW Talstraße", hersteller="VAG", modell="EKO plus",
                dn=125, pn=10, werkstoff="EN-GJL-250 / EPDM", baujahr=1998, serien="VAG-18813",
                medium="Abwasser", t_max=45, p_max=7, antrieb="Handrad",
                stellung="AUF", bh=198200, wartung="05/2022",
                zustand="sanierung",
                meldung="Korrosion am Flansch, Undichtigkeit dokumentiert. Austausch im Sanierungspaket.",
            ),
            "LA-001": dict(
                kks="LA-001", kurz="Be-/Entlüftungsventil", einbau="Hauptleitung DN 200, Hochpunkt 1",
                anlagenteil="Druckrohrleitung PW Talstraße", hersteller="ARI Armaturen", modell="DP 17",
                dn=80, pn=10, werkstoff="EN-GJL-250 / NBR", baujahr=1998, serien="ARI-83491",
                medium="Abwasser", t_max=45, p_max=7, antrieb="selbsttätig",
                stellung="betriebsbedingt", bh=198200, wartung="05/2022",
                zustand="sanierung",
                meldung="Gehäuse mit Korrosionsspuren – Austausch im Zuge Rohrleitungserneuerung.",
            ),
            "LA-002": dict(
                kks="LA-002", kurz="Be-/Entlüftungsventil", einbau="Zweigleitung DN 125, Hochpunkt 2",
                anlagenteil="Druckrohrleitung PW Talstraße", hersteller="ARI Armaturen", modell="DP 17",
                dn=50, pn=10, werkstoff="EN-GJL-250 / NBR", baujahr=1998, serien="ARI-83492",
                medium="Abwasser", t_max=45, p_max=7, antrieb="selbsttätig",
                stellung="betriebsbedingt", bh=198200, wartung="05/2022",
                zustand="sanierung",
                meldung="Gehäuse mit Korrosionsspuren – Austausch im Zuge Rohrleitungserneuerung.",
            ),
        }

        # Betriebsstunden leicht dynamisch fortschreiben (Simulationszeit)
        for _k, _a in ARMATUREN.items():
            if _a.get("zustand") != "defekt":
                _a["bh"] = int(_a["bh"] + _th * 0.9)

        # Statuszählung
        _n_ok = sum(1 for a in ARMATUREN.values() if a["zustand"] == "ok")
        _n_san = sum(1 for a in ARMATUREN.values() if a["zustand"] == "sanierung")
        _n_def = sum(1 for a in ARMATUREN.values() if a["zustand"] == "defekt")
        _n_ges = len(ARMATUREN)

        # Farb-/Icon-Zuordnung nach Zustand
        def _z_farbe(z):
            return {"ok": "#00b894", "wartung": "#fdcb6e",
                    "sanierung": "#e17055", "defekt": "#e94560"}.get(z, "#74b9ff")

        def _z_icon(z):
            return {"ok": "🟢", "wartung": "🟡",
                    "sanierung": "🟠", "defekt": "🔴"}.get(z, "⚪")

        def _z_text(z):
            return {"ok": "in Betrieb", "wartung": "Wartung fällig",
                    "sanierung": "Sanierung empfohlen", "defekt": "STÖRUNG"}.get(z, z)

        # --- Armaturenliste: gruppiert nach Anlagenteil ---
        gruppen = {}
        for kks, a in ARMATUREN.items():
            gruppen.setdefault(a["anlagenteil"], []).append((kks, a))

        armaturen_liste_html = ""
        for gr, items in gruppen.items():
            rows = ""
            for kks, a in items:
                zf = _z_farbe(a["zustand"])
                rows += f'''
                <tr style="border-bottom:1px solid #0f3460">
                    <td style="padding:6px 12px;font-family:monospace;color:#74b9ff;font-weight:bold">{kks}</td>
                    <td style="padding:6px 12px">{a["kurz"]}</td>
                    <td style="padding:6px 12px;color:#b2bec3;font-size:0.9em">{a["einbau"]}</td>
                    <td style="padding:6px 12px;text-align:center">DN {a["dn"]}</td>
                    <td style="padding:6px 12px;text-align:center;color:#b2bec3">{a["stellung"]}</td>
                    <td style="padding:6px 12px;text-align:center;color:#b2bec3">{a["bh"]:,} h</td>
                    <td style="padding:6px 12px;color:{zf};font-weight:bold;white-space:nowrap">{_z_icon(a["zustand"])} {_z_text(a["zustand"])}</td>
                </tr>'''
            armaturen_liste_html += f'''
            <div class="pls-c" style="padding:8px 10px">
                <h3 style="font-size:0.95em">{gr}</h3>
                <table style="width:100%;border-collapse:collapse;font-size:0.86em;color:#ffffff;background:#16213e">
                    <tr style="background:#0f1a30;border-bottom:2px solid #0f3460">
                        <th style="padding:6px 12px;color:#74b9ff;text-align:left">KKS</th>
                        <th style="padding:6px 12px;color:#74b9ff;text-align:left">Typ</th>
                        <th style="padding:6px 12px;color:#74b9ff;text-align:left">Einbauort</th>
                        <th style="padding:6px 12px;color:#74b9ff;text-align:center">Nennweite</th>
                        <th style="padding:6px 12px;color:#74b9ff;text-align:center">Stellung</th>
                        <th style="padding:6px 12px;color:#74b9ff;text-align:center">Betriebsstd.</th>
                        <th style="padding:6px 12px;color:#74b9ff;text-align:center">Status</th>
                    </tr>
                    {rows}
                </table>
            </div>'''

        # --- Detailansicht für gezielt geöffnete Armatur (Details über <details>/<summary>) ---
        # Hier rendern wir jede Armatur als aufklappbare Karte mit Typenschild.
        def _typenschild_svg(a):
            """Erzeugt ein KSB-ähnliches Typenschild als SVG, Daten variabel."""
            marke = a["hersteller"]
            # Farbschema dezent nach Hersteller
            mfarbe = {
                "KSB": "#1a4a90", "VAG": "#2a6030", "ERHARD": "#603020",
                "AVK": "#8a4818", "ARI Armaturen": "#50208a",
                "Adams Armaturen": "#1a5a80",
            }.get(marke, "#1a4080")
            return f'''
<svg viewBox="0 0 480 280" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:480px;height:auto">
  <!-- Blechplatte -->
  <defs>
    <linearGradient id="mtl-{a["kks"]}" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:#e8e8ec"/>
      <stop offset="50%" style="stop-color:#c8c8cc"/>
      <stop offset="100%" style="stop-color:#a8a8ac"/>
    </linearGradient>
  </defs>
  <rect x="4" y="4" width="472" height="272" rx="6" fill="url(#mtl-{a["kks"]})" stroke="#707080" stroke-width="1"/>
  <!-- Blaue Kopfzeile -->
  <rect x="4" y="4" width="472" height="46" rx="6" fill="{mfarbe}"/>
  <text x="240" y="34" text-anchor="middle" fill="#ffffff" font-family="Arial,sans-serif" font-size="22" font-weight="bold" letter-spacing="2">{a["kurz"].upper()}</text>

  <!-- Typ + Hersteller-Logo-Bereich -->
  <text x="30" y="80" fill="#1a1a1a" font-family="Arial,sans-serif" font-size="14" font-weight="bold">Typ:</text>
  <text x="75" y="80" fill="#1a1a1a" font-family="Arial,sans-serif" font-size="15" font-weight="bold">{a["modell"]}</text>
  <line x1="75" y1="84" x2="280" y2="84" stroke="#303040" stroke-width="0.6"/>
  <!-- Hersteller-„Logo" -->
  <rect x="340" y="60" width="115" height="32" rx="3" fill="#ffffff" stroke="{mfarbe}" stroke-width="1.5"/>
  <text x="397" y="82" text-anchor="middle" fill="{mfarbe}" font-family="Arial,sans-serif" font-size="15" font-weight="bold">{marke}</text>
  <line x1="20" y1="100" x2="460" y2="100" stroke="{mfarbe}" stroke-width="1.2"/>

  <!-- Linke Spalte -->
  <text x="30" y="125" fill="#1a1a1a" font-family="Arial,sans-serif" font-size="11" font-weight="bold">Einbauort:</text>
  <text x="100" y="125" fill="#1a1a1a" font-family="Arial,sans-serif" font-size="11">{a["einbau"][:38]}</text>
  <line x1="100" y1="128" x2="240" y2="128" stroke="#303040" stroke-width="0.4"/>

  <text x="30" y="152" fill="#1a1a1a" font-family="Arial,sans-serif" font-size="11" font-weight="bold">Nennweite:</text>
  <text x="105" y="152" fill="#1a1a1a" font-family="Arial,sans-serif" font-size="11" font-weight="bold">DN {a["dn"]}</text>
  <line x1="105" y1="155" x2="240" y2="155" stroke="#303040" stroke-width="0.4"/>

  <text x="30" y="175" fill="#1a1a1a" font-family="Arial,sans-serif" font-size="11" font-weight="bold">Druckstufe:</text>
  <text x="105" y="175" fill="#1a1a1a" font-family="Arial,sans-serif" font-size="11" font-weight="bold">PN {a["pn"]}</text>
  <line x1="105" y1="178" x2="240" y2="178" stroke="#303040" stroke-width="0.4"/>

  <!-- Rechte Spalte -->
  <text x="260" y="125" fill="#1a1a1a" font-family="Arial,sans-serif" font-size="11" font-weight="bold">Werkstoff:</text>
  <text x="327" y="125" fill="#1a1a1a" font-family="Arial,sans-serif" font-size="11" font-weight="bold">{a["werkstoff"]}</text>
  <line x1="327" y1="128" x2="460" y2="128" stroke="#303040" stroke-width="0.4"/>

  <text x="260" y="152" fill="#1a1a1a" font-family="Arial,sans-serif" font-size="11" font-weight="bold">Baujahr:</text>
  <text x="318" y="152" fill="#1a1a1a" font-family="Arial,sans-serif" font-size="11" font-weight="bold">{a["baujahr"]}</text>
  <line x1="318" y1="155" x2="460" y2="155" stroke="#303040" stroke-width="0.4"/>

  <text x="260" y="175" fill="#1a1a1a" font-family="Arial,sans-serif" font-size="11" font-weight="bold">Serien-Nr.:</text>
  <text x="327" y="175" fill="#1a1a1a" font-family="Arial,sans-serif" font-size="11" font-weight="bold">{a["serien"]}</text>
  <line x1="327" y1="178" x2="460" y2="178" stroke="#303040" stroke-width="0.4"/>

  <!-- Untere Zeile -->
  <line x1="20" y1="200" x2="460" y2="200" stroke="{mfarbe}" stroke-width="1.2"/>
  <text x="30" y="223" fill="#1a1a1a" font-family="Arial,sans-serif" font-size="11" font-weight="bold">Medium: {a["medium"]}</text>
  <line x1="163" y1="210" x2="163" y2="235" stroke="#606060" stroke-width="0.4"/>
  <text x="175" y="223" fill="#1a1a1a" font-family="Arial,sans-serif" font-size="11" font-weight="bold">max. Temp.: {a["t_max"]} °C</text>
  <line x1="310" y1="210" x2="310" y2="235" stroke="#606060" stroke-width="0.4"/>
  <text x="322" y="223" fill="#1a1a1a" font-family="Arial,sans-serif" font-size="11" font-weight="bold">max. Druck: {a["p_max"]} bar</text>

  <!-- Fußzeile -->
  <rect x="4" y="245" width="472" height="31" fill="{mfarbe}" rx="0"/>
  <text x="240" y="266" text-anchor="middle" fill="#ffffff" font-family="Arial,sans-serif" font-size="12" font-weight="bold" letter-spacing="1">Made in Germany</text>

  <!-- Bohrungen (Ecken) -->
  <circle cx="24" cy="24" r="4.5" fill="#707080" stroke="#303040" stroke-width="0.6"/>
  <circle cx="456" cy="24" r="4.5" fill="#707080" stroke="#303040" stroke-width="0.6"/>
  <circle cx="24" cy="256" r="4.5" fill="#707080" stroke="#303040" stroke-width="0.6"/>
  <circle cx="456" cy="256" r="4.5" fill="#707080" stroke="#303040" stroke-width="0.6"/>
</svg>'''

        # --- Aufklappbare Armatur-Karten nur für Armaturen, die nicht "ok" sind ---
        # (Alle OK-Armaturen erscheinen in der Übersicht, für Details sind die
        # auffälligen Armaturen primär relevant. OK-Armaturen kann man über den
        # Dropdown unten ebenfalls einsehen → Wartung proaktiv anmelden.)
        auffaellig_html = ""
        for kks, a in ARMATUREN.items():
            if a["zustand"] == "ok":
                continue
            zf = _z_farbe(a["zustand"])
            meldung_html = ""
            if a.get("meldung"):
                meldung_html = f'''
                <div style="background:rgba({("233,69,96" if a["zustand"]=="defekt" else "225,112,85")},0.12);
                            border-left:3px solid {zf};padding:6px 10px;margin:6px 0 10px;font-size:0.85em">
                    <strong style="color:{zf}">{"⚡ Störmeldung" if a["zustand"]=="defekt" else "ℹ️ Anlagenbefund"}:</strong>
                    <span style="color:#dfe6e9"> {a["meldung"]}</span>
                </div>'''
            auffaellig_html += f'''
<details style="margin:6px 0;background:#16213e;border:1px solid {zf};border-radius:6px;padding:8px 14px">
  <summary style="cursor:pointer;font-weight:bold;color:{zf};font-family:monospace;font-size:0.95em">
    {_z_icon(a["zustand"])} {kks} – {a["kurz"]} · {a["einbau"]} <span style="color:#b2bec3;font-weight:normal">&nbsp;▸&nbsp;Details anzeigen</span>
  </summary>
  <div style="margin-top:10px">
    {meldung_html}
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;align-items:start">
      <div>
        <h4 style="color:#74b9ff;margin:0 0 6px;font-size:0.85em;border-bottom:1px solid #0f3460;padding-bottom:3px">📋 Typenschild (Original)</h4>
        {_typenschild_svg(a)}
      </div>
      <div>
        <h4 style="color:#74b9ff;margin:0 0 6px;font-size:0.85em;border-bottom:1px solid #0f3460;padding-bottom:3px">📊 Betriebsdaten</h4>
        <table class="pls-tbl" style="font-size:0.85em">
          <tr><td>Anlagenteil</td><td class="c-v">{a["anlagenteil"]}</td></tr>
          <tr><td>Antriebsart</td><td class="c-v">{a["antrieb"]}</td></tr>
          <tr><td>Aktuelle Stellung</td><td class="c-v">{a["stellung"]}</td></tr>
          <tr><td>Betriebsstunden</td><td class="c-v">{a["bh"]:,} h</td></tr>
          <tr><td>Letzte Wartung</td><td class="c-v">{a["wartung"]}</td></tr>
          <tr><td>Zustand</td><td style="color:{zf};font-weight:bold;text-align:right">{_z_text(a["zustand"])}</td></tr>
        </table>
        <div style="margin-top:10px;padding:8px 10px;background:#0f1a30;border-radius:4px;font-size:0.8em;color:#b2bec3">
          💡 Für eine Wartung oder Instandsetzung dieser Armatur bitte den Auswahldialog unten verwenden.
        </div>
      </div>
    </div>
  </div>
</details>'''

        # --- Wartungsauftrag (bei Button-Klick) ---
        wartung_html = ""
        if wartung_btn.value and armatur_auswahl.value and armatur_auswahl.value != "—":
            _sel_kks = armatur_auswahl.value.split()[0]
            _sel = ARMATUREN.get(_sel_kks)
            if _sel:
                _auftrag_nr = f"WA-{2025000 + (_sel_kks.__hash__() % 1000):06d}"
                _datum = _dt.datetime.now().strftime("%d.%m.%Y %H:%M")
                wartung_html = f'''
<div style="background:#fffdf5;color:#1a1a2e;border:2px solid #5a4820;border-radius:6px;padding:16px 20px;margin-top:10px;font-family:'Consolas','Courier New',monospace">
  <div style="display:flex;justify-content:space-between;align-items:flex-start;border-bottom:2px solid #1a1a2e;padding-bottom:8px;margin-bottom:10px">
    <div>
      <div style="font-size:0.75em;color:#5a4820;letter-spacing:1.5px">KLÄRANLAGE MUSTERSTADT – BETRIEBSFÜHRUNG</div>
      <div style="font-size:1.1em;font-weight:bold">WARTUNGSAUFTRAG / INSTANDSETZUNG</div>
    </div>
    <div style="text-align:right;font-size:0.8em;color:#5a4820">
      <div><strong style="color:#1a1a2e">Auftrag-Nr.: {_auftrag_nr}</strong></div>
      <div>Ausgestellt: {_datum}</div>
      <div>Priorität: {"HOCH (Störung)" if _sel["zustand"]=="defekt" else "MITTEL"}</div>
    </div>
  </div>
  <table style="width:100%;font-size:0.88em;border-collapse:collapse">
    <tr><td style="padding:3px 8px;color:#5a4820;width:35%">Armatur (KKS)</td>    <td style="padding:3px 8px;font-weight:bold">{_sel["kks"]}</td></tr>
    <tr><td style="padding:3px 8px;color:#5a4820">Typ / Modell</td>               <td style="padding:3px 8px;font-weight:bold">{_sel["kurz"]} · {_sel["hersteller"]} {_sel["modell"]}</td></tr>
    <tr><td style="padding:3px 8px;color:#5a4820">Einbauort</td>                   <td style="padding:3px 8px;font-weight:bold">{_sel["einbau"]}</td></tr>
    <tr><td style="padding:3px 8px;color:#5a4820">Nennweite / Druckstufe</td>     <td style="padding:3px 8px;font-weight:bold">DN {_sel["dn"]} / PN {_sel["pn"]}</td></tr>
    <tr><td style="padding:3px 8px;color:#5a4820">Werkstoff</td>                   <td style="padding:3px 8px;font-weight:bold">{_sel["werkstoff"]}</td></tr>
    <tr><td style="padding:3px 8px;color:#5a4820">Serien-Nr. / Baujahr</td>       <td style="padding:3px 8px;font-weight:bold">{_sel["serien"]} · {_sel["baujahr"]}</td></tr>
    <tr><td style="padding:3px 8px;color:#5a4820">Aktueller Zustand</td>          <td style="padding:3px 8px;font-weight:bold;color:{_z_farbe(_sel["zustand"])}">{_z_text(_sel["zustand"])}</td></tr>
    <tr><td style="padding:3px 8px;color:#5a4820;vertical-align:top">Anlass / Befund</td><td style="padding:3px 8px">{_sel.get("meldung") or "Routine-Wartung, planmäßig"}</td></tr>
  </table>
  <div style="margin-top:12px;padding-top:8px;border-top:1px dashed #5a4820">
    <table style="width:100%;font-size:0.85em">
      <tr>
        <td style="padding:3px 8px;color:#5a4820;width:35%">Meldende Stelle</td>
        <td style="padding:3px 8px">Anlagenfahrer (Auszubildende/-r)</td>
      </tr>
      <tr>
        <td style="padding:3px 8px;color:#5a4820">Empfänger</td>
        <td style="padding:3px 8px">Leitwarte / Instandhaltung</td>
      </tr>
      <tr>
        <td style="padding:3px 8px;color:#5a4820">Erforderliche Unterlagen</td>
        <td style="padding:3px 8px">Betriebsanleitung, Explosionszeichnung, Stückliste</td>
      </tr>
    </table>
  </div>
  <div style="margin-top:10px;padding:8px 10px;background:#f4f0e0;border-left:3px solid #5a4820;font-size:0.82em">
    <strong>📩 Auftrag an Leitwarte übermittelt.</strong> Die Leitwarte bestätigt den Eingang und
    terminiert die Maßnahme mit der Instandhaltung. Bei Störungsmeldungen (Priorität HOCH) erfolgt
    die Kontaktaufnahme binnen 30 Minuten.
  </div>
</div>'''

        # --- Tab zusammensetzen ---
        armaturen = mo.vstack([
            # Kopfzeile mit Status-Übersicht
            mo.Html(f'''<div class="pls"><div class="pls-c">
                <h3>🛠️ Armaturenverzeichnis</h3>
                <p style="font-size:0.88em;margin:4px 0 10px">
                    Zentrale Übersicht aller Armaturen der Kläranlage und der zugehörigen Außenstationen.
                    Zustand, Stellung und Betriebsstunden werden live aus dem PLS übernommen.
                </p>
                <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:10px">
                    <div style="background:#0f1a30;border-radius:4px;padding:10px;border-left:3px solid #74b9ff">
                        <div style="font-size:0.75em;color:#b2bec3">Gesamt</div>
                        <div style="font-size:1.4em;font-weight:bold;color:#74b9ff">{_n_ges}</div>
                    </div>
                    <div style="background:#0f1a30;border-radius:4px;padding:10px;border-left:3px solid #00b894">
                        <div style="font-size:0.75em;color:#b2bec3">🟢 in Betrieb</div>
                        <div style="font-size:1.4em;font-weight:bold;color:#00b894">{_n_ok}</div>
                    </div>
                    <div style="background:#0f1a30;border-radius:4px;padding:10px;border-left:3px solid #e17055">
                        <div style="font-size:0.75em;color:#b2bec3">🟠 Sanierung empfohlen</div>
                        <div style="font-size:1.4em;font-weight:bold;color:#e17055">{_n_san}</div>
                    </div>
                    <div style="background:#0f1a30;border-radius:4px;padding:10px;border-left:3px solid #e94560">
                        <div style="font-size:0.75em;color:#b2bec3">🔴 Störung</div>
                        <div style="font-size:1.4em;font-weight:bold;color:#e94560">{_n_def}</div>
                    </div>
                </div>
            </div></div>'''),

            # Armaturenliste (gruppiert)
            mo.Html(f'<div class="pls">{armaturen_liste_html}</div>'),

            # Auffällige Armaturen mit Details (Typenschild + Betriebsdaten)
            mo.Html(f'''<div class="pls"><div class="pls-c">
                <h3>🔍 Auffällige Armaturen (Details)</h3>
                <p style="font-size:0.82em;color:#b2bec3;margin:0 0 10px">
                    Klick auf eine Zeile öffnet die Detailansicht mit Original-Typenschild und
                    Betriebsdaten. OK-Armaturen können über den Auswahldialog unten eingesehen werden.
                </p>
                {auffaellig_html}
            </div></div>'''),

            # Wartungsanmeldung
            mo.Html('''<div class="pls"><div class="pls-c" style="border-color:#fdcb6e">
                <h3 style="color:#fdcb6e">📨 Wartung bei Leitwarte anmelden</h3>
                <p style="font-size:0.85em;color:#b2bec3;margin:0 0 10px">
                    Armatur aus der Liste wählen und den Wartungsauftrag an die Leitwarte übermitteln.
                    Das PLS erzeugt automatisch ein strukturiertes Auftragsformular mit allen Stammdaten.
                </p>
            </div></div>'''),
            mo.hstack([armatur_auswahl, wartung_btn], justify="start", gap=1),
            mo.Html(f'<div class="pls">{wartung_html}</div>') if wartung_html else mo.Html(""),
        ])


        # ====== ENERGIE-TAB: Zählerauswertung, Lastgang, Stromvertrag, Eigenerzeugung ======
        en_vt = st.get("e_vortag", dict())
        en_rng = np.random.default_rng(int(th // 24) * 3 + 11)  # Wetter PV: je Tag fest
        en_uv = dict(en_vt.get("e_uv", dict()))
        en_bhkw_d = en_vt.get("e_bhkw", 0.0)
        en_pv_d = en_vt.get("e_pv", 0.0) * (1 + en_rng.normal(0, 0.15)) if en_vt.get("e_pv", 0.0) > 0 else 0.0
        en_apw_d = en_vt.get("e_apw03", 0.0)
        en_tg = pm["tagesgang"]
        en_pv_form = [max(0.0, np.sin(np.pi * (hh + 0.5 - 6.0) / 14.0)) if 6 <= hh < 20 else 0.0 for hh in range(24)]
        en_pv_sum = sum(en_pv_form)
        en_last, en_bezug, en_einsp, en_bh, en_pvh = [], [], [], [], []
        for hh in range(24):
            _l = (en_uv.get("uv1", 0) / 24 * en_tg[hh]
                  + en_uv.get("uv2", 0) / 24 * (0.7 + 0.3 * en_tg[hh])
                  + (en_uv.get("uv3", 0) + en_uv.get("uv4", 0) + en_uv.get("uv5", 0) + en_uv.get("uv6", 0)) / 24)
            _b = en_bhkw_d / 24
            _p = en_pv_d * en_pv_form[hh] / en_pv_sum if en_pv_sum > 0 else 0.0
            en_last.append(_l); en_bh.append(_b); en_pvh.append(_p)
            en_bezug.append(max(0.0, _l - _b - _p)); en_einsp.append(max(0.0, _b + _p - _l))
        en_ges_d = sum(en_last)
        en_bezug_d = sum(en_bezug)
        en_einsp_d = sum(en_einsp)
        en_spitze = max(en_bezug) * 1.08
        en_h = int(th % 24)

        def en_zeile(nr, bez, wert, fett=False):
            _fw = "bold" if fett else "normal"
            return (f'<tr style="border-bottom:1px solid #0f3460"><td style="padding:5px 14px;color:#b2bec3;white-space:nowrap">{nr}</td>'
                    f'<td style="padding:5px 14px;white-space:nowrap;font-weight:{_fw}">{bez}</td>'
                    f'<td style="padding:5px 14px;text-align:right;white-space:nowrap;font-weight:bold;color:#74b9ff">{wert:.0f}&ensp;kWh</td></tr>')
        en_rows = (en_zeile("EZ-01", "Übergabezähler Netzbezug (Bezug)", en_bezug_d, True)
                   + en_zeile("EZ-01", "Übergabezähler Netzbezug (Einspeisung)", en_einsp_d)
                   + en_zeile("EZ-10", "Erzeugung BHKW-Modul 1", en_bhkw_d))
        if en_pv_d > 0:
            en_rows += en_zeile("EZ-11", "Erzeugung PV-Anlage", en_pv_d)
        en_rows += (en_zeile("EZ-21", "UV-1 Zulauf, Hebewerk, Rechen, Sandfang", en_uv.get("uv1", 0))
                    + en_zeile("EZ-22", "UV-2 Gebläsestation", en_uv.get("uv2", 0))
                    + en_zeile("EZ-23", "UV-3 Biologie, Nachklärung, RS-Pumpwerk", en_uv.get("uv3", 0))
                    + en_zeile("EZ-24", "UV-4 Schlammbehandlung, Faulung", en_uv.get("uv4", 0))
                    + en_zeile("EZ-25", "UV-5 Betriebsgebäude, Labor, Werkstatt", en_uv.get("uv5", 0)))
        if en_uv.get("uv6", 0) > 0:
            en_rows += en_zeile("EZ-26", "UV-6 GAK-Filter (4. Reinigungsstufe)", en_uv.get("uv6", 0))
        en_rows += en_zeile("APW03-EZ 01", "PW Talstraße (eigener Netzanschluss)", en_apw_d)
        en_zaehler_html = f'''<div class="pls-c"><h3>🔢 Zählerauswertung – Tageswerte Vortag</h3>
            <table style="border-collapse:collapse;font-size:0.86em;color:#ffffff;background:#16213e">
              <tr style="border-bottom:2px solid #0f3460;background:#0f1a30">
                <th style="padding:8px 14px;color:#74b9ff;text-align:left">Zähler</th>
                <th style="padding:8px 14px;color:#74b9ff;text-align:left">Messstelle</th>
                <th style="padding:8px 14px;color:#74b9ff;text-align:right">Arbeit Vortag</th></tr>
              {en_rows}
            </table>
            <p style="font-size:0.78em;color:#b2bec3;margin:6px 0 0">EZ-01: registrierende Leistungsmessung (RLM, 15-min-Mittelwerte) ·
               höchste Bezugsleistung Vortag: <b style="color:#74b9ff">{en_spitze:.0f} kW</b></p></div>'''
        en_live_html = f'''<div class="pls-c"><h3>⚡ Aktuelle Leistungen ({en_h:02d}:00 Uhr)</h3>
            {vtbl(
                vr("Netzbezug EZ-01", f"{en_bezug[en_h]:.0f}", "kW")
                + vr("Erzeugung BHKW EZ-10", f"{en_bh[en_h]:.0f}", "kW")
                + (vr("Erzeugung PV EZ-11", f"{en_pvh[en_h]:.0f}", "kW") if en_pv_d > 0 else "")
                + vr("Faulgas zum BHKW FI 608", f"{en_vt.get('gas_nm3', 0) / 24:.0f}", "Nm³/h")
                + vr("Gasspeicher Füllstand", f"{55 + 10 * np.sin(th / 5.0):.0f}", "%")
            )}</div>'''

        import plotly.graph_objects as _ego
        fig_en = _ego.Figure()
        _xh = list(range(25))
        en_last.append(en_last[-1]); en_bezug.append(en_bezug[-1]); en_bh.append(en_bh[-1]); en_pvh.append(en_pvh[-1])
        fig_en.add_trace(_ego.Scatter(x=_xh, y=en_last, name="Verbrauch Kläranlage", mode="lines", line=dict(color="#dfe6e9", width=2), line_shape="hv"))
        fig_en.add_trace(_ego.Scatter(x=_xh, y=en_bezug, name="Netzbezug EZ-01", mode="lines", line=dict(color="#e17055", width=2), line_shape="hv"))
        fig_en.add_trace(_ego.Scatter(x=_xh, y=en_bh, name="BHKW EZ-10", mode="lines", line=dict(color="#fdcb6e", width=1.6), line_shape="hv"))
        if en_pv_d > 0:
            fig_en.add_trace(_ego.Scatter(x=_xh, y=en_pvh, name="PV EZ-11", mode="lines", line=dict(color="#00b894", width=1.6), line_shape="hv"))
        fig_en.update_layout(height=340, template="plotly_dark", paper_bgcolor="#1a1a2e", plot_bgcolor="#16213e",
                             font=dict(family="Consolas,monospace", size=10, color="#dfe6e9"),
                             margin=dict(t=30, b=40, l=55, r=20), legend=dict(orientation="h", y=1.12),
                             xaxis=dict(title="Uhrzeit Vortag [h]", gridcolor="#0f3460", dtick=2),
                             yaxis=dict(title="Leistung [kW] (Stundenmittel)", gridcolor="#0f3460", rangemode="tozero"))

        _sd = pm["strom"]
        _ap_rows = ""
        for _j, (_nm, _ct) in enumerate(_sd["arbeitspreise"]):
            _bg = "#f5f0d8" if _j % 2 else "transparent"
            _ap_rows += (f'<tr style="background:{_bg}"><td style="padding:4px 12px;color:#5a4820">{_nm}</td>'
                         f'<td style="padding:4px 12px;text-align:right;font-weight:bold;white-space:nowrap">{_ct:.2f}&ensp;ct/kWh</td></tr>')
        _ap_sum = sum(v for _, v in _sd["arbeitspreise"])
        en_vertrag_html = f'''<div class="pls-c" style="background:#fffef5;color:#1a1a2e;border:2px solid #5a4820">
          <div style="display:flex;justify-content:space-between;border-bottom:2px solid #1a1a2e;padding-bottom:6px;margin-bottom:8px">
            <div><div style="font-size:0.75em;color:#5a4820;letter-spacing:2px">{_sd["lieferant"].upper()}</div>
                 <div style="font-size:1.05em;font-weight:bold">PREISBLATT ZUM STROMLIEFERVERTRAG</div></div>
            <div style="text-align:right;font-size:0.75em;color:#5a4820">Vertrag: {_sd["vertragsnr"]}<br>{_sd["vertrag"]}<br>Laufzeit: {_sd["laufzeit"]}</div>
          </div>
          <div style="font-size:0.85em;margin-bottom:6px">Kunde: Abwasserbetrieb Stadt Meckelberg, Kläranlage Musterstadt · Abrechnungszähler EZ-01 (RLM)</div>
          <table style="border-collapse:collapse;font-size:0.86em;color:#1a1a2e">
            {_ap_rows}
            <tr style="border-top:2px solid #1a1a2e"><td style="padding:5px 12px;font-weight:bold">Summe Arbeitspreis</td>
                <td style="padding:5px 12px;text-align:right;font-weight:bold">{_ap_sum:.2f}&ensp;ct/kWh</td></tr>
            <tr><td style="padding:4px 12px;color:#5a4820">Leistungspreis (Jahreshöchstleistung Netzbezug)</td>
                <td style="padding:4px 12px;text-align:right;font-weight:bold;white-space:nowrap">{_sd["leistungspreis"]:.2f}&ensp;€/(kW·a)</td></tr>
            <tr style="background:#f5f0d8"><td style="padding:4px 12px;color:#5a4820">Grundpreis Messstellenbetrieb</td>
                <td style="padding:4px 12px;text-align:right;font-weight:bold;white-space:nowrap">{_sd["grundpreis"]:.2f}&ensp;€/a</td></tr>
          </table>
          <p style="font-size:0.76em;color:#5a4820;margin:8px 0 0;font-style:italic">Alle Preise netto zzgl. Umsatzsteuer ({_sd["mwst"]} %).
             Eigenerzeugter und selbst verbrauchter Strom (BHKW, PV) wird nicht über diesen Vertrag abgerechnet.</p>
        </div>'''
        _sa = _sd["apw"]
        _apw_rows = ""
        for _j, (_nm, _ct) in enumerate(_sa["arbeitspreise"]):
            _bg = "#f5f0d8" if _j % 2 else "transparent"
            _apw_rows += (f'<tr style="background:{_bg}"><td style="padding:4px 12px;color:#5a4820">{_nm}</td>'
                          f'<td style="padding:4px 12px;text-align:right;font-weight:bold;white-space:nowrap">{_ct:.2f}&ensp;ct/kWh</td></tr>')
        _apw_sum = sum(v for _, v in _sa["arbeitspreise"])
        en_vertrag_apw_html = f'''<div class="pls-c" style="background:#fffef5;color:#1a1a2e;border:2px solid #5a4820">
          <div style="display:flex;justify-content:space-between;border-bottom:2px solid #1a1a2e;padding-bottom:6px;margin-bottom:8px">
            <div><div style="font-size:0.75em;color:#5a4820;letter-spacing:2px">{_sd["lieferant"].upper()}</div>
                 <div style="font-size:1.05em;font-weight:bold">PREISBLATT ZUM STROMLIEFERVERTRAG</div></div>
            <div style="text-align:right;font-size:0.75em;color:#5a4820">Vertrag: {_sa["vertragsnr"]}<br>{_sa["vertrag"]}<br>Laufzeit: {_sd["laufzeit"]}</div>
          </div>
          <div style="font-size:0.85em;margin-bottom:6px">Kunde: Abwasserbetrieb Stadt Meckelberg · Lieferstelle: {_sa["lieferstelle"]}</div>
          <table style="border-collapse:collapse;font-size:0.86em;color:#1a1a2e">
            {_apw_rows}
            <tr style="border-top:2px solid #1a1a2e"><td style="padding:5px 12px;font-weight:bold">Summe Arbeitspreis</td>
                <td style="padding:5px 12px;text-align:right;font-weight:bold">{_apw_sum:.2f}&ensp;ct/kWh</td></tr>
            <tr><td style="padding:4px 12px;color:#5a4820">Grundpreis (Messstellenbetrieb, Abrechnung)</td>
                <td style="padding:4px 12px;text-align:right;font-weight:bold;white-space:nowrap">{_sa["grundpreis"]:.2f}&ensp;€/a</td></tr>
          </table>
          <p style="font-size:0.76em;color:#5a4820;margin:8px 0 0;font-style:italic">Alle Preise netto zzgl. Umsatzsteuer ({_sd["mwst"]} %).
             Standardlastprofil, kein Leistungspreis.</p>
        </div>'''
        _mix_rows = ""
        for _j, (_nm, _pc) in enumerate(_sd["mix"]):
            _bg = "#f5f0d8" if _j % 2 else "transparent"
            _mix_rows += (f'<tr style="background:{_bg}"><td style="padding:4px 12px;color:#5a4820">{_nm}</td>'
                          f'<td style="padding:4px 12px;text-align:right;font-weight:bold;white-space:nowrap">{_pc}&ensp;%</td>'
                          f'<td style="padding:4px 12px;width:120px"><div style="background:#5a4820;height:9px;width:{_pc * 1.2:.0f}px"></div></td></tr>')
        en_kennz_html = f'''<div class="pls-c" style="background:#fffef5;color:#1a1a2e;border:2px solid #5a4820">
          <div style="font-size:0.75em;color:#5a4820;letter-spacing:2px">{_sd["lieferant"].upper()}</div>
          <div style="font-size:1.05em;font-weight:bold;border-bottom:2px solid #1a1a2e;padding-bottom:6px;margin-bottom:8px">STROMKENNZEICHNUNG</div>
          <div style="font-size:0.8em;color:#5a4820;margin-bottom:6px">{_sd["stand_mix"]} · Unternehmensverkaufsmix</div>
          <table style="border-collapse:collapse;font-size:0.86em;color:#1a1a2e">{_mix_rows}</table>
          <table style="border-collapse:collapse;font-size:0.86em;color:#1a1a2e;margin-top:8px">
            <tr><td style="padding:4px 12px;color:#5a4820">CO₂-Emissionen</td><td style="padding:4px 12px;font-weight:bold">{_sd["co2_g_kwh"]}&ensp;g/kWh</td></tr>
            <tr style="background:#f5f0d8"><td style="padding:4px 12px;color:#5a4820">Radioaktiver Abfall</td><td style="padding:4px 12px;font-weight:bold">{_sd["rad_g_kwh"]:.4f}&ensp;g/kWh</td></tr>
          </table>
        </div>'''
        _bk = pm["bhkw"]
        en_bhkw_html = f'''<div class="pls-c" style="background:#fffef5;color:#1a1a2e;border:2px solid #5a4820">
          <div style="font-size:0.75em;color:#5a4820;letter-spacing:2px">ANLAGENDOKUMENTATION · SCHLAMMFAULUNG</div>
          <div style="font-size:1.05em;font-weight:bold;border-bottom:2px solid #1a1a2e;padding-bottom:6px;margin-bottom:8px">DATENBLATT {_bk["bez"].upper()}</div>
          <table style="border-collapse:collapse;font-size:0.86em;color:#1a1a2e">
            <tr><td style="padding:4px 12px;color:#5a4820">Bauart</td><td style="padding:4px 12px;font-weight:bold">{_bk["typ"]}</td></tr>
            <tr style="background:#f5f0d8"><td style="padding:4px 12px;color:#5a4820">Elektrische Nennleistung</td><td style="padding:4px 12px;font-weight:bold">{_bk["p_el"]:.0f} kW</td></tr>
            <tr><td style="padding:4px 12px;color:#5a4820">Elektrischer / thermischer Wirkungsgrad</td><td style="padding:4px 12px;font-weight:bold">{_bk["eta_el"] * 100:.0f} % / {_bk["eta_th"] * 100:.0f} %</td></tr>
            <tr style="background:#f5f0d8"><td style="padding:4px 12px;color:#5a4820">Brennstoff</td><td style="padding:4px 12px;font-weight:bold">Faulgas aus FT-1 (biogen), CH₄ ca. {_bk["ch4"]} %</td></tr>
            <tr><td style="padding:4px 12px;color:#5a4820">Heizwert Faulgas H_u</td><td style="padding:4px 12px;font-weight:bold">ca. {_bk["hu"]:.1f} kWh/Nm³</td></tr>
            <tr style="background:#f5f0d8"><td style="padding:4px 12px;color:#5a4820">Betriebsweise</td><td style="padding:4px 12px;font-weight:bold">gasgeführt, modulierend; Wärme für W10.1 und Gebäude</td></tr>
            <tr><td style="padding:4px 12px;color:#5a4820">Baujahr</td><td style="padding:4px 12px;font-weight:bold">{_bk["baujahr"]}</td></tr>
          </table>
        </div>'''
        en_pv_html = ""
        if en_pv_d > 0:
            en_pv_html = f'''<div class="pls-c"><h3>☀️ PV-Anlage Dachflächen</h3>
                {vtbl(vr("Installierte Leistung", f"{pm['pv']['kwp']:.0f}", "kWp")
                      + vr("Erzeugung Vortag EZ-11", f"{en_pv_d:.0f}", "kWh")
                      + vr("Aktuelle Leistung", f"{en_pvh[en_h]:.0f}", "kW"))}</div>'''

        # --- Jahresbericht Energie 2025 (Bestand vor Umbauten, Betriebstagebuch) ---
        _jb_zeilen = [
            ("Stromverbrauch Kläranlage gesamt", "1.718.400 kWh", True),
            ("&nbsp;&nbsp;UV-1 Zulauf, Hebewerk, Rechen, Sandfang", "221.300 kWh", False),
            ("&nbsp;&nbsp;UV-2 Gebläsestation", "876.200 kWh", False),
            ("&nbsp;&nbsp;UV-3 Biologie, Nachklärung, RS-Pumpwerk", "354.900 kWh", False),
            ("&nbsp;&nbsp;UV-4 Schlammbehandlung, Faulung", "105.400 kWh", False),
            ("&nbsp;&nbsp;UV-5 Betriebsgebäude, Labor, Werkstatt", "160.600 kWh", False),
            ("Netzbezug Übergabezähler EZ-01", "881.500 kWh", True),
            ("Stromerzeugung BHKW-Modul 1 (EZ-10)", "836.900 kWh", True),
            ("Einspeisung ins Netz", "0 kWh", False),
            ("Faulgasproduktion (FI 608)", "362.100 Nm³", False),
            ("PW Talstraße, eigener Netzanschluss (APW03-EZ 01)", "67.900 kWh", True),
            ("Behandelte Abwassermenge", "4.412.000 m³", False),
            ("Angeschlossene Einwohnerwerte", "50.000 EW", False),
        ]
        _jb_bh = [
            ("P-001 Förderpumpe PW Talstraße", "4.392 h"), ("P-002 Förderpumpe PW Talstraße", "21 h"),
            ("P3.1 – P3.5 Rücklaufschlammpumpen (je)", "8.716 – 8.748 h"), ("P3.6 Rücklaufschlammpumpe", "196 h"),
            ("P10.1 Umwälzpumpe Faulturm", "8.736 h"), ("P10.2 Umwälzpumpe Faulturm", "24 h"),
        ]
        _jb_tr = ""
        for _j, (_nm, _vv, _fett) in enumerate(_jb_zeilen):
            _bg = "#f5f0d8" if _j % 2 else "transparent"
            _fw = "bold" if _fett else "normal"
            _jb_tr += (f'<tr style="background:{_bg}"><td style="padding:4px 12px;color:#5a4820;font-weight:{_fw}">{_nm}</td>'
                       f'<td style="padding:4px 12px;text-align:right;font-weight:bold;white-space:nowrap">{_vv}</td></tr>')
        _jb_bhr = ""
        for _j, (_nm, _vv) in enumerate(_jb_bh):
            _bg = "#f5f0d8" if _j % 2 else "transparent"
            _jb_bhr += (f'<tr style="background:{_bg}"><td style="padding:4px 12px;color:#5a4820">{_nm}</td>'
                        f'<td style="padding:4px 12px;text-align:right;font-weight:bold;white-space:nowrap">{_vv}</td></tr>')
        en_jb_html = f'''<div class="pls-c" style="background:#fffef5;color:#1a1a2e;border:2px solid #5a4820">
          <div style="display:flex;justify-content:space-between;border-bottom:2px solid #1a1a2e;padding-bottom:6px;margin-bottom:8px">
            <div><div style="font-size:0.75em;color:#5a4820;letter-spacing:2px">ABWASSERBETRIEB STADT MECKELBERG · KLÄRANLAGE MUSTERSTADT</div>
                 <div style="font-size:1.05em;font-weight:bold">JAHRESBERICHT ENERGIE 2025 (AUSZUG)</div></div>
            <div style="text-align:right;font-size:0.75em;color:#5a4820">Berichtszeitraum 01.01.–31.12.2025<br>Stand: Februar 2026</div>
          </div>
          <div class="pls-g2">
            <div><div style="font-size:0.8em;color:#5a4820;margin-bottom:4px">Energiebilanz (Jahressummen)</div>
              <table style="border-collapse:collapse;font-size:0.85em;color:#1a1a2e">{_jb_tr}</table></div>
            <div><div style="font-size:0.8em;color:#5a4820;margin-bottom:4px">Betriebsstunden 2025 (Betriebstagebuch)</div>
              <table style="border-collapse:collapse;font-size:0.85em;color:#1a1a2e">{_jb_bhr}</table>
              <p style="font-size:0.76em;color:#5a4820;margin:8px 0 0;font-style:italic">Anlagenzustand 2025: Bestand vor den Umbaumaßnahmen,
                 keine PV-Anlage. Zählerwerte aus Fernauslesung, Summen gerundet.</p></div>
          </div>
        </div>'''
        energie_tab = mo.vstack([
            mo.Html(f'''<div class="pls"><div class="pls-g2"><div>{en_zaehler_html}</div><div>{en_live_html}{en_pv_html}</div></div></div>'''),
            mo.Html(f'<div class="pls">{en_jb_html}</div>'),
            mo.Html('<div class="pls"><div class="pls-c"><h3>📈 Lastgang Vortag (Stundenmittelwerte)</h3></div></div>'),
            fig_en,
            mo.Html(f'''<div class="pls"><div class="pls-g2"><div>{en_vertrag_html}</div><div>{en_vertrag_apw_html}</div></div>
                <div class="pls-g2"><div>{en_kennz_html}</div><div>{en_bhkw_html}</div></div></div>'''),
        ])

        # === ZWEISTUFIGE TAB-STRUKTUR ===
        # Gruppierung der 13 Einzeltabs in 6 Hauptrubriken, die
        # den Fachperspektiven der Unterrichtsnutzung entsprechen:
        #   🏭 Anlage            – Topografie & Schema
        #   ⚙️ Betrieb           – Live-Steuerung & Verlaufsdaten
        #   🔬 Prozess           – Detailsicht je Verfahrensstufe
        #   🔧 Instandhaltung    – Ausrüstung & Wartung
        #   📐 Regelung & Labor  – Regelungstechnik, Chemie, Analytik
        #   🏗️ Modifikationen   – strategische Umbauten (eigenständig)
        #
        # lazy=True: Inhalte nicht-aktiver (Unter-)Tabs werden erst
        # beim Anklicken berechnet → spürbar schnelleres Erstladen.
        tabs = mo.ui.tabs({
            "🏭 Anlage": mo.ui.tabs({
                "Übersicht": overview,
                "Fließschema": fliessschema,
                "Außenanlagen": aussenanlagen,
            }, lazy=True),
            "⚙️ Betrieb": mo.ui.tabs({
                "Steuerung": steuerung,
                "Ablauf & Verlauf": ablauf,
                "Energie": energie_tab,
            }, lazy=True),
            "🔬 Prozess": mo.ui.tabs({
                "Zulauf": zulauf,
                "Biologie": biologie,
                "Nachklärung": nachklaerung,
            }, lazy=True),
            "🔧 Instandhaltung": mo.ui.tabs({
                "Pumpen": pumpen,
                "Armaturen": armaturen,
            }, lazy=True),
            "📐 Regelung & Labor": mo.ui.tabs({
                "Regelung": regelung,
                "Labor": labor,
            }, lazy=True),
            "🏗️ Modifikationen": modifikationen,
        }, lazy=True)

        mo.output.replace(mo.vstack([mo.Html(hdr), tabs]))
    return


if __name__ == "__main__":
    app.run()
