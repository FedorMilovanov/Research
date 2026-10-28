#!/usr/bin/env python3
"""REC-01 source locus and a pinned derived anthology witness; no independent-reader claim."""
import argparse
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from audit_charnock_pastoral_contexts import ROOT, source_structure
from audit_charnock_book_route import NS, plain
from audit_charnock_thoughts import digest, HOLDS

KEY='receptionLocusReview'
FLAGS=('originalSpurgeonEditionVerified','nicholPaginationVerified','independentReaderAdded',
       'wholeDiscourseRead','wholeMirrorRead','publicationApproval')

class Paragraphs(HTMLParser):
    def __init__(self):super().__init__(convert_charrefs=True);self.rows=[];self.current=None
    def handle_starttag(self,tag,attrs):
        if tag=='p':self.current=[]
    def handle_data(self,data):
        if self.current is not None:self.current.append(data)
    def handle_endtag(self,tag):
        if tag=='p' and self.current is not None:
            self.rows.append(' '.join(''.join(self.current).split()));self.current=None

def words(text):return re.findall(r'[a-z]+',text.lower())

def extract(directory,registry):
    _,_,parents,pages,paragraphs=source_structure(directory,registry,'A32723')
    selected=paragraphs[2638:2649];node=paragraphs[2646]
    while node in parents:
        node=parents[node]
        if node.tag==NS+'div':break
    return dict(source='A32723',sourceSha256=registry['sources']['A32723']['sha256'],
                heading=plain(node.find(NS+'head')),
                paragraphs=[dict(paragraphIndexZeroBased=paragraphs.index(p),startTeiPage=pages[p],text=plain(p),textSha256=digest(plain(p))) for p in selected])

def extract_mirror(path):
    raw=path.read_bytes();parser=Paragraphs();parser.feed(raw.decode('utf-8'))
    probes=['When sin is pardoned;', '"To do them." Commands are to be remembered', 'Psa 103:19. - "A Discourse upon God\'s Dominion."']
    selected=[]
    for probe in probes:
        hits=[(i,t) for i,t in enumerate(parser.rows) if t.startswith(probe)]
        if len(hits)!=1:raise ValueError('Unique anthology paragraph not found')
        i,t=hits[0];selected.append(dict(htmlParagraphIndexZeroBased=i,text=t,textSha256=digest(t)))
    return dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),gitBlobSha1=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest(),paragraphs=selected)

def extract_condensed(directory,registry,mirror):
    _,_,_,pages,paragraphs=source_structure(directory,registry,'A32723')
    parser=Paragraphs();parser.feed(mirror.read_text())
    return dict(sourceParagraphs=[dict(paragraphIndexZeroBased=i,startTeiPage=pages[paragraphs[i]],
                        text=plain(paragraphs[i]),textSha256=digest(plain(paragraphs[i]))) for i in range(2661,2669)],
                mirrorParagraphs=[dict(htmlParagraphIndexZeroBased=i,text=parser.rows[i],
                        textSha256=digest(parser.rows[i])) for i in range(325,332)],
                followingMirrorAuthor=parser.rows[333].rsplit(' - ',1)[-1])


