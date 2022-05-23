import psycopg2
from flask import Flask, request
import pandas as pd
from sqlalchemy import create_engine
from werkzeug.utils import secure_filename
import os

def connect_to_server ():
    user = "postgres"
    password = "example"
    host = "localhost"
    database = "postgres"

    engine = create_engine("postgresql+psycopg2://"+user+":"+password+"@"+host+"/"+database)

    return engine


def get_table (engine, file):

    pd_data = pd.read_sql_query('Select * from '+file,engine)
    print("Consulta tabla " + file)
    return pd_data



def insert_data(engine,df,file):

    df.to_sql(file, engine, if_exists='replace', index= False)
    print("insertar datos")

    return "insertar datos"


app = Flask(__name__)

@app.route('/get_data', methods=['GET','POST'])

def get_data():

    if request.method == 'POST':

        engine = connect_to_server()

        uploaded_file = request.files['file']
        filename = secure_filename(uploaded_file.filename)

        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            file = os.path.splitext(filename)[0]
            os.makedirs(os.path.join(app.root_path, 'Files_to_Process'), exist_ok=True)
            uploaded_file.save(os.path.join(app.root_path, 'Files_to_Process', filename))

            df_data2 = pd.read_csv('Files_to_Process/'+filename)
            insert_data( engine,df_data2, file)
            df_table = get_table(engine,file)

        return df_table.to_html(header="true", table_id="data")

    return '''
           <form method="POST" action="" enctype="multipart/form-data">
               <h1 style ="font-size:26px;position:absolute;top:30px;left:100px">Seleccionar el archivo:</h1>
                <input type="file" name="file" multiple style="float:left;position:absolute;left:400px;top:52px">
               <input type="submit" value="Cargar Datos" style="float:left;position:absolute;left:400px;top:102px">
           </form>'''



@app.route('/')
def default():
    return "Inicio"


if __name__ =='__main__':
    app.run(debug= True, port= 4040)
