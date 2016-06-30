__author__ = 'Abdul'
import MySQLdb
import settings
import datetime
import json


def refresh_ratings():
    updated_rows = 0
    try:
        print "********"+str(datetime.datetime.now())+"********"
        conn = MySQLdb.connect(host=settings.DATABASE_HOST, user=settings.DATABASE_USER, passwd=settings.DATABASE_PASS,
                               db=settings.DATABASES_CURRENT)
        conn.autocommit(True)
        print "Connection Successful."

        cursor = conn.cursor()
        contest_query = "SELECT val FROM app_customattributes ca WHERE ca.key='contest_ending_date';"
        cursor.execute(contest_query)
        data = cursor.fetchone()
        if data:
            contest_end_date =  data[0]
            end_date = datetime.datetime.strptime(contest_end_date, '%m/%d/%Y  %I:%M %p')
            print end_date
            current_time = datetime.datetime.now()
            diff = end_date-current_time
            print diff.total_seconds()
            if diff.total_seconds() > 0:
            # if 1:
                query = "UPDATE app_user t1 " \
                        "JOIN (SELECT rated_profile_id AS id,AVG(rating) AS ratings, COUNT(rated_profile_id) AS votes " \
                        "FROM app_ratings t2 GROUP BY rated_profile_id)t2 ON t1.id = t2.id " \
                        "SET t1.profile_rating = t2.ratings,t1.vote_count = t2.votes;"

                print "Executing Query."
                cursor.execute(query)
                updated_rows = cursor.rowcount
                print "No of user were updated :" + str(updated_rows)
            else:
                check_query = "SELECT * FROM app_contests WHERE end_date = '%s'"%(end_date)
                cursor.execute(check_query)
                if cursor.rowcount == 0:
                    vote_count_limit_q = "SELECT val FROM app_customattributes ca WHERE ca.key='top_ten_min_votes';"
                    cursor.execute(vote_count_limit_q)
                    vote_limit = cursor.fetchone()
                    vote_limit = vote_limit[0] if vote_limit else 1
                    current_top_ten_q = "SELECT id, profile_rating, vote_count FROM app_user " \
                                        "WHERE (is_public= TRUE AND is_active = TRUE AND is_approved = TRUE AND " \
                                        "vote_count>="+vote_limit+") ORDER BY profile_rating DESC LIMIT 10;"
                    cursor.execute(current_top_ten_q)
                    top_ten = cursor.fetchall()

                    update_rating_q = "UPDATE app_user SET profile_rating=0,vote_count=0;"
                    cursor.execute(update_rating_q)

                    print "No of profiles(rating) updated: " + str(cursor.rowcount)
                    del_rating_table_q = "truncate app_ratings;"
                    cursor.execute(del_rating_table_q)
                    top_ten = json.dumps(list(top_ten))
                    cursor.execute("insert into app_contests (end_date, top_ten,updated_on,created_on)values(%s, %s, %s, %s)",
                                   (end_date, top_ten, current_time, current_time))
                    print "Contest has been added successfully."
                else:
                    print "Contest is already in contest table."



        cursor.close()
        conn.close()
        print "Closing Connection."
    except Exception, ex:
        updated_rows = 'NA'
        print str(ex)
    return updated_rows


refresh_ratings()