def check_condensed(review):
    c=review['condensedPassage'];reading=c['byteVerifiedReading'];source=reading['sourceParagraphs'];mirror=reading['mirrorParagraphs']
    if (c['reviewState']!='ALL_SIX_ORDERED_POINTS_LOCATED_SELECTIVE_CONDENSATION'
            or any(c[k] is not False for k in ['verbatimWholePassage','newIndependentReader',
                   'printedEditionCollated','modernAstronomyVerified','publicationApproval'])):
        raise ValueError('Six-source correspondence is not verbatim quotation or edition collation')
    if ([r['paragraphIndexZeroBased'] for r in source]!=list(range(2661,2669))
            or [r['htmlParagraphIndexZeroBased'] for r in mirror]!=list(range(325,332))
            or [r['startTeiPage'] for r in source[1:7]]!=['701']*4+['702']*2
            or not mirror[-1]['text'].endswith(' - Condensed from Charnock.')
            or reading['followingMirrorAuthor']!='Thomas Adams.'):
        raise ValueError('Preserve all six points and the adjacent author boundary')
    if any(digest(r['text'])!=r['textSha256'] for r in source+mirror):
        raise ValueError('Condensed passage paragraph hash mismatch')
    if (not mirror[3]['text'].startswith('3. Peculiarity of this dominion lie rules')
            or not source[3]['text'].startswith('3. Peculiarly of this Dominion.')):
        raise ValueError('Do not silently repair derived lie or source Peculiarly')
    if [p['point'] for p in c['pointComparisons']]!=list(range(1,7)):
        raise ValueError('Each ordered point needs a retained and omitted span')
    for i,p in enumerate(c['pointComparisons'],1):
        if p['sourceParagraph']!=2661+i or p['mirrorParagraph']!=325+i or not p['finding']:
            raise ValueError('Six corresponding points, not a rearranged anthology')
        for key,text in [('retainedSourceSpan',source[i]['text']),('retainedMirrorSpan',mirror[i]['text']),('omittedSourceSpan',source[i]['text'])]:
            span=p[key]
            if not span['text'] or span['text'] not in text or digest(span['text'])!=span['sha256']:
                raise ValueError('Each comparison must be grounded in exact source and mirror spans')
        if p['omittedSourceSpan']['text'].casefold() in mirror[i]['text'].casefold():
            raise ValueError('Claimed omission is still present')
    if not c['scope'] or not c['limits'] or not c['boundaryConclusion']:
        raise ValueError('Retain selected scope and source/derived witness distinction')
    return dict(receptionCondensedPointsLocated=6,receptionCondensedVerbatimWholePassage=False)



SYMPIN={'repository': 'BenjaminPoole/Ecumenical-Christian-Library-Obsidian-Vault', 'path': '06 Puritans (1600–1700)/Stephen Charnock/The Existence and Attributes of God/EAG 01 Life and Character of Charnock.md', 'commit': 'c8babb9c7f648c6ed625ffedd16575973da14808', 'blob': '1a20abcddcfdfe375386f61fca4c5e90e6ea270e', 'bytes': 38106, 'sha256': '0405687f5ac825c7d18719aae7e7785a029f7045642f34fe4d181b5704fcc709', 'url': 'https://github.com/BenjaminPoole/Ecumenical-Christian-Library-Obsidian-Vault/blob/c8babb9c7f648c6ed625ffedd16575973da14808/06%20Puritans%20%281600%E2%80%931700%29/Stephen%20Charnock/The%20Existence%20and%20Attributes%20of%20God/EAG%2001%20Life%20and%20Character%20of%20Charnock.md'}

def extract_praise(directory,registry,mirror):
    raw=mirror.read_bytes()
    if (len(raw)!=SYMPIN['bytes'] or hashlib.sha256(raw).hexdigest()!=SYMPIN['sha256']
            or hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()!=SYMPIN['blob']):
        raise ValueError('Biographical mirror byte/blob mismatch')
    text=raw.decode('utf-8');start=text.index('All Charnock’s writings');end=text.index('ANNFIELD PLACE, Glasgow, June, 1846.',start)
    parts=text[start:end].strip().split('\n\n')
    if len(parts)!=4:raise ValueError('Four complete terminal prose paragraphs required')
    _,_,_,pages,paras=source_structure(directory,registry,'A32723');original=plain(paras[4])
    return dict(mirrorFrontmatter=text[:text.index('\n# Life and Character')].strip(),
                paragraphs=[dict(indexFromSelectedStart=i,text=t,textSha256=digest(t)) for i,t in enumerate(parts)],
                dateline='ANNFIELD PLACE, Glasgow, June, 1846.',
                topLadyFootnote='[^3]: Toplady.' if '[^3]: Toplady.' in text else None,
                editorialContext=dict(source='A32723',sourceSha256=registry['sources']['A32723']['sha256'],
                    paragraphIndexZeroBased=4,startTeiPage=pages[paras[4]],text=original,textSha256=digest(original)))


