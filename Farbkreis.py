import streamlit as st
import numpy as np
from collections import Counter



st.set_page_config(
    page_title="Farbkreisrätsel 🎨",
    page_icon="🎨",
    layout="centered",
    initial_sidebar_state="expanded"
)



st.title("🎨 Farbkreis-Rätsel")






if not st.session_state.get("farben_bestätigt"):
    # 🔧 Verfügbare Farbemojis & Hexcodes
    verfügbare_farben = {
        "🔴": "#CA082D",
        "🟠": "#FBB416",
        "🟡": "#FAEF52",
        "🟢": "#09AB3B",
        "🔵": "#0068C9",
        "🟣": "#800080"
    }



    # 🧠 Nur einmalig initialisieren (nicht jedes Mal überschreiben!)
    if "ausgewählte_farben" not in st.session_state:
        st.session_state.ausgewählte_farben = []

    st.subheader("**🎨 Wähle drei Farben aus:**")
    spalten = st.columns(len(verfügbare_farben))

    # 🟡 Interaktive Buttons: ergänzen oder entfernen
    for i, (emoji, hexcode) in enumerate(verfügbare_farben.items()):
        aktiv = emoji in st.session_state.ausgewählte_farben
        label = f"{'✅ ' if aktiv else ''}{emoji}"
        
        if spalten[i].button(label, key=f"btn_{emoji}"):
            # Beim Klick toggeln
            if aktiv:
                st.session_state.ausgewählte_farben.remove(emoji)
                st.rerun()
            elif len(st.session_state.ausgewählte_farben) < 3:
                st.session_state.ausgewählte_farben.append(emoji)
                st.rerun()       

    # 📦 Optional: Mapping für spätere Verwendung im Spiel
    if len(st.session_state.ausgewählte_farben) == 3:
        st.session_state.benutzer_farben = {
            emoji: verfügbare_farben[emoji]
            for emoji in st.session_state.ausgewählte_farben
        }
        st.success(f"Farben ausgewählt: {' '.join(st.session_state.ausgewählte_farben)} 🎯")
    else:
        fehlend = 3 - len(st.session_state.ausgewählte_farben)
        st.info(f"{fehlend} Farbe{'n' if fehlend > 1 else ''} fehlen noch zur Auswahl.")



    if len(st.session_state.ausgewählte_farben) == 3:
        if st.button("✅ Farben übernehmen"):
            st.session_state.benutzer_farben = {
                f: verfügbare_farben[f] for f in st.session_state.ausgewählte_farben
            }
            st.session_state.farben_bestätigt = True
            st.rerun()
else:
    st.markdown("🎨 Farben festgelegt: **" + " ".join(st.session_state.ausgewählte_farben) + "**")






anzahl_kreise = 27

# 🧠 Session-Variablen initialisieren
st.session_state.setdefault("kreis_farben", ["white"] * anzahl_kreise)
st.session_state.setdefault("aktueller_idx", 0)


aktueller_idx = st.session_state.aktueller_idx

import time

# Startzeit initialisieren
st.session_state.setdefault("startzeit", time.time())


st.subheader("🔥 Deine Mission:")
st.info("Gestalte den Kreis mit **nur drei Farben**, sodass **jede Kombination von drei aufeinanderfolgenden Farben im Uhrzeigersinn nur einmal erscheint.**")


# Farbkreis anzeigen
winkel = np.linspace(0, 2 * np.pi, anzahl_kreise, endpoint=False)
radius = 140
mitte = 150
punkte = [(mitte + np.cos(w)*radius, mitte + np.sin(w)*radius) for w in winkel]

html = f"<div style='position:relative;width:{2*mitte}px;height:{2*mitte}px;margin:auto;'>"
for i, (x, y) in enumerate(punkte):
    farbe = st.session_state.kreis_farben[i]
    rahmen = "4px solid black" if i == aktueller_idx else "1px solid gray"
    gesamt = anzahl_kreise
    z_index = gesamt + 1 if i == aktueller_idx else gesamt - i

    html += f"""
    <div style='
        position:absolute;
        top:{y}px; left:{x}px;
        transform:translate(-50%, -50%);
        width:30px; height:30px;
        background-color:{farbe};
        border-radius:50%;
        border:{rahmen};
        z-index:{z_index};
        ' title='Kreis {i+1}'>
    </div>
    """
html += "</div>"
st.components.v1.html(html, height=2*mitte + 30)





