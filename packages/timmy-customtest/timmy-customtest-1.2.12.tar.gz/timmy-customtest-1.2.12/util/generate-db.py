#!/usr/bin/python

import sys
import argparse
import urllib2
import sqlite3
import os
import bz2
import zlib
import tempfile
import xml.etree.ElementTree as ET
from StringIO import StringIO

releases = ['5.1',
            '5.1.1',
            '6.0',
            '6.1',
            '7.0',
            '8.0',
           ]

systems = ['ubuntu',
           'centos',
          ]

def main(argv=None):

    def verify_args():
        if not args.os:
            return 'OS not specified.'
        if args.os not in systems:
            return 'Unknown OS specified.'
        if not args.release:
            return 'Release not specified.'
        elif args.release not in releases:
                return 'Specified release "'+args.release+'" is unknown.'
        if not args.updates_source:
            if not args.release_source:
                return 'Release source not specified.'
        else:
            if not args.mu_number:
                return 'MU file provided but MU number not specified.'
            if not args.database:
                return 'MU file provided but database not specified.'
        if not args.output:
            return 'Output file not specified.'
        try:
            open(args.output, 'w')
        except Exception:
            return 'Cannot write to the output file '+args.output

    def fetch(sources):
        fetched = {}
        for source in sources:
            try:
                request = urllib2.urlopen(source)
            except Exception:
                sys.stderr.write('Error: Could not access "%s", verify URL correctness.\n'
                    % (str(source),))
                sys.exit(1)
            fetched[source] = request.read()
        return fetched

    def debs_from_source(data):
        packages = []
        packagedata = data.split('\n\n')
        for pd in packagedata:
            if len(pd) == 0:
                continue
            package = {}
            lines = pd.split('\n')
            for line in lines:
                unpacked = line.split(': ', 1)
                if len(unpacked) > 1:
                    package[unpacked[0]] = unpacked[1]
            package['Filename'] = package['Filename'].split('/')[-1]
            packages.append(package)
        return packages

    def rpms_from_source(data, source):
        packages = []
        with tempfile.NamedTemporaryFile() as tf:
            if source.endswith('.sqlite.bz2'):
                tf.write(bz2.decompress(data))
                tf.flush()
                db = sqlite3.connect(tf.name)
                dbc = db.cursor()
                packagedata = dbc.execute('''
                   SELECT
                       name,
                       epoch,
                       version,
                       release,
                       location_href
                   FROM packages
                   ''')
                for pd in packagedata:
                    if pd[4].split('/')[0] != 'Packages':
                        #ignore source rpms
                        continue
                    package = {}
                    package['Package'] = pd[0]
                    if pd[1] != '0':
                        package['Version'] = pd[1]+':'+pd[2]+'-'+pd[3]
                    else:
                        package['Version'] = pd[2]+'-'+pd[3]
                    package['Filename'] = pd[4].split('/')[-1]
                    packages.append(package)
                db.close()
            elif source.endswith('xml.gz'):
                xmldata = zlib.decompress(data, zlib.MAX_WBITS | 16)
                xmltree = ET.iterparse(StringIO(xmldata))
                # strip namespaces
                for _, el in xmltree:
                    if '}' in el.tag:
                        el.tag = el.tag.split('}', 1)[1]
                for pd in xmltree.root:
                    package = {}
                    p_ep = pd.find('version').get('epoch')
                    p_ver = pd.find('version').get('ver')
                    p_rel = pd.find('version').get('rel')
                    package['Package'] = pd.findtext('name')
                    package['Filename'] = pd.find('location').get('href').split('/')[-1]
                    if p_ep != '0':
                        package['Version'] = '%s:%s-%s' % (p_ep, p_ver, p_rel)
                    else:
                        package['Version'] = '%s-%s' % (p_ver, p_rel)
                    packages.append(package)
            else:
                print('unknown format of %s' % (source,))
        return packages

    def dbgen(sources, mu=0, job_id=-1):
        db = sqlite3.connect(args.output)
        dbc = db.cursor()
        if os.stat(args.output).st_size == 0:
            #empty file -> new db, creating tables
            dbc.execute('''
                CREATE TABLE sources
                (
                    id INTEGER PRIMARY KEY,
                    source TEXT
                )''')
            dbc.execute('''
                CREATE TABLE versions
                (
                    id INTEGER PRIMARY KEY,
                    source_id INTEGER,
                    job_id INTEGER,
                    release TEXT,
                    mu INTEGER,
                    os TEXT,
                    package_name TEXT,
                    package_version TEXT,
                    package_filename TEXT
                )''')
        for source, data in sources.items():
            r = dbc.execute('''
                SELECT rowid FROM sources WHERE source = ?
                ''', (source,)).fetchall()
            if len(r) == 0:
                dbc.execute('''
                    INSERT INTO sources (source) VALUES (?)
                    ''', (source,))
                r = dbc.execute('''
                        SELECT rowid FROM sources
                        WHERE source = ? 
                    ''', (source,)).fetchall()
            source_id = r[0][0]
            if args.os == 'ubuntu':
                packages = debs_from_source(data)
            if args.os == 'centos':
                packages = rpms_from_source(data, source)
            for package in packages:
                r = dbc.execute('''
                    SELECT source_id, mu FROM versions
                    WHERE release = ?
                          AND mu = ?
                          AND os = ?
                          AND package_name = ?
                          AND package_version = ?
                          AND package_filename = ?
                    ''', (args.release,
                          mu,
                          args.os,
                          package['Package'],
                          package['Version'],
                          package['Filename']))
                pkgs = r.fetchall()
                if len(pkgs) > 0:
                    found_mu = 'GA' if pkgs[0][1] == 0 else 'MU%s' % (pkgs[0][1])
                    r = dbc.execute('''
                        SELECT source FROM sources
                        WHERE id = ?
                        ''', (pkgs[0][0],))
                    found_source = r.fetchone()[0]
                    print('  Duplicate package in %s\n    %s %s\n'
                          '    already provided by %s (%s)\n  Skipping...' % (
                              source,
                              package['Package'],
                              package['Version'],
                              found_source,
                              found_mu))
                else:
                    dbc.execute('''
                        INSERT INTO versions
                        (
                            source_id,
                            job_id,
                            release,
                            mu,
                            os,
                            package_name,
                            package_version,
                            package_filename
                        ) VALUES (?,?,?,?,?,?,?,?)
                        ''', (source_id,
                              job_id,
                              args.release,
                              mu,
                              args.os,
                              package['Package'],
                              package['Version'],
                              package['Filename']))
        db.commit()

    # validating arguments
    if not argv:
        sys.stderr.write('Error: no parameters specified.\n')
        return 1
    else:
        parser = argparse.ArgumentParser(description='Build or update a versions database')
        parser.add_argument('-s', '--os',
                            help=('Mandatory. '
                                  'OS, for which the db is generated - '
                                  '"ubuntu" or "centos".'
                                 ))
        parser.add_argument('-r', '--release',
                            help=('Mandatory. '
                                  'Release version (example: 6.1).'
                                 ))
        parser.add_argument('-g', '--release-source', nargs='+',
                            help=('Mandatory when GA is processed. '
                                  'URL(s) to GA packages db file(s). '
                                  'If --os is ubuntu - "Packages" file(s), '
                                  'if --os is centos - '
                                  '"...-primary.sqlite.bz2" file(s). '
                                  'Local files are supported via '
                                  'file://<abs-path>. '
                                  'You must provide all URLs at once, like '
                                  'so: -g http://... file://... file://...'
                                 ))
        parser.add_argument('-d', '--database',
                            help=('Mandatory when MU is processed. '
                                  'URL (only one) to a most updated '
                                  'database previously built by this '
                                  'tool for the specified release. '
                                  'See help for -g for more details.'
                                 ))
        parser.add_argument('-u', '--updates-source', nargs='+',
                            help=('Mandatory when MU is processed. '
                                  'URL(s) to MU update packages db file(s). '
                                  'See help for -g for more details.'
                                 ))
        parser.add_argument('-n', '--mu-number',
                            help=('Mandatory when MU is processed. '
                                  'integer ID of the MU update.'
                                 ))
        parser.add_argument('-o', '--output',
                            help=('Mandatory. '
                                  'Path (not URL) to the output database '
                                  'file. Must not be the same file as -d '
                                  'because output file is cleaned before '
                                  'opening the database.'
                                 ))
        parser.add_argument('-j', '--job-id',
                            help='Optional. ID of the current Jenkins job.')

        args = parser.parse_args(argv[1:])
        args_check_error = verify_args()
        if args_check_error:
            sys.stderr.write('Error: '+args_check_error+'\n')
            return 1
    # database generation / update
    if not args.updates_source:
        #GA db generation
        print('GA -> db generation...')
        release_source = fetch(args.release_source)
        dbgen(sources=release_source, job_id=args.job_id)
    else:
        #MU db update
        print('MU -> db update...')
        updates_source = fetch(args.updates_source)
        updates_db = fetch([args.database])[args.database]
        with open(args.output,'w') as file:
            file.write(updates_db)
        dbgen(updates_source, args.mu_number, args.job_id)

if __name__ == '__main__':
    exit(main(sys.argv))

