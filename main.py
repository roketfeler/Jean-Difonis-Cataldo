from flask import Flask, render_template, request

app = Flask(__name__)

historial_evaluaciones = []
historial_nombres = []


def calcular_estado_academico(n1: float, n2: float, n3: float, asistencia: float) -> tuple[float, str]:
    promedio = round((n1 + n2 + n3) / 3, 2)
    if promedio >= 40 and asistencia >= 75:
        estado = "APROBADO"
    else:
        estado = "REPROBADO"
    return promedio, estado


def obtener_nombre_mas_largo(nombres: list[str]) -> tuple[str, int]:
    nombre_mayor = max(nombres, key=len)
    return nombre_mayor, len(nombre_mayor)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/ejercicio1", methods=["GET", "POST"])
def ejercicio1():
    promedio = None
    estado = None
    error = None
    nota1 = nota2 = nota3 = asistencia = None

    if request.method == "POST":
        nota1 = request.form.get("nota1", "").strip()
        nota2 = request.form.get("nota2", "").strip()
        nota3 = request.form.get("nota3", "").strip()
        asistencia = request.form.get("asistencia", "").strip()

        try:
            n1 = float(nota1)
            n2 = float(nota2)
            n3 = float(nota3)
            asist = float(asistencia)

            if not (10 <= n1 <= 70 and 10 <= n2 <= 70 and 10 <= n3 <= 70):
                error = "Las notas deben estar entre 10 y 70."
            elif not (0 <= asist <= 100):
                error = "La asistencia debe estar entre 0 y 100."
            else:
                promedio, estado = calcular_estado_academico(n1, n2, n3, asist)
                historial_evaluaciones.append({
                    "notas": [n1, n2, n3],
                    "asistencia": asist,
                    "promedio": promedio,
                    "estado": estado,
                })
        except ValueError:
            error = "Por favor ingresa valores numéricos válidos."

    return render_template(
        "ejercicio1.html",
        promedio=promedio,
        estado=estado,
        error=error,
        nota1=nota1,
        nota2=nota2,
        nota3=nota3,
        asistencia=asistencia,
    )


@app.route("/ejercicio2", methods=["GET", "POST"])
def ejercicio2():
    nombre_mayor = None
    cantidad_caracteres = None
    error = None
    nombre1 = nombre2 = nombre3 = None

    if request.method == "POST":
        nombre1 = request.form.get("nombre1", "").strip()
        nombre2 = request.form.get("nombre2", "").strip()
        nombre3 = request.form.get("nombre3", "").strip()

        if not nombre1 or not nombre2 or not nombre3:
            error = "Debes completar los tres nombres."
        else:
            nombres = [nombre1, nombre2, nombre3]
            nombre_mayor, cantidad_caracteres = obtener_nombre_mas_largo(nombres)
            historial_nombres.append({
                "nombres": nombres,
                "mayor": nombre_mayor,
                "caracteres": cantidad_caracteres,
            })

    return render_template(
        "ejercicio2.html",
        nombre_mayor=nombre_mayor,
        cantidad_caracteres=cantidad_caracteres,
        error=error,
        nombre1=nombre1,
        nombre2=nombre2,
        nombre3=nombre3,
    )


if __name__ == "__main__":
    app.run(debug=True)