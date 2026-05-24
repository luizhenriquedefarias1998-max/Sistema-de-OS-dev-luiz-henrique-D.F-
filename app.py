from flask import Flask, render_template, request, jsonify, Response
import mysql.connector
from io import StringIO, BytesIO
import csv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

app = Flask(__name__)

# Configuração do MySQL
db_config = {
    'host': 'localhost',
    'user': 'root',       # Substitua pelo seu usuário do MySQL
    'password': '',       # Substitua pela sua senha do MySQL
    'database': 'sistema_os'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

# Rota principal - Renderiza a página
@app.route('/')
def index():
    return render_template('index.html')

# 1. Criar ordem de serviço
@app.route('/api/ordens', methods=['POST'])
def criar_ordem():
    dados = request.json
    titulo = dados.get('titulo')
    descricao = dados.get('descricao')
    prioridade = dados.get('prioridade')

    if not titulo or not prioridade:
        return jsonify({'error': 'Título e prioridade são obrigatórios.'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO ordens (titulo, descricao, prioridade) VALUES (%s, %s, %s)',
        (titulo, descricao, prioridade)
    )
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'message': 'Ordem de serviço criada com sucesso!'}), 201

# 2. Alterar status
@app.route('/api/ordens/<int:id_os>/status', methods=['PATCH'])
def alterar_status(id_os):
    dados = request.json
    novo_status = dados.get('status')

    if novo_status not in ['Aberta', 'Em andamento', 'Concluída']:
        return jsonify({'error': 'Status inválido.'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE ordens SET status = %s WHERE id = %s', (novo_status, id_os))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'message': 'Status atualizado com sucesso!'})

# 3. Listar todas as ordens
@app.route('/api/ordens', methods=['GET'])
def listar_ordens():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM ordens ORDER BY id DESC')
    ordens = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(ordens)

# 4. Baixar CSV com as ordens
@app.route('/api/exportar/csv', methods=['GET'])
def exportar_csv():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM ordens')
    ordens = cursor.fetchall()
    cursor.close()
    conn.close()

    si = StringIO()
    cw = csv.writer(si, delimiter=';')
    cw.writerow(['ID', 'Titulo', 'Descricao', 'Prioridade', 'Status'])

    for o in ordens:
        cw.writerow([o['id'], o['titulo'], o['descricao'] or '', o['prioridade'], o['status']])

    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=ordens_de_servico.csv"
    output.headers["Content-type"] = "text/csv; charset=utf-8"
    return output

# 5. Baixar PDF com o relatório
@app.route('/api/exportar/pdf', methods=['GET'])
def exportar_pdf():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM ordens')
    ordens = cursor.fetchall()
    cursor.close()
    conn.close()

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Cabeçalho do PDF
    p.setFont("Helvetica-Bold", 20)
    p.drawCentredString(width / 2.0, height - 50, "Relatório de Ordens de Serviço")
    
    y = height - 100
    p.setFont("Helvetica", 10)

    for o in ordens:
        if y < 80:  # Cria uma nova página se o espaço acabar
            p.showPage()
            y = height - 50
            p.setFont("Helvetica", 10)

        p.setFont("Helvetica-Bold", 12)
        p.drawString(50, y, f"OS #{o['id']} - {o['titulo']}")
        y -= 15
        
        p.setFont("Helvetica", 10)
        p.drawString(50, y, f"Prioridade: {o['prioridade']} | Status: {o['status']}")
        y -= 15
        p.drawString(50, y, f"Descrição: {o['descricao'] or 'Sem descrição.'}")
        y -= 20
        
        # Linha divisória
        p.setStrokeColorRGB(0.8, 0.8, 0.8)
        p.line(50, y, width - 50, y)
        y -= 20

    p.showPage()
    p.save()

    buffer.seek(0)
    return Response(buffer, mimetype='application/pdf', headers={"Content-Disposition": "attachment; filename=relatorio_ordens.pdf"})

# Helper para corrigir encode do CSV no Flask
from flask import make_response

if __name__ == '__main__':
    app.run(debug=True, port=5000)