__author__ = 'Abdul'
import MySQLdb
import settings
import datetime


def auto_approve():
    updated_rows = 0
    try:
        print "********Running Auto Approval Script********"
        print "********"+str(datetime.datetime.now())+"********"
        conn = MySQLdb.connect(host=settings.DATABASE_HOST, user=settings.DATABASE_USER, passwd=settings.DATABASE_PASS,
                               db=settings.DATABASES_CURRENT)
        print "Connection Successful."
        cursor = conn.cursor()
        query = "UPDATE app_user SET is_approved=1 WHERE" \
                " created_on > SUBDATE( CURRENT_TIMESTAMP, INTERVAL 7 HOUR) AND is_approved=0"

        print "Executing Query."
        cursor.execute(query)
        updated_rows = cursor.rowcount
        print "No of users approved: " + str(updated_rows)
        conn.commit()
        cursor.close()
        conn.close()
        print "Closing Connection."
    except Exception, ex:
        updated_rows = 'NA'
        print str(ex)
    return updated_rows


auto_approve()