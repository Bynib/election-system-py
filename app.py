from flask import Flask, request, render_template, flash, redirect, url_for
import db

app = Flask(__name__)
app.secret_key = 'secret_key'

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    
@app.route('/position-management', methods=['GET','POST'])
def position_management():
    if request.method == 'GET':
        positions = db.get_all_positions()
        return render_template('position.html', positions=positions)
    
@app.route('/voter-management', methods=['GET','POST'])
def voter_management():
    if request.method=='GET':
        voters = db.get_all_voters()
        return render_template('voter.html', voters=voters)

@app.route('/add-position', methods=['GET','POST'])
def add_position():
    if request.method == 'POST':
        posName = request.form['posName']
        numOfPositions = request.form['numOfPositions']
        
        if db.add_position(posName, numOfPositions):
            flash("Position Added!")
            return redirect(url_for('position_management'))
    return redirect(url_for('position_management'))

@app.route('/update-position', methods=['GET','POST'])
def update_position():
    if request.method == 'GET':
        posID = request.args.get('posID')
        posName = request.args.get('posName')
        numOfPositions = request.args.get('numOfPositions')
        posStat = request.args.get('posStat')
        
        position = {"posID":posID,"posName":posName,"numOfPositions":numOfPositions,"posStat":posStat}

        return render_template('update-position.html', position=position)
    
    posID = request.form['posID']
    posName = request.form['posName']
    numOfPositions = request.form['numOfPositions']
    posStat = request.form['posStat']

    if db.update_position(posName, numOfPositions, posStat, posID):
        flash('Position Updated!')
        return redirect(url_for('position_management'))    
    
    return redirect(url_for('position_management'))

@app.route('/deactivate-position', methods=['GET','POST'])
def deactivate_vote():
    posID = request.form['posID']

    if db.deactivate_position(posID):
        flash('Position Deactivated!')
        return redirect(url_for('position_management'))
    return redirect(url_for('position_management'))

@app.route('/search-position', methods=['GET','POST'])
def search_position():
    query = request.form['query']

    positions = db.search_position(query)
    return render_template('position.html', positions=positions, query=query)

@app.route('/add-voter', methods=['GET','POST'])
def add_voter():
    voterFName = request.form['voterFName']
    voterMName = request.form['voterMName']
    voterLName = request.form['voterLName']
    voterPass = request.form['voterPass']

    if db.add_voter(voterFName, voterMName, voterLName, voterPass):
        flash("Voter Added!")
        return redirect(url_for('voter_management'))
    
    return redirect(url_for('voter_management'))
    
@app.route('/update-voter', methods=['GET','POST'])
def update_voter():
    if request.method == 'GET':
        voterID = request.args.get('voterID')
        voterFName = request.args.get('voterFName')
        voterMName = request.args.get('voterMName')
        voterLName = request.args.get('voterLName')
        voterPass = request.args.get('voterPass')
        voterStat = request.args.get('voterStat')

        voter = {"voterID":voterID,"voterFName":voterFName,"voterMName":voterMName,"voterLName":voterLName,"voterPass":voterPass,"voterStat":voterStat}
        print("voter: ", voter)
        return render_template('update-voter.html', voter=voter)
    
    
    voterID = request.form['voterID']
    voterFName = request.form['voterFName']
    voterMName = request.form['voterMName']
    voterLName = request.form['voterLName']
    
    voterPass = request.form['voterPass']

    if db.update_voter(voterFName, voterMName, voterLName, voterPass, voterID):
        flash("Voter Updated!")
        return redirect(url_for('voter_management'))
    return redirect(url_for('voter_management'))

@app.route('/deactivate-voter', methods=['GET','POST'])
def deactivate_voter():
    voterID = request.form['voterID']

    if db.deactivate_voter(voterID):
        flash("Voter Deactivated!")
        return redirect(url_for('voter_management'))
    return redirect(url_for('voter_management'))

@app.route('/search-voter', methods=['GET','POST'])
def search_voter():
    query = request.form['query']

    voters = db.search_voter(query)
    return render_template('voter.html', voters=voters, query=query)

@app.route('/candidate-management', methods=['GET','POST'])
def candidate_management():
    if request.method == "GET":
        positions = db.get_all_positions()
        candidates = db.get_all_candidates()
        return render_template('candidate.html', positions=positions, candidates=candidates)

@app.route('/add-candidate', methods=['GET','POST'])
def add_candidate():
    candFName = request.form['candFName']
    candMName = request.form['candMName']
    candLName = request.form['candLName']
    posID = request.form['posID']


    if db.add_candidate(candFName, candMName, candLName, posID):
        flash("Candidate Added!")
        return redirect(url_for('candidate_management'))
    return redirect(url_for('candidate_management'))
    
@app.route('/update-candidate', methods=['GET','POST'])
def update_candidate():
    if request.method=="GET":
        candID = request.args.get('candID')
        candFName = request.args.get('candFName')
        candMName = request.args.get('candMName')
        candLName = request.args.get('candLName')
        posName = request.args.get('posName')
        candStat = request.args.get('candStat')

        positions = db.get_all_positions()

        candidate = {
            "candID": candID,
            "candFName": candFName,
            "candMName": candMName,
            "candLName": candLName,
            "posName": posName,
            "candStat": candStat
        }
        return render_template('update-candidate.html', candidate=candidate,positions=positions)
    
    candID = request.form['candID']
    candFName = request.form['candFName']
    candMName = request.form['candMName']
    candLName = request.form['candLName']
    posID = request.form['posID']
    candStat = request.form['candStat']

    if db.update_candidate(candFName, candMName, candLName, posID, candStat, candID):
        flash("Candidate Updated!")
        return redirect(url_for('candidate_management'))
    return redirect(url_for('candidate_management'))

@app.route('/deactivate-candidate', methods=['GET','POST'])
def deactivate_candidate():
    candID = request.form['candID']

    if db.deactivate_candidate(candID):
        flash("Candidate Deactivated!")
        return redirect(url_for('candidate_management'))
    return redirect(url_for('candidate_management'))

if __name__ == "__main__":
    app.run(debug=True)