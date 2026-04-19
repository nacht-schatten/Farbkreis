import streamlit as st
import numpy as np
from collections import Counter
import time


st.set_page_config(
    page_title="Farbkreisrätsel 🎨",
    page_icon="🎨",
    layout="centered",
    initial_sidebar_state="expanded"
)





st.title("🎨 Farbkreis-Rätsel")



if not st.session_state.get("level_bestätigt"):
    st.markdown("### 🧩 Wähle deine Mission:")

    level_optionen = {
        "🪄 Einfach (2 Farben, 3er-Tupel)": (2, 3),
        "💘 Farbpärchen (3 Farben, 2er-Tupel)": (3, 2),
        "🔍 Detektiv (4 Farben, 2er-Tupel)": (4, 2),
        "🦚 Paradies (5 Farben, 2er-Tupel)": (5, 2),
        "🌈 Pride (6 Farben, 2er-Tupel)": (6, 2),
        "🎨 Klassik (3 Farben, 3er-Tupel)": (3, 3),
        "🧮 Quartett (2 Farben, 4er-Tupel)": (2, 4),
        "🧠 Genie (2 Farben, 5er-Tupel)": (2, 5),
        "🗿 Boss (2 Farben, 6er-Tupel)": (2, 6),
        "👑 Endgame (4 Farben, 3er-Tupel)": (4, 3),
        "🫶 für Lisa (3 Farben, 4er-Tupel)": (3, 4),
        "🐦‍🔥 Magic (5 Farben, 3er-Tupel)": (5, 3),
        "🏹 (2 Farben, 7er-Tupel)": (2, 7),
    }

    ausgewähltes_level = st.selectbox(
        "Mission wählen",
        list(level_optionen.keys()),
        index=5
    )
    


    anzahl_farben, tupel_länge = level_optionen[ausgewähltes_level]
    anzahl_kreise = anzahl_farben ** tupel_länge
    st.session_state.level_name = ausgewähltes_level
    st.session_state.anzahl_farben, st.session_state.tupel_länge = level_optionen[ausgewähltes_level]
    st.session_state.anzahl_kreise = st.session_state.anzahl_farben ** st.session_state.tupel_länge

    if st.button("🚀 Mission starten"):
        st.session_state.level_gestartet = True
        st.session_state.level_bestätigt = True  # 👈 Neu!
        st.session_state.kreis_farben = ["white"] * anzahl_kreise
        st.session_state.aktueller_idx = 0
        st.session_state.farben_bestätigt = False
        st.session_state.letzte_farbauswahl = []
        st.session_state.ausgewählte_farben = []
        st.session_state.benutzer_farben = {}
        st.session_state.tupel_länge = tupel_länge
        st.session_state.anzahl_farben = anzahl_farben
        st.session_state.startzeit = time.time()
        st.rerun()

 
else:
    st.markdown(f"🏆 Gewählte Mission: **{st.session_state.level_name}**")

anzahl_farben = st.session_state.get("anzahl_farben")
tupel_länge = st.session_state.get("tupel_länge")
anzahl_kreise = st.session_state.get("anzahl_kreise")

st.info("##### 🔥 Deine Mission:\n\n" + f"\nBemale den Ring aus **{anzahl_kreise} Feldern** mit **{anzahl_farben} Farben** so, dass jede mögliche **{tupel_länge}-er-Gruppe benachbarter Felder** im Uhrzeigersinn eine einzigartige Farbfolge hat.")


if "kreis_farben" not in st.session_state or len(st.session_state.kreis_farben) != anzahl_kreise:
    st.session_state.kreis_farben = ["white"] * anzahl_kreise

# 🧠 Session-Variablen initialisieren
st.session_state.setdefault("kreis_farben", ["white"] * anzahl_kreise)
st.session_state.setdefault("aktueller_idx", 0)


aktueller_idx = st.session_state.aktueller_idx





if st.session_state.get("level_gestartet"):

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

        st.markdown(f"**🎨 Wähle {anzahl_farben} Farben aus:**")
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
                elif len(st.session_state.ausgewählte_farben) < anzahl_farben:
                    st.session_state.ausgewählte_farben.append(emoji)
                    st.rerun()       

    # 📦 Optional: Mapping für spätere Verwendung im Spiel
        if len(st.session_state.ausgewählte_farben) == anzahl_farben:
            st.session_state.benutzer_farben = {
                emoji: verfügbare_farben[emoji]
                for emoji in st.session_state.ausgewählte_farben
                }
            st.success(f"Farben ausgewählt: {' '.join(st.session_state.ausgewählte_farben)} 🎯")
        else:
            fehlend = anzahl_farben - len(st.session_state.ausgewählte_farben)
            st.info(f"{fehlend} Farbe{'n' if fehlend > 1 else ''} fehlen noch zur Auswahl.")



        if len(st.session_state.ausgewählte_farben) == anzahl_farben:
            if st.button("✅ Farben übernehmen"):
                st.session_state.benutzer_farben = {
                    f: verfügbare_farben[f] for f in st.session_state.ausgewählte_farben
                    }
                st.session_state.farben_bestätigt = True
                st.rerun()
    else:
        st.markdown("🎨 Farben festgelegt: **" + " ".join(st.session_state.ausgewählte_farben) + "**")

