from flask import Flask, jsonify, request, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)

# Konfigurasi MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'universitas'
mysql = MySQL(app)

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/person')
def person():
    return jsonify({'name': 'Yunika', 'address': 'Indralaya'})

@app.route('/mahasiswa', methods=['GET', 'POST'])
def mahasiswa():
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM MAHASISWA")
        column_names = [i[0] for i in cursor.description]
        data = [dict(zip(column_names, row)) for row in cursor.fetchall()]
        cursor.close()
        return jsonify(data)

    elif request.method == 'POST':
        data = request.get_json()
        if not all(k in data for k in ('nama', 'univ', 'jurusan')):
            return jsonify({'message': 'Invalid data'}), 400
        
        cursor = mysql.connection.cursor()
        sql = "INSERT INTO MAHASISWA (nama, univ, jurusan) VALUES (%s, %s, %s)"
        val = (data['nama'], data['univ'], data['jurusan'])
        cursor.execute(sql, val)
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Data added successfully!'})

@app.route('/mahasiswa/<int:id>', methods=['GET'])
def get_mahasiswa_by_id(id):
    cursor = mysql.connection.cursor()
    sql = "SELECT * FROM MAHASISWA WHERE mahasiswa_id = %s"
    cursor.execute(sql, (id,))
    column_names = [i[0] for i in cursor.description]
    data = cursor.fetchone()
    cursor.close()

    if data:
        return jsonify(dict(zip(column_names, data)))
    else:
        return jsonify({'message': 'Mahasiswa not found'}), 404

@app.route('/deletemahasiswa', methods=['DELETE'])
def deletemahasiswa():
    if 'id' in request.args:
        cursor = mysql.connection.cursor()
        sql = "DELETE FROM MAHASISWA WHERE mahasiswa_id = %s"
        val = (request.args['id'],)
        cursor.execute(sql, val)
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Data deleted successfully!'})
    else:
        return jsonify({'message': 'ID is required'}), 400

@app.route('/editmahasiswa', methods=['PUT'])
def editmahasiswa():
    if 'id' in request.args:
        data = request.get_json()
        if not all(k in data for k in ('nama', 'univ', 'jurusan')):
            return jsonify({'message': 'Invalid data'}), 400

        cursor = mysql.connection.cursor()
        sql = "UPDATE MAHASISWA SET nama=%s, univ=%s, jurusan=%s WHERE mahasiswa_id = %s"
        val = (data['nama'], data['univ'], data['jurusan'], request.args['id'])
        cursor.execute(sql, val)
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Data updated successfully!'})
    else:
        return jsonify({'message': 'ID is required'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=50, debug=True)