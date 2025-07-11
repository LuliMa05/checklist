import streamlit as st
import pandas as pd
from datetime import datetime
from fpdf import FPDF

st.title("APT")

st.markdown("## datos del ejecutante de la tarea")
nombre = st.text_input("Nombre y apellido")
area = st.selectbox("area", ["prod", "mant", "mpr", "ing"])
fecha = st.date_input("fecha de ejecucion de la tarea")

st.markdown("## factores de riesgos identificados")
riesgos = {
    "trab altura": st.checkbox("trabj en alt"),
    "izaje": st.checkbox("izaje"),
    "bloqueos": st.checkbox("bloqueo"),
}

comentarios = st.text_area("coment adicionales")

if st.button("enviar checklist"):
    df = pd.DataFrame([{
        "nombre": nombre,
        "area": area,
        "fecha": fecha.strftime("%Y-%m-%d"),
        **riesgos,
        "comentarios": comentarios
        }])

    df.to_csv("respuestas.csv", mode='a', header=False, index=False)

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)
pdf.cell(200, 10, txt="Checklist de Peligros Críticos", ln=True, align='C')
pdf.ln(10)

pdf.cell(200, 10, txt=f"Nombre: {nombre}", ln=True)
pdf.cell(200, 10, txt=f"Área: {area}", ln=True)
pdf.cell(200, 10, txt=f"Fecha: {fecha.strftime('%Y-%m-%d')}", ln=True)
pdf.ln(5)

for clave, valor in riesgos.items():
    pdf.cell(200, 10, txt=f"{clave}: {'Sí' if valor else 'No'}", ln=True)

pdf.ln(5)
pdf.multi_cell(200, 10, txt=f"Comentarios: {comentarios}")
nombre_archivo_pdf = f"checklist_{nombre.replace(' ', '_')}_{fecha.strftime('%Y%m%d')}.pdf"
pdf.output(nombre_archivo_pdf)

import io

# Guardar el PDF en memoria
pdf_buffer = io.BytesIO()
pdf.output(pdf_buffer)
pdf_buffer.seek(0)

# Botón para descargar el PDF
st.download_button(
    label="Descargar PDF",
    data=pdf_buffer,
    file_name=nombre_archivo_pdf,
    mime="application/pdf"
)

st.success("Checklist enviado y PDF generado.")

