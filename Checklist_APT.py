import streamlit as st
import pandas as pd
from datetime import datetime
from fpdf import FPDF

st.title("APT")

st.markdown("## Datos del ejecutante de la tarea")
Nombre = st.text_input("Nombre y apellido")
Área = st.selectbox("area", ["Producción", "MME", "MEE", "MPR", "Almacenes", "Playa de Materia Prima"])
Fecha = st.date_input("Fecha de ejecucion de la tarea")
Fecha_fin = st.date_input("Fecha de finalización de la tarea")

st.markdown("## Factores de riesgos identificados")
riesgos = {
    "Trabajo en altura": st.checkbox("Trabajo en altura"),
    "Izaje de cargas": st.checkbox("Izaje de cargas"),
    "Intervención de máquinas con energías acumuladas": st.checkbox("Intervención de máquinas con energías acumuladas"),
}

comentarios = st.text_area("Comentarios adicionales de la tarea")

if st.button("Enviar checklist"):
    df = pd.DataFrame([{
        "Nombre": Nombre,
        "Área": Área,
        "Fecha de ejecución": Fecha.strftime("%Y-%m-%d"),
        "Riesgos involucrados": riesgos,
        "Comentarios adicionales": comentarios
        }])

    df.to_csv("respuestas.csv", mode='a', header=False, index=False)

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=15, italic=TRUE)
pdf.cell(200, 10, txt="Checklist de Peligros Críticos", ln=True, align='C')
pdf.ln(10)

pdf.cell(200, 10, txt=f"Nombre: {Nombre}", ln=True)
pdf.cell(200, 10, txt=f"Área: {Área}", ln=True)
pdf.cell(200, 10, txt=f"Fecha: {Fecha.strftime('%Y-%m-%d')}", ln=True)
pdf.ln(5)

for clave, valor in riesgos.items():
    pdf.cell(200, 10, txt=f"{clave}: {'Sí' if valor else 'No'}", ln=True)

pdf.ln(5)
pdf.multi_cell(200, 10, txt=f"Comentarios: {comentarios}")
nombre_archivo_pdf = f"checklist_{Nombre.replace(' ', '_')}_{Fecha.strftime('%Y%m%d')}.pdf"
pdf.output(nombre_archivo_pdf)

# Guardar el PDF en memoria
import io

# Crear buffer de memoria
pdf_buffer = io.BytesIO()

# Guardar el PDF en el buffer usando dest='S' para obtener el contenido
pdf_bytes = pdf.output(dest='S').encode('latin1')
pdf_buffer.write(pdf_bytes)
pdf_buffer.seek(0)

# Botón de descarga en Streamlit
st.download_button(
    label="Descargar PDF",
    data=pdf_buffer,
    file_name=nombre_archivo_pdf,
    mime="application/pdf"
)



