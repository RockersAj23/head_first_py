from flask import Flask,render_template,request,escape
from vsearch import search4letters
import mysql.connector
app=Flask(__name__)

def log_request(req , res:str) -> None :
    dbconfig={'host':'127.0.0.1',
              'user':'vsearch',
              'password':'vsearchpasswd',
              'database':'vsearchlogdb',}
    
    conn = mysql.connector.connect(**dbconfig)
    cursor=conn.cursor()
    _SQL = """insert into log
               (phrase,letters,ip,browser_string,results)
               values
               (%s, %s, %s, %s, %s)"""
    cursor.execute(_SQL,(req.form['phrase'],
                         req.form['letters'],
                         req.remote_addr,
                         req.user_agent.browser,
                         res,))
    conn.commit()
    cursor.close()
    conn.close()

@app.route('/viewlog')
def view_the_log() :
    contents=[]
    with open('vsearch.log') as log:
        for line in log:
            contents.append([])
            for item in line.split('|'):
                contents[-1].append(escape(item))
    titles=('From Data','Remote_addr','User_agent','results')
    return render_template('viewlog.html',
                           the_title='View Log',
                           the_row_titles=titles,
                           the_data=contents,)
    

@app.route('/search4' ,methods=['POST'])
def do_search()  :
    phrase=request.form['phrase']
    letters=request.form['letters']
    results = str(search4letters(phrase,letters))
    title = 'Here are your results:'
    log_request(request,results)
    return render_template('results.html',
                           the_phrase=phrase,
                           the_letters=letters,
                           the_title = title,
                           the_results = results,)


@app.route('/')
@app.route('/entry')
def entry_page():
    return render_template('entry.html',the_title='Welcom to search4letters on the web')


if __name__ == '__main__':
    app.run(debug=True)
