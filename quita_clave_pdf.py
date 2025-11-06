import PyPDF2
import os


def quitar_clave_pdf(archivo_entrada, archivo_salida, clave):
    """
    Intenta desencriptar un PDF y guarda una copia sin contraseña.
    """
    try:
        # Abre el archivo PDF en modo binario
        with open(archivo_entrada, "rb") as archivo:
            lector = PyPDF2.PdfReader(archivo)

            # Verifica si el archivo está encriptado
            if lector.is_encrypted:
                # Intenta desencriptar con la clave proporcionada
                if lector.decrypt(clave):
                    # Crea un escritor para guardar el nuevo PDF
                    escritor = PyPDF2.PdfWriter()

                    # Copia todas las páginas al nuevo escritor
                    for pagina in lector.pages:
                        escritor.add_page(pagina)

                    # Guarda el nuevo PDF sin contraseña
                    with open(archivo_salida, "wb") as salida:
                        escritor.write(salida)

                    print(
                        f"✅ Éxito: Se ha guardado una copia sin clave en **{archivo_salida}**"
                    )
                    return True
                else:
                    print(
                        f"❌ Error: La clave proporcionada NO es correcta para **{archivo_entrada}**"
                    )
                    return False
            else:
                print(
                    f"⚠️ Aviso: El archivo **{archivo_entrada}** NO estaba encriptado."
                )
                return True

    except FileNotFoundError:
        print(f"❌ Error: Archivo no encontrado en **{archivo_entrada}**")
    except Exception as e:
        print(f"❌ Ocurrió un error inesperado al procesar el archivo: {e}")
    return False


# --- Configuración de Uso ---

# 1. Define el archivo a procesar (ejemplo)
pdf_a_procesar = "Estado_de_Cuenta_CMR_102025_0232119.pdf"

# 2. Define el nombre para el nuevo archivo sin clave
pdf_sin_clave = "Estado_de_Cuenta_CMR_102025_0232119.desprotegida.pdf"

# 3. Define la clave (debes saberla, por ejemplo, tu RUT con/sin dígito verificador)
# Asegúrate de que la clave sea de tipo string
clave_del_pdf = "12487175"  # Reemplaza con la clave correcta

# Ejecuta la función
quitar_clave_pdf(pdf_a_procesar, pdf_sin_clave, clave_del_pdf)