def check_praise(review,registry):
    r=review['biographicalPraiseReview'];data=r['byteVerifiedReading']
    if (r['reviewState']!='DERIVED_SYMINGTON_ATTRIBUTION_PRAISE_CONTEXT_NOT_PRINTED_BIOGRAPHY'
            or r['sourcePin']!=SYMPIN
            or any(r[k] is not False for k in ['printedBiographyVerified','mirrorMetadataAuthorshipAccepted',
                'allPraiseIsBiographerOwnVoice','independentEyewitnessAdded','salesEstablished',
                'wholeBiographyRead','publicationApproval'])):
        raise ValueError('Praise and modern metadata are not independent biography or print verification')
    rows=data['paragraphs'];editor=data['editorialContext']
    if ([x['indexFromSelectedStart'] for x in rows]!=list(range(4))
            or data['dateline']!='ANNFIELD PLACE, Glasgow, June, 1846.'
            or data['topLadyFootnote']!='[^3]: Toplady.'
            or 'author: "Stephen Charnock"' not in data['mirrorFrontmatter']
            or '1682 (published posthumously)' not in data['mirrorFrontmatter']):
        raise ValueError('Keep the metadata/body conflict and attribution footnote visible')
    if (editor['sourceSha256']!=registry['sources']['A32723']['sha256']
            or editor['paragraphIndexZeroBased']!=4 or editor['startTeiPage'] is not None):
        raise ValueError('Original editorial context remains unnumbered, not a biography page')
    if any(digest(x['text'])!=x['textSha256'] for x in rows+[editor]):raise ValueError('Praise/context hash mismatch')
    if [x['id'] for x in r['observations']]!=[f'BP{i:02}' for i in range(1,7)]:raise ValueError('Six bounded voice/context decisions required')
    texts={str(i):x['text'] for i,x in enumerate(rows)};texts['EDITOR']=editor['text']
    for obs in r['observations']:
        if not obs['finding'] or not obs['limit'] or not obs['spans']:raise ValueError('Praise observation needs attribution limits')
        for span in obs['spans']:
            if not span['text'] or span['text'] not in texts[span['source']] or digest(span['text'])!=span['sha256']:
                raise ValueError('Praise reading must preserve actual words and nested voices')
    if not r['attributionBasis'] or not r['scope'] or not r['rightsLimits']:raise ValueError('Preserve derived attribution, selected scope and rights')
    return dict(biographicalPraiseSelectedParagraphs=4,biographicalPraiseObservations=6,biographicalPraisePrintVerified=False)



DIGITAL_PINS={'INDEX': {'repository': 'jonnyg23/mahabrain', 'path': 'sacred_obsidian_vault/chr/charnock/index.md', 'commit': '025ee3c09f8d5bf6eb8c832c55fdd65e9d7d6c55', 'blob': '70e24dccb33dc5f76b27b1f97db0c43aab2d6df1', 'bytes': 2727, 'sha256': '8e808cf429704ad9969d1a35a7a9831ce31c30faa4573fab2a0b61781ea6050d', 'cacheName': 'chaindex-83.md', 'url': 'https://github.com/jonnyg23/mahabrain/blob/025ee3c09f8d5bf6eb8c832c55fdd65e9d7d6c55/sacred_obsidian_vault/chr/charnock/index.md'}, 'TITLE': {'repository': 'jonnyg23/mahabrain', 'path': 'sacred_obsidian_vault/chr/charnock/cha00.md', 'commit': '025ee3c09f8d5bf6eb8c832c55fdd65e9d7d6c55', 'blob': 'dd69b4e5dd5dff753ebd02adbbd3bf96d791c2c7', 'bytes': 729, 'sha256': '6f022cefb331eb906b06830eafea10a88deb814aaae984d1d31ff85c0621c070', 'cacheName': 'cha00-83.md', 'url': 'https://github.com/jonnyg23/mahabrain/blob/025ee3c09f8d5bf6eb8c832c55fdd65e9d7d6c55/sacred_obsidian_vault/chr/charnock/cha00.md'}}

class LinkedTitles(HTMLParser):
    def __init__(self):super().__init__(convert_charrefs=True);self.links=[];self.href=None;self.parts=[]
    def handle_starttag(self,tag,attrs):
        if tag=='a':self.href=dict(attrs).get('href');self.parts=[]
    def handle_data(self,data):
        if self.href is not None:self.parts.append(data)
    def handle_endtag(self,tag):
        if tag=='a' and self.href is not None:
            self.links.append(dict(href=self.href,title=' '.join(''.join(self.parts).split())));self.href=None


