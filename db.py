import sqlite3

db = "election.db"

def connect():
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    return conn

def run(sql):
    with connect() as conn:
        records = conn.execute(sql).fetchall()
        records = [dict(record) for record in records]
        return records

def create_tables():
    sql = {'''
                create table if not exists positions (
                    posID integer primary key autoincrement,
                    posName text,
                    numOfPositions integer,
                    posStat text default 'open'
                )
            ''',
            '''
                create table if not exists voters (
                    voterID integer primary key autoincrement,
                    voterPass text,
                    voterFName text,
                    voterMName text,
                    voterLName text,
                    voterStat text default 'active',
                    voted integer default 0
                )
            ''','''
                create table if not exists candidates (
                    candID integer primary key autoincrement,
                    candFName text,
                    candMName text,
                    candLName text,
                    posID integer references position(posID),
                    candStat text default 'active'
                )
            ''','''
                create table if not exists vote (
                    posID integer references position(posID),
                    voterID integer references voter(voterID),
                    candID integer references candidate(candID),
                    primary key (posID, voterID, candID)
                )
            ''',}
    with connect() as conn:
        for query in sql:
            conn.execute(query)
            conn.commit()

def get_all_positions():
    sql = 'select * from positions'
    with connect() as conn:
        positions = conn.execute(sql).fetchall()
        return [dict(position) for position in positions]

def add_position(posName, numOfPositions):
    sql = 'insert into positions (posName, numOfPositions) values (?,?)'
    with connect() as conn:
        conn.execute(sql,(posName, numOfPositions))
        conn.commit()
        return True

def update_position(posName, numOfPositions, posStat, posID):
    sql = 'update positions set posName = ?, numOfPositions = ?, posStat = ? where posID = ?'
    with connect() as conn:
        conn.execute(sql,(posName, numOfPositions, posStat, posID))
        conn.commit()
        return True
    
def deactivate_position(posID):
    sql = 'update positions set posStat = "closed" where posID = ?'
    with connect() as conn:
        conn.execute(sql,(posID))
        conn.commit()
        return True

def search_position(query):
    sql = "select * from positions where posName like ? or posStat like ?"
    query = f"%{query}%"
    with connect() as conn:
        results = conn.execute(sql,(query, query)).fetchall()
        return [dict(result) for result in results]

def add_voter(voterFName, voterMName, voterLName, voterPass):
    sql = 'insert into voters (voterFName, voterMName, voterLName, voterPass) values (?,?,?,?)'
    with connect() as conn:
        conn.execute(sql,(voterFName, voterMName, voterLName, voterPass))
        conn.commit()
        return True
    
def get_all_voters():
    sql = 'select * from voters'
    with connect() as conn:
        voters = conn.execute(sql).fetchall()
        return [dict(voter) for voter in voters]

def update_voter(voterFName, voterMName, voterLName, voterPass, voterID):
    sql = 'update voters set voterFName = ?, voterMName = ?, voterLName = ?, voterPass = ? where voterID = ?'
    with connect() as conn:
        conn.execute(sql,(voterFName, voterMName, voterLName, voterPass, voterID))
        conn.commit()
        return True
    
def deactivate_voter(voterID):
    sql = 'update voters set voterStat = "Inactive" where voterID = ?'
    with connect() as conn:
        conn.execute(sql,(voterID))
        conn.commit()
        return True
    
def search_voter(query):
    sql = "select * from voters where voterFName like ? or voterMName like ? or voterLName like ? or voterStat like ?"
    query = f"%{query}%"
    with connect() as conn:
        results = conn.execute(sql,(query, query, query, query)).fetchall()
        return [dict(result) for result in results]
    
def get_all_candidates():
    sql = 'select * from candidates c join positions p where c.posID == p.posID'
    with connect() as conn:
        candidates = conn.execute(sql).fetchall()
        return [dict(candidate) for candidate in candidates]
    
def add_candidate(candFName, candMName, candLName, posID):
    sql = 'insert into candidates (candFName, candMName, candLName, posID) values (?,?,?,?)'
    with connect() as conn:
        conn.execute(sql,(candFName, candMName, candLName, posID))
        conn.commit()
        return True
    
def update_candidate(candFName, candMName, candLName, posID, candStat, candID):
    sql = 'update candidates set candFName = ?, candMName = ?, candLName = ?, posID = ?, candStat = ? where candID = ?'
    with connect() as conn:
        conn.execute(sql,(candFName, candMName, candLName, posID, candStat, candID))
        conn.commit()
        return True

def deactivate_candidate(candID):
    sql = 'update candidates set candStat = "Inactive" where candID = ?'
    with connect() as conn:
        conn.execute(sql,(candID))
        conn.commit()
        return True

if __name__ == "__main__":
    create_tables()
    # print(search_position('vice'))
    # print(run('select * from vote'))
    # print(get_all_candidates())
    # run('drop table candidates')