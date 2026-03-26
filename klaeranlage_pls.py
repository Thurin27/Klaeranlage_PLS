# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
#     "numpy",
#     "datetime",
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
    mod_faulturm = mo.ui.switch(label="Faulturm + BHKW")
    mod_pv = mo.ui.switch(label="PV-Anlage (Dachflächen)")
    return mod_anammox, mod_faulturm, mod_intermit, mod_membran, mod_nh4_sensor, mod_p_online, mod_pv, mod_spektral, mod_stufe4, mod_truebung, mod_turbo


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
    # === PERSISTENTER ZUSTAND mit mo.state ===
    get_sim_state, set_sim_state = mo.state(None)
    return get_sim_state, set_sim_state


@app.cell
def _(
    abschlag_schwelle, btn_1h, btn_24h, btn_6h, btn_7d, btn_reset,
    faellmittel, get_sim_state,
    mod_anammox, mod_faulturm, mod_intermit, mod_membran, mod_nh4_sensor,
    mod_p_online, mod_pv, mod_spektral, mod_stufe4, mod_truebung, mod_turbo,
    np, o2_soll, regen_faktor, rs_verhaeltnis, set_sim_state,
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

        # Denitrifikation — intermittierende Belüftung verbessert Deni deutlich
        deni_basis = min(0.90, 0.5 + ctrl["rs_verhaeltnis"] * 0.25)
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
        Q_rs = Q * ctrl["rs_verhaeltnis"]
        ts_rs = float(np.clip(ts * (1 + 1 / ctrl["rs_verhaeltnis"]) * 0.7, 5, 15))

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
        Q_rs=0.05, ts_rs=0.02,
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
        stufe4=mod_stufe4.value, faulturm=mod_faulturm.value, pv=mod_pv.value,
    )
    ctrl = dict(
        o2_soll=o2_soll.value, rs_verhaeltnis=rs_verhaeltnis.value,
        ues_menge=ues_menge.value, faellmittel=faellmittel.value,
        zulauf_q=zulauf_q.value, regen_faktor=regen_faktor.value,
        temperatur=temperatur.value, abschlag_schwelle=abschlag_schwelle.value,
        mods=mods,
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

    # Energie mit Modifikationen
    e_belueftung = Q * ctrl["o2_soll"] * 0.8 / 1000
    if mods["nh4_sensor"]: e_belueftung *= 0.75  # NH₄-geführt spart ~25%
    if mods["membran"]: e_belueftung *= 0.70  # besserer O₂-Transfer
    if mods["intermit"]: e_belueftung *= 0.85  # Belüftungspausen
    e_geblaese = e_belueftung
    if mods["turbo"]: e_geblaese *= 0.82  # ~18% effizienter als Drehkolben
    e_pumpen = (Q + current["Q_rs"]) * 0.02
    e_grundlast = 500
    e_stufe4 = Q * 0.05 / 24 if mods["stufe4"] else 0  # GAK: ~0.05 kWh/m³
    e_anammox = 30 if mods["anammox"] else 0  # Heizung + Mischer
    e_gesamt = e_geblaese + e_pumpen + e_grundlast + e_stufe4 + e_anammox

    # Energieerzeugung
    e_bhkw = Q * 0.04 if mods["faulturm"] else 0  # ~40% Eigenversorgung
    e_pv = 350 if mods["pv"] else 0  # ~350 kWh/d bei 100 kWp
    e_erzeugung = e_bhkw + e_pv
    e_netto = e_gesamt - e_erzeugung

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
        "fm_kosten": fm_kosten,
    })
    return


