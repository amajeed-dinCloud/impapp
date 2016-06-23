__author__ = 'Abdul'
import MySQLdb
import settings
import datetime


def refresh_ratings():
    updated_rows = 0
    try:
        print "********"+str(datetime.datetime.now())+"********"
        conn = MySQLdb.connect(host=settings.DATABASE_HOST, user=settings.DATABASE_USER, passwd=settings.DATABASE_PASS,
                               db=settings.DATABASES_CURRENT)
        print "Connection Successful."
        cursor = conn.cursor()
        query = "UPDATE app_user SET profile_rating=(SELECT AVG(rating) FROM app_ratings" \
                " WHERE app_user.id = app_ratings.rated_profile_id);"
        print "Executing Query."
        cursor.execute(query)
        updated_rows = cursor.rowcount
        print "No of user were updated :" + str(updated_rows)
        conn.commit()
        cursor.close()
        conn.close()
        print "Closing Connection."
    except Exception, ex:
        updated_rows = 'NA'
        print str(ex)
    return updated_rows


refresh_ratings()