else:
    st.info("Sobald du ein Level gestartet hast, kannst du dir Farben aussuchen!")






# Farbkreis anzeigen
radius = int(85 + np.log2(0.3*anzahl_kreise) * 32)      # wächst mit log2
punktgröße = int(max(12, 76 - np.sqrt(anzahl_kreise) * 6.9))
mitte = radius + punktgröße

winkel = np.linspace(0, 2 * np.pi, anzahl_kreise, endpoint=False)
punkte = [(mitte + np.cos(w)*radius, mitte + np.sin(w)*radius) for w in winkel]

html = f"<div style='position:relative;width:{2*mitte}px;height:{2*mitte}px;margin:auto;'>"

for i, (x, y) in enumerate(punkte):
    farbe = st.session_state.kreis_farben[i]
    rahmen = "4px solid black" if i == aktueller_idx else "1px solid gray"
    z_index = anzahl_kreise + 1 if i == aktueller_idx else anzahl_kreise - i

    html += f"""
    <div style='
        position:absolute;
        top:{y}px; left:{x}px;
        transform:translate(-50%, -50%);
        width:{punktgröße}px; height:{punktgröße}px;
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
    spalten = st.columns(len(farben) +3)
    
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

       
elif len(st.session_state.get("ausgewählte_farben", [])) == anzahl_farben:
    st.info(f"✅ Du hast {anzahl_farben} Farben gewählt – bitte bestätige die Auswahl, um loszulegen.")
        
    

# 🏷️ Fortschrittsanzeige
bemalt = [f for f in st.session_state.kreis_farben if f != "white"]
fortschritt = len(bemalt) / len(st.session_state.kreis_farben)
st.caption(f"Fortschritt: {int(fortschritt * 100)} %")
st.progress(fortschritt)
    
    
    
# 🧼 Zurücksetzen & Zufällig befüllen
spalten = st.columns(2)
if st.session_state.get("farben_bestätigt"):
    if spalten[0].button("🧽 Kunstwerk zurücksetzen"):
        st.session_state.kreis_farben = ["white"] * anzahl_kreise
        st.session_state.aktueller_idx = 0
        st.session_state.startzeit = time.time()
        st.rerun()

    if spalten[1].button("🎲 Zufällig befüllen"):
        st.session_state.kreis_farben = [np.random.choice(list(farben.values())) for _ in range(anzahl_kreise)]
        st.rerun()
   
    



      # ----------------------------------------------------         



# 🧪 Prüfung der n-er-Tripel


def tupel_check(farbenliste, tupel_länge, erwartet_kombis):
    n = len(farbenliste)
    tupel = [
        tuple(farbenliste[(i + j) % n] for j in range(tupel_länge))
        for i in range(n)
    ]
    zaehlung = Counter(tupel)
    doppelt = [k for k, v in zaehlung.items() if v > 1]
    korrekt = len(zaehlung) == erwartet_kombis and not doppelt
    return korrekt, doppelt



farbe_emoji = {"#CA082D": "🔴", "#09AB3B": "🟢", "#0068C9": "🔵", "#FAEF52": "🟡", "#FBB416":"🟠", "#800080": "🟣" }
def tripel_zu_emojis(tripel_liste):
    return "\n\n".join("• " + "".join(farbe_emoji.get(f, "❓") for f in tripel) for tripel in tripel_liste)



# 👀 Prüfen, ob alle Kreise bemalt sind
alle_bemalt = "white" not in st.session_state.kreis_farben

st.subheader("🔍 Lösung prüfen")
if alle_bemalt:
    if st.button("✅ Prüfen"):
        farbenliste = st.session_state.kreis_farben
        tupel_länge = st.session_state.tupel_länge
        anzahl_farben = len(st.session_state.ausgewählte_farben)
        erwartet_kombis = anzahl_farben ** tupel_länge
        

        gültig, fehler = tupel_check(farbenliste, tupel_länge, erwartet_kombis)

        if gültig:
            dauer = int(time.time() - st.session_state.startzeit)
            m, s = divmod(dauer, 60)
            st.success(f"🎉 Alle {tupel_länge}er-Farbkombinationen sind einzigartig! Rätsel gelöst in {m:02d}:{s:02d} Minuten! 🎯")
            st.session_state.rätsel_gelöst = True 
            st.balloons()
           

        
        if not gültig:
            fehlermeldung = f"⚠️ Folgende {tupel_länge}er-Farbkombinationen treten mehrfach auf:\n\n" + tripel_zu_emojis(fehler)
            st.error(fehlermeldung)

else:
    st.info("💡 Wenn alle Kreise bemalt sind, kannst du deine Lösung prüfen!")



