#!/usr/bin/env python
# encoding: utf-8

# Front Matter {{{
'''
Copyright (c) 2016 The Broad Institute, Inc.  All rights are reserved.

mdbcp: this file is part of mdbtools.  See the <root>/COPYRIGHT
file for the SOFTWARE COPYRIGHT and WARRANTY NOTICE.

@author: Michael S. Noble
@date:  2016_05_06
'''

# }}}

from MDBtool  import *
from MDButils import *

class mdbcp(MDBtool):

    def __init__(self):
        super(mdbcp, self).__init__(version='0.2.0')

        cli = self.cli
        desc = 'Simple CLI tool to copy (clone) a MongoDB collection\n\n'
        cli.description = desc

        cli.add_argument('-c', '--chunkSize', type=int, default=5000,
                    help='number of documents to copy/insert at a time')
        cli.add_argument('-f', '--force', action='store_true',
                    help='force copy: remove To collection first, if it exists')
        cli.add_argument('-n', '--numToCopy', default=None,
                    help='how many documents to copy (default: all)')

        # Positional (required) arguments
        cli.add_argument('From', help='name of existing collection')
        cli.add_argument('To', help='name of new collection to create '+\
                '(prefix with "<database_name>/" to copy to different DB)')

    def validate(self):
        opts = self.options
        if not opts.From in self.collection_names:
            eprint('Collection %s does not exist in %s:%s' %
                        (opts.From, opts.server, opts.dbname), abort=101)

        # 'To' can be database/collection (but for now, only on same server)
        To = opts.To.split("/")
        if len(To) > 1:
            self.To_db = self.connection[To[0]]
        else:
            self.To_db = self.db

        # Check if like-named collection already exists in destination DB
        opts.To = To[-1]
        if not opts.To in self.To_db.collection_names():
            return

        # Destination collection already exists: oh my, what to do?
        if opts.force:
            self.To_db[opts.To].drop()
        else:
            eprint('%s collection already exists in %s:%s' % \
                        (opts.To, opts.server, self.To_db.name), abort=102)

    def clone(self):

        opts = self.options
        To = self.To_db[opts.To]
        From = self.db[opts.From]
        numCopied = 0
        totalNumRows = From.find().count()
        chunkSize = opts.chunkSize
        if opts.numToCopy:
            totalNumRows = min(totalNumRows, int(opts.numToCopy))

        chunkSize = min(chunkSize, totalNumRows)
        src  = self.db.name + "/" + opts.From
        dest = self.To_db.name + "/" + opts.To
        mprint('Copying collection %s to %s' % (src, dest))

        while True:
            documents = From.find().skip(numCopied).limit(chunkSize)
            if not documents or documents.count()==0:
                break
            count = documents.count(with_limit_and_skip=True)
            To.insert(documents)
            numCopied = numCopied + count
            percentage = 100.0 * numCopied / totalNumRows
            mprint('Copied %d (of %d total, %f %%)' % \
                                (numCopied, totalNumRows, percentage))
            if numCopied >= totalNumRows:
                break
            chunkSize = min(chunkSize, totalNumRows - numCopied)

        mprint('Done copying documents ... ',end='')
        index_info = From.index_information()
        index_info.pop('_id_', None)

        indexes = []
        for idx in index_info.values():
            indexes.append( IndexModel(idx['key']) )

        # Add all indexes in one call, to iterate single time over data
        if indexes:
            mprint('now adding indexes',end='')
            To.create_indexes(indexes)
        mprint('')

    def execute(self):
        super(mdbcp, self).execute()
        self.validate()
        self.clone()

if __name__ == '__main__':
    mdbcp().execute()
