import streamlit as st

# ---------- Controls ----------
# If you already manage `x` elsewhere (e.g., with your own button),
# just set x before this block and comment out the number_input.
x = st.number_input("Number of columns", min_value=1, max_value=20, value=5, step=1)

ROWS_TOTAL = 9 + 9 + 6  # 24 rows
emoji = {"True": "✅", "False": "❌", "Maybe": "🤔", "Unkown": "❓"}

colors = ['Gelb', 'Lila', 'Grün', 'Blau', 'Rot', 'Weiß']
weapons = ['Messer', 'Leuchter', 'Pistole', 'Gift', 'Trophäe', 'Seil', 'Baseball', 'Axt', 'Hantel']
rooms = ['Halle','Speisezimmer', 'Küche', 'Terrasse', 'Observatorium', 'Kino', 'Wohnzimmer', 'Spa', 'Gästezimmer']

rows = colors + weapons + rooms

# ---------- Init / Reset on x change ----------
if "last_x" not in st.session_state:
    st.session_state.last_x = x

# Reinitialize grid & column names the first time or whenever x changes
if ("grid" not in st.session_state) or (st.session_state.last_x != x):
    st.session_state.grid = [["Unkown"] * x for _ in range(ROWS_TOTAL)]
    st.session_state.col_names = [f"Col {i+1}" for i in range(x)]
    st.session_state.last_x = x


# ---------- Column header (visual names only) ----------
header = st.columns(x + 1)
header[0].markdown("**Row**")
for c in range(x):
    # Visual-only column names; not tied to any DataFrame
    st.session_state.col_names[c] = header[c + 1].text_input(
        label=f"Column {c+1}",
        value=st.session_state.col_names[c],
        key=f"colname-{c}-{x}",
        label_visibility="collapsed",
        placeholder=f"Col {c+1}",
        
    )

# can you add something that I dont have to double press each button

# ---------- Grid of emoji buttons ----------

for r in range(ROWS_TOTAL):
    cols = st.columns(x + 1)
    cols[0].markdown(f"{rows[r]}")

    for c in range(x):
        current = st.session_state.grid[r][c]
        pressed = cols[c + 1].button(
            emoji[current],
            key=f"btn-{r}-{c}-{x}",
            help=f"{st.session_state.col_names[c]} – {current}",
            use_container_width=True,
        )
        if pressed:
            if current == "Unkown":
                st.session_state.grid[r][c] = "False"
            elif current == "False":
                st.session_state.grid[r][c] = "Maybe"
            elif current == "Maybe":
                st.session_state.grid[r][c] = "True"
            else:
                st.session_state.grid[r][c] = "Unkown"

# add a counter of total trues for each column under the entire buttons
col_true_count = []
for c in range(x):
    col_true_count.append(sum(1 for r in range(ROWS_TOTAL) if st.session_state.grid[r][c] == "True"))
# print col true count all of them 
for c in range(x):
    st.write(f"**{st.session_state.col_names[c]}**: {col_true_count[c]} True(s)")

st.caption("Legend: ✅ True   ❌ False   🤔 Maybe   ❓ Unknown")