@app.cell
def _(
    abschlag_schwelle, btn_1h, btn_24h, btn_6h, btn_7d, btn_reset,
    detail_p11, detail_p51,
    faellmittel, get_sim_state,
    lab_analyse_btn, lab_kal_btn, lab_show_isv, lab_show_proto, lab_show_qs, lab_woche_btn,
    mod_anammox, mod_faulturm, mod_intermit, mod_membran, mod_nh4_sensor,
    mod_p_online, mod_pv, mod_spektral, mod_stufe4, mod_truebung, mod_turbo,
    mo, np, o2_soll,
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
                    + vr("spez. Verbrauch", f"{st['energie']/max(1,c['Q_zu'])*1000:.1f}", "Wh/m³")
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

        # RS-Pumpe aus Verhältnis
        rs_q = c["Q_zu"] / 24 * rs_verhaeltnis.value
        rs_fu_hz = min(50, max(25, 50 * rs_verhaeltnis.value / 1.0))

        # ÜS aus Menge
        ues_q_h = ues_menge.value / 24
        ues_laufzeit = min(24, ues_menge.value / max(1, ues_q_h * 3) * 24) if ues_q_h > 0 else 0

        steuerung = mo.vstack([
            mo.Html('<div class="pls"><div class="pls-c" style="border-color:#e94560"><h3 style="color:#e94560">⏱ Zeitsimulation</h3><p style="font-size:0.85em;color:#b2bec3">Stelle zuerst die Steuerungsparameter ein, dann drücke einen Zeitschritt-Button. Änderungen wirken sich verzögert aus – genau wie in der Realität!</p></div></div>'),
            mo.hstack([btn_1h, btn_6h, btn_24h, btn_7d, btn_reset], justify="start", gap=0.5),
            mo.Html(f'<div class="pls"><p style="font-size:0.9em">Simulationszeit: <strong>{sim_zeit}</strong> ({th:.0f} Stunden gesamt)</p></div>'),

            # --- ZULAUFBEDINGUNGEN ---
            mo.Html('<div class="pls"><div class="pls-c"><h3>🌊 Zulaufbedingungen & Abschlag</h3></div></div>'),
            mo.hstack([
                mo.vstack([zulauf_q, regen_faktor, temperatur, abschlag_schwelle]),
                mo.Html(f'''<div class="pls" style="font-size:0.85em">
                    <div class="pls-c">
                        <h3>Technischer Hintergrund</h3>
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
            ]),
            mo.Html(f'<div class="pls">{abschlag_html}</div>') if abschlag_aktiv else mo.Html(""),

            # --- BIOLOGISCHE STUFE ---
            mo.Html('<div class="pls"><div class="pls-c"><h3>🔬 Biologische Stufe</h3></div></div>'),
            mo.hstack([
                mo.vstack([o2_soll, rs_verhaeltnis, ues_menge]),
                mo.Html(f'''<div class="pls" style="font-size:0.85em">
                    <div class="pls-c">
                        <h3>O₂-Sollwert → Gebläse & Belüftung</h3>
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
                    <div class="pls-c">
                        <h3>RS-Verhältnis → Rücklaufschlammpumpe P3.1</h3>
                        <p>Das RS-Verhältnis bestimmt den Volumenstrom der
                        <strong>KSB Sewatec RS-Pumpe</strong> (FU-geregelt).</p>
                        {vtbl(
                            vr("RS-Förderstrom Q", f"{rs_q:.0f}", "m³/h")
                            + vr("FU-Frequenz", f"{rs_fu_hz:.0f}", "Hz")
                            + vr("TS Rücklaufschlamm", f"{c['ts_rs']:.1f}", "g/L")
                        )}
                        <p>Höheres RS-Verhältnis → bessere Denitrifikation (mehr NO₃-Rückführung),
                        aber dünnerer RS → niedrigerer TS im Belebungsbecken. Außerdem steigt
                        die hydraulische Belastung der Nachklärung.</p>
                    </div>
                    <div class="pls-c">
                        <h3>Überschussschlamm → ESP P5.1 (Seepex BN 52-6L)</h3>
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
            ]),

            # --- CHEMISCHE STUFE ---
            mo.Html('<div class="pls"><div class="pls-c"><h3>🧪 Chemische Stufe</h3></div></div>'),
            mo.hstack([
                mo.vstack([faellmittel]),
                mo.Html(f'''<div class="pls" style="font-size:0.85em">
                    <div class="pls-c">
                        <h3>Fällmitteldosierung → Kolbenmembranpumpe P7.1</h3>
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
            ]),

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

        # Rücklaufschlammpumpen: 2 Stück, Typ: Propellerpumpe / Kreiselpumpe
        rsp_Q_nenn = Q_rs_h * 1.2
        rsp_Q_ist = Q_rs_h
        rsp_H_geo = 1.5
        rsp_H_verl = 0.3 + (rsp_Q_ist / 500) ** 2 * 1.8
        rsp_H_ist = rsp_H_geo + rsp_H_verl
        rsp_eta = max(0.50, 0.75 - abs(rsp_Q_ist - rsp_Q_nenn * 0.85) / max(1, rsp_Q_nenn) * 0.25)
        rsp_P = rsp_Q_ist / 3600 * 9810 * rsp_H_ist / rsp_eta / 1000 if rsp_eta > 0 else 0
        rsp_f = min(50, max(25, 50 * rsp_Q_ist / max(1, rsp_Q_nenn * 0.85)))
        rsp_bh = 12450 + th

        # Interne Rezirkulation (Denizone → Nitrifikation)
        irez_Q_ist = Q_h * 2.0  # ca. 2× Qzu
        irez_Q_nenn = Q_h * 2.5
        irez_H_ist = 0.4
        irez_eta = 0.65
        irez_P = irez_Q_ist / 3600 * 9810 * irez_H_ist / irez_eta / 1000 if irez_eta > 0 else 0
        irez_f = min(50, max(30, 50 * irez_Q_ist / max(1, irez_Q_nenn * 0.85)))
        irez_bh = 11800 + th

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
                    + vr("Leistung P₁", f"{zp_P:.1f}", "kW")
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
                    + vr("Leistung P₁", f"{irez_P:.2f}", "kW")
                    + vr("Wirkungsgrad η", f"{irez_eta*100:.0f}", "%")
                    + vr("Betriebsstunden", f"{irez_bh:.0f}", "h")
                    + vr("Rez.-Verhältnis", f"{irez_Q_ist/max(1,Q_h):.1f}", "× Q_zu")
                )}
            </div>
        </div>

        <div class="pls-g2">
            <div class="pls-c">
                <h3>RS-Pumpe P3.1 (Betrieb) {pump_status(True)}</h3>
                <p style="font-size:0.8em;color:#b2bec3;margin:0 0 6px">KSB Sewatec – Kreiselpumpe, FU-geregelt</p>
                {vtbl(
                    vr("Förderstrom Q", f"{rsp_Q_ist:.0f}", "m³/h")
                    + vr("Förderhöhe H", f"{rsp_H_ist:.1f}", "m")
                    + vr("Drehzahl (FU)", f"{rsp_f:.0f}", "Hz")
                    + vr("Leistung P₁", f"{rsp_P:.1f}", "kW")
                    + vr("Wirkungsgrad η", f"{rsp_eta*100:.0f}", "%", wl=60, dl=50)
                    + vr("TS Rücklaufschlamm", f"{c['ts_rs']:.1f}", "g/L")
                    + vr("Betriebsstunden", f"{rsp_bh:.0f}", "h")
                    + vr("RS-Verhältnis", f"{rs_verhaeltnis.value:.2f}", "-")
                )}
                {pump_curve_svg(rsp_Q_nenn, 4.0, rsp_Q_ist, rsp_H_ist, rsp_eta, "RS-Pumpe P3.1")}
            </div>
            <div class="pls-c">
                <h3>RS-Pumpe P3.2 (Reserve) {pump_status_reserve()}</h3>
                <p style="font-size:0.8em;color:#b2bec3;margin:0 0 6px">KSB Sewatec – Kreiselpumpe, FU-geregelt</p>
                {vtbl(
                    vr("Status", "Standby", "")
                    + vr("Nenn-Q / Nenn-H", f"{rsp_Q_nenn:.0f} / 4.0", "m³/h / m")
                    + vr("Betriebsstunden", f"{rsp_bh - 1800:.0f}", "h")
                )}
                {pump_curve_svg(rsp_Q_nenn, 4.0, 0, rsp_H_ist*0.65, 0, "RS-Pumpe P3.2 (Reserve)")}
            </div>
        </div>

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
                    <th style="padding:8px 16px;color:#74b9ff;text-align:right">P [kW]</th>
                    <th style="padding:8px 16px;color:#74b9ff;text-align:center">Status</th>
                </tr>
                <tr style="border-bottom:1px solid #0f3460"><td style="padding:5px 16px">P1.1 Zulauf</td><td style="padding:5px 16px">Kreiselpumpe</td><td style="text-align:right;padding:5px 16px">{zp_Q_ist:.0f}&ensp;m³/h</td><td style="text-align:right;padding:5px 16px">{zp_P:.1f}</td><td style="text-align:center;padding:5px 16px">{pump_status(True)}</td></tr>
                <tr style="border-bottom:1px solid #0f3460"><td style="padding:5px 16px">P1.2 Zulauf</td><td style="padding:5px 16px">Kreiselpumpe</td><td style="text-align:right;padding:5px 16px">–</td><td style="text-align:right;padding:5px 16px">–</td><td style="text-align:center;padding:5px 16px">{pump_status_reserve()}</td></tr>
                <tr style="border-bottom:1px solid #0f3460"><td style="padding:5px 16px">P3.1 RS</td><td style="padding:5px 16px">Kreiselpumpe</td><td style="text-align:right;padding:5px 16px">{rsp_Q_ist:.0f}&ensp;m³/h</td><td style="text-align:right;padding:5px 16px">{rsp_P:.1f}</td><td style="text-align:center;padding:5px 16px">{pump_status(True)}</td></tr>
                <tr style="border-bottom:1px solid #0f3460"><td style="padding:5px 16px">P3.2 RS</td><td style="padding:5px 16px">Kreiselpumpe</td><td style="text-align:right;padding:5px 16px">–</td><td style="text-align:right;padding:5px 16px">–</td><td style="text-align:center;padding:5px 16px">{pump_status_reserve()}</td></tr>
                <tr style="border-bottom:1px solid #0f3460"><td style="padding:5px 16px">P4.1 Rez.</td><td style="padding:5px 16px">Propellerpumpe</td><td style="text-align:right;padding:5px 16px">{irez_Q_ist:.0f}&ensp;m³/h</td><td style="text-align:right;padding:5px 16px">{irez_P:.2f}</td><td style="text-align:center;padding:5px 16px">{pump_status(True)}</td></tr>
                <tr style="border-bottom:1px solid #0f3460"><td style="padding:5px 16px">P2.1 PS</td><td style="padding:5px 16px">Exz.schnecke</td><td style="text-align:right;padding:5px 16px">{ps_Q_h:.2f}&ensp;m³/h</td><td style="text-align:right;padding:5px 16px">{ps_P:.1f}</td><td style="text-align:center;padding:5px 16px">{pump_status(True)}</td></tr>
                <tr style="border-bottom:1px solid #0f3460"><td style="padding:5px 16px">P5.1 ÜS</td><td style="padding:5px 16px">Exz.schnecke</td><td style="text-align:right;padding:5px 16px">{ues_Q_h:.2f}&ensp;m³/h</td><td style="text-align:right;padding:5px 16px">{ues_P:.1f}</td><td style="text-align:center;padding:5px 16px">{pump_status(True)}</td></tr>
                <tr style="border-bottom:1px solid #0f3460"><td style="padding:5px 16px">P6.1 DS</td><td style="padding:5px 16px">Exz.schnecke</td><td style="text-align:right;padding:5px 16px">{ds_Q_h:.2f}&ensp;m³/h</td><td style="text-align:right;padding:5px 16px">{ds_P:.1f}</td><td style="text-align:center;padding:5px 16px">{pump_status(ds_Q_h > 0.1)}</td></tr>
                <tr style="border-bottom:1px solid #0f3460"><td style="padding:5px 16px">P7.1 Fe³⁺</td><td style="padding:5px 16px">Kolbenmembran</td><td style="text-align:right;padding:5px 16px">{fm_Q:.1f}&ensp;L/h</td><td style="text-align:right;padding:5px 16px">{fm_P:.2f}</td><td style="text-align:center;padding:5px 16px">{pump_status(fm_Q > 0)}</td></tr>
                <tr style="border-bottom:1px solid #0f3460"><td style="padding:5px 16px">P8.1 Poly</td><td style="padding:5px 16px">Kolbenmembran</td><td style="text-align:right;padding:5px 16px">{poly_Q:.1f}&ensp;L/h</td><td style="text-align:right;padding:5px 16px">{poly_P:.2f}</td><td style="text-align:center;padding:5px 16px">{pump_status(poly_Q > 0.5)}</td></tr>
                <tr style="border-bottom:1px solid #0f3460"><td style="padding:5px 16px">P9.1 Kalk</td><td style="padding:5px 16px">Kolbenmembran</td><td style="text-align:right;padding:5px 16px">{kalk_Q:.1f}&ensp;L/h</td><td style="text-align:right;padding:5px 16px">{kalk_P:.2f}</td><td style="text-align:center;padding:5px 16px">{pump_status(kalk_aktiv)}</td></tr>
                <tr style="border-top:2px solid #74b9ff"><td colspan="3" style="padding:6px 16px;font-weight:bold;color:#74b9ff">Σ Pumpenleistung</td>
                    <td style="text-align:right;padding:6px 16px;font-weight:bold;color:#74b9ff">{zp_P + rsp_P + irez_P + ps_P + ues_P + ds_P + fm_P + poly_P + kalk_P:.1f}</td>
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
        p11_strom = zp_P * np.ones(56) + np.random.normal(0, zp_P * 0.03, 56) + _tage * 0.003
        p11_strom[-7:] += 0.15
        p11_flow = zp_Q_ist * 1.02 * np.ones(56) + np.random.normal(0, zp_Q_ist * 0.04, 56) - _tage * 0.02
        p11_vib = 2.5 + np.random.normal(0, 0.3, 56) + _tage * 0.015
        p11_vib[-5:] += np.array([0.3, 0.5, 0.2, 0.8, 0.6])
        p11_tlager = 45 + np.random.normal(0, 1.5, 56) + _tage * 0.08
        p11_tlager[-7:] += 3

        if detail_p11.value:
            fig11 = _mp(rows=2, cols=2,
                subplot_titles=("Stromaufnahme P₁ [kW]", "Förderstrom Q [m³/h]",
                                "Vibration [mm/s]", "Lagertemperatur [°C]"),
                vertical_spacing=0.18, horizontal_spacing=0.10)
            fig11.add_trace(_go.Scatter(x=_tage, y=p11_strom, mode='lines+markers',
                line=dict(color='#0984e3', width=1.5), marker=dict(size=3)), row=1, col=1)
            fig11.add_hline(y=zp_P*1.15, line_dash="dash", line_color="#e17055", row=1, col=1,
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
                    P1.1/P1.2 und RS-Pumpen P3.1/P3.2 im Rahmen der Inbetriebnahme und bei
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
                <tr style="border-bottom:1px solid #0f3460"><td style="padding:5px 16px">RS-Regelung</td><td style="padding:5px 16px">Schlammschicht NK [cm]</td><td style="padding:5px 16px">P3.1 RS-Pumpe (FU)</td><td style="padding:5px 16px">PI</td></tr>
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
            "faulturm": {"name": "Faulturm + BHKW", "kat": "Umbau", "inv": 1500000, "betr": 40000,
                "icon": "🟣", "color": "#a29bfe",
                "tech": "Mesophiler Faulturm (37°C, HRT ~20 d) für Primär- und Überschussschlamm. Biogas → BHKW (Gasmotor, η_el ~38%, η_th ~45%). Wärme für Faulturm-Heizung und Gebäude.",
                "wirkung": f"Energieerzeugung ca. {c['Q_zu']*0.04:.0f} kWh/d. Faulgasproduktion ca. {c['Q_zu']*0.025:.0f} Nm³/d. Reduktion Klärschlammvolumen um ~30%. Kann 30-50% des Eigenbedarfs decken."},
            "pv": {"name": "PV-Anlage (Dachflächen)", "kat": "Umbau", "inv": 100000, "betr": 1500,
                "icon": "🟣", "color": "#a29bfe",
                "tech": "100 kWp PV auf Betriebsgebäuden und NK-Abdeckungen. ~950 kWh/(kWp·a) in NRW → ~350 kWh/d im Jahresmittel. Eigenverbrauchsanteil auf KA typisch >85%.",
                "wirkung": "Ca. 350 kWh/d Eigenstromerzeugung. Amortisation 7-10 Jahre. CO₂-Einsparung ~90 t/a. Kombinierbar mit Batteriespeicher für Spitzenabdeckung."},
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
        e_spar = max(0, 500 + c["Q_zu"] * o2_soll.value * 0.8 / 1000 + (c["Q_zu"] + c["Q_rs"]) * 0.02 - e.get("e_gesamt", 0))

        modifikationen = mo.vstack([
            mo.Html(f'''<div class="pls">
            <div class="pls-c"><h3>🏗️ Anlagenmodifikationen – Virtueller Umbau</h3>
                <p style="font-size:0.9em;margin:6px 0">
                    Aktiviere Modifikationen um deren Auswirkungen auf Ablaufqualität, Energieverbrauch und
                    Betriebskosten direkt in der Simulation zu sehen. Die Effekte werden sofort in allen Tabs sichtbar.
                </p>
                {vtbl(
                    vr("Aktive Modifikationen", f"{n_aktiv}", "von 11")
                    + vr("Investitionssumme", f"{inv_total:,.0f}", "€")
                    + vr("Zusätzl. Betriebskosten", f"{betr_total:,.0f}", "€/a")
                    + vr("Energieeinsparung Belüftung", f"{e_spar:.0f}", "kWh/d")
                    + vr("Energieerzeugung", f"{e.get('e_erzeugung',0):.0f}", "kWh/d")
                    + vr("Netto-Energieverbrauch", f"{e.get('e_netto',0):.0f}", "kWh/d")
                    + vr("Fällmittelkosten", f"{e.get('fm_kosten',0):.1f}", "€/d")
                )}
            </div>
            </div>'''),

            # Messtechnik
            mo.Html('<div class="pls"><div class="pls-c" style="border-color:#00b894"><h3 style="color:#00b894">🟢 Messtechnik & Regelungsoptimierung</h3><p style="font-size:0.85em;color:#b2bec3;margin:0">Geringe Investition, schneller Effekt, oft die wirtschaftlichste Maßnahme.</p></div></div>'),
            mo.hstack([mod_p_online, mod_nh4_sensor, mod_spektral, mod_truebung], justify="start", gap=0.5),
            mo.Html(f'''<div class="pls"><div class="pls-g2">
                {mod_card("p_online", mod_p_online)}
                {mod_card("nh4_sensor", mod_nh4_sensor)}
            </div><div class="pls-g2">
                {mod_card("spektral", mod_spektral)}
                {mod_card("truebung", mod_truebung)}
            </div></div>'''),

            # Verfahrenstechnik
            mo.Html('<div class="pls"><div class="pls-c" style="border-color:#0984e3"><h3 style="color:#0984e3">🔵 Verfahrenstechnische Erweiterungen</h3><p style="font-size:0.85em;color:#b2bec3;margin:0">Mittlere Investition, erhebliche Betriebsverbesserung.</p></div></div>'),
            mo.hstack([mod_membran, mod_turbo, mod_intermit, mod_anammox], justify="start", gap=0.5),
            mo.Html(f'''<div class="pls"><div class="pls-g2">
                {mod_card("membran", mod_membran)}
                {mod_card("turbo", mod_turbo)}
            </div><div class="pls-g2">
                {mod_card("intermit", mod_intermit)}
                {mod_card("anammox", mod_anammox)}
            </div></div>'''),

            # Große Umbauten
            mo.Html('<div class="pls"><div class="pls-c" style="border-color:#a29bfe"><h3 style="color:#a29bfe">🟣 Größere Umbauten & Neubauten</h3><p style="font-size:0.85em;color:#b2bec3;margin:0">Hohe Investition, transformative Wirkung.</p></div></div>'),
            mo.hstack([mod_stufe4, mod_faulturm, mod_pv], justify="start", gap=0.5),
            mo.Html(f'''<div class="pls"><div class="pls-g2">
                {mod_card("stufe4", mod_stufe4)}
                {mod_card("faulturm", mod_faulturm)}
            </div><div class="pls-g2">
                {mod_card("pv", mod_pv)}
                <div></div>
            </div></div>'''),
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
            mo.Html(f'''<div class="pls"><div class="pls-c">
                <h3>🔬 Betriebslabor – Analysentechnik & Qualitätssicherung</h3>
                <p style="font-size:0.9em;margin:6px 0">
                    Das Betriebslabor führt die Eigenüberwachung nach SüwVO Abw NRW durch.
                    Hier können Analysen simuliert, Messprotokolle ausgewertet und die
                    Qualitätssicherung geprüft werden. Alle Messwerte basieren auf den
                    aktuellen Simulationsdaten der Kläranlage.
                </p>
            </div></div>'''),

            # Analysen-Bereich
            mo.Html('<div class="pls"><div class="pls-c" style="border-color:#00b894"><h3 style="color:#00b894">🧪 Probenahme & Analyse</h3><p style="font-size:0.85em;color:#b2bec3;margin:0">Führe eine virtuelle Probenahme mit Doppelbestimmung durch. Jeder Klick = neue Probe mit realistischer Messstreuung.</p></div></div>'),
            mo.hstack([lab_analyse_btn], justify="start"),
            mo.Html(f'<div class="pls">{analysen_html}</div>') if analysen_html else mo.Html(""),

            # Methodensteckbriefe
            mo.Html(f'''<div class="pls"><div class="pls-c"><h3>📖 Analysenmethoden (Steckbriefe)</h3></div>
            <div class="pls-g3">{methoden_cards}</div></div>'''),

            # ISV
            mo.Html('<div class="pls"><div class="pls-c" style="border-color:#e17055"><h3 style="color:#e17055">🔬 Schlammanalytik</h3></div></div>'),
            lab_show_isv,
            isv_panel,

            # Eigenüberwachung
            mo.Html('<div class="pls"><div class="pls-c" style="border-color:#74b9ff"><h3 style="color:#74b9ff">📋 Eigenüberwachung & Probenahmeplan</h3></div></div>'),
            mo.hstack([lab_show_proto, lab_woche_btn], justify="start", gap=1),
            proto_panel,

            # QS
            mo.Html('<div class="pls"><div class="pls-c" style="border-color:#a29bfe"><h3 style="color:#a29bfe">📈 Qualitätssicherung</h3></div></div>'),
            mo.hstack([lab_show_qs, lab_kal_btn], justify="start", gap=1),
            qs_panel,
        ])

        tabs = mo.ui.tabs({
            "🏭 Übersicht": overview,
            "⚙️ Steuerung": steuerung,
            "🏗️ Modifikationen": modifikationen,
            "🌊 Ablauf & Verlauf": ablauf,
            "🚰 Zulauf": zulauf,
            "🔬 Biologie": biologie,
            "⬇️ Nachklärung": nachklaerung,
            "🔧 Pumpen": pumpen,
            "📐 Regelung": regelung,
            "🧪 Labor": labor,
        })

        mo.output.replace(mo.vstack([mo.Html(hdr), tabs]))
    return


if __name__ == "__main__":
    app.run()
