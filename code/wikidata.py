#!/usr/bin/env python
from __future__ import print_function, division
import argparse
import json
import sys
from gzip import GzipFile
from SPARQLWrapper import SPARQLWrapper, JSON, XML, TURTLE, RDF, N3

def concat_claims(claims):
    for rel_id, rel_claims in claims.iteritems():
        for claim in rel_claims:
            yield claim

def test():
	a="valami"

def to_triplets(ent):
    claims = concat_claims(ent['claims'])
    triplets = []
    e1 = ent['labels']['en']['value']
    for claim in claims:
        mainsnak = claim['mainsnak']
        if mainsnak['snaktype'] != "value":
            continue
        if mainsnak['datatype'] == 'wikibase-item':
	    e2 = 'Q{}'.format(mainsnak['datavalue']['value']['numeric-id'])
	    sparql = SPARQLWrapper('https://query.wikidata.org/sparql')
	    sparql.setQuery('''
                 PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                 PREFIX wd: <http://www.wikidata.org/entity/>
                 select  * where {wd:%s rdfs:label ?label .FILTER (langMatches( lang(?label), "EN" ) )} LIMIT 1'''%e2)
            sparql.setReturnFormat(JSON)
            results = sparql.query().convert()
	    rel = mainsnak['property']
            try:
            	final = results['results']['bindings'][0]['label']['value']
            except IndexError:
		final = "novalue"

	    sparql2 = SPARQLWrapper('https://query.wikidata.org/sparql')
	    sparql2.setQuery('''
                 PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                 PREFIX wd: <http://www.wikidata.org/entity/>
                 select  * where {wd:%s rdfs:label ?label .FILTER (langMatches( lang(?label), "EN" ) )} LIMIT 1'''%rel)
	    sparql2.setReturnFormat(JSON)
	    property = sparql2.query().convert()
	    try:
                propertyfinal = property['results']['bindings'][0]['label']['value']
            except IndexError:
                propertyfinal = "novalue"

            triplets.append((e1, propertyfinal, final))
	    #results['results']['bindings'][0]['label']['value'])
    return triplets


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Log-Bilinear model for relation extraction.')
    _arg = parser.add_argument
    _arg('--read-dump', type=str, action='store',
         metavar='PATH', help='Reads in a wikidata json dump.')
    args = parser.parse_args()

    train_set = None
    if args.read_dump:
        dump_in = GzipFile(args.read_dump, 'r')
        line = dump_in.readline();
        iter = 0
        while line != '':
            iter += 1
            line = dump_in.readline()
            try:
                ent = json.loads(line.rstrip('\n,'))
                if not ent['id'].startswith('Q'):
                    print("Skipping item with id {}".format(ent['id']),
                          file=sys.stderr)
                    continue
                #print('\n'.join(
                 #   ['{}\t{}\t{}'.format(*t) for t in to_triplets(ent)]),
                  #    file=sys.stdout)
		for result in to_triplets(ent):
			d = {}
			
			d["arg1"] =result[0]
			d["arg2"] =result[1]
			d["arg3"] =result[2]
			print(d)
            except (KeyError, ValueError, IndexError) as e:
                print(e, file=sys.stderr)
            if iter % 1000 == 0:
                sys.stdout.flush()
