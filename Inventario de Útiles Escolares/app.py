from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

productos = []
contador_id = 1

# LISTAR + CREAR
@app.route("/", methods=["GET", "POST"])
def index():
    global contador_id

    if request.method == "POST":
        nombre = request.form["nombre"]
        cantidad = int(request.form["cantidad"])
        precio = float(request.form["precio"])

        productos.append({
            "id": contador_id,
            "nombre": nombre,
            "cantidad": cantidad,
            "precio": precio
        })

        contador_id += 1
        return redirect(url_for("index"))

    # 🔥 cálculo del total (BIEN UBICADO)
    total = sum(p["cantidad"] * p["precio"] for p in productos)

    return render_template("index.html", productos=productos, total=total)


# ELIMINAR
@app.route("/eliminar/<int:id>")
def eliminar(id):
    global productos
    productos = [p for p in productos if p["id"] != id]
    return redirect(url_for("index"))


# EDITAR
@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    producto = next((p for p in productos if p["id"] == id), None)

    if request.method == "POST":
        producto["nombre"] = request.form["nombre"]
        producto["cantidad"] = int(request.form["cantidad"])
        producto["precio"] = float(request.form["precio"])
        return redirect(url_for("index"))

    return render_template("editar.html", producto=producto)


if __name__ == "__main__":
    app.run(debug=True)