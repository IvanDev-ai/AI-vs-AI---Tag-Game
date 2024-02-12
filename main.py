import streamlit as st
from agent import train

def main():
    st.title("Escape Game")

    st.write("¡Bienvenido al Escape Game! Haz clic en el botón para comenzar a jugar.")

    # Botón para iniciar el juego
    if st.button("Comenzar juego"):
        st.write("El juego ha comenzado.")
        train()  # Llama a la función train() desde tu archivo agent.py para iniciar el juego

if __name__ == "__main__":
    main()