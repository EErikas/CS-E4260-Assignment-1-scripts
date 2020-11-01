import sqlite3
import os


post_url = 'https://03637650b3826afe48a00e3c488f39bc.m.pipedream.net'
header = [
    'ID',
    'Service',
    'Url',
    'CacheUrl',
    'CacheServerDelay',
    'IP',
    'Resolver',
    'ResolveTime',
    'ASNumber',
    'PingMin',
    'PingAvg',
    'PingMax',
    'DownloadTime',
    'VideoType',
    'VideoDuration',
    'VideoLength',
    'EncodingRate',
    'DownloadBytes',
    'DownloadInterruptions',
    'InitialData',
    'InitialRate',
    'InitialPlaybackBuffer',
    'BufferingDuration',
    'PlaybackDuration',
    'BufferDurationAtEnd',
    'TimeTogetFirstByte',
    'MaxInstantThp',
    'RedirectUrl',
    'StatusCode'
]
pwd = os.path.dirname(os.path.realpath(__file__))
db_dir = os.path.join(pwd, 'databases')


def readSqliteTable():
    latest_db = sorted(os.listdir(db_dir))[-1]
    name = '_'.join(latest_db.split('.')[2:4])

    try:
        sqliteConnection = sqlite3.connect(os.path.join(db_dir, latest_db))
        cursor = sqliteConnection.cursor()
        print("Connected to database")
        sqlite_select_query = """SELECT * from pytomo_crawl_{}""".format(
            name.replace('-', '_'))
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()
        result_file = 'crawl_results_{}.txt'.format(name)
        with open(result_file, 'w') as file:
            file.write(','.join(header) + ',\n')
            for record in records:
                file.write(','.join(str(foo) for foo in record) + ',\n')
        cursor.close()
        sqliteConnection.close()

        return result_file

    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)


if __name__ == "__main__":
    source_dir = os.path.join(pwd, 'sources')
    for soure_file in os.listdir(source_dir):
        print('Executing command...')
        file_path = os.path.join(source_dir, soure_file)
        os.system('./start_crawl.py -f "{}" -b'.format(file_path))
        print('Reading database....')
        result_file = readSqliteTable()
        print('Sending data....')
        os.system("curl -X POST -H 'Content-Type: text/csv' -H 'Vantage-Point: {0}' -d @{1} {2}".format(
            os.uname()[1] + '-' + soure_file,
            result_file,
            post_url
        ))
    print('Done')
