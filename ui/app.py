import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.solver import solve_dual_simplex

st.set_page_config(page_title="Двоїстий симплекс-метод", layout="wide")

st.markdown("""
    <style>
        .stApp header {visibility: hidden;}
        .stDeployButton {display:none;}
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

st.title("Двоїстий симплекс-метод")

st.sidebar.header("Налаштування матриці")
num_vars = st.sidebar.number_input("Кількість змінних (n)", min_value=1, max_value=10, value=2)
num_cons = st.sidebar.number_input("Кількість обмежень (m)", min_value=1, max_value=10, value=2)

st.subheader("Цільова функція Z")
default_c = [-3.0, -2.0]
c_data = [default_c[i] if i < len(default_c) else 0.0 for i in range(num_vars)]
c_df = pd.DataFrame([c_data], columns=[f"x{i+1}" for i in range(num_vars)])
c_edited = st.data_editor(c_df, num_rows="fixed", use_container_width=True)

st.subheader("Матриця обмежень (Ax <= b)")

default_A = [[-1.0, -1.0], [1.0, -1.0]]
default_b = [-2.0, 1.0]

data = []
for i in range(num_cons):
    row = []
    for j in range(num_vars):
        row.append(default_A[i][j] if i < len(default_A) and j < len(default_A[0]) else 0.0)
    row.append(default_b[i] if i < len(default_b) else 0.0)
    data.append(row)

cols = [f"x{i+1}" for i in range(num_vars)] + ["b"]
Ab_df = pd.DataFrame(data, columns=cols)
Ab_edited = st.data_editor(Ab_df, num_rows="fixed", use_container_width=True)

if st.button("Розв'язати", type="primary", use_container_width=True):
    c = c_edited.iloc[0].values
    A = Ab_edited.iloc[:, :-1].values
    b = Ab_edited.iloc[:, -1].values
    
    st.markdown("---")
    st.header("Хід розв'язання")
    
    steps = solve_dual_simplex(c, A, b)
    
    for iteration, df, message in steps:
        if "Оптимальний" in message:
            st.success(message)
        elif "Задача не має" in message or "Помилка" in message or "Перевищено" in message:
            st.error(message)
        else:
            st.info(message)
            
        st.dataframe(
            df.style.map(lambda x: "color: red;" if x < 0 else None, subset=["b"]),
            use_container_width=True
        )
        
    if steps and "Оптимальний" in steps[-1][2]:
        final_table = steps[-1][1]
        z_val = final_table.loc["Z", "b"]
        st.metric(label="Екстремум функції Z", value=round(z_val, 3))