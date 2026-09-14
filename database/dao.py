from database.DB_connect import DBConnect
from model.team import Team


class DAO:


    """
    Permettere all’utente di selezionare da un apposito menu a tendina il
     valore di un anno di campionato, tra quelli disponibili nel database
      (colonna year della tabella team), a partire dal 1980
      (gli anni precedenti non devono comparire)
    """

    @staticmethod
    def get_years_from_1980():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
                    SELECT DISTINCT year
                    FROM team
                    WHERE year >= 1980
                    ORDER BY year
                    """
        cursor.execute(query)
        years = [row["year"] for row in cursor]
        cursor.close()
        conn.close()
        return years




    """
        Non appena viene selezionato l’anno (intercettando l’evento on_change), 
        si dovrà stampare il numero di squadre (tabella team) che ha giocato in tale anno,
         e l’elenco delle rispettive sigle, nella prima area di testo (txt_out_squadre).
          Nello stesso momento occorre aggiornare il contenuto del menu a tendina “Squadre”.
        """
    @staticmethod
    def get_teams_by_year(year):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
                    SELECT id, team_code, name
                    FROM team
                    WHERE year = %s
                    """
        cursor.execute(query, (year,))
        teams = [Team(row["id"], row["team_code"], row["name"]) for row in cursor]
        cursor.close()
        conn.close()
        return teams


    """
    Il peso di ciascun arco del grafo deve corrispondere alla somma dei salari dei 
    giocatori delle due squadre nell’anno considerato. Nota: potrebbe essere 
    conveniente calcolare e memorizzare la somma dei salari di ciascuna squadra.
    """
    @staticmethod
    def get_team_salary(year):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
                    SELECT team_id, SUM(salary) AS total
                    FROM salary
                    WHERE year = %s
                    GROUP BY team_id
                    """
        cursor.execute(query, (year,))
        result = {row["team_id"]: row["total"] for row in cursor}
        cursor.close()
        conn.close()
        return result