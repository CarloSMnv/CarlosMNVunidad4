import flet as ft
from database import Database
import subprocess
import os

def main(page: ft.Page):
    db = Database()

    # Función para agregar un libro
    def agregar_libro(e):
        autor_id = db.insertar_autor(nombre_autor.value, apellido_autor.value)
        db.insertar_libro(titulo_libro.value, autor_id)
        lista_libros.controls.clear()
        cargar_libros()
        page.update()

    # Función para cargar libros
    def cargar_libros():
        libros = db.obtener_libros()
        for libro in libros:
            lista_libros.controls.append(ft.Text(f"{libro[1]} - {libro[2]} {libro[3]}"))
        page.update()

    # Función para exportar BD
    def exportar_bd(e):
        file_picker = ft.FilePicker(on_result=lambda result: on_file_picked_export(result))
        page.overlay.append(file_picker)
        page.update()
        file_picker.save_file(dialog_title="Guardar archivo SQL", file_name="biblioteca.sql")

    def on_file_picked_export(result):
        if result.path:
            try:
                subprocess.run(['mysqldump', '-u', usuario.value, '-p' + password.value, 'biblioteca', '--result-file', result.path], check=True)
                estado_texto.value = f"Base de datos exportada exitosamente a {result.path}"
            except subprocess.CalledProcessError as ex:
                estado_texto.value = f"Error al exportar: {ex}"
            page.update()

    # Función para importar BD
    def importar_bd(e):
        file_picker = ft.FilePicker(on_result=lambda result: on_file_picked_import(result))
        page.overlay.append(file_picker)
        page.update()
        file_picker.pick_files(dialog_title="Seleccionar archivo SQL", allow_multiple=False)

    def on_file_picked_import(result):
        if result.files:
            try:
                with open(result.files[0].path, 'r') as f:
                    subprocess.run(['mysql', '-u', usuario.value, '-p' + password.value, 'biblioteca'], stdin=f, check=True)
                estado_texto.value = f"Base de datos importada exitosamente desde {result.files[0].path}"
            except subprocess.CalledProcessError as ex:
                estado_texto.value = f"Error al importar: {ex}"
            page.update()

    # Campos de entrada para credenciales
    usuario = ft.TextField(label="Usuario MySQL", value="adms2")
    password = ft.TextField(label="Contraseña MySQL", password=True, value="9ss3xa")

    # Campos de entrada para libros
    titulo_libro = ft.TextField(label="Título del Libro")
    nombre_autor = ft.TextField(label="Nombre del Autor")
    apellido_autor = ft.TextField(label="Apellido del Autor")
    boton_agregar = ft.ElevatedButton(text="Agregar Libro", on_click=agregar_libro)
    lista_libros = ft.Column()

    # Botones para exportar e importar
    boton_exportar = ft.ElevatedButton(text="Exportar BD", on_click=exportar_bd)
    boton_importar = ft.ElevatedButton(text="Importar BD", on_click=importar_bd)

    # Texto para mostrar estado
    estado_texto = ft.Text()

    # Cargar libros al inicio
    cargar_libros()

    # Agregar controles a la página
    page.add(
        usuario, password,
        titulo_libro, nombre_autor, apellido_autor, boton_agregar,
        lista_libros,
        boton_exportar, boton_importar, estado_texto
    )

ft.app(target=main)