def extract_digital_collection(directory,biography):
    result={}
    for key,pin in DIGITAL_PINS.items():
        raw=(directory/pin['cacheName']).read_bytes()
        if (len(raw)!=pin['bytes'] or hashlib.sha256(raw).hexdigest()!=pin['sha256']
                or hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()!=pin['blob']):
            raise ValueError('Digital collection raw pin mismatch')
        text=raw.decode('utf-8');paras=Paragraphs();paras.feed(text);links=LinkedTitles();links.feed(text)
        result[key]=dict(paragraphs=paras.rows,headings=re.findall(r'<h[14][^>]*>(.*?)</h[14]>',text),
                         contentLinks=[x for x in links.links if re.fullmatch(r'cha0[1-7]\.htm',x['href'])])
    raw=biography.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=SYMPIN['sha256']:raise ValueError('Biographical edition claim witness changed')
    text=raw.decode('utf-8');a=text.index('The best edition of Charnock’s works');b=text.index('Leeds.',a)+len('Leeds.')
    result['biographicalEditionClaim']=dict(text=text[a:b],textSha256=digest(text[a:b]))
    return result


def check_digital_collection(review):
    c=review['digitalCollectionReview'];r=c['byteVerifiedReading']
    if (c['reviewState']!='SEVEN_WEB_LINKS_NOT_IDENTIFIED_COLLECTED_EDITION'
            or c['sourcePins']!=DIGITAL_PINS
            or any(c[k] is not False for k in ['parsonsPhysicalEditionVerified','bestEditionRankingVerified',
                 'webCollectionIdentifiedAsParsons1815','completeWorksVerified','sevenLinksAreSevenTreatises',
                 'birthYearConflictResolved','linkedBodiesRead','publicationApproval'])):
        raise ValueError('A digital label and recommendation are not a verified physical edition')
    links=r['INDEX']['contentLinks']
    if [x['href'] for x in links]!=[f'cha0{i}.htm' for i in range(1,8)]:raise ValueError('Seven navigation segments, not total printed works')
    if (not links[4]['title'].endswith('Part I') or not links[5]['title'].endswith('Part II')
            or links[0]['title']!='Discourse of the Nature of Regeneneration'):
        raise ValueError('Preserve split text and literal web title spelling')
    if ('[1629-1680]' not in r['TITLE']['headings'] or '[1629-1680]' not in r['INDEX']['headings']
            or not any('1628 - 1680' in t for t in r['INDEX']['paragraphs'])
            or not any('[1628-1680]' in t for t in r['TITLE']['paragraphs'])):
        raise ValueError('Preserve unresolved banner/body birth-year conflict')
    claim=r['biographicalEditionClaim']
    if (digest(claim['text'])!=claim['textSha256'] or '1815, in nine volumes, royal 8vo' not in claim['text']
            or 'Edward Parsons of Leeds' not in claim['text'] or not c['scope'] or not c['limits']):
        raise ValueError('Keep the exact attributed 1815 claim distinct from modern collection')
    return dict(digitalCollectionContentLinks=7,parsons1815PhysicalEditionVerified=False)


