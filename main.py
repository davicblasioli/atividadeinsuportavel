from flask import Flask, render_template, request, redirect, flash, url_for
import fdb

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'

host = 'localhost'
database = r'C:\Users\Aluno\Downloads\coisafinanca\FINANCA.FDB'
user = 'sysdba'
password = 'sysdba'


con = fdb.connect(host=host, database=database, user=user, password=password)


class Receitas:
    def __init__(self, id_receita, valor, datadia, fonte, id_usuario):
        self.id_receita = id_receita
        self.valor = valor
        self.datadia = datadia
        self.fonte = fonte
        self.id_usuario = id_usuario


@app.route('/tabela_receitas')
def tabela_receitas():
    cursor = con.cursor()
    cursor.execute('SELECT id_receita, valor, datadia, fonte FROM receitas')
    receita = cursor.fetchall()
    cursor.close()
    return render_template('tabela_receitas.html', receita=receita)


@app.route('/receitas')
def receitas():
    return render_template('receitas.html', titulo='Nova Receita')


@app.route('/criar_receitas', methods=['POST'])
def criar_receitas():
    valor = request.form['valor']
    datadia = request.form['datadia']
    fonte = request.form['fonte']

    # Criando o cursor
    cursor = con.cursor()

    try:
        # Verificar se a receita já existe com a combinação de fonte e data
        cursor.execute("SELECT 1 FROM receitas WHERE FONTE = ? AND DATADIA = ?", (fonte, datadia))
        if cursor.fetchone():  # Se existir algum registro
            flash("Erro: Receita já cadastrada.", "error")
            return redirect(url_for('receitas'))

        # Inserir o novo registro
        cursor.execute("INSERT INTO receitas (VALOR, DATADIA, FONTE) VALUES (?, ?, ?)",
                       (valor, datadia, fonte))
        con.commit()
        flash("Receita cadastrada com sucesso!", "success")
    except Exception as e:
        # Se ocorrer um erro, exibe uma mensagem de erro
        flash(f"Erro ao cadastrar receita: {str(e)}", "error")
        con.rollback()  # Faz rollback caso ocorra erro
    finally:
        cursor.close()

    return redirect(url_for('tabela_receitas'))



@app.route('/editar_receita')
def editar_receita():
    return render_template('editar_receita.html', titulo='Editar Receita')


@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    cursor = con.cursor()  # Abre o cursor

    # Buscar o  específico para edição
    cursor.execute("SELECT ID_RECEITA, VALOR, FONTE, DATADIA FROM receitas WHERE ID_RECEITA = ?", (id,))
    receita = cursor.fetchone()

    if not receita:
        cursor.close()  # Fecha o cursor se o  não for encontrado
        flash("Receita não encontrado!", "error")
        return redirect(url_for('tabela_receitas'))  # Redireciona para a página principal se o  não for encontrado


    if request.method == 'POST':
        # Coleta os dados do formulário
        valor = request.form['valor']
        fonte = request.form['fonte']
        datadia = request.form['datadia']

        # Atualiza o  no banco de dados
        cursor.execute("UPDATE receitas SET VALOR = ?, FONTE = ?, DATADIA = ? WHERE ID_RECEITA = ?",
                       (valor, fonte, datadia, id))
        con.commit()  # Salva as mudanças no banco de dados
        cursor.close()  # Fecha o cursor
        flash("Receita atualizada com sucesso!", "success")
        return redirect(url_for('tabela_receitas'))  # Redireciona para a página principal após a atualização

    cursor.close()  # Fecha o cursor ao final da função, se não for uma requisição POST
    return render_template('editar.html', receita=receita, titulo='Editar Receita')  # Renderiza a página de edição


@app.route('/deletar/<int:id>', methods=('POST',))
def deletar(id):
    cursor = con.cursor()  # Abre o cursor

    try:
        cursor.execute('DELETE FROM receitas WHERE id_receita = ?', (id,))
        con.commit()  # Salva as alterações no banco de dados
        flash('Receita excluída com sucesso!', 'success')  # Mensagem de sucesso
    except Exception as e:
        con.rollback()  # Reverte as alterações em caso de erro
        flash('Erro ao excluir a receita.', 'error')  # Mensagem de erro
    finally:
        cursor.close()  # Fecha o cursor independentemente do resultado

    return redirect(url_for('tabela_receitas'))  # Redireciona para a página principal


