from flask import Flask, render_template, request, redirect,url_for # type: ignore
import os
import database as db

#para acceder al archivo html
template_dir=os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
#unir template a nuestra carpeta principal
template_dir = os.path.join(template_dir,'src','templates')

#Inicialización de flask para que busque el index html y pueda renderizar en pantalla
app = Flask(__name__, template_folder= template_dir)

#Rutas de la aplicacion
@app.route('/')
def home():
    cursor =db.database.cursor()
    cursor.execute("SELECT * FROM users")
    #obtenemos los datos en una estructura de datos
    myresult =cursor.fetchall()
    #convertimos los datos a diccionario
    insertObject=[]
    columnNames=[column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursor.close()
    return render_template('index.html',data=insertObject)

@app.route('/about')
def about():
    #return "about page"
    return render_template('about.html')


#Ruta para guardar usuarios en la base de datos
@app.route('/user', methods=['Post'])
def addUser():
    correo= request.form['correo']
    nombre= request.form['nombre']
    password= request.form['password']

    if correo and nombre and password:
        cursor=db.database.cursor()
        sql="insert into users (correo, nombre, password) values (%s,%s,%s)"
        data= (correo, nombre, password)
        cursor.execute(sql,data)
        db.database.commit()
    return redirect(url_for('home'))

@app.route("/delete/<string:id>")
def delete(id):
    cursor=db.database.cursor()
    sql="delete from users where id=%s"
    data= (id,)
    cursor.execute(sql,data)
    db.database.commit()
    return redirect(url_for('home'))

@app.route('/edit/<string:id>', methods=['POST'])
def edit(id):
    correo= request.form['correo']
    nombre=request.form['nombre']
    password= request.form['password']

    if correo and nombre and password:
        cursor=db.database.cursor()
        sql="update users set correo=%s, nombre=%s, password=%s where id=%s"
        data=(correo, nombre, password, id)
        cursor.execute(sql,data)
        db.database.commit()
    return redirect(url_for('home'))




if __name__ == '__main__':
    app.run(debug=True,port=4000)