def check_review(plan,registry):
    r=plan[KEY];a=r['byteVerifiedSource'];m=r['derivedWitness'];rows=a['paragraphs']
    if (r['reviewState']!='REC01_SOURCE_LOCUS_LOCATED_DERIVED_WITNESS_NOT_ORIGINAL_EDITION'
            or any(r[k] is not False for k in FLAGS)):
        raise ValueError('Located source sentence does not verify printed anthology or independent reception')
    if (a['source']!='A32723' or a['sourceSha256']!=registry['sources']['A32723']['sha256']
            or a['heading']!='A DISCOURSE UPON GODS Dominion.'
            or [p['paragraphIndexZeroBased'] for p in rows]!=list(range(2638,2649))
            or rows[8]['startTeiPage']!='699'):
        raise ValueError('Retain Dominion context and REC01 page699 locator')
    historical=next(x for x in registry['supportAnchors'] if x['id']=='REC-01')
    if historical['observedText'] not in rows[8]['text'] or 'ещё не найден' not in historical['claimBoundary']:
        raise ValueError('Historical unlocated observation must remain historical, not silently rewritten')
    if [x['htmlParagraphIndexZeroBased'] for x in m['reading']['paragraphs']]!=[248,317,116]:
        raise ValueError('Three selected mirror paragraphs, not full anthology reading')
    for row in rows+m['reading']['paragraphs']:
        if digest(row['text'])!=row['textSha256']:raise ValueError('Reception paragraph hash mismatch')
    primary=rows[8]['text'];secondary=m['reading']['paragraphs'][0]['text']
    start=primary.index('When sin is pardoned, it is never charged again;')
    if (r['comparison']['sourceSentence']!=primary[start:]
            or r['comparison']['mirrorSentence']!=secondary.removesuffix(' - Stephen Charnock.')
            or words(r['comparison']['sourceSentence'])!=words(r['comparison']['mirrorSentence'])
            or r['comparison']['relation']!='SAME_WORD_SEQUENCE_DIFFERENT_PUNCTUATION_AND_CASE'):
        raise ValueError('Match whole sentence without silently equating punctuation')
    if (m['commit']!='025ee3c09f8d5bf6eb8c832c55fdd65e9d7d6c55'
            or m['reading']['sha256']!='556d58c5a1e454d1d4a4bbe760928c9f651182b99cc09148b71dd68fe4096788'
            or m['reading']['bytes']!=133381 or m['reading']['gitBlobSha1']!='3b64aee88c789279a51607e32d65924b82eb97ff'):
        raise ValueError('Derived mirror pin changed')
    if (r['historicalUnlocatedRowRetained'] is not True or r['supersedesOnly']!='REC-01_SOURCE_LOCUS_UNLOCATED'
            or not r['contextLimits'] or not r['derivedWitnessLimits']
            or KEY not in plan['documents'][8]['supplementaryContextReadings']):
        raise ValueError('Preserve historical row and partVIII limits')
    if (r['evidenceClass']!='C' or r['accessState']!='FULL_OBJECT_VERIFIED'
            or r['locatorState']!='EXACT_LOCATOR_VERIFIED' or r['rightsState']!='RIGHTS_UNKNOWN'
            or r['publicationState']!='BLOCKED' or set(r['holds'])!=HOLDS):
        raise ValueError('No evidence or rights promotion from modern mirror')
    return dict(receptionREC01SourceLocated=True,receptionAdditionalIndependentReaders=0,receptionOriginalPrintedEditionVerified=False,**check_condensed(r),**check_praise(r,registry),**check_digital_collection(r))

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('directory',type=Path);p.add_argument('mirror',type=Path);p.add_argument('--biography-mirror',type=Path);p.add_argument('--digital-collection-directory',type=Path);args=p.parse_args()
    try:
        plan=json.loads((ROOT/'data/charnock-series-editorial-plan-v1.json').read_text());registry=json.loads((ROOT/plan['baselineRegistry']).read_text());check_review(plan,registry)
        if extract(args.directory,registry)!=plan[KEY]['byteVerifiedSource'] or extract_mirror(args.mirror)!=plan[KEY]['derivedWitness']['reading']:raise ValueError('Pinned reception replay differs')
        if extract_condensed(args.directory,registry,args.mirror)!=plan[KEY]['condensedPassage']['byteVerifiedReading']:raise ValueError('Six-point condensation replay differs')
        if args.biography_mirror and extract_praise(args.directory,registry,args.biography_mirror)!=plan[KEY]['biographicalPraiseReview']['byteVerifiedReading']:raise ValueError('Biographical praise replay differs')
        if args.digital_collection_directory:
            if not args.biography_mirror:raise ValueError('Digital collection replay also needs --biography-mirror')
            if extract_digital_collection(args.digital_collection_directory,args.biography_mirror)!=plan[KEY]['digitalCollectionReview']['byteVerifiedReading']:raise ValueError('Digital collection replay differs')
        print('Reception replay:PASS;optional biography/collection checked when supplied;not physical-edition verification')
    except (OSError,KeyError,ValueError,TypeError) as exc:p.exit(1,str(exc)+'\n')

if __name__=='__main__':main()