# 🎛️ Button-Leiste – nur wenn Farben gewählt wurden
if st.session_state.get("farben_bestätigt"):
    # 🎛️ Jetzt darf bemalt werden
    # Zeige Farb-Buttons, Navigation, etc.

    farben = st.session_state.benutzer_farben
    spalten = st.columns(len(farben) + 3)
    
    # 1–3: Farb-Buttons aus benutzerdefinierter Auswahl
    for i, (emoji, hexcode) in enumerate(farben.items()):
        if spalten[i].button(emoji, key=f"farb_{emoji}"):
            st.session_state.kreis_farben[aktueller_idx] = hexcode
            st.session_state.aktueller_idx = (aktueller_idx + 1) % anzahl_kreise
            st.rerun()
    
    # 4: Überspringen
    if spalten[-3].button("⏭️"):
        st.session_state.aktueller_idx = (aktueller_idx + 1) % anzahl_kreise
        st.rerun()
    
    # 5: Zurück
    if spalten[-2].button("↩️"):
        st.session_state.aktueller_idx = (aktueller_idx - 1) % anzahl_kreise
        st.rerun()

    # 6: Löschen & zurück
    if spalten[-1].button("❌"):
        st.session_state.kreis_farben[aktueller_idx] = "white"
        st.session_state.aktueller_idx = (aktueller_idx - 1) % anzahl_kreise
        st.rerun()
elif len(st.session_state.get("ausgewählte_farben", [])) == 3:
    st.info("✅ Du hast drei Farben gewählt – bitte bestätige die Auswahl, um loszulegen.")

    

# 🏷️ Fortschrittsanzeige
bemalt = [f for f in st.session_state.kreis_farben if f != "white"]
fortschritt = len(bemalt) / len(st.session_state.kreis_farben)
st.caption(f"Fortschritt: {int(fortschritt * 100)} %")
st.progress(fortschritt)
    
    
    
# 🧼 Zurücksetzen & Zufällig befüllen
spalten = st.columns(2)

if spalten[0].button("🔁 Alles zurücksetzen"):
    st.session_state.kreis_farben = ["white"] * anzahl_kreise
    st.session_state.aktueller_idx = 0
    #st.session_state.startzeit = time.time()
    st.experimental_rerun()

if spalten[1].button("🎲 Zufällig befüllen"):
    st.session_state.kreis_farben = [np.random.choice(list(farben.values())) for _ in range(27)]
    st.rerun()


# Spielende
if st.session_state.aktueller_idx >= 27:
    st.success("🎉 Alle Kreise wurden durchlaufen! Vielleicht willst du jetzt prüfen?")

      # ----------------------------------------------------         

# 🧪 Prüfung der 3er-Tripel
def tripel_check(farbenliste):
    n = len(farbenliste)
    tripel = [(farbenliste[i % n], farbenliste[(i + 1) % n], farbenliste[(i + 2) % n]) for i in range(n)]
    zaehlung = Counter(tripel)
    doppelt = [k for k, v in zaehlung.items() if v > 1]
    return len(zaehlung) == 27, doppelt


farbe_emoji = {"#CA082D": "🔴", "#09AB3B": "🟢", "#0068C9": "🔵", "#FAEF52": "🟡", "#FBB416":"🟠", "#800080": "🟣" }
def tripel_zu_emojis(tripel_liste):
    return "\n\n".join("• " + "".join(farbe_emoji.get(f, "❓") for f in tripel) for tripel in tripel_liste)



# 👀 Prüfen, ob alle Kreise bemalt sind
alle_bemalt = "white" not in st.session_state.kreis_farben

st.subheader("🔍 Lösung prüfen")
if alle_bemalt:
    if st.button("✅ Prüfen"):
        gültig, fehler = tripel_check(st.session_state.kreis_farben)
        if gültig:
            dauer = int(time.time() - st.session_state.startzeit)
            m, s = divmod(dauer, 60)
            st.success(f"🎉 Alle 3er-Farbkombinationen sind eindeutig! Rätsel gelöst in {m:02d}:{s:02d} Minuten! 🎯")
            st.balloons()
        
        if not gültig:
            fehlermeldung = "⚠️ Folgende Kombinationen treten mehrfach auf:\n\n" + tripel_zu_emojis(fehler)
            st.error(fehlermeldung)

else:
    st.info("💡 Wenn alle Kreise bemalt sind, kannst du deine Lösung prüfen!")