class Despesas:
    def __init__(self, id_despesa, valor, datadia, fonte, id_usuario):
        self.id_despesa = id_despesa
        self.valor = valor
        self.datadia = datadia
        self.fonte = fonte
        self.id_usuario = id_usuario


@app.route('/tabela_despesas')
def tabela_despesas():
    cursor = con.cursor()
    cursor.execute('SELECT id_despesa, valor, datadia, fonte FROM despesas')
    despesa = cursor.fetchall()
    cursor.close()
    return render_template('tabela_despesas.html', despesa=despesa)


@app.route('/despesas')
def despesas():
    return render_template('despesas.html', titulo='Nova Despesa')


@app.route('/criar_despesas', methods=['POST'])
def criar_despesas():
    valor = request.form['valor']
    datadia = request.form['datadia']
    fonte = request.form['fonte']

    # Criando o cursor
    cursor = con.cursor()

    try:
        # Verificar se a despesa já existe com a combinação de fonte e data
        cursor.execute("SELECT 1 FROM despesas WHERE FONTE = ? AND DATADIA = ?", (fonte, datadia))
        if cursor.fetchone():  # Se existir algum registro
            flash("Erro: Despesa já cadastrada.", "error")
            return redirect(url_for('despesas'))

        # Inserir o novo registro
        cursor.execute("INSERT INTO despesas (VALOR, DATADIA, FONTE) VALUES (?, ?, ?)",
                       (valor, datadia, fonte))
        con.commit()
        flash("Despesa cadastrada com sucesso!", "success")
    except Exception as e:
        # Se ocorrer um erro, exibe uma mensagem de erro
        flash(f"Erro ao cadastrar despesa: {str(e)}", "error")
        con.rollback()  # Faz rollback caso ocorra erro
    finally:
        cursor.close()

    return redirect(url_for('tabela_despesas'))



@app.route('/editar_despesa')
def editar_despesa():
    return render_template('editar_despesa.html', titulo='Editar Despesa')


@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    cursor = con.cursor()  # Abre o cursor

    # Buscar o  específico para edição
    cursor.execute("SELECT ID_DESPESA, VALOR, FONTE, DATADIA FROM despesas WHERE ID_DESPESA = ?", (id,))
    despesa = cursor.fetchone()

    if not despesa:
        cursor.close()  # Fecha o cursor se o  não for encontrado
        flash("Despesa não encontrado!", "error")
        return redirect(url_for('tabela_despesas'))  # Redireciona para a página principal se o  não for encontrado


    if request.method == 'POST':
        # Coleta os dados do formulário
        valor = request.form['valor']
        fonte = request.form['fonte']
        datadia = request.form['datadia']

        # Atualiza o  no banco de dados
        cursor.execute("UPDATE despesas SET VALOR = ?, FONTE = ?, DATADIA = ? WHERE ID_DESPESA = ?",
                       (valor, fonte, datadia, id))
        con.commit()  # Salva as mudanças no banco de dados
        cursor.close()  # Fecha o cursor
        flash("Despesa atualizada com sucesso!", "success")
        return redirect(url_for('tabela_despesas'))  # Redireciona para a página principal após a atualização

    cursor.close()  # Fecha o cursor ao final da função, se não for uma requisição POST
    return render_template('editar.html', despesa=despesa, titulo='Editar Despesa')  # Renderiza a página de edição


@app.route('/deletar/<int:id>', methods=('POST',))
def deletar(id):
    cursor = con.cursor()  # Abre o cursor

    try:
        cursor.execute('DELETE FROM despesas WHERE id_despesa = ?', (id,))
        con.commit()  # Salva as alterações no banco de dados
        flash('Despesa excluída com sucesso!', 'success')  # Mensagem de sucesso
    except Exception as e:
        con.rollback()  # Reverte as alterações em caso de erro
        flash('Erro ao excluir a despesa.', 'error')  # Mensagem de erro
    finally:
        cursor.close()  # Fecha o cursor independentemente do resultado

    return redirect(url_for('tabela_despesas'))  # Redireciona para a página principal


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/controle')
def controle():
    return render_template('controle.html')


@app.route('/criar_conta')
def criar_conta():
    return render_template('criar_conta.html')


@app.route('/login')
def login():
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)
