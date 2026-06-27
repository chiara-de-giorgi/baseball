from database.DB_connect import DBConnect
from model.arco import Arco
from model.team import Team


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllYears():
        # Carica tutti gli oggetti della tabella objects, restituendoli come lista di ArtObject.
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        result = []  # Lista di ArtOjbect

        cursor = conn.cursor(dictionary=True)
        query = """ select distinct year
                    from teams
                    where year>=1980
                    order by year """

        cursor.execute(query)

        for row in cursor:
            result.append(row['year'])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getTeamsYear(year):
        # Carica tutti gli oggetti della tabella objects, restituendoli come lista di ArtObject.
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        result = []  # Lista di ArtOjbect

        cursor = conn.cursor(dictionary=True)
        query = """  select t.*
                    from teams t
                    where t.year=%s"""

        cursor.execute(query, (year,))

        for row in cursor:
            result.append(Team(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdges(idMapT, year):
        # Carica tutti gli oggetti della tabella objects, restituendoli come lista di ArtObject.
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        result = []  # Lista di ArtOjbect

        cursor = conn.cursor(dictionary=True)
        query = """select t1.id as t1, t2.id as t2  , (sal1.totsalary + sal2.totsalary ) as peso
                    from teams t1, teams t2, 
                        (
                            select t.ID, t.teamCode, sum(s.salary) as totSalary
                            from teams t, salaries s, appearances a  
                            where a.year=%s and s.year=t.year and t.year=a.year 
                                and t.ID =a.teamID and a.playerID = s.playerID 
                            group by t.ID, t.teamCode  ) sal1,
                        (
                            select t.ID, t.teamCode, sum(s.salary) as totSalary
                            from teams t, salaries s, appearances a  
                            where a.year=%s and s.year=t.year and t.year=a.year 
                                and t.ID =a.teamID and a.playerID = s.playerID 
                            group by t.ID, t.teamCode  ) sal2 
                    where t1.year=%s and t2.year=%s
                            and t1.ID=sal1.ID and t2.ID= sal2.id 
                            and t1.id> t2.id"""

        cursor.execute(query, (year, year, year, year))

        for row in cursor:
            t1=idMapT[row['t1']]
            t2=idMapT[row['t2']]
            peso=row['peso']
            result.append(Arco(t1, t2, peso))

        cursor.close()
        conn.close()
        